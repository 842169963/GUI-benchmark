"""
Lightweight dynamic workflow evaluator for generated Track B HTML.

The evaluator reads a generated single-file HTML submission and the item's
Vision2Web workflow.json, simulates workflow clicks through data-route-target
anchors/buttons, and reports route success separately from content validation.

This is intentionally deterministic and dependency-free. It does not replace a
full browser runner, but it gives a reproducible first-pass task validation
signal for the thesis pilot.

Examples:
    py -3.12 scripts/run_track_b_dynamic_workflow.py --item F03_about_gitlab --run gwdg_qwen36_35b_v9_smoke
    py -3.12 scripts/run_track_b_dynamic_workflow.py --item F03_about_gitlab --run gwdg_qwen36_35b_v9_smoke --json-out report.json
"""

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ITEMS_DIR = PROJECT_ROOT / "data" / "track_b" / "items"


def read_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def norm(value):
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()


def clean_text(value):
    return re.sub(r"\s+", " ", value or "").strip()


def attrs_dict(attrs):
    return {key.lower(): value if value is not None else "" for key, value in attrs}


class TrackBHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.routes = []
        self.section_stack = []
        self.text_by_route = {}
        self.global_text = []
        self.clickables = []
        self.current_clickable = None
        self.card_count_by_route = {}
        self.image_count_by_route = {}
        self.input_count_by_route = {}

    def current_route(self):
        return self.section_stack[-1] if self.section_stack else None

    def append_text(self, text):
        text = clean_text(text)
        if not text:
            return
        route = self.current_route()
        if route:
            self.text_by_route.setdefault(route, []).append(text)
        else:
            self.global_text.append(text)
        if self.current_clickable is not None:
            self.current_clickable["parts"].append(text)

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs = attrs_dict(attrs)
        if tag == "section" and "data-track-route" in attrs:
            route = attrs.get("id", "")
            if route:
                self.routes.append(route)
                self.section_stack.append(route)
                self.text_by_route.setdefault(route, [])
                self.card_count_by_route.setdefault(route, 0)
                self.image_count_by_route.setdefault(route, 0)
                self.input_count_by_route.setdefault(route, 0)
        route = self.current_route()
        class_name = attrs.get("class", "")
        if route and re.search(r"\b(card|grid-item|book|solution|video)\b", class_name, re.IGNORECASE):
            self.card_count_by_route[route] = self.card_count_by_route.get(route, 0) + 1
        if route and tag == "img":
            self.image_count_by_route[route] = self.image_count_by_route.get(route, 0) + 1
            self.append_text(attrs.get("alt", ""))
        if route and tag in {"input", "select", "textarea"}:
            self.input_count_by_route[route] = self.input_count_by_route.get(route, 0) + 1
        if tag in {"a", "button"}:
            self.current_clickable = {
                "tag": tag,
                "route_context": route,
                "target": attrs.get("data-route-target", ""),
                "href": attrs.get("href", ""),
                "aria_label": attrs.get("aria-label", ""),
                "title": attrs.get("title", ""),
                "parts": [],
            }

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in {"a", "button"} and self.current_clickable is not None:
            clickable = dict(self.current_clickable)
            text = clean_text(" ".join(clickable.pop("parts", [])))
            labels = " ".join([text, clickable.get("aria_label", ""), clickable.get("title", "")])
            clickable["text"] = text
            clickable["label_text"] = clean_text(labels)
            self.clickables.append(clickable)
            self.current_clickable = None
        if tag == "section" and self.section_stack:
            self.section_stack.pop()

    def handle_data(self, data):
        self.append_text(data)


def parse_html(html):
    parser = TrackBHTMLParser()
    parser.feed(html)
    return {
        "routes": parser.routes,
        "default_route": parser.routes[0] if parser.routes else "",
        "global_text": clean_text(" ".join(parser.global_text)),
        "text_by_route": {
            route: clean_text(" ".join(parts))
            for route, parts in parser.text_by_route.items()
        },
        "clickables": parser.clickables,
        "card_count_by_route": parser.card_count_by_route,
        "image_count_by_route": parser.image_count_by_route,
        "input_count_by_route": parser.input_count_by_route,
    }


