/*
 * Accessibility evaluator for generated Track B HTML (axe-core).
 *
 * Opens the generated single-file HTML in Chromium, injects axe-core, runs the
 * WCAG rule checks in-page, and writes a normalized Accessibility Score.
 * Free, local, deterministic, no API tokens.
 *
 * Example:
 *   node scripts/run_track_b_accessibility.js --item F03_about_gitlab --run gwdg_qwen36_35b_v9_smoke
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
const axeCore = require("axe-core");

const PROJECT_ROOT = path.resolve(__dirname, "..");
const ITEMS_DIR = path.join(PROJECT_ROOT, "data", "track_b", "items");

function parseArgs(argv) {
  const args = { run: "gwdg_qwen36_35b_v9_smoke" };
  for (let i = 0; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === "--item") args.item = argv[++i];
    else if (a === "--run") args.run = argv[++i];
    else if (a === "--json-out") args.jsonOut = argv[++i];
    else throw new Error(`Unknown argument: ${a}`);
  }
  if (!args.item) throw new Error("--item is required");
  return args;
}

async function evaluateItem(item, run) {
  const htmlPath = path.join(ITEMS_DIR, item, "generated", run, "index.html");
  if (!fs.existsSync(htmlPath)) {
    throw new Error(`Missing artifact: ${htmlPath}`);
  }
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: "load" });
  await page.addScriptTag({ content: axeCore.source });
  const results = await page.evaluate(async () => {
    // Run the WCAG 2.0/2.1 A & AA rule set.
    return await window.axe.run(document, {
      runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"] },
    });
  });
  await browser.close();

  const countNodes = (arr) => arr.reduce((n, r) => n + r.nodes.length, 0);
  const passNodes = countNodes(results.passes);
  const violationNodes = countNodes(results.violations);
  const denom = passNodes + violationNodes;
  const accessibilityScore = denom > 0 ? passNodes / denom : 1.0;

  const bySeverity = { critical: 0, serious: 0, moderate: 0, minor: 0 };
  for (const v of results.violations) {
    const impact = v.impact || "minor";
    bySeverity[impact] = (bySeverity[impact] || 0) + v.nodes.length;
  }
  const contrast = results.violations.find((v) => v.id === "color-contrast");

  return {
    item,
    run,
    accessibility_score: Number(accessibilityScore.toFixed(4)),
    pass_nodes: passNodes,
    violation_nodes: violationNodes,
    violations_by_severity: bySeverity,
    violated_rules: results.violations.map((v) => ({
      id: v.id,
      impact: v.impact,
      nodes: v.nodes.length,
    })),
    color_contrast_violation_nodes: contrast ? contrast.nodes.length : 0,
    // Coverage breadth, for interpreting how much the score actually measures.
    passed_rule_count: results.passes.length,
    passed_rules: results.passes.map((r) => r.id),
    incomplete_rules: results.incomplete.map((r) => ({ id: r.id, nodes: r.nodes.length })),
    inapplicable_rule_count: results.inapplicable.length,
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const report = await evaluateItem(args.item, args.run);
  const outPath =
    args.jsonOut ||
    path.join(ITEMS_DIR, args.item, "generated", args.run, "accessibility_report.json");
  fs.writeFileSync(outPath, JSON.stringify(report, null, 2));
  console.log(
    `${args.item}: accessibility_score=${report.accessibility_score} ` +
      `(pass=${report.pass_nodes}, violations=${report.violation_nodes}, ` +
      `contrast_violations=${report.color_contrast_violation_nodes})`
  );
}

main().catch((err) => {
  console.error(err.message || err);
  process.exit(1);
});
