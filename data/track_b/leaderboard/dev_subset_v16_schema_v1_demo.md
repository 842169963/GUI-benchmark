# Track B Schema v1 Demo Leaderboard

Schema: `track-b-leaderboard-v1`
Generated at: `2026-06-11T20:57:41.512063+00:00`

This is a meeting demo, not the final formal leaderboard. It shows schema-aligned failure-aware reporting.

## Model-Level Rows

| Model/config | Attempted | Eligible | Failed | Completion reliability | Static technical | Dynamic task | Route | Content | Overall | Failure detail |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `gwdg-openai/qwen3.6-35b-a3b/TB-GEN-v16` | 5 | 5 | 0 | 1.000 | 0.954 | 0.558 | 1 | 0.558 | pending | none |
| `gwdg-openai/qwen3-omni-30b-a3b-instruct/TB-GEN-v16` | 3 | 2 | 1 | 0.667 | 0.846 | 0.500 | 0.750 | 0.625 | pending | F01_1daycloud:completion_truncation_failure |

## Artifact-Level Rows

| Item | Branch | Model | Finish | Gate | Dynamic | Screenshots | Eligible | Failure category |
| --- | --- | --- | --- | --- | ---: | ---: | --- | --- |
| F01_1daycloud | executable_workflow | `qwen3.6-35b-a3b` | `stop` | pass | 7/12 | pending | yes | `content_validation_failure` |
| F03_about_gitlab | executable_workflow | `qwen3.6-35b-a3b` | `stop` | pass | 4/8 | pending | yes | `content_validation_failure` |
| F06_community_dynamics | executable_workflow | `qwen3.6-35b-a3b` | `stop` | pass | 4/10 | pending | yes | `content_validation_failure` |
| F10_gourmania | executable_workflow | `qwen3.6-35b-a3b` | `stop` | pass | 6/8 | pending | yes | `content_validation_failure` |
| W03_eventbrite | static_responsive | `qwen3.6-35b-a3b` | `stop` | pass | n/a | 1 | yes | `passed_static_responsive_checks` |
| F01_1daycloud | executable_workflow | `qwen3-omni-30b-a3b-instruct` | `length` | fail | 0/12 | pending | no | `completion_truncation_failure` |
| F03_about_gitlab | executable_workflow | `qwen3-omni-30b-a3b-instruct` | `stop` | pass | 3/8 | pending | yes | `dynamic_route_or_content_failure` |
| F10_gourmania | executable_workflow | `qwen3-omni-30b-a3b-instruct` | `stop` | pass | 5/8 | pending | yes | `dynamic_route_or_content_failure` |

## Pending Metric Slots

- Static visual score: schema slot present; pending validated visual judge / human rubric.
- Accessibility score: schema slot present; pending integration of axe weighted-density reports.
- Efficiency score: raw token/latency fields present; normalized score pending cost reference.
- Overall score: intentionally pending until category weights are approved.