def extract_action_label(action):
    named = re.search(r'named\s+"([^"]+)"', action, flags=re.IGNORECASE)
    if named:
        return named.group(1).strip()
    quoted = re.findall(r'"([^"]{2,80})"', action)
    if quoted:
        return quoted[0].strip()
    related = re.search(r"related to ([A-Za-z0-9 .&'/-]+?)(?: in | on | from |$)", action, flags=re.IGNORECASE)
    if related:
        return clean_text(related.group(1))
    if "logo" in action.lower():
        return "logo"
    match = re.search(
        r"Click the (.+?)(?: button| link| option| card| navigation menu item| in the| from the|$)",
        action,
        flags=re.IGNORECASE,
    )
    if match:
        return clean_text(match.group(1))
    return None


def is_clickable_available(clickable, current_route):
    context = clickable.get("route_context")
    return context is None or context == "" or context == current_route


def score_clickable(label, clickable):
    wanted = norm(label)
    text = norm(clickable.get("label_text"))
    target = norm(clickable.get("target"))
    if wanted == "logo":
        if "logo" in text or target in {"home", "homepage"}:
            return 120
        return 0
    score = 0
    if text == wanted:
        score += 120
    elif wanted and wanted in text:
        score += 90
    terms = [term for term in wanted.split() if len(term) > 1]
    matched = False
    for term in terms:
        if term in text:
            score += 10
            matched = True
        if term in target:
            score += 15
            matched = True
    return score if matched or text == wanted or wanted in text else 0


def choose_clickable(label, clickables, current_route):
    candidates = [
        clickable for clickable in clickables
        if is_clickable_available(clickable, current_route)
    ]
    scored = [
        (score_clickable(label, clickable), clickable)
        for clickable in candidates
    ]
    scored = [(score, clickable) for score, clickable in scored if score > 0]
    if not scored:
        return None
    scored.sort(key=lambda item: item[0], reverse=True)
    chosen = dict(scored[0][1])
    chosen["score"] = scored[0][0]
    return chosen


def validation_kind_and_needle(validation):
    if re.search(r"navigates? to the .+ page", validation, flags=re.IGNORECASE):
        return "route", None
    quoted = re.findall(r'"([^"]{2,120})"', validation)
    if quoted:
        return "text", quoted[0].strip()
    patterns = [
        (r"displays the (.+?) heading", "text"),
        (r"displays the (.+?) page content", "text"),
        (r"displays the (.+?) content", "text"),
        (r"displays (.+?) content", "text"),
    ]
    for pattern, kind in patterns:
        match = re.search(pattern, validation, flags=re.IGNORECASE)
        if match:
            return kind, match.group(1).strip()
    lower = validation.lower()
    if "grid" in lower and ("image" in lower or "cover" in lower):
        return "image_grid", None
    if "thumbnail" in lower or "play button" in lower:
        return "media_grid", None
    if "service category card" in lower or "course card" in lower:
        return "card_grid", None
    if "form" in lower and "field" in lower:
        return "form", None
    if "branding" in lower or "logo" in lower:
        return "brand_or_logo", None
    if "ingredients and instructions" in lower:
        return "text_all", "ingredients instructions"
    if "service information" in lower:
        return "text_any", "service services"
    if "company information" in lower:
        return "text_any", "company leadership digital transformation"
    return "text", validation


def validate_content(validation, route_success, route, parsed):
    kind, needle = validation_kind_and_needle(validation)
    route_text = parsed["text_by_route"].get(route, "")
    combined_text = clean_text(parsed["global_text"] + " " + route_text)
    norm_text = norm(combined_text)
    if kind == "route":
        passed = route_success
    elif kind == "text":
        passed = norm(needle) in norm_text
    elif kind == "text_any":
        passed = any(term in norm_text for term in norm(needle).split())
    elif kind == "text_all":
        passed = all(term in norm_text for term in norm(needle).split())
    elif kind == "image_grid":
        passed = parsed["image_count_by_route"].get(route, 0) >= 3
    elif kind == "media_grid":
        passed = parsed["image_count_by_route"].get(route, 0) >= 2 or "video" in norm_text
    elif kind == "card_grid":
        passed = parsed["card_count_by_route"].get(route, 0) >= 2
    elif kind == "form":
        passed = parsed["input_count_by_route"].get(route, 0) >= 2 or "form" in norm_text
    elif kind == "brand_or_logo":
        passed = "logo" in norm_text or any(term in norm_text for term in {"gitlab", "duo"})
    else:
        passed = False
    return {
        "validation": validation,
        "kind": kind,
        "needle": needle,
        "passed": bool(passed),
    }


