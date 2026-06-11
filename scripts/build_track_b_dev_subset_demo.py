"""
Build a failure-aware Track B v16 development-subset demo.

This script does not run generation or evaluation. It aggregates existing
F01/F03/F10 v16 artifacts into a small benchmark + leaderboard demo for
supervisor discussion.
"""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ITEMS_DIR = PROJECT_ROOT / "data" / "track_b" / "items"
OUT_DIR = PROJECT_ROOT / "data" / "track_b" / "leaderboard"


RUNS = [
    {
        "item": "F01_1daycloud",
        "model_label": "qwen3.6-35b-a3b",
        "run": "gwdg_qwen36_35b_v16_f01_dev",
    },
    {
        "item": "F03_about_gitlab",
        "model_label": "qwen3.6-35b-a3b",
        "run": "gwdg_qwen36_35b_v16_f03_compact_smoke",
    },
    {
        "item": "F10_gourmania",
        "model_label": "qwen3.6-35b-a3b",
        "run": "gwdg_qwen36_35b_v16_f10_dev",
    },
    {
        "item": "F06_community_dynamics",
        "model_label": "qwen3.6-35b-a3b",
        "run": "gwdg_qwen36_35b_v16_f06_dev_omit_maxtokens",
    },
    {
        "item": "F01_1daycloud",
        "model_label": "qwen3-omni-30b-a3b-instruct",
        "run": "gwdg_qwen3_omni_30b_v16_f01_dev_omit_maxtokens",
    },
    {
        "item": "F03_about_gitlab",
        "model_label": "qwen3-omni-30b-a3b-instruct",
        "run": "gwdg_qwen3_omni_30b_v16_f03_compact_smoke",
    },
    {
        "item": "F10_gourmania",
        "model_label": "qwen3-omni-30b-a3b-instruct",
        "run": "gwdg_qwen3_omni_30b_v16_f10_dev_omit_maxtokens",
    },
]


def read_json(path: Path):
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def rel(path: Path):
    return str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")


def usage(metadata):
    response = (metadata or {}).get("response_metadata", {})
    usage_data = response.get("usage") or {}
    return {
        "prompt_tokens": usage_data.get("prompt_tokens"),
        "completion_tokens": usage_data.get("completion_tokens"),
        "total_tokens": usage_data.get("total_tokens"),
        "finish_reason": response.get("finish_reason") or response.get("stop_reason"),
        "max_tokens": (metadata or {}).get("max_tokens"),
        "elapsed_seconds": (metadata or {}).get("elapsed_seconds"),
    }


def dynamic_report(run_dir: Path):
    for name in [
        "browser_workflow_normalized_report.json",
        "browser_workflow_report.json",
        "dynamic_workflow_report.json",
    ]:
        path = run_dir / name
        data = read_json(path)
        if data:
            return data, path
    return None, None


def classify_failure(gate, finish_reason, dynamic):
    if not gate:
        return "missing_gate_report"
    if finish_reason in {"length", "max_tokens"}:
        return "completion_truncation_failure"
    if not gate.get("passed"):
        return "static_gate_failure"
    if not dynamic:
        return "missing_dynamic_report"
    if dynamic.get("route_success_rate", 0) < 1:
        return "dynamic_route_or_content_failure"
    if dynamic.get("content_validation_success_rate", 0) < 1:
        return "content_validation_failure"
    return "passed_all_current_checks"


def artifact_row(spec):
    run_dir = ITEMS_DIR / spec["item"] / "generated" / spec["run"]
    metadata_path = run_dir / "generation_metadata.json"
    gate_path = run_dir / "gate_report.json"
    metadata = read_json(metadata_path)
    gate = read_json(gate_path)
    dynamic, dynamic_path = dynamic_report(run_dir)
    tokens = usage(metadata)
    failure_category = classify_failure(gate, tokens["finish_reason"], dynamic)
    eligible = bool(gate and gate.get("passed") and tokens["finish_reason"] not in {"length", "max_tokens"} and dynamic)
    provider = (metadata or {}).get("provider", "unknown-provider")
    model = (metadata or {}).get("model", spec["model_label"])
    prompt = (metadata or {}).get("prompt_id", "unknown-prompt")
    return {
        "item": spec["item"],
        "run": spec["run"],
        "model_label": spec["model_label"],
        "model_key": f"{provider}/{model}/{prompt}",
        "artifact": rel(run_dir / "index.html") if (run_dir / "index.html").exists() else None,
        "metadata": rel(metadata_path) if metadata_path.exists() else None,
        "gate_report": rel(gate_path) if gate_path.exists() else None,
        "dynamic_report": rel(dynamic_path) if dynamic_path else None,
        "finish_reason": tokens["finish_reason"],
        "max_tokens": tokens["max_tokens"],
        "prompt_tokens": tokens["prompt_tokens"],
        "completion_tokens": tokens["completion_tokens"],
        "elapsed_seconds": tokens["elapsed_seconds"],
        "static_gate_passed": bool(gate and gate.get("passed")),
        "gate_errors": gate.get("failed_error_count") if gate else None,
        "gate_warnings": gate.get("failed_warning_count") if gate else None,
        "eligible": eligible,
        "failure_category": failure_category,
        "workflow_passed": dynamic.get("passed_case_count") if dynamic else None,
        "workflow_cases": dynamic.get("case_count") if dynamic else None,
        "route_success": dynamic.get("route_success_rate") if dynamic else None,
        "content_success": dynamic.get("content_validation_success_rate") if dynamic else None,
        "task_success": dynamic.get("task_success_rate") if dynamic else None,
    }


