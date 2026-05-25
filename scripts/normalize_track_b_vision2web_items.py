"""
Normalize selected Vision2Web pilot tasks into Track B item directories.

Input:
  data/track_b/vision2web_pilot_manifest.json
  data/track_b/vision2web_raw/{frontend,webpage}/{task_name}/...

Output:
  data/track_b/items/{item_id}/
    requirement.md
    workflow.json
    prototypes/
    resources/
    source_meta.json
    generated/
    renders/
"""

import argparse
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = PROJECT_ROOT / "data" / "track_b" / "vision2web_pilot_manifest.json"
DEFAULT_OUTPUT_ROOT = PROJECT_ROOT / "data" / "track_b" / "items"
DEFAULT_RAW_ROOT = PROJECT_ROOT / "data" / "track_b" / "vision2web_raw"
DEFAULT_SUMMARY = PROJECT_ROOT / "data" / "track_b" / "normalization_summary.json"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def assert_inside(path, root):
    path = path.resolve()
    root = root.resolve()
    if path != root and root not in path.parents:
        raise RuntimeError(f"Path {path} is outside expected root {root}")


def copy_tree(src, dst):
    if not src.exists():
        return False
    shutil.copytree(src, dst, dirs_exist_ok=True)
    return True


def write_frontend_requirement(raw_dir, out_path, item):
    prompt_path = raw_dir / "prompt.txt"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Missing prompt.txt for frontend task {item['task_name']}")
    text = prompt_path.read_text(encoding="utf-8").strip()
    out_path.write_text(
        "# Requirement\n\n"
        f"Source task: `{item['task_name']}`\n\n"
        "The generated interface should implement the following Vision2Web "
        "Level 2 frontend requirement.\n\n"
        f"{text}\n",
        encoding="utf-8",
    )


def write_webpage_requirement(raw_dir, out_path, item):
    workflow = load_json(raw_dir / "workflow.json")
    prototypes = item.get("prototypes", [])
    resolutions = []
    for step in workflow:
        summary = step.get("summary", "prototype")
        resolution = step.get("resolution", {})
        width = resolution.get("width")
        height = resolution.get("height")
        resolutions.append(f"- {summary}: {width}x{height}")
    out_path.write_text(
        "# Requirement\n\n"
        f"Source task: `{item['task_name']}`\n\n"
        "Build a responsive static webpage that visually matches the provided "
        "Vision2Web Level 1 prototypes. The output should be a self-contained "
        "HTML/CSS implementation that can be rendered locally without external "
        "services. Preserve the visible layout, hierarchy, typography, imagery, "
        "and responsive structure shown in the prototype images.\n\n"
        "Prototype files:\n"
        + "\n".join(f"- `{name}`" for name in prototypes)
        + "\n\nTarget viewport checks:\n"
        + "\n".join(resolutions)
        + "\n",
        encoding="utf-8",
    )


def normalize_item(item, raw_root, output_root, overwrite):
    raw_dir = raw_root / item["config"] / item["task_name"]
    if not raw_dir.exists():
        raise FileNotFoundError(f"Missing raw task directory: {raw_dir}")

    item_dir = output_root / item["item_id"]
    assert_inside(item_dir, output_root)
    if item_dir.exists() and overwrite:
        shutil.rmtree(item_dir)
    item_dir.mkdir(parents=True, exist_ok=True)

    if item["config"] == "frontend":
        write_frontend_requirement(raw_dir, item_dir / "requirement.md", item)
    elif item["config"] == "webpage":
        write_webpage_requirement(raw_dir, item_dir / "requirement.md", item)
    else:
        raise ValueError(f"Unsupported config: {item['config']}")

    shutil.copy2(raw_dir / "workflow.json", item_dir / "workflow.json")
    copied_prototypes = copy_tree(raw_dir / "prototypes", item_dir / "prototypes")
    copied_resources = copy_tree(raw_dir / "resources", item_dir / "resources")

    (item_dir / "generated").mkdir(exist_ok=True)
    (item_dir / "renders").mkdir(exist_ok=True)

    source_meta = {
        "normalized_at": datetime.now().isoformat(),
        "item_id": item["item_id"],
        "source_dataset": item["source"],
        "source_config": item["config"],
        "source_level": item["level"],
        "source_task_name": item["task_name"],
        "source_license": "CC-BY-NC-SA-4.0",
        "raw_dir": str(raw_dir.relative_to(PROJECT_ROOT)),
        "workflow_steps": item["workflow_steps"],
        "num_test_cases": item["num_test_cases"],
        "resources_count": item["resources_count"],
        "prototypes": item["prototypes"],
        "use_for_static": item["use_for_static"],
        "use_for_dynamic": item["use_for_dynamic"],
        "copied_prototypes": copied_prototypes,
        "copied_resources": copied_resources,
    }
    (item_dir / "source_meta.json").write_text(
        json.dumps(source_meta, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return {
        "item_id": item["item_id"],
        "task_name": item["task_name"],
        "config": item["config"],
        "item_dir": str(item_dir.relative_to(PROJECT_ROOT)),
        "copied_prototypes": copied_prototypes,
        "copied_resources": copied_resources,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    manifest = load_json(args.manifest)
    args.output_root.mkdir(parents=True, exist_ok=True)

    normalized = []
    for item in manifest["items"]:
        normalized.append(
            normalize_item(item, args.raw_root, args.output_root, args.overwrite)
        )

    summary = {
        "created_at": datetime.now().isoformat(),
        "manifest": str(args.manifest.relative_to(PROJECT_ROOT)),
        "output_root": str(args.output_root.relative_to(PROJECT_ROOT)),
        "item_count": len(normalized),
        "items": normalized,
    }
    args.summary.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Normalized {len(normalized)} Track B items into {args.output_root}")
    print(f"Summary: {args.summary}")
    for item in normalized:
        print(f"{item['item_id']}: {item['item_dir']}")


if __name__ == "__main__":
    main()