def run_dynamic(item_dir, run_dir):
    workflow = read_json(item_dir / "workflow.json")
    html_path = run_dir / "index.html"
    html = html_path.read_text(encoding="utf-8")
    parsed = parse_html(html)

    cases = []
    for block in workflow:
        for case_index, workflow_case in enumerate(block.get("content", [])):
            actions = workflow_case.get("actions", [])
            if not actions:
                continue
            current_route = parsed["default_route"]
            last_target = None
            action_reports = []
            case_error = None
            for action in actions:
                action_report = {"action": action, "passed": False}
                if action.lower().startswith("browser:back") or "navigate back" in action.lower():
                    current_route = parsed["default_route"]
                    action_report.update({
                        "method": "reset_to_default_route",
                        "route_after": current_route,
                        "passed": True,
                    })
                elif "click" in action.lower():
                    label = extract_action_label(action)
                    action_report["label"] = label
                    chosen = choose_clickable(label, parsed["clickables"], current_route) if label else None
                    if not chosen:
                        case_error = f"No clickable candidate for label {label!r}"
                        action_report["passed"] = False
                        action_reports.append(action_report)
                        break
                    target = chosen.get("target") or ""
                    action_report["chosen"] = {
                        "text": chosen.get("text", ""),
                        "target": target,
                        "href": chosen.get("href", ""),
                        "route_context": chosen.get("route_context", ""),
                        "score": chosen.get("score", 0),
                    }
                    if target and target in parsed["routes"]:
                        current_route = target
                        last_target = target
                        action_report["passed"] = True
                    else:
                        case_error = f"Chosen clickable has no valid data-route-target: {target!r}"
                        action_report["passed"] = False
                    action_report["route_after"] = current_route
                else:
                    action_report.update({"skipped": True, "passed": True})
                action_reports.append(action_report)

            route_success = bool(last_target is None or current_route == last_target)
            validation_reports = [
                validate_content(validation, route_success, current_route, parsed)
                for validation in workflow_case.get("validations", [])
            ]
            action_success = all(action.get("passed") for action in action_reports)
            content_success = all(validation.get("passed") for validation in validation_reports)
            cases.append({
                "block_index": block.get("index"),
                "case_index": case_index,
                "objective": workflow_case.get("objective", ""),
                "actions": action_reports,
                "validations": validation_reports,
                "final_route": current_route,
                "route_success": route_success and action_success,
                "content_validation_success": content_success,
                "passed": action_success and route_success and content_success,
                "error": case_error,
            })

    case_count = len(cases)
    route_success_count = sum(1 for case in cases if case["route_success"])
    content_success_count = sum(1 for case in cases if case["content_validation_success"])
    passed_count = sum(1 for case in cases if case["passed"])
    return {
        "item_id": item_dir.name,
        "run": run_dir.name,
        "html": str(html_path),
        "evaluator": "route-simulation-v1",
        "case_count": case_count,
        "passed_case_count": passed_count,
        "route_success_case_count": route_success_count,
        "content_validation_success_case_count": content_success_count,
        "task_success_rate": passed_count / case_count if case_count else 0,
        "route_success_rate": route_success_count / case_count if case_count else 0,
        "content_validation_success_rate": content_success_count / case_count if case_count else 0,
        "passed": passed_count == case_count,
        "cases": cases,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--items-dir", default=str(DEFAULT_ITEMS_DIR))
    parser.add_argument("--item", required=True)
    parser.add_argument("--run", required=True)
    parser.add_argument("--json-out")
    parser.add_argument("--no-fail", action="store_true")
    args = parser.parse_args()

    item_dir = Path(args.items_dir).resolve() / args.item
    run_dir = item_dir / "generated" / args.run
    if not item_dir.exists():
        raise SystemExit(f"ERROR: item not found: {item_dir}")
    if not run_dir.exists():
        raise SystemExit(f"ERROR: run not found: {run_dir}")

    report = run_dynamic(item_dir, run_dir)
    if args.json_out:
        out_path = Path(args.json_out)
    else:
        out_path = run_dir / "dynamic_workflow_report.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(json.dumps({
        "item_id": report["item_id"],
        "run": report["run"],
        "evaluator": report["evaluator"],
        "passed_case_count": report["passed_case_count"],
        "case_count": report["case_count"],
        "task_success_rate": report["task_success_rate"],
        "route_success_rate": report["route_success_rate"],
        "content_validation_success_rate": report["content_validation_success_rate"],
        "passed": report["passed"],
        "report": str(out_path),
    }, indent=2, ensure_ascii=False))
    if not report["passed"] and not args.no_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
