"""
Build a schema-v1 Track B development-subset demo.

This script does not run generation or evaluation. It aggregates existing
F-series dynamic artifacts and one W-series static/responsive probe into a
failure-aware benchmark + leaderboard payload.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ITEMS_DIR = PROJECT_ROOT / "data" / "track_b" / "items"
OUT_DIR = PROJECT_ROOT / "data" / "track_b" / "leaderboard"
SCHEMA_VERSION = "track-b-leaderboard-v1"

METRIC_VERSIONS = {
    "static_technical": "static-gate-v2-relaxed",
    "dynamic": "browser-workflow-v1",
    "static_visual": "pending-judge-validation",
    "accessibility": "axe-weighted-density-v1",
    "efficiency": "raw-token-latency-v1",
    "failure_taxonomy": "track-b-failure-taxonomy-v1",
}

RUNS = [
    ("F01_1daycloud", "qwen3.6-35b-a3b", "gwdg_qwen36_35b_v16_f01_dev"),
    ("F03_about_gitlab", "qwen3.6-35b-a3b", "gwdg_qwen36_35b_v16_f03_compact_smoke"),
    ("F06_community_dynamics", "qwen3.6-35b-a3b", "gwdg_qwen36_35b_v16_f06_dev_omit_maxtokens"),
    ("F10_gourmania", "qwen3.6-35b-a3b", "gwdg_qwen36_35b_v16_f10_dev"),
    ("W03_eventbrite", "qwen3.6-35b-a3b", "gwdg_qwen36_35b_v16_w03_static_omit_maxtokens"),
    ("F01_1daycloud", "qwen3-omni-30b-a3b-instruct", "gwdg_qwen3_omni_30b_v16_f01_dev_omit_maxtokens"),
    ("F03_about_gitlab", "qwen3-omni-30b-a3b-instruct", "gwdg_qwen3_omni_30b_v16_f03_compact_smoke"),
    ("F10_gourmania", "qwen3-omni-30b-a3b-instruct", "gwdg_qwen3_omni_30b_v16_f10_dev_omit_maxtokens"),
]


def read_json(path: Path):
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def rel(path: Path | None):
    if path is None:
        return None
    return str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")


def item_branch(item_id: str):
    return "static_responsive" if item_id.startswith("W") else "executable_workflow"


def model_key(metadata, fallback_model):
    provider = (metadata or {}).get("provider", "unknown-provider")
    model = (metadata or {}).get("model", fallback_model)
    prompt = (metadata or {}).get("prompt_id", "unknown-prompt")
    return f"{provider}/{model}/{prompt}"


def usage(metadata):
    response = (metadata or {}).get("response_metadata", {})
    usage_data = response.get("usage") or {}
    return {
        "finish_reason": response.get("finish_reason") or response.get("stop_reason"),
        "max_tokens": (metadata or {}).get("max_tokens"),
        "prompt_tokens": usage_data.get("prompt_tokens"),
        "completion_tokens": usage_data.get("completion_tokens"),
        "total_tokens": usage_data.get("total_tokens"),
        "latency_seconds": (metadata or {}).get("elapsed_seconds"),
    }


def gate_score(gate):
    checks = (gate or {}).get("checks", [])
    score = None
    if checks:
        score = sum(1 for check in checks if check.get("passed")) / len(checks)
    elif gate:
        score = 1.0 if gate.get("passed") else 0.0
    return {
        "available": gate is not None,
        "passed": bool(gate and gate.get("passed")),
        "score": score,
        "errors": (gate or {}).get("failed_error_count"),
        "warnings": (gate or {}).get("failed_warning_count"),
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


def screenshot_manifest(run_dir: Path):
    path = run_dir / "standard_screenshots" / "manifest.json"
    data = read_json(path)
    return data, path if data else None


def applicable_metrics(branch: str):
    if branch == "static_responsive":
        return ["static_technical", "static_visual", "accessibility", "efficiency"]
    return ["static_technical", "dynamic", "static_visual", "accessibility", "efficiency"]


def not_applicable_metrics(branch: str):
    if branch == "static_responsive":
        return ["dynamic"]
    return []


def classify(branch, gate, finish_reason, dynamic):
    if finish_reason in {"length", "max_tokens"}:
        return "completion_truncation_failure", "Generation ended by length/max-token stop and the artifact is structurally incomplete or suspect."
    if not gate["passed"]:
        return "static_gate_failure", "Static technical gate failed."
    if branch == "static_responsive":
        return "passed_static_responsive_checks", "Static responsive artifact passed the technical gate; visual score is pending."
    if not dynamic:
        return "missing_dynamic_report", "Dynamic report is missing for a workflow item."
    if dynamic.get("route_success_rate", 0) < 1:
        return "dynamic_route_or_content_failure", "At least one workflow route did not reach the expected destination."
    if dynamic.get("content_validation_success_rate", 0) < 1:
        return "content_validation_failure", "Routes work, but destination content evidence is incomplete."
    return "passed_all_current_checks", "Artifact passed all currently implemented checks."


def artifact_result(item_id: str, model_label: str, run: str):
    branch = item_branch(item_id)
    run_dir = ITEMS_DIR / item_id / "generated" / run
    metadata_path = run_dir / "generation_metadata.json"
    gate_path = run_dir / "gate_report.json"
    metadata = read_json(metadata_path)
    gate = gate_score(read_json(gate_path))
    dynamic, dynamic_path = dynamic_report(run_dir)
    screenshots, screenshot_path = screenshot_manifest(run_dir)
    gen = usage(metadata)
    failure_category, failure_reason = classify(branch, gate, gen["finish_reason"], dynamic)
    eligible = bool(
        gate["passed"]
        and gen["finish_reason"] not in {"length", "max_tokens"}
        and (branch == "static_responsive" or dynamic is not None)
    )
    dyn_status = "not_applicable" if branch == "static_responsive" else ("available" if dynamic else "missing")
    visual_status = "pending_rubric_scoring" if screenshots else "pending_standard_screenshots"

    return {
        "artifact_result_id": f"{item_id}::{run}",
        "item_id": item_id,
        "item_branch": branch,
        "model_label": model_label,
        "model_key": model_key(metadata, model_label),
        "run": run,
        "paths": {
            "artifact": rel(run_dir / "index.html") if (run_dir / "index.html").exists() else None,
            "metadata": rel(metadata_path) if metadata_path.exists() else None,
            "gate_report": rel(gate_path) if gate_path.exists() else None,
            "dynamic_report": rel(dynamic_path),
            "screenshot_manifest": rel(screenshot_path),
        },
        "applicable_metrics": applicable_metrics(branch),
        "not_applicable_metrics": not_applicable_metrics(branch),
        "generation": gen,
        "static_technical": gate,
        "dynamic": {
            "status": dyn_status,
            "route_success": dynamic.get("route_success_rate") if dynamic else None,
            "content_success": dynamic.get("content_validation_success_rate") if dynamic else None,
            "task_success": dynamic.get("task_success_rate") if dynamic else None,
            "passed_cases": dynamic.get("passed_case_count") if dynamic else None,
            "case_count": dynamic.get("case_count") if dynamic else None,
        },
        "static_visual": {
            "status": visual_status,
            "score": None,
            "screenshot_coverage": screenshots.get("screenshot_coverage") if screenshots else None,
        },
        "accessibility": {
            "status": "pending",
            "score": None,
        },
        "efficiency": {
            "status": "raw_only",
            "score": None,
            "total_tokens": gen["total_tokens"],
            "latency_seconds": gen["latency_seconds"],
        },
        "eligibility": {
            "eligible": eligible,
            "failure_category": failure_category,
            "failure_reason": failure_reason,
        },
    }


def avg(values):
    nums = [value for value in values if isinstance(value, (int, float))]
    return mean(nums) if nums else None


def model_results(artifacts):
    grouped = defaultdict(list)
    for artifact in artifacts:
        grouped[artifact["model_key"]].append(artifact)

    rows = []
    for model, group in grouped.items():
        eligible = [item for item in group if item["eligibility"]["eligible"]]
        failed = [item for item in group if not item["eligibility"]["eligible"]]
        failure_by_item = {
            item["item_id"]: {
                "category": item["eligibility"]["failure_category"],
                "reason": item["eligibility"]["failure_reason"],
                "finish_reason": item["generation"]["finish_reason"],
                "completion_tokens": item["generation"]["completion_tokens"],
                "run": item["run"],
            }
            for item in failed
        }
        counts = Counter(item["eligibility"]["failure_category"] for item in failed)
        rows.append({
            "model_key": model,
            "attempted_items": [item["item_id"] for item in group],
            "eligible_items": [item["item_id"] for item in eligible],
            "failed_items": [item["item_id"] for item in failed],
            "failure_by_item": failure_by_item,
            "failure_category_counts": dict(counts),
            "completion_reliability": len(eligible) / len(group) if group else None,
            "category_scores": {
                "static_technical": avg([item["static_technical"]["score"] for item in eligible]),
                "dynamic": avg([item["dynamic"]["task_success"] for item in eligible if "dynamic" in item["applicable_metrics"]]),
                "static_visual": None,
                "accessibility": None,
                "efficiency": None,
            },
            "raw_averages": {
                "route_success": avg([item["dynamic"]["route_success"] for item in eligible if item["dynamic"]["route_success"] is not None]),
                "content_success": avg([item["dynamic"]["content_success"] for item in eligible if item["dynamic"]["content_success"] is not None]),
                "completion_tokens": avg([item["generation"]["completion_tokens"] for item in group]),
                "latency_seconds": avg([item["generation"]["latency_seconds"] for item in group]),
            },
            "overall_score": None,
            "rankings": {},
        })
    add_rankings(rows)
    return rows


def add_rankings(rows):
    ranking_specs = {
        "completion_reliability_rank": lambda row: row["completion_reliability"],
        "static_technical_rank": lambda row: row["category_scores"]["static_technical"],
        "dynamic_rank": lambda row: row["category_scores"]["dynamic"],
    }
    for rank_name, getter in ranking_specs.items():
        sortable = [row for row in rows if getter(row) is not None]
        sortable.sort(key=getter, reverse=True)
        for index, row in enumerate(sortable, start=1):
            row["rankings"][rank_name] = index
        for row in rows:
            row["rankings"].setdefault(rank_name, None)
        for row in rows:
            row["rankings"]["overall_rank"] = None


def category_rankings(rows):
    output = {}
    for rank_name, label in [
        ("completion_reliability_rank", "completion_reliability"),
        ("static_technical_rank", "static_technical"),
        ("dynamic_rank", "dynamic"),
    ]:
        ranked = sorted(
            [row for row in rows if row["rankings"].get(rank_name) is not None],
            key=lambda row: row["rankings"][rank_name],
        )
        output[label] = [
            {
                "rank": row["rankings"][rank_name],
                "model_key": row["model_key"],
                "score": row["completion_reliability"] if label == "completion_reliability" else row["category_scores"][label],
            }
            for row in ranked
        ]
    output["overall"] = []
    return output


def fmt(value):
    if isinstance(value, float):
        return f"{value:.3f}"
    if isinstance(value, int):
        return str(value)
    if value is None:
        return "pending"
    return str(value)


def markdown(payload):
    rows = payload["model_results"]
    lines = [
        "# Track B Schema v1 Demo Leaderboard",
        "",
        f"Schema: `{payload['leaderboard_schema_version']}`",
        f"Generated at: `{payload['generated_at']}`",
        "",
        "This is a meeting demo, not the final formal leaderboard. It shows schema-aligned failure-aware reporting.",
        "",
        "## Model-Level Rows",
        "",
        "| Model/config | Attempted | Eligible | Failed | Completion reliability | Static technical | Dynamic task | Route | Content | Overall | Failure detail |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        failure_detail = ", ".join(f"{item}:{detail['category']}" for item, detail in row["failure_by_item"].items()) or "none"
        lines.append(
            "| `{model}` | {attempted} | {eligible} | {failed} | {rel} | {tech} | {dyn} | {route} | {content} | {overall} | {failure} |".format(
                model=row["model_key"],
                attempted=len(row["attempted_items"]),
                eligible=len(row["eligible_items"]),
                failed=len(row["failed_items"]),
                rel=fmt(row["completion_reliability"]),
                tech=fmt(row["category_scores"]["static_technical"]),
                dyn=fmt(row["category_scores"]["dynamic"]),
                route=fmt(row["raw_averages"]["route_success"]),
                content=fmt(row["raw_averages"]["content_success"]),
                overall=fmt(row["overall_score"]),
                failure=failure_detail,
            )
        )

    lines.extend([
        "",
        "## Artifact-Level Rows",
        "",
        "| Item | Branch | Model | Finish | Gate | Dynamic | Screenshots | Eligible | Failure category |",
        "| --- | --- | --- | --- | --- | ---: | ---: | --- | --- |",
    ])
    for item in payload["artifact_results"]:
        dynamic = "n/a"
        if item["dynamic"]["case_count"] is not None:
            dynamic = f"{item['dynamic']['passed_cases']}/{item['dynamic']['case_count']}"
        screenshots = fmt(item["static_visual"]["screenshot_coverage"])
        lines.append(
            "| {item} | {branch} | `{model}` | `{finish}` | {gate} | {dynamic} | {screens} | {eligible} | `{failure}` |".format(
                item=item["item_id"],
                branch=item["item_branch"],
                model=item["model_label"],
                finish=item["generation"]["finish_reason"],
                gate="pass" if item["static_technical"]["passed"] else "fail",
                dynamic=dynamic,
                screens=screenshots,
                eligible="yes" if item["eligibility"]["eligible"] else "no",
                failure=item["eligibility"]["failure_category"],
            )
        )

    lines.extend([
        "",
        "## Pending Metric Slots",
        "",
        "- Static visual score: schema slot present; pending validated visual judge / human rubric.",
        "- Accessibility score: schema slot present; pending integration of axe weighted-density reports.",
        "- Efficiency score: raw token/latency fields present; normalized score pending cost reference.",
        "- Overall score: intentionally pending until category weights are approved.",
    ])
    return "\n".join(lines) + "\n"


def main():
    artifacts = [artifact_result(*spec) for spec in RUNS]
    models = model_results(artifacts)
    payload = {
        "leaderboard_schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": {
            "prompt_id": "TB-GEN-v16",
            "input_profile": "compact",
            "item_subset": sorted({item["item_id"] for item in artifacts}),
            "ranking_target": "generator_model_configuration",
            "evaluation_target": "generated_ui_artifact",
            "notes": "F-series items use dynamic workflow metrics; W-series static responsive items exclude dynamic as not applicable.",
        },
        "metric_versions": METRIC_VERSIONS,
        "artifact_results": artifacts,
        "model_results": models,
        "category_rankings": category_rankings(models),
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    schema_json = OUT_DIR / "dev_subset_v16_schema_v1_demo.json"
    schema_md = OUT_DIR / "dev_subset_v16_schema_v1_demo.md"
    schema_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    schema_md.write_text(markdown(payload), encoding="utf-8")

    # Keep the earlier failure-demo filenames as aliases for continuity.
    (OUT_DIR / "dev_subset_v16_failure_demo.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (OUT_DIR / "dev_subset_v16_failure_demo.md").write_text(markdown(payload), encoding="utf-8")

    print(json.dumps({
        "schema_json": rel(schema_json),
        "schema_markdown": rel(schema_md),
        "artifact_count": len(artifacts),
        "model_count": len(models),
    }, indent=2))


if __name__ == "__main__":
    main()
