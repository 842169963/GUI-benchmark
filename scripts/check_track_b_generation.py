"""
Static render/interaction gate for generated Track B HTML.

This gate intentionally checks only cheap, deterministic conditions. It catches
the common failure modes before a generated page enters screenshot or dynamic
workflow evaluation.

Examples:
    py -3.12 scripts/check_track_b_generation.py --item F09_elections_bc --run claude_sonnet45_smoke
"""

import argparse
import json
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ITEMS_DIR = PROJECT_ROOT / "data" / "track_b" / "items"


def read_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def strip_tags(value):
    value = re.sub(r"<script\b.*?</script>", " ", value, flags=re.IGNORECASE | re.DOTALL)
    value = re.sub(r"<style\b.*?</style>", " ", value, flags=re.IGNORECASE | re.DOTALL)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def function_definitions(html):
    names = set(re.findall(r"\bfunction\s+([A-Za-z_$][\w$]*)\s*\(", html))
    names.update(re.findall(r"\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:function\b|\([^)]*\)\s*=>|[A-Za-z_$][\w$]*\s*=>)", html))
    names.update(re.findall(r"\bwindow\.([A-Za-z_$][\w$]*)\s*=", html))
    return names


def onclick_function_calls(html):
    calls = []
    for handler in re.findall(r"\bonclick\s*=\s*(['\"])(.*?)\1", html, flags=re.IGNORECASE | re.DOTALL):
        calls.extend(re.findall(r"\b([A-Za-z_$][\w$]*)\s*\(", handler[1]))
    return sorted(set(calls))


def route_ids_from_handlers(html):
    ids = set()
    for quote, value in re.findall(r"showPage\s*\(\s*(['\"])(.*?)\1\s*\)", html):
        ids.add(value)
    return ids


def html_ids(html):
    return set(value for _, value in re.findall(r"\bid\s*=\s*(['\"])(.*?)\1", html, flags=re.IGNORECASE))


def workflow_label_groups(workflow):
    exact_labels = set()
    semantic_labels = set()
    for block in workflow:
        for case in block.get("content", []):
            for action in case.get("actions", []):
                if not isinstance(action, str):
                    continue
                lower = action.lower()
                if lower.startswith("browser:") or "click" not in lower:
                    continue

                quoted = re.findall(r'"([^"]{2,80})"', action)
                if quoted:
                    exact_labels.update(label.strip() for label in quoted)
                    continue

                related = re.search(
                    r"related to ([A-Za-z0-9 .&'/-]+?)(?: in | on | from |$)",
                    action,
                    flags=re.IGNORECASE,
                )
                if related:
                    label = related.group(1).strip()
                    label = re.sub(r"\s+", " ", label)
                    if 2 <= len(label) <= 80:
                        semantic_labels.add(label)
                    continue

                named = re.search(r"named\s+\"([^\"]+)\"", action, flags=re.IGNORECASE)
                if named:
                    label = named.group(1).strip()
                    if 2 <= len(label) <= 80:
                        exact_labels.add(label)
                    continue

                match = re.search(
                    r"Click the (.+?)(?: button| link| option| card| navigation menu item| in the| from the|$)",
                    action,
                    flags=re.IGNORECASE,
                )
                if match:
                    label = match.group(1).strip()
                    label = re.sub(r"\s+", " ", label)
                    if 2 <= len(label) <= 80 and not label.lower().startswith("learn more button in"):
                        semantic_labels.add(label)
    return {
        "exact": sorted(exact_labels),
        "semantic": sorted(semantic_labels - exact_labels),
    }


def clickable_texts(html):
    texts = {}
    for tag, attrs, body in re.findall(r"<(a|button)\b([^>]*)>(.*?)</\1>", html, flags=re.IGNORECASE | re.DOTALL):
        text = strip_tags(body)
        if not text:
            continue
        entries = texts.setdefault(text.lower(), [])
        entries.append(attrs)
    return texts


def has_working_clickable(label, clickables):
    entries = clickables.get(label.lower(), [])
    if not entries:
        return False
    for attrs in entries:
        lower = attrs.lower()
        if "onclick" in lower:
            return True
        if "data-route-target" in lower:
            return True
        if "href" in lower and not re.search(r"href\s*=\s*['\"]#['\"]", lower):
            return True
    return False


