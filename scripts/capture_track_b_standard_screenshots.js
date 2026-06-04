/*
 * Capture standardized predefined-route screenshots for a generated Track B UI.
 *
 * The screenshots are intended for Static Visual Score inputs. They are not
 * agent trace screenshots and should be captured with a fixed viewport and
 * route list.
 *
 * Examples:
 *   node scripts/capture_track_b_standard_screenshots.js --item F03_about_gitlab --run gwdg_qwen36_35b_v9_smoke
 *   node scripts/capture_track_b_standard_screenshots.js --item F03_about_gitlab --run gwdg_qwen36_35b_v9_smoke --full-page
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
    outDir: "",
    width: 1440,
    height: 900,
    waitMs: 500,
    timeoutMs: 10000,
    fullPage: false,
    headed: false,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--items-dir") args.itemsDir = argv[++i];
    else if (arg === "--item") args.item = argv[++i];
    else if (arg === "--run") args.run = argv[++i];
    else if (arg === "--out-dir") args.outDir = argv[++i];
    else if (arg === "--width") args.width = Number(argv[++i]);
    else if (arg === "--height") args.height = Number(argv[++i]);
    else if (arg === "--wait-ms") args.waitMs = Number(argv[++i]);
    else if (arg === "--timeout-ms") args.timeoutMs = Number(argv[++i]);
    else if (arg === "--full-page") args.fullPage = true;
    else if (arg === "--headed") args.headed = true;
    else throw new Error(`Unknown argument: ${arg}`);
  }
  if (!args.item) throw new Error("Missing required --item");
  if (!args.run) throw new Error("Missing required --run");
  return args;
}

function sanitizeName(value) {
  return String(value || "route")
    .toLowerCase()
    .replace(/[^a-z0-9_-]+/g, "_")
    .replace(/^_+|_+$/g, "")
    .slice(0, 80) || "route";
}

function readJsonIfExists(filePath) {
  if (!fs.existsSync(filePath)) return null;
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function routesFromHtml(html) {
  const scriptMatch = html.match(/window\.__TRACK_B_ROUTES\s*=\s*(\[[\s\S]*?\])/);
  if (scriptMatch) {
    try {
      const parsed = JSON.parse(scriptMatch[1]);
      if (Array.isArray(parsed) && parsed.length) return parsed.map(String);
    } catch (_) {
      // Fall through to section parsing.
    }
  }
  const routes = [];
  const sectionRegex = /<section\b[^>]*\bid\s*=\s*["']([^"']+)["'][^>]*\bdata-track-route\b/gi;
  let match;
  while ((match = sectionRegex.exec(html)) !== null) routes.push(match[1]);
  return [...new Set(routes)];
}

function routesFromPrototypeMetadata(metadata) {
  const prototypes = metadata && metadata.source_meta && Array.isArray(metadata.source_meta.prototypes)
    ? metadata.source_meta.prototypes
    : [];
  return prototypes.map((fileName) => path.basename(fileName, path.extname(fileName)));
}

async function showRoute(page, htmlUrl, route, timeoutMs, waitMs) {
  await page.goto(`${htmlUrl}#${encodeURIComponent(route)}`, { waitUntil: "load", timeout: timeoutMs });
  await page.waitForTimeout(waitMs);
  await page.evaluate((routeId) => {
    if (typeof window.showPage === "function") {
      window.showPage(routeId);
    }
  }, route).catch(() => {});
  await page.waitForTimeout(waitMs);
}

async function captureScreenshots(args) {
  const itemDir = path.resolve(args.itemsDir, args.item);
  const runDir = path.join(itemDir, "generated", args.run);
  const htmlPath = path.join(runDir, "index.html");
  const metadataPath = path.join(runDir, "generation_metadata.json");
  if (!fs.existsSync(itemDir)) throw new Error(`Item not found: ${itemDir}`);
  if (!fs.existsSync(runDir)) throw new Error(`Run not found: ${runDir}`);
  if (!fs.existsSync(htmlPath)) throw new Error(`HTML not found: ${htmlPath}`);

  const outDir = args.outDir
    ? path.resolve(args.outDir)
    : path.join(runDir, "standard_screenshots");
  fs.mkdirSync(outDir, { recursive: true });

  const html = fs.readFileSync(htmlPath, "utf8");
  const metadata = readJsonIfExists(metadataPath);
  let routes = routesFromHtml(html);
  if (!routes.length) routes = routesFromPrototypeMetadata(metadata);
  if (!routes.length) throw new Error("No routes found from __TRACK_B_ROUTES, data-track-route sections, or prototype metadata.");

  const htmlUrl = pathToFileURL(htmlPath).href;
  const browser = await chromium.launch({ headless: !args.headed });
  const context = await browser.newContext({ viewport: { width: args.width, height: args.height } });
  const page = await context.newPage();
  const consoleErrors = [];
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });
  page.on("pageerror", (error) => consoleErrors.push(error.message));

  const captures = [];
  try {
    for (const route of routes) {
      const fileName = `${String(captures.length + 1).padStart(2, "0")}_${sanitizeName(route)}.png`;
      const screenshotPath = path.join(outDir, fileName);
      const capture = {
        route_id: route,
        path: path.relative(PROJECT_ROOT, screenshotPath),
        width: args.width,
        height: args.height,
        full_page: args.fullPage,
        captured: false,
        error: null,
      };
      try {
        await showRoute(page, htmlUrl, route, args.timeoutMs, args.waitMs);
        await page.screenshot({ path: screenshotPath, fullPage: args.fullPage });
        capture.captured = true;
        capture.url = page.url();
      } catch (error) {
        capture.error = error.message;
      }
      captures.push(capture);
    }
  } finally {
    await browser.close();
  }

  const manifest = {
    item_id: args.item,
    run: args.run,
    evaluator: "standard-route-screenshot-v1",
    purpose: "static_visual_input",
    html: path.relative(PROJECT_ROOT, htmlPath),
    output_dir: path.relative(PROJECT_ROOT, outDir),
    viewport: { width: args.width, height: args.height },
    wait_ms: args.waitMs,
    full_page: args.fullPage,
    route_count: routes.length,
    captured_count: captures.filter((capture) => capture.captured).length,
    screenshot_coverage: routes.length ? captures.filter((capture) => capture.captured).length / routes.length : 0,
    console_errors: [...new Set(consoleErrors)],
    captures,
  };
  const manifestPath = path.join(outDir, "manifest.json");
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2), "utf8");
  manifest.manifest = path.relative(PROJECT_ROOT, manifestPath);
  return manifest;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const manifest = await captureScreenshots(args);
  console.log(JSON.stringify({
    item_id: manifest.item_id,
    run: manifest.run,
    evaluator: manifest.evaluator,
    route_count: manifest.route_count,
    captured_count: manifest.captured_count,
    screenshot_coverage: manifest.screenshot_coverage,
    manifest: manifest.manifest,
  }, null, 2));
  if (manifest.captured_count !== manifest.route_count) process.exit(1);
}

main().catch((error) => {
  console.error(`ERROR: ${error.message}`);
  process.exit(1);
});
