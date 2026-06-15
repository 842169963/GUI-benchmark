"""
Build Track B artifact-level results and a mini model-level leaderboard.

This script aggregates existing generation metadata, static gate reports,
standardized screenshot manifests, and dynamic workflow reports. It does not run
new generation or real-agent execution.

Examples:
    python scripts/build_track_b_mini_leaderboard.py --prompt-id TB-GEN-v9
    python scripts/build_track_b_mini_leaderboard.py --prompt-id TB-GEN-v9 --include-ineligible
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ITEMS_DIR = PROJECT_ROOT / "data" / "track_b" / "items"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "track_b" / "leaderboard"


def read_json(path: Path):
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def rel(path: Path | None):
    if path is None:
        return None
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def nested_get(data, *keys, default=None):
    current = data or {}
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def score_gate(gate):
    if not gate:
        return {
            "score": None,
            "passed": False,
            "available": False,
            "failed_error_count": None,
            "failed_warning_count": None,
            "report": None,
        }
    checks = gate.get("checks", [])
    if checks:
        score = sum(1 for check in checks if check.get("passed")) / len(checks)
    else:
        score = 1.0 if gate.get("passed") else 0.0
    return {
        "score": score,
        "passed": bool(gate.get("passed")),
        "available": True,
        "failed_error_count": gate.get("failed_error_count"),
        "failed_warning_count": gate.get("failed_warning_count"),
    }


def dynamic_report(run_dir: Path):
    normalized_browser = read_json(run_dir / "browser_workflow_normalized_report.json")
    if normalized_browser:
        return normalized_browser, run_dir / "browser_workflow_normalized_report.json"
    browser = read_json(run_dir / "browser_workflow_report.json")
    if browser:
        return browser, run_dir / "browser_workflow_report.json"
    route_sim = read_json(run_dir / "dynamic_workflow_report.json")
    if route_sim:
        return route_sim, run_dir / "dynamic_workflow_report.json"
    return None, None


def visual_manifest(run_dir: Path):
    manifest_path = run_dir / "standard_screenshots" / "manifest.json"
    manifest = read_json(manifest_path)
    return manifest, manifest_path if manifest else None


def usage_from_metadata(metadata):
    usage = nested_get(metadata, "response_metadata", "usage", default={}) or {}
    return {
        "input_tokens": usage.get("prompt_tokens"),
        "output_tokens": usage.get("completion_tokens"),
        "total_tokens": usage.get("total_tokens"),
        "finish_reason": nested_get(metadata, "response_metadata", "finish_reason"),
        "elapsed_seconds": metadata.get("elapsed_seconds") if metadata else None,
        "max_tokens_setting": metadata.get("max_tokens") if metadata else None,
    }


def artifact_result(item_dir: Path, run_dir: Path):
    metadata_path = run_dir / "generation_metadata.json"
    gate_path = run_dir / "gate_report.json"
    metadata = read_json(metadata_path)
    gate = read_json(gate_path)
    dynamic, dynamic_path = dynamic_report(run_dir)
    visual, visual_path = visual_manifest(run_dir)

    gate_score = score_gate(gate)
    usage = usage_from_metadata(metadata or {})
    dynamic_score = dynamic.get("task_success_rate") if dynamic else None
    dynamic_available = dynamic_score is not None
    dynamic_required = not item_dir.name.startswith("W")
    static_visual_score = None
    static_visual_status = "pending_standard_screenshots"
    screenshot_coverage = None
    if visual:
        screenshot_coverage = visual.get("screenshot_coverage")
        static_visual_status = "pending_rubric_scoring"

    efficiency_score = None
    efficiency_status = "raw_only_no_usd_reference"
    category_scores = [
        gate_score["score"],
        static_visual_score,
        dynamic_score,
        efficiency_score,
    ]
    overall_score = mean(category_scores) if all(score is not None for score in category_scores) else None
    finish_reason = usage.get("finish_reason")
    eligible = bool(
        gate_score["passed"]
        and finish_reason not in {"length", "max_tokens"}
        and (dynamic_available or not dynamic_required)
    )

    return {
        "item_id": item_dir.name,
        "item_branch": "static_responsive" if item_dir.name.startswith("W") else "executable_workflow",
        "run": run_dir.name,
        "model_key": model_key(metadata),
        "prompt_id": metadata.get("prompt_id") if metadata else None,
        "artifact": {
            "html": rel(run_dir / "index.html"),
            "metadata": rel(metadata_path) if metadata_path.exists() else None,
        },
        "static_technical": {
            **gate_score,
            "report": rel(gate_path) if gate_path.exists() else None,
        },
        "static_visual": {
            "score": static_visual_score,
            "status": static_visual_status,
            "screenshot_coverage": screenshot_coverage,
            "manifest": rel(visual_path) if visual_path else None,
        },
        "dynamic": {
            "score": dynamic_score,
            "status": "available" if dynamic_available else ("missing" if dynamic_required else "not_applicable"),
            "evaluator": dynamic.get("evaluator") if dynamic else None,
            "task_success_rate": dynamic.get("task_success_rate") if dynamic else None,
            "route_success_rate": dynamic.get("route_success_rate") if dynamic else None,
            "content_validation_success_rate": dynamic.get("content_validation_success_rate") if dynamic else None,
            "case_count": dynamic.get("case_count") if dynamic else None,
            "passed_case_count": dynamic.get("passed_case_count") if dynamic else None,
            "report": rel(dynamic_path) if dynamic_path else None,
        },
        "efficiency": {
            "score": efficiency_score,
            "status": efficiency_status,
            **usage,
            "cost_usd": None,
            "cost_status": "not_estimated_no_stable_price_reference",
        },
        "overall_score": overall_score,
        "eligible_for_leaderboard": eligible,
        "ineligibility_reasons": ineligibility_reasons(gate_score, finish_reason, dynamic_required, dynamic_available),
    }


def model_key(metadata):
    if not metadata:
        return "unknown"
    provider = metadata.get("provider") or "unknown-provider"
    model = metadata.get("model") or "unknown-model"
    prompt = metadata.get("prompt_id") or "unknown-prompt"
    return f"{provider}/{model}/{prompt}"


def ineligibility_reasons(gate_score, finish_reason, dynamic_required, dynamic_available):
    reasons = []
    if not gate_score["passed"]:
        reasons.append("static_technical_gate_failed")
    if finish_reason in {"length", "max_tokens"}:
        reasons.append("generation_token_truncated")
    if dynamic_required and not dynamic_available:
        reasons.append("dynamic_report_missing")
    return reasons


def iter_runs(items_dir: Path):
    for item_dir in sorted(path for path in items_dir.iterdir() if path.is_dir()):
        generated_dir = item_dir / "generated"
        if not generated_dir.exists():
            continue
        for run_dir in sorted(path for path in generated_dir.iterdir() if path.is_dir()):
            if (run_dir / "index.html").exists():
                yield item_dir, run_dir


def aggregate_model_rows(artifacts, include_ineligible=False):
    grouped = defaultdict(list)
    for artifact in artifacts:
        if artifact["eligible_for_leaderboard"] or include_ineligible:
            grouped[artifact["model_key"]].append(artifact)

    rows = []
    for model, group in sorted(grouped.items()):
        eligible = [item for item in group if item["eligible_for_leaderboard"]]
        failed = [item for item in group if not item["eligible_for_leaderboard"]]
        scoring_group = eligible if eligible else group
        reason_counts = Counter(
            reason
            for item in failed
            for reason in (item["ineligibility_reasons"] or ["unknown_ineligibility"])
        )
        rows.append({
            "model": model,
            "artifact_count": len(group),
            "eligible_artifact_count": len(eligible),
            "failed_artifact_count": len(failed),
            "completion_reliability": len(eligible) / len(group) if group else None,
            "attempted_items": sorted({item["item_id"] for item in group}),
            "ineligibility_reason_counts": dict(reason_counts),
            "overall_score": avg([item["overall_score"] for item in scoring_group]),
            "static_technical_score": avg([item["static_technical"]["score"] for item in scoring_group]),
            "static_visual_score": avg([item["static_visual"]["score"] for item in scoring_group]),
            "dynamic_score": avg([item["dynamic"]["score"] for item in scoring_group]),
            "efficiency_score": avg([item["efficiency"]["score"] for item in scoring_group]),
            "average_prompt_tokens": avg([item["efficiency"]["input_tokens"] for item in group]),
            "average_completion_tokens": avg([item["efficiency"]["output_tokens"] for item in group]),
            "average_total_tokens": avg([item["efficiency"]["total_tokens"] for item in group]),
            "average_output_tokens": avg([item["efficiency"]["output_tokens"] for item in group]),
            "average_latency_seconds": avg([item["efficiency"]["elapsed_seconds"] for item in group]),
            "average_cost_per_app": None,
            "cost_status": "not_estimated_no_stable_price_reference",
            "notes": "Overall/static visual/efficiency scores remain null; raw token/latency efficiency fields are reported without USD cost estimation.",
        })
    rows.sort(
        key=lambda row: (
            row["overall_score"] if row["overall_score"] is not None else row["dynamic_score"] if row["dynamic_score"] is not None else -1,
            row["eligible_artifact_count"],
        ),
        reverse=True,
    )
    for index, row in enumerate(rows, start=1):
        row["rank"] = index
    return rows


def format_score(value):
    if isinstance(value, (int, float)):
        return f"{value:.3f}"
    return "pending"


def format_number(value):
    if isinstance(value, (int, float)):
        return f"{value:.1f}"
    return "n/a"


def leaderboard_markdown(model_rows, prompt_id, provider_failure_count):
    mixed_prompt = not prompt_id
    lines = [
        "# Track B Mini Leaderboard" if not mixed_prompt else "# Track B Mixed-Prompt Pipeline Summary",
        "",
        f"Prompt filter: `{prompt_id or 'all'}`",
        "",
        "Generated UI/Web app artifacts are the direct evaluation target; generator models are the ranking target.",
        "",
        f"Provider failures recorded: {provider_failure_count}",
        "",
        "| Rank | Model | Attempted | Eligible | Failed | Completion reliability | Static Technical | Static Visual | Dynamic | Efficiency | Overall | Avg prompt tokens | Avg completion tokens | Avg total tokens | Avg latency (s) | Cost status |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in model_rows:
        lines.append(
            "| {rank} | {model} | {attempted} | {eligible} | {failed} | {reliability} | {static_technical} | {static_visual} | {dynamic} | {efficiency} | {overall} | {prompt_tokens} | {completion_tokens} | {tokens} | {latency} | {cost_status} |".format(
                rank=row["rank"],
                model=row["model"],
                attempted=row["artifact_count"],
                eligible=row["eligible_artifact_count"],
                failed=row["failed_artifact_count"],
                reliability=format_score(row["completion_reliability"]),
                static_technical=format_score(row["static_technical_score"]),
                static_visual=format_score(row["static_visual_score"]),
                dynamic=format_score(row["dynamic_score"]),
                efficiency=format_score(row["efficiency_score"]),
                overall=format_score(row["overall_score"]),
                prompt_tokens=format_number(row["average_prompt_tokens"]),
                completion_tokens=format_number(row["average_completion_tokens"]),
                tokens=format_number(row["average_total_tokens"]),
                latency=format_number(row["average_latency_seconds"]),
                cost_status=row["cost_status"],
            )
        )
    failed_rows = [
        row for row in model_rows
        if row.get("ineligibility_reason_counts")
    ]
    if failed_rows:
        lines.extend([
            "",
            "Failure summary:",
            "",
            "| Model | Ineligibility reasons |",
            "| --- | --- |",
        ])
        for row in failed_rows:
            reasons = ", ".join(
                f"{reason}: {count}"
                for reason, count in sorted(row["ineligibility_reason_counts"].items())
            )
            lines.append(f"| {row['model']} | {reasons} |")
    lines.extend([
        "",
        "Notes:",
        "",
        "- Static Visual is pending until the standardized screenshots are scored with a visual rubric.",
        "- Efficiency score remains pending, but raw token and latency fields are reported for quality-vs-efficiency comparison.",
        "- USD cost is not estimated in this output because no stable provider price or billing reference is fixed.",
        "- Overall remains pending while any component score is pending.",
        "- Current demo ranking falls back to Dynamic score while Overall is pending.",
    ])
    if mixed_prompt:
        lines.extend([
            "- This `all` table mixes prompt versions and is only a pipeline summary, not a fair model leaderboard.",
            "- Use a fixed prompt filter such as `TB-GEN-v9` for same-prompt leaderboard comparisons.",
        ])
    return "\n".join(lines) + "\n"


def avg(values):
    numeric = [value for value in values if isinstance(value, (int, float))]
    return mean(numeric) if numeric else None


def load_provider_failures(summary_path: Path | None, prompt_id: str | None):
    if not summary_path:
        return []
    summary = read_json(summary_path)
    if not summary:
        return []
    failures = summary.get("provider_failures", [])
    if prompt_id:
        failures = [failure for failure in failures if failure.get("prompt_id") == prompt_id]
    return failures


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--items-dir", type=Path, default=DEFAULT_ITEMS_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--prompt-id", default="")
    parser.add_argument("--include-ineligible", action="store_true")
    parser.add_argument("--summary-json", type=Path, default=PROJECT_ROOT / "data" / "track_b" / "dynamic_workflow_v9_summary.json")
    args = parser.parse_args()

    artifacts = []
    for item_dir, run_dir in iter_runs(args.items_dir):
        result = artifact_result(item_dir, run_dir)
        if args.prompt_id and result["prompt_id"] != args.prompt_id:
            continue
        artifacts.append(result)

    suffix = args.prompt_id.lower().replace("-", "_") if args.prompt_id else "all"
    args.out_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = args.out_dir / f"artifact_results_{suffix}.json"
    model_path = args.out_dir / f"model_leaderboard_{suffix}.json"
    markdown_path = args.out_dir / f"model_leaderboard_{suffix}.md"
    provider_failures = load_provider_failures(args.summary_json, args.prompt_id or None)
    model_rows = aggregate_model_rows(artifacts, include_ineligible=args.include_ineligible)

    artifact_payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "prompt_id_filter": args.prompt_id or None,
        "direct_evaluation_target": "generated UI/Web app artifact",
        "leaderboard_ranking_target": "generator LLM/model configuration",
        "artifact_count": len(artifacts),
        "eligible_artifact_count": sum(1 for item in artifacts if item["eligible_for_leaderboard"]),
        "provider_failures": provider_failures,
        "artifacts": artifacts,
    }
    model_payload = {
        "generated_at": artifact_payload["generated_at"],
        "prompt_id_filter": args.prompt_id or None,
        "aggregation_note": "Artifact-level scores are aggregated into model-level leaderboard rows. Ineligible artifacts are excluded from score means.",
        "provider_failure_count": len(provider_failures),
        "models": model_rows,
    }
    artifact_path.write_text(json.dumps(artifact_payload, indent=2), encoding="utf-8")
    model_path.write_text(json.dumps(model_payload, indent=2), encoding="utf-8")
    markdown_path.write_text(leaderboard_markdown(model_rows, args.prompt_id, len(provider_failures)), encoding="utf-8")

    print(json.dumps({
        "artifact_results": rel(artifact_path),
        "model_leaderboard": rel(model_path),
        "model_leaderboard_markdown": rel(markdown_path),
        "artifact_count": artifact_payload["artifact_count"],
        "eligible_artifact_count": artifact_payload["eligible_artifact_count"],
        "model_count": len(model_rows),
        "provider_failure_count": len(provider_failures),
    }, indent=2))


if __name__ == "__main__":
    main()