def add(checks, level, name, passed, detail):
    checks.append({
        "level": level,
        "name": name,
        "passed": bool(passed),
        "detail": detail,
    })


def run_gate(item_dir, run_dir):
    html_path = run_dir / "index.html"
    workflow_path = item_dir / "workflow.json"
    metadata_path = run_dir / "generation_metadata.json"

    html = html_path.read_text(encoding="utf-8")
    workflow = read_json(workflow_path)
    metadata = read_json(metadata_path) if metadata_path.exists() else {}

    checks = []
    lower = html.lower()

    add(checks, "error", "complete_doctype_html", "<!doctype" in lower and "<html" in lower,
        "Document should include doctype and html root.")
    add(checks, "error", "closed_body_html", "</body>" in lower and "</html>" in lower,
        "Document should close body and html tags.")
    add(checks, "error", "closed_style_script", lower.count("<style") == lower.count("</style>") and lower.count("<script") == lower.count("</script>"),
        "Style and script tags should not be truncated.")

    response_meta = metadata.get("response_metadata") or {}
    stop_reason = response_meta.get("stop_reason") or response_meta.get("finish_reason")
    add(checks, "error", "not_token_truncated", stop_reason not in {"max_tokens", "length"},
        f"Provider stop/finish reason: {stop_reason!r}.")

    defined = function_definitions(html)
    calls = onclick_function_calls(html)
    missing = [name for name in calls if name not in defined and name not in {"alert", "confirm", "prompt"}]
    add(checks, "error", "onclick_functions_defined", not missing,
        f"Missing onclick function definitions: {missing}.")

    routes = route_ids_from_handlers(html)
    ids = html_ids(html)
    missing_routes = sorted(route for route in routes if route not in ids)
    add(checks, "error", "onclick_routes_exist", not missing_routes,
        f"showPage route ids without matching id attributes: {missing_routes}.")

    add(checks, "warning", "track_b_routes_self_test", "__TRACK_B_ROUTES" in html,
        "Generated page should expose window.__TRACK_B_ROUTES for cheap route introspection.")

    label_groups = workflow_label_groups(workflow)
    labels = label_groups["exact"]
    semantic_labels = label_groups["semantic"]
    clickables = clickable_texts(html)
    missing_labels = [label for label in labels if label.lower() not in clickables]
    add(checks, "error", "workflow_clickable_labels_present", not missing_labels,
        f"Workflow click labels not found as <a> or <button>: {missing_labels}.")

    inert_labels = [label for label in labels if label.lower() in clickables and not has_working_clickable(label, clickables)]
    add(checks, "error", "workflow_clickables_not_inert", not inert_labels,
        f"Workflow click labels found only as inert controls: {inert_labels}.")

    missing_semantic_labels = [label for label in semantic_labels if label.lower() not in clickables]
    add(checks, "warning", "semantic_workflow_click_labels_present", not missing_semantic_labels,
        f"Semantic workflow click descriptions not found as exact <a> or <button> text: {missing_semantic_labels}.")

    failed_errors = [check for check in checks if check["level"] == "error" and not check["passed"]]
    failed_warnings = [check for check in checks if check["level"] == "warning" and not check["passed"]]
    return {
        "item_id": item_dir.name,
        "run": run_dir.name,
        "html": str(html_path),
        "passed": not failed_errors,
        "failed_error_count": len(failed_errors),
        "failed_warning_count": len(failed_warnings),
        "checks": checks,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--items-dir", default=str(DEFAULT_ITEMS_DIR))
    parser.add_argument("--item", required=True)
    parser.add_argument("--run", required=True, help="Directory name under the item's generated/ folder.")
    parser.add_argument("--json-out", help="Optional path to write the gate report.")
    parser.add_argument("--no-fail", action="store_true", help="Always exit 0, even when the gate fails.")
    args = parser.parse_args()

    item_dir = Path(args.items_dir).resolve() / args.item
    run_dir = item_dir / "generated" / args.run
    if not item_dir.exists():
        raise SystemExit(f"ERROR: item not found: {item_dir}")
    if not run_dir.exists():
        raise SystemExit(f"ERROR: run not found: {run_dir}")

    report = run_gate(item_dir, run_dir)
    if args.json_out:
        out_path = Path(args.json_out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

    print(json.dumps(report, indent=2, ensure_ascii=False))
    if not report["passed"] and not args.no_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
