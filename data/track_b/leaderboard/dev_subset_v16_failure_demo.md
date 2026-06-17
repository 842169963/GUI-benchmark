# Track B Schema v1 Demo Leaderboard

Schema: `track-b-leaderboard-v1`
Generated at: `2026-06-15T22:01:54.642873+00:00`

This is a meeting demo, not the final formal leaderboard. It shows schema-aligned failure-aware reporting.

## Model-Level Rows

| Model | Provider | Prompt | Attempted | Eligible | Failed | Completion reliability | Static technical | Dynamic task | Route | Content | Avg prompt tokens | Avg completion tokens | Avg total tokens | Avg latency (s) | Cost status | Overall | Failure detail |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- |
| `qwen3.6-35b-a3b` | `gwdg-openai` | `TB-GEN-v16` | 5 | 5 | 0 | 1.000 | 0.954 | 0.558 | 1 | 0.558 | 21726 | 17588.200 | 39314.200 | 146.742 | not_estimated_no_stable_price_reference | pending | none |
| `qwen3-omni-30b-a3b-instruct` | `gwdg-openai` | `TB-GEN-v16` | 3 | 2 | 1 | 0.667 | 0.846 | 0.500 | 0.750 | 0.625 | 23113 | 21733.667 | 44846.667 | 175.663 | not_estimated_no_stable_price_reference | pending | F01_1daycloud:completion_truncation_failure |

## Category Rankings

Each ranking uses the same model rows above. Quality metrics are higher-is-better; raw efficiency metrics are lower-is-better.

### Completion reliability

| Rank | Model | Provider | Value |
| ---: | --- | --- | ---: |
| 1 | `qwen3.6-35b-a3b` | `gwdg-openai` | 1.000 |
| 2 | `qwen3-omni-30b-a3b-instruct` | `gwdg-openai` | 0.667 |

### Static technical

| Rank | Model | Provider | Score |
| ---: | --- | --- | ---: |
| 1 | `qwen3.6-35b-a3b` | `gwdg-openai` | 0.954 |
| 2 | `qwen3-omni-30b-a3b-instruct` | `gwdg-openai` | 0.846 |

### Dynamic task

| Rank | Model | Provider | Score |
| ---: | --- | --- | ---: |
| 1 | `qwen3.6-35b-a3b` | `gwdg-openai` | 0.558 |
| 2 | `qwen3-omni-30b-a3b-instruct` | `gwdg-openai` | 0.500 |

### Average total tokens

| Rank | Model | Provider | Tokens |
| ---: | --- | --- | ---: |
| 1 | `qwen3.6-35b-a3b` | `gwdg-openai` | 39314.200 |
| 2 | `qwen3-omni-30b-a3b-instruct` | `gwdg-openai` | 44846.667 |

### Average latency

| Rank | Model | Provider | Seconds |
| ---: | --- | --- | ---: |
| 1 | `qwen3.6-35b-a3b` | `gwdg-openai` | 146.742 |
| 2 | `qwen3-omni-30b-a3b-instruct` | `gwdg-openai` | 175.663 |

## Artifact-Level Rows

| Item | Branch | Model | Finish | Gate | Dynamic | Total tokens | Latency (s) | Screenshots | Eligible | Failure category |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| F01_1daycloud | executable_workflow | `qwen3.6-35b-a3b` | `stop` | pass | 7/12 | 42263 | 122.520 | pending | yes | `content_validation_failure` |
| F03_about_gitlab | executable_workflow | `qwen3.6-35b-a3b` | `stop` | pass | 4/8 | 29376 | 81.970 | pending | yes | `content_validation_failure` |
| F06_community_dynamics | executable_workflow | `qwen3.6-35b-a3b` | `stop` | pass | 4/10 | 57254 | 213.870 | pending | yes | `content_validation_failure` |
| F10_gourmania | executable_workflow | `qwen3.6-35b-a3b` | `stop` | pass | 6/8 | 41033 | 109.000 | pending | yes | `content_validation_failure` |
| W03_eventbrite | static_responsive | `qwen3.6-35b-a3b` | `stop` | pass | n/a | 26645 | 206.350 | 1 | yes | `passed_static_responsive_checks` |
| F01_1daycloud | executable_workflow | `qwen3-omni-30b-a3b-instruct` | `length` | fail | 0/12 | 65536 | 325.650 | pending | no | `completion_truncation_failure` |
| F03_about_gitlab | executable_workflow | `qwen3-omni-30b-a3b-instruct` | `stop` | pass | 3/8 | 31780 | 124.150 | pending | yes | `dynamic_route_or_content_failure` |
| F10_gourmania | executable_workflow | `qwen3-omni-30b-a3b-instruct` | `stop` | pass | 5/8 | 37224 | 77.190 | pending | yes | `dynamic_route_or_content_failure` |

## Pending Metric Slots

- Static visual score: schema slot present; pending validated visual judge / human rubric.
- Accessibility score: schema slot present; pending integration of axe weighted-density reports.
- Efficiency score: raw token/latency fields are reported; normalized score and USD cost remain null until a stable price/cost reference is fixed.
- Overall score: intentionally pending until category weights are approved.
