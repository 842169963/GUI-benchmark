# Track B Leaderboard Schema v1

Status: meeting-demo schema, pending supervisor feedback.

Date: 2026-06-11

## Purpose

This schema defines how Track B generated UI artifacts, metric outputs, failure
states, and model-level leaderboard rows are represented. It separates the data
container from the metric formulas: the schema says what fields exist; metric
specifications define how scores are computed.

## Scope

The schema supports two Track B item branches:

- **Executable workflow items** such as F-series items. These can use static
  technical checks, dynamic route/content/task checks, screenshots, accessibility
  checks, efficiency metadata, and optional visual scoring.
- **Static responsive webpage items** such as W-series items. These use static
  technical checks, standardized desktop/tablet/mobile screenshots, visual
  scoring, accessibility checks, and efficiency metadata. Dynamic workflow
  scores are not applicable unless a separate task workflow is explicitly
  defined.

## Leaderboard Payload

Top-level shape:

```json
{
  "leaderboard_schema_version": "track-b-leaderboard-v1",
  "generated_at": "2026-06-11T00:00:00Z",
  "scope": {
    "prompt_id": "TB-GEN-v16",
    "input_profile": "compact",
    "item_subset": ["F01_1daycloud", "F03_about_gitlab"],
    "ranking_target": "generator_model_configuration",
    "evaluation_target": "generated_ui_artifact"
  },
  "metric_versions": {
    "static_technical": "static-gate-v2-relaxed",
    "dynamic": "browser-workflow-v1",
    "static_visual": "pending-judge-validation",
    "accessibility": "axe-weighted-density-v1",
    "efficiency": "raw-token-latency-v1",
    "failure_taxonomy": "track-b-failure-taxonomy-v1"
  },
  "artifact_results": [],
  "model_results": [],
  "category_rankings": {}
}
```

## Artifact-Level Result

One artifact-level result records one generated artifact for one model on one
benchmark item.

Required fields:

```json
{
  "artifact_result_id": "F01_1daycloud::gwdg_qwen36_35b_v16_f01_dev",
  "item_id": "F01_1daycloud",
  "item_branch": "executable_workflow",
  "model_key": "gwdg-openai/qwen3.6-35b-a3b/TB-GEN-v16",
  "run": "gwdg_qwen36_35b_v16_f01_dev",
  "paths": {
    "artifact": "data/track_b/items/.../index.html",
    "metadata": "data/track_b/items/.../generation_metadata.json",
    "gate_report": "data/track_b/items/.../gate_report.json",
    "dynamic_report": "data/track_b/items/.../browser_workflow_normalized_report.json",
    "screenshot_manifest": null
  },
  "applicable_metrics": ["static_technical", "dynamic", "accessibility", "efficiency"],
  "not_applicable_metrics": ["static_visual"],
  "generation": {
    "finish_reason": "stop",
    "max_tokens": null,
    "prompt_tokens": 12345,
    "completion_tokens": 6789,
    "total_tokens": 19134,
    "latency_seconds": 85.2
  },
  "static_technical": {
    "available": true,
    "passed": true,
    "score": 1.0,
    "errors": 0,
    "warnings": 1
  },
  "dynamic": {
    "status": "available",
    "route_success": 1.0,
    "content_success": 0.75,
    "task_success": 0.75,
    "passed_cases": 6,
    "case_count": 8
  },
  "static_visual": {
    "status": "pending",
    "score": null,
    "screenshot_coverage": null
  },
  "accessibility": {
    "status": "pending",
    "score": null
  },
  "efficiency": {
    "status": "raw_only",
    "score": null,
    "total_tokens": 19134,
    "latency_seconds": 85.2
  },
  "eligibility": {
    "eligible": true,
    "failure_category": "content_validation_failure",
    "failure_reason": "Eligible artifact with incomplete content evidence."
  }
}
```

## Failure-Aware Reporting

Failures must be visible at artifact and model level. A failed artifact is not
deleted from the leaderboard payload.

Failure categories:

- `provider_failure`
- `completion_truncation_failure`
- `static_gate_failure`
- `dynamic_route_or_content_failure`
- `content_validation_failure`
- `passed_all_current_checks`
- `not_applicable`

For model-level rows, store:

- `attempted_items`
- `eligible_items`
- `failed_items`
- `failure_by_item`
- `failure_category_counts`
- `completion_reliability`

This prevents models with many failed attempts from looking strong only because
their few eligible artifacts score well.

## Applicable Metric Rule

Metrics that do not apply to an item are excluded from that item's denominator.
They are not scored as zero.

Examples:

- W-series static responsive items: `dynamic` is not applicable unless a real
  task workflow is defined.
- F-series executable workflow items: `dynamic` is applicable.
- `static_visual` may be applicable but pending until screenshots are scored by
  a validated visual judge or human rubric.

## Model-Level Result

Model-level rows aggregate artifact-level results over the fixed item subset.

Required fields:

```json
{
  "model_key": "gwdg-openai/qwen3.6-35b-a3b/TB-GEN-v16",
  "attempted_items": ["F01_1daycloud", "F03_about_gitlab"],
  "eligible_items": ["F01_1daycloud", "F03_about_gitlab"],
  "failed_items": [],
  "failure_by_item": {},
  "failure_category_counts": {},
  "completion_reliability": 1.0,
  "category_scores": {
    "static_technical": 1.0,
    "dynamic": 0.75,
    "static_visual": null,
    "accessibility": null,
    "efficiency": null
  },
  "overall_score": null,
  "rankings": {
    "overall_rank": null,
    "dynamic_rank": 1,
    "static_technical_rank": 1,
    "completion_reliability_rank": 1
  }
}
```

## Category Rankings

The leaderboard should expose both an optional overall ranking and category
rankings:

- completion reliability
- static technical
- static visual
- dynamic workflow
- accessibility
- efficiency

Overall ranking is optional until all selected category scores are implemented
and validated.

## Current Demo Status

The 2026-06 meeting demo implements:

- generation metadata
- static technical gate
- standardized screenshots
- dynamic route/content/task scoring for F-series items
- failure-aware model aggregation
- schema-aligned JSON/Markdown output

Pending:

- validated static visual score
- accessibility score integrated into the main leaderboard
- efficiency/cost normalization
- final overall score and weights
