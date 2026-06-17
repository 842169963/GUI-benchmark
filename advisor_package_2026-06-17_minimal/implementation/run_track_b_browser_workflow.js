/*
 * Browser workflow evaluator for generated Track B HTML.
 *
 * This is a real-browser counterpart to route-simulation-v1. It opens the
 * generated single-file HTML in Chromium, executes workflow clicks with
 * Playwright, and validates visible destination content.
 *
 * Example:
 *   node scripts/run_track_b_browser_workflow.js --item F03_about_gitlab --run gwdg_qwen36_35b_v9_smoke
 */

const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");

function loadPlaywright() {
  try {
    return require("playwright");
  } catch (error) {
    const home = process.env.USERPROFILE || process.env.HOME;
    if (!home) throw error;
    const bundled = path.join(
      home,
      ".cache",
      "codex-runtimes",
      "codex-primary-runtime",
      "dependencies",
      "node",
      "node_modules",
      ".pnpm",
      "playwright@1.60.0",
      "node_modules",
      "playwright"
    );
    return require(bundled);
  }
}

const { chromium } = loadPlaywright();

const PROJECT_ROOT = path.resolve(__dirname, "..");
const DEFAULT_ITEMS_DIR = path.join(PROJECT_ROOT, "data", "track_b", "items");

