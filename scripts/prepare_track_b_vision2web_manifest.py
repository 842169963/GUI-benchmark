"""
Create a small Vision2Web pilot manifest for Track B.

This script reads metadata from the Hugging Face dataset
`zai-org/Vision2Web` and writes a normalized JSON manifest for the
selected Level 1 / Level 2 pilot tasks. It intentionally does not
download the large task archives.
"""

import argparse
import json
import os
from datetime import datetime

import datasets.config as datasets_config
from datasets import load_dataset

datasets_config.TORCH_AVAILABLE = False

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DEFAULT_OUTPUT = os.path.join(
    PROJECT_ROOT, "data", "track_b", "vision2web_pilot_manifest.json"
)

FRONTEND_TASKS = [
    "1daycloud",
    "401trucksource",
    "about_gitlab",
    "academy_govloop",
    "balancingbirthbaby",
    "community_dynamics",
    "community_hpe",
    "copenhagenmarathon",
    "elections_bc",
    "gourmania",
]

WEBPAGE_TASKS = [
    "aihw",
    "aws",
    "eventbrite",
    "ebay",
]


def load_rows(config_name):
    rows = {}
    dataset = load_dataset(
        "zai-org/Vision2Web",
        config_name,
        split="test",
        streaming=True,
    )
    for row in dataset:
        rows[row["task_name"]] = row
    return rows


def normalize_row(row, config_name):
    item_id_prefix = "F" if config_name == "frontend" else "W"
    return {
        "source": "zai-org/Vision2Web",
        "config": config_name,
        "level": row["level"],
        "task_name": row["task_name"],
        "workflow_steps": int(row["workflow_steps"]),
        "num_test_cases": int(row["num_test_cases"]),
        "resources_count": int(row["resources_count"]),
        "prototypes": list(row["prototypes"]),
        "prompt_preview": row.get("prompt_preview"),
        "local_raw_dir": f"data/track_b/vision2web_raw/{config_name}/{row['task_name']}",
        "normalized_item_dir": "",
        "use_for_static": True,
        "use_for_dynamic": config_name == "frontend",
        "notes": "",
        "item_id_prefix": item_id_prefix,
    }


def add_item_ids(items):
    counters = {"F": 0, "W": 0}
    for item in items:
        prefix = item.pop("item_id_prefix")
        counters[prefix] += 1
        item_id = f"{prefix}{counters[prefix]:02d}_{item['task_name']}"
        item["item_id"] = item_id
        item["normalized_item_dir"] = f"data/track_b/items/{item_id}"
    return items


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    frontend_rows = load_rows("frontend")
    webpage_rows = load_rows("webpage")

    items = []
    missing = []
    for task in FRONTEND_TASKS:
        row = frontend_rows.get(task)
        if row:
            items.append(normalize_row(row, "frontend"))
        else:
            missing.append(("frontend", task))
    for task in WEBPAGE_TASKS:
        row = webpage_rows.get(task)
        if row:
            items.append(normalize_row(row, "webpage"))
        else:
            missing.append(("webpage", task))

    if missing:
        raise SystemExit(f"Missing selected tasks: {missing}")

    items = add_item_ids(items)
    manifest = {
        "created_at": datetime.now().isoformat(),
        "source_dataset": "zai-org/Vision2Web",
        "license": "CC-BY-NC-SA-4.0",
        "scope": {
            "included": ["Level 1 static webpage", "Level 2 interactive frontend"],
            "excluded": ["Level 3 full-stack website"],
            "reason": (
                "Level 3 introduces backend state, deployment, authentication, "
                "and long-horizon workflow complexity outside the thesis scope."
            ),
        },
        "selection_summary": {
            "frontend_level2_dynamic_items": len(FRONTEND_TASKS),
            "webpage_level1_static_controls": len(WEBPAGE_TASKS),
            "total_items": len(items),
        },
        "items": items,
    }

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(items)} pilot items to {args.output}")
    for item in items:
        print(
            f"{item['item_id']}: {item['config']} {item['task_name']} "
            f"tests={item['num_test_cases']} resources={item['resources_count']}"
        )


if __name__ == "__main__":
    main()

