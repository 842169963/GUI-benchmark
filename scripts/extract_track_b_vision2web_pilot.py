"""
Extract selected Vision2Web pilot task directories.

The Vision2Web Hugging Face repository stores task contents in large
archives. This script downloads the needed archives and extracts only
the tasks listed in `data/track_b/vision2web_pilot_manifest.json`.
"""

import argparse
import json
import os
import tarfile

from huggingface_hub import hf_hub_download

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DEFAULT_MANIFEST = os.path.join(
    PROJECT_ROOT, "data", "track_b", "vision2web_pilot_manifest.json"
)
DEFAULT_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "track_b", "vision2web_raw")

ARCHIVES = {
    "webpage": "archives/webpage.tar.gz",
    "frontend": "archives/frontend.tar.gz",
}


def load_manifest(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def path_matches(member_name, config_name, selected_tasks):
    normalized = member_name.replace("\\", "/").strip("/")
    parts = normalized.split("/")
    for task in selected_tasks:
        candidates = [
            [config_name, task],
            [task],
            ["datasets", config_name, task],
        ]
        for candidate in candidates:
            if len(parts) >= len(candidate) and parts[:len(candidate)] == candidate:
                return task
            if f"/{config_name}/{task}/" in f"/{normalized}/":
                return task
            if f"/{task}/" in f"/{normalized}/":
                return task
    return None


def stripped_member_path(member_name, config_name):
    normalized = member_name.replace("\\", "/").strip("/")
    parts = normalized.split("/")
    if len(parts) >= 2 and parts[0] == config_name:
        parts = parts[1:]
    elif len(parts) >= 3 and parts[0] == "datasets" and parts[1] == config_name:
        parts = parts[2:]
    return "/".join(parts)


def safe_extract_stripped_member(tar, member, target_root, config_name):
    relative = stripped_member_path(member.name, config_name)
    if not relative:
        return
    target_path = os.path.abspath(os.path.join(target_root, relative))
    root = os.path.abspath(target_root)
    if not target_path.startswith(root + os.sep) and target_path != root:
        raise RuntimeError(f"Refusing path traversal in tar member: {member.name}")
    if member.isdir():
        os.makedirs(target_path, exist_ok=True)
        return
    if not member.isfile():
        return
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    source = tar.extractfile(member)
    if source is None:
        return
    with source, open(target_path, "wb") as f:
        f.write(source.read())


def extract_config(config_name, tasks, output_dir, dry_run):
    archive_path = ARCHIVES[config_name]
    print(f"Downloading {archive_path} if not cached...")
    local_archive = hf_hub_download(
        "zai-org/Vision2Web",
        archive_path,
        repo_type="dataset",
    )
    print(f"Archive: {local_archive}")

    extracted = {task: 0 for task in tasks}
    config_output = os.path.join(output_dir, config_name)
    os.makedirs(config_output, exist_ok=True)

    with tarfile.open(local_archive, "r:gz") as tar:
        for member in tar:
            task = path_matches(member.name, config_name, tasks)
            if not task:
                continue
            extracted[task] += 1
            if dry_run:
                continue
            safe_extract_stripped_member(tar, member, config_output, config_name)

    for task, count in extracted.items():
        print(f"{config_name}/{task}: {count} archive members")
    missing = [task for task, count in extracted.items() if count == 0]
    if missing:
        raise SystemExit(f"No archive members found for {config_name}: {missing}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--configs", nargs="+", choices=["webpage", "frontend"],
                        default=["webpage", "frontend"])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    tasks_by_config = {config: [] for config in args.configs}
    for item in manifest["items"]:
        config = item["config"]
        if config in tasks_by_config:
            tasks_by_config[config].append(item["task_name"])

    for config, tasks in tasks_by_config.items():
        if tasks:
            extract_config(config, tasks, args.output_dir, args.dry_run)


if __name__ == "__main__":
    main()