function parseArgs(argv) {
  const args = {
    itemsDir: DEFAULT_ITEMS_DIR,
    jsonOut: "",
    screenshotDir: "",
    noFail: false,
    headed: false,
    timeoutMs: 5000,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--items-dir") args.itemsDir = argv[++i];
    else if (arg === "--item") args.item = argv[++i];
    else if (arg === "--run") args.run = argv[++i];
    else if (arg === "--workflow") args.workflowPath = argv[++i];
    else if (arg === "--json-out") args.jsonOut = argv[++i];
    else if (arg === "--screenshot-dir") args.screenshotDir = argv[++i];
    else if (arg === "--timeout-ms") args.timeoutMs = Number(argv[++i]);
    else if (arg === "--no-fail") args.noFail = true;
    else if (arg === "--headed") args.headed = true;
    else throw new Error(`Unknown argument: ${arg}`);
  }
  if (!args.item) throw new Error("Missing required --item");
  if (!args.run) throw new Error("Missing required --run");
  return args;
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function cleanText(value) {
  return String(value || "").replace(/\s+/g, " ").trim();
}

function norm(value) {
  return cleanText(value).toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
}

function extractActionLabel(action) {
  const named = action.match(/named\s+"([^"]+)"/i);
  if (named) return named[1].trim();
  const quoted = [...action.matchAll(/"([^"]{2,80})"/g)];
  if (quoted.length) return quoted[0][1].trim();
  const related = action.match(/related to ([A-Za-z0-9 .&'/-]+?)(?: in | on | from |$)/i);
  if (related) return cleanText(related[1]);
  if (action.toLowerCase().includes("logo")) return "logo";
  const click = action.match(/Click the (.+?)(?: button| link| option| card| navigation menu item| in the| from the|$)/i);
  if (click) return cleanText(click[1]);
  return null;
}

function extractActionContext(action) {
  const contexts = [];
  const patterns = [
    /in the (.+?)(?: successfully| demonstrating|$)/i,
    /from the (.+?)(?: successfully| demonstrating|$)/i,
    /via the (.+?)(?: successfully| demonstrating|$)/i,
  ];
  for (const pattern of patterns) {
    const match = action.match(pattern);
    if (match) contexts.push(cleanText(match[1].replace(/\s+button$/i, "").replace(/\s+link$/i, "")));
  }
  return contexts.filter(Boolean);
}

function isSemanticRelatedAction(action) {
  return /related to [A-Za-z0-9 .&'/-]+/i.test(action);
}

function implementedRoutesFromHtml(html) {
  const routeSet = new Set();
  const routeArray = html.match(/__TRACK_B_ROUTES\s*=\s*(\[[^\]]+\])/);
  if (routeArray) {
    try {
      for (const route of JSON.parse(routeArray[1])) routeSet.add(route);
    } catch (_) {
      // Fall through to section-id parsing.
    }
  }
  for (const match of html.matchAll(/<section\b[^>]*\bid\s*=\s*["']([^"']+)["'][^>]*\bdata-track-route\b/gi)) {
    routeSet.add(match[1]);
  }
  for (const match of html.matchAll(/<section\b[^>]*\bdata-track-route\b[^>]*\bid\s*=\s*["']([^"']+)["']/gi)) {
    routeSet.add(match[1]);
  }
  return [...routeSet];
}

function startRouteForRoutes(routes) {
  return ["homepage", "home", "index", "main"].find((route) => routes.includes(route)) || "";
}

function startUrlForHtml(htmlUrl, startRoute) {
  return startRoute ? `${htmlUrl}#${startRoute}` : htmlUrl;
}

async function gotoStart(page, startUrl, startRoute, timeoutMs) {
  await page.goto(startUrl, { waitUntil: "load", timeout: timeoutMs });
  if (startRoute) {
    await page.evaluate((route) => {
      if (typeof window.showPage === "function") window.showPage(route);
      else if (location.hash !== `#${route}`) location.hash = route;
    }, startRoute).catch(() => {});
  }
  await page.waitForTimeout(250);
}

function validationKindAndNeedle(validation) {
  if (/navigates? to the .+ page/i.test(validation)) return { kind: "route", needle: null };
  const activeNav = validation.match(/The\s+(.+?)\s+(?:tab|link|navigation menu item).*?(?:highlighted|active)/i);
  if (activeNav) return { kind: "active_nav", needle: activeNav[1].trim() };
  const quoted = [...validation.matchAll(/"([^"]{2,120})"/g)];
  if (quoted.length) return { kind: "text", needle: quoted[0][1].trim() };
  const patterns = [
    /displays the (.+?) heading/i,
    /displays the (.+?) page content/i,
    /displays the (.+?) content/i,
    /displays (.+?) content/i,
  ];
  for (const pattern of patterns) {
    const match = validation.match(pattern);
    if (match) return { kind: "text", needle: match[1].trim() };
  }
  const lower = validation.toLowerCase();
  if (lower.includes("grid") && (lower.includes("image") || lower.includes("cover"))) return { kind: "image_grid", needle: null };
  if (lower.includes("thumbnail") || lower.includes("play button")) return { kind: "media_grid", needle: null };
  if (lower.includes("service category card") || lower.includes("course card")) return { kind: "card_grid", needle: null };
  if (lower.includes("form") && lower.includes("field")) return { kind: "form", needle: null };
  if (lower.includes("branding") || lower.includes("logo")) return { kind: "brand_or_logo", needle: null };
  if (lower.includes("ingredients and instructions")) return { kind: "text_all", needle: "ingredients instructions" };
  if (lower.includes("service information")) return { kind: "text_any", needle: "service services" };
  if (lower.includes("company information")) return { kind: "text_any", needle: "company leadership digital transformation" };
  return { kind: "text", needle: validation };
}

async function visibleBodyText(page) {
  return cleanText(await page.locator("body").innerText({ timeout: 1000 }).catch(() => ""));
}

async function visibleRoute(page) {
  return page.evaluate(() => {
    const sections = [...document.querySelectorAll("section[data-track-route][id]")];
    function isVisible(el) {
      const style = window.getComputedStyle(el);
      const rect = el.getBoundingClientRect();
      return style.display !== "none" && style.visibility !== "hidden" && rect.width > 0 && rect.height > 0;
    }
    const visible = sections.find(isVisible);
    return visible ? visible.id : "";
  });
}

async function clickByWorkflowLabel(page, action, label, timeoutMs) {
  const beforeUrl = page.url();
  const beforeRoute = await visibleRoute(page);
  const beforeText = await visibleBodyText(page);
  const candidates = page.locator("a, button");
  const count = await candidates.count();
  const wanted = norm(label);
  const contexts = extractActionContext(action);
  const semanticRelated = isSemanticRelatedAction(action);
  let best = null;

  for (let i = 0; i < count; i += 1) {
    const candidate = candidates.nth(i);
    if (!(await candidate.isVisible().catch(() => false))) continue;
    const text = cleanText(await candidate.innerText().catch(() => ""));
    const aria = cleanText(await candidate.getAttribute("aria-label").catch(() => ""));
    const title = cleanText(await candidate.getAttribute("title").catch(() => ""));
    const target = cleanText(await candidate.getAttribute("data-route-target").catch(() => ""));
    const href = cleanText(await candidate.getAttribute("href").catch(() => ""));
    const labelText = cleanText(`${text} ${aria} ${title}`);
    const haystack = norm(`${labelText} ${target} ${href}`);
    const labelNorm = norm(labelText);
    const containerText = await candidate.evaluate((element) => {
      const container = element.closest("article, section, aside, nav, header, .card, .banner, .feature, .sidebar, .hero, li, div");
      return container ? container.innerText || "" : "";
    }).catch(() => "");
    const containerNorm = norm(containerText);
    let score = 0;
    if (wanted === "logo") {
      score = haystack.includes("logo") || ["home", "homepage"].includes(norm(target)) ? 120 : 0;
    } else if (labelNorm === wanted) {
      score = 120;
    } else if (wanted && labelNorm.includes(wanted)) {
      score = 90;
    } else if (semanticRelated && wanted && haystack.includes(wanted)) {
      score = 110;
    } else if (semanticRelated && wanted && containerNorm.includes(wanted)) {
      score = 95;
    } else {
      for (const term of wanted.split(" ").filter((part) => part.length > 1)) {
        if (labelNorm.includes(term)) score += 10;
      }
    }
    if (score === 0) continue;
    if (semanticRelated && score < 40) continue;
    if (!semanticRelated && !labelNorm.includes(wanted) && score < 40) continue;
    if (contexts.length) {
      for (const context of contexts) {
        const terms = norm(context).split(" ").filter((part) => part.length > 2);
        const matchedTerms = terms.filter((term) => containerNorm.includes(term)).length;
        if (terms.length && matchedTerms / terms.length >= 0.5) score += 80;
      }
    }
    if (score > 0 && (!best || score > best.score)) {
      best = { locator: candidate, text, target, href, score };
    }
  }

  if (!best) {
    return {
      passed: false,
      label,
      error: `No visible clickable candidate for label ${JSON.stringify(label)}`,
      route_before: beforeRoute,
    };
  }

  await best.locator.scrollIntoViewIfNeeded().catch(() => {});
  await best.locator.click({ timeout: timeoutMs }).catch(async (error) => {
    throw new Error(`Click failed for ${JSON.stringify(label)}: ${error.message}`);
  });
  await page.waitForTimeout(250);

  const afterRoute = await visibleRoute(page);
  const afterText = await visibleBodyText(page);
  const afterUrl = page.url();
  const changed =
    beforeUrl !== afterUrl ||
    beforeRoute !== afterRoute ||
    norm(beforeText).slice(0, 500) !== norm(afterText).slice(0, 500) ||
    Boolean(best.target && afterRoute === best.target);

  return {
    passed: changed || Boolean(best.target),
    label,
    chosen: {
      text: best.text,
      target: best.target,
      href: best.href,
      score: best.score,
    },
    route_before: beforeRoute,
    route_after: afterRoute,
    url_before: beforeUrl,
    url_after: afterUrl,
    changed,
  };
}

async function validateContent(page, validation, routeSuccess) {
  const { kind, needle } = validationKindAndNeedle(validation);
  const bodyText = await visibleBodyText(page);
  const text = norm(bodyText);
  let passed = false;

  if (kind === "route") {
    passed = routeSuccess;
  } else if (kind === "text") {
    passed = text.includes(norm(needle));
  } else if (kind === "text_any") {
    passed = norm(needle).split(" ").some((term) => text.includes(term));
  } else if (kind === "text_all") {
    passed = norm(needle).split(" ").every((term) => text.includes(term));
  } else if (kind === "image_grid") {
    passed = await page.locator("img:visible").count().then((count) => count >= 3);
  } else if (kind === "media_grid") {
    const images = await page.locator("img:visible").count();
    passed = images >= 2 || text.includes("video");
  } else if (kind === "card_grid") {
    passed = await page.locator(".card:visible, .grid-item:visible, .book:visible, .solution:visible, .video:visible").count().then((count) => count >= 2);
  } else if (kind === "form") {
    const inputs = await page.locator("input:visible, select:visible, textarea:visible").count();
    passed = inputs >= 2 || text.includes("form");
  } else if (kind === "brand_or_logo") {
    const visibleLogo = await page.locator("img[alt*=logo i]:visible, [aria-label*=logo i]:visible").count();
    passed = visibleLogo > 0 || text.includes("logo") || text.includes("gitlab") || text.includes("duo");
  } else if (kind === "active_nav") {
    const wanted = norm(needle);
    const currentRoute = await visibleRoute(page);
    const controls = page.locator("a:visible, button:visible");
    const count = await controls.count();
    for (let i = 0; i < count; i += 1) {
      const control = controls.nth(i);
      const labelText = norm(await control.innerText().catch(() => ""));
      if (!labelText.includes(wanted)) continue;
      const className = norm(await control.getAttribute("class").catch(() => ""));
      const ariaCurrent = norm(await control.getAttribute("aria-current").catch(() => ""));
      const ariaSelected = norm(await control.getAttribute("aria-selected").catch(() => ""));
      const target = cleanText(await control.getAttribute("data-route-target").catch(() => ""));
      if (
        className.includes("active") ||
        className.includes("selected") ||
        ariaCurrent === "page" ||
        ariaSelected === "true" ||
        (target && target === currentRoute)
      ) {
        passed = true;
        break;
      }
    }
  }

  return {
    validation,
    kind,
    needle,
    passed: Boolean(passed),
  };
}

async function runCase(page, htmlUrl, startUrl, startRoute, workflowCase, blockIndex, caseIndex, timeoutMs, screenshotPath) {
  await gotoStart(page, startUrl, startRoute, timeoutMs);

  const actionReports = [];
  let caseError = null;
  for (const action of workflowCase.actions || []) {
    const actionReport = { action, passed: false };
    try {
      const lower = action.toLowerCase();
      if (lower.startsWith("browser:back") || lower.includes("navigate back")) {
        await gotoStart(page, startUrl, startRoute, timeoutMs);
        actionReport.method = "reset_to_initial_page";
        actionReport.route_after = await visibleRoute(page);
        actionReport.passed = true;
      } else if (lower.includes("click")) {
        const label = extractActionLabel(action);
        Object.assign(actionReport, await clickByWorkflowLabel(page, action, label, timeoutMs));
        if (!actionReport.passed) caseError = actionReport.error || "Click action did not change browser state.";
      } else {
        actionReport.skipped = true;
        actionReport.passed = true;
      }
    } catch (error) {
      caseError = error.message;
      actionReport.error = error.message;
      actionReport.passed = false;
    }
    actionReports.push(actionReport);
    if (!actionReport.passed) break;
  }

  const actionSuccess = actionReports.every((action) => action.passed);
  const routeSuccess = actionSuccess;
  const validationReports = [];
  for (const validation of workflowCase.validations || []) {
    validationReports.push(await validateContent(page, validation, routeSuccess));
  }
  const contentSuccess = validationReports.every((validation) => validation.passed);

  if (screenshotPath) {
    fs.mkdirSync(path.dirname(screenshotPath), { recursive: true });
    await page.screenshot({ path: screenshotPath, fullPage: true }).catch(() => {});
  }

  return {
    block_index: blockIndex,
    case_index: caseIndex,
    objective: workflowCase.objective || "",
    actions: actionReports,
    validations: validationReports,
    final_route: await visibleRoute(page),
    final_url: page.url(),
    route_success: routeSuccess,
    content_validation_success: contentSuccess,
    passed: actionSuccess && routeSuccess && contentSuccess,
    error: caseError,
  };
}

async function runBrowserWorkflow(args) {
  const itemDir = path.resolve(args.itemsDir, args.item);
  const runDir = path.join(itemDir, "generated", args.run);
  const workflowPath = args.workflowPath ? path.resolve(args.workflowPath) : path.join(itemDir, "workflow.json");
  const htmlPath = path.join(runDir, "index.html");
  if (!fs.existsSync(itemDir)) throw new Error(`Item not found: ${itemDir}`);
  if (!fs.existsSync(runDir)) throw new Error(`Run not found: ${runDir}`);
  if (!fs.existsSync(workflowPath)) throw new Error(`Workflow not found: ${workflowPath}`);
  if (!fs.existsSync(htmlPath)) throw new Error(`HTML not found: ${htmlPath}`);

  const workflow = readJson(workflowPath);
  const html = fs.readFileSync(htmlPath, "utf8");
  const htmlUrl = pathToFileURL(htmlPath).href;
  const routes = implementedRoutesFromHtml(html);
  const startRoute = startRouteForRoutes(routes);
  const startUrl = startUrlForHtml(htmlUrl, startRoute);
  const browser = await chromium.launch({ headless: !args.headed });
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
  const page = await context.newPage();
  const cases = [];
  const consoleErrors = [];
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });
  page.on("pageerror", (error) => consoleErrors.push(error.message));

  try {
    for (const block of workflow) {
      const width = block.resolution && block.resolution.width ? block.resolution.width : 1920;
      const height = block.resolution && block.resolution.height ? block.resolution.height : 1080;
      await page.setViewportSize({ width, height });
      const content = block.content || [];
      for (let caseIndex = 0; caseIndex < content.length; caseIndex += 1) {
        const screenshotPath = args.screenshotDir
          ? path.join(args.screenshotDir, `block_${block.index}_case_${caseIndex}.png`)
          : "";
        cases.push(await runCase(page, htmlUrl, startUrl, startRoute, content[caseIndex], block.index, caseIndex, args.timeoutMs, screenshotPath));
      }
    }
  } finally {
    await browser.close();
  }

  const caseCount = cases.length;
  const routeSuccessCount = cases.filter((item) => item.route_success).length;
  const contentSuccessCount = cases.filter((item) => item.content_validation_success).length;
  const passedCount = cases.filter((item) => item.passed).length;
  return {
    item_id: path.basename(itemDir),
    run: path.basename(runDir),
    html: htmlPath,
    workflow: workflowPath,
    start_url: startUrl,
    start_route: startRoute,
    evaluator: "browser-workflow-v1",
    case_count: caseCount,
    passed_case_count: passedCount,
    route_success_case_count: routeSuccessCount,
    content_validation_success_case_count: contentSuccessCount,
    task_success_rate: caseCount ? passedCount / caseCount : 0,
    route_success_rate: caseCount ? routeSuccessCount / caseCount : 0,
    content_validation_success_rate: caseCount ? contentSuccessCount / caseCount : 0,
    passed: passedCount === caseCount,
    console_errors: [...new Set(consoleErrors)],
    cases,
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const itemDir = path.resolve(args.itemsDir, args.item);
  const runDir = path.join(itemDir, "generated", args.run);
  const report = await runBrowserWorkflow(args);
  const outPath = args.jsonOut || path.join(runDir, "browser_workflow_report.json");
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, JSON.stringify(report, null, 2), "utf8");

  const summary = {
    item_id: report.item_id,
    run: report.run,
    evaluator: report.evaluator,
    passed_case_count: report.passed_case_count,
    case_count: report.case_count,
    task_success_rate: report.task_success_rate,
    route_success_rate: report.route_success_rate,
    content_validation_success_rate: report.content_validation_success_rate,
    passed: report.passed,
    console_error_count: report.console_errors.length,
    report: outPath,
  };
  console.log(JSON.stringify(summary, null, 2));
  if (!report.passed && !args.noFail) process.exit(1);
}

main().catch((error) => {
  console.error(`ERROR: ${error.message}`);
  process.exit(1);
});
