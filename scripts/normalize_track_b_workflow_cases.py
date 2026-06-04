"""
Normalize Track B workflow cases for independent browser-workflow scoring.

The item-level Vision2Web normalization already creates requirement.md,
workflow.json, and source_meta.json. This script handles a narrower issue:
some workflow cases assume that a previous case has already navigated to a
nested/sidebar page. Browser-workflow scoring treats each case independently,
so those cases need their own prerequisite navigation actions.

The script writes normalized workflow copies and a summary report. It does not
modify the original item workflow.json files.
"""

from __future__ import annotations

import argparse
import copy
import json
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ITEMS_DIR = PROJECT_ROOT / "data" / "track_b" / "items"
DEFAULT_OUT_DIR = PROJECT_ROOT / "data" / "track_b" / "workflows_normalized"


def read_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def has_action(actions, needle):
    needle_lower = needle.lower()
    return any(needle_lower in action.lower() for action in actions)


def normalize_case(item_id, block, case_index, workflow_case):
    updated = copy.deepcopy(workflow_case)
    actions = list(updated.get("actions", []))
    objective = updated.get("objective", "")
    changes = []

    if item_id == "F09_elections_bc" and has_action(actions, "Local Forms"):
        prereq = "Click the Learn more button in the 2026 GENERAL LOCAL ELECTIONS card"
        if not has_action(actions, "2026 GENERAL LOCAL ELECTIONS"):
            actions.insert(0, prereq)
            changes.append({
                "type": "insert_prerequisite",
                "reason": "Local Forms is a sidebar link visible after navigating to the local-elections page.",
                "inserted_action": prereq,
            })

    if item_id == "F06_community_dynamics" and "from the blogs page" in objective.lower():
        prereq = 'Click the "Discover events" navigation menu item'
        if has_action(actions, "breadcrumb link"):
            old_actions = actions
            actions = [prereq, 'Click the "Dynamics 365 Community" breadcrumb link']
            changes.append({
                "type": "replace_with_prerequisite_path",
                "reason": "The breadcrumb link is only visible on the blogs page; browser:back would reset an independent case to homepage.",
                "old_actions": old_actions,
                "new_actions": actions,
            })
        elif not has_action(actions, "Discover events"):
            actions.insert(0, prereq)
            changes.append({
                "type": "insert_prerequisite",
                "reason": "The Dynamics 365 Community navigation action is defined from the blogs page.",
                "inserted_action": prereq,
            })

    if changes:
        updated["actions"] = actions
        notes = list(updated.get("normalization_notes", []))
        for change in changes:
            notes.append(change["reason"])
        updated["normalization_notes"] = notes

    return updated, changes


def normalize_workflow(item_id, workflow):
    normalized = []
    changes = []
    for block in workflow:
        new_block = copy.deepcopy(block)
        new_content = []
        for case_index, workflow_case in enumerate(block.get("content", [])):
            updated_case, case_changes = normalize_case(item_id, block, case_index, workflow_case)
            new_content.append(updated_case)
            for change in case_changes:
                changes.append({
                    "item_id": item_id,
                    "block_index": block.get("index"),
                    "case_index": case_index,
                    "objective": workflow_case.get("objective", ""),
                    **change,
                })
        new_block["content"] = new_content
        normalized.append(new_block)
    return normalized, changes


def iter_item_dirs(items_dir: Path, requested_items):
    requested = set(requested_items or [])
    for item_dir in sorted(path for path in items_dir.iterdir() if path.is_dir()):
        if requested and item_dir.name not in requested:
            continue
        if (item_dir / "workflow.json").exists():
            yield item_dir


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--items-dir", type=Path, default=DEFAULT_ITEMS_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--item", action="append", default=[])
    args = parser.parse_args()

    reports = []
    for item_dir in iter_item_dirs(args.items_dir, args.item):
        original_path = item_dir / "workflow.json"
        workflow = read_json(original_path)
        normalized, changes = normalize_workflow(item_dir.name, workflow)
        normalized_path = args.out_dir / f"{item_dir.name}_browser_v1.json"
        write_json(normalized_path, normalized)
        reports.append({
            "item_id": item_dir.name,
            "original_workflow": str(original_path.relative_to(PROJECT_ROOT)),
            "normalized_workflow": str(normalized_path.relative_to(PROJECT_ROOT)),
            "change_count": len(changes),
            "changes": changes,
        })

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "normalizer": "workflow-case-normalization-v1",
        "purpose": "Make browser-workflow cases independently executable from the item homepage route.",
        "items": reports,
    }
    summary_path = args.out_dir / "normalization_summary.json"
    write_json(summary_path, summary)
    print(json.dumps({
        "summary": str(summary_path.relative_to(PROJECT_ROOT)),
        "item_count": len(reports),
        "changed_item_count": sum(1 for item in reports if item["change_count"]),
        "change_count": sum(item["change_count"] for item in reports),
    }, indent=2))


if __name__ == "__main__":
    main()