def avg(values):
    nums = [value for value in values if isinstance(value, (int, float))]
    return mean(nums) if nums else None


def model_rows(artifacts):
    grouped = defaultdict(list)
    for artifact in artifacts:
        grouped[artifact["model_key"]].append(artifact)

    rows = []
    for model, group in grouped.items():
        eligible = [item for item in group if item["eligible"]]
        rows.append({
            "model": model,
            "attempted_items": len(group),
            "generated_artifacts": sum(1 for item in group if item["artifact"]),
            "provider_failures": 0,
            "truncation_failures": sum(1 for item in group if item["failure_category"] == "completion_truncation_failure"),
            "static_gate_passed": sum(1 for item in group if item["static_gate_passed"]),
            "eligible_artifacts": len(eligible),
            "average_route_success": avg([item["route_success"] for item in eligible]),
            "average_content_success": avg([item["content_success"] for item in eligible]),
            "average_task_success": avg([item["task_success"] for item in eligible]),
            "average_completion_tokens": avg([item["completion_tokens"] for item in group]),
            "note": note_for_model(group, eligible),
        })
    rows.sort(
        key=lambda row: (
            row["eligible_artifacts"],
            row["average_task_success"] if row["average_task_success"] is not None else -1,
            -row["truncation_failures"],
        ),
        reverse=True,
    )
    for index, row in enumerate(rows, start=1):
        row["rank"] = index
    return rows


def note_for_model(group, eligible):
    if len(eligible) == len(group):
        return "All dev-subset artifacts complete and eligible; remaining losses are dynamic/content quality."
    failures = [item for item in group if not item["eligible"]]
    categories = sorted({item["failure_category"] for item in failures})
    return "Ineligible artifacts: " + ", ".join(categories)


def fmt(value):
    if isinstance(value, float):
        return f"{value:.3f}"
    if isinstance(value, int):
        return str(value)
    if value is None:
        return "n/a"
    return str(value)


def markdown(payload):
    lines = [
        "# Track B v16 Dev-Subset Pipeline Demo",
        "",
        f"Generated at: `{payload['generated_at']}`",
        "",
        "Scope: fixed-item benchmark demo using `F01_1daycloud`, `F03_about_gitlab`, `F06_community_dynamics`, and `F10_gourmania`.",
        "",
        "Prompt/input policy: `TB-GEN-v16`, compact input. OpenAI-compatible runs use omitted `max_tokens` where rerun evidence exists.",
        "",
        "## Model-Level Leaderboard",
        "",
        "| Rank | Model/config | Attempted | Generated | Truncation failures | Static pass | Eligible | Avg route | Avg content | Avg task | Avg completion tok. | Note |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in payload["models"]:
        lines.append(
            "| {rank} | `{model}` | {attempted} | {generated} | {trunc} | {static} | {eligible} | {route} | {content} | {task} | {tokens} | {note} |".format(
                rank=row["rank"],
                model=row["model"],
                attempted=row["attempted_items"],
                generated=row["generated_artifacts"],
                trunc=row["truncation_failures"],
                static=row["static_gate_passed"],
                eligible=row["eligible_artifacts"],
                route=fmt(row["average_route_success"]),
                content=fmt(row["average_content_success"]),
                task=fmt(row["average_task_success"]),
                tokens=fmt(row["average_completion_tokens"]),
                note=row["note"],
            )
        )

    lines.extend([
        "",
        "## Artifact-Level Evidence",
        "",
        "| Item | Model | Run | Finish | Gate | Workflow | Route | Content | Failure category |",
        "| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |",
    ])
    for item in payload["artifacts"]:
        workflow = "n/a"
        if item["workflow_passed"] is not None and item["workflow_cases"] is not None:
            workflow = f"{item['workflow_passed']}/{item['workflow_cases']}"
        lines.append(
            "| {item} | `{model}` | `{run}` | `{finish}` | {gate} | {workflow} | {route} | {content} | `{category}` |".format(
                item=item["item"],
                model=item["model_label"],
                run=item["run"],
                finish=item["finish_reason"],
                gate="pass" if item["static_gate_passed"] else "fail",
                workflow=workflow,
                route=fmt(item["route_success"]),
                content=fmt(item["content_success"]),
                category=item["failure_category"],
            )
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "- This is a pipeline demo, not the final formal leaderboard.",
        "- The demo shows generation, static technical gating, browser-workflow scoring, model aggregation, and explicit failure accounting.",
        "- `qwen3.6-35b-a3b` completes all four demo items and enters scoring for all four.",
        "- `qwen3-omni-30b-a3b-instruct` completes F03 and F10, but F01 remains a completion/truncation failure even without a client-side `max_tokens` field.",
        "- The next thesis step is to expose this failure accounting in the main leaderboard pipeline before expanding to more items.",
    ])
    return "\n".join(lines) + "\n"


def main():
    artifacts = [artifact_row(spec) for spec in RUNS]
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": {
            "items": ["F01_1daycloud", "F03_about_gitlab", "F06_community_dynamics", "F10_gourmania"],
            "prompt_id": "TB-GEN-v16",
            "input_profile": "compact",
            "purpose": "failure-aware benchmark + leaderboard pipeline demo",
        },
        "models": model_rows(artifacts),
        "artifacts": artifacts,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUT_DIR / "dev_subset_v16_failure_demo.json"
    md_path = OUT_DIR / "dev_subset_v16_failure_demo.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_path.write_text(markdown(payload), encoding="utf-8")
    print(json.dumps({
        "json": rel(json_path),
        "markdown": rel(md_path),
        "artifact_count": len(artifacts),
        "model_count": len(payload["models"]),
    }, indent=2))


if __name__ == "__main__":
    main()
