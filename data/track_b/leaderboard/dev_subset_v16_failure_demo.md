# Track B v16 Dev-Subset Pipeline Demo

Generated at: `2026-06-10T15:30:24.475076+00:00`

Scope: fixed-item benchmark demo using `F01_1daycloud`, `F03_about_gitlab`, `F06_community_dynamics`, and `F10_gourmania`.

Prompt/input policy: `TB-GEN-v16`, compact input. OpenAI-compatible runs use omitted `max_tokens` where rerun evidence exists.

## Model-Level Leaderboard

| Rank | Model/config | Attempted | Generated | Truncation failures | Static pass | Eligible | Avg route | Avg content | Avg task | Avg completion tok. | Note |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | `gwdg-openai/qwen3.6-35b-a3b/TB-GEN-v16` | 4 | 4 | 0 | 4 | 4 | 1 | 0.558 | 0.558 | 17854 | All dev-subset artifacts complete and eligible; remaining losses are dynamic/content quality. |
| 2 | `gwdg-openai/qwen3-omni-30b-a3b-instruct/TB-GEN-v16` | 3 | 3 | 1 | 2 | 2 | 0.750 | 0.625 | 0.500 | 21733.667 | Ineligible artifacts: completion_truncation_failure |

## Artifact-Level Evidence

| Item | Model | Run | Finish | Gate | Workflow | Route | Content | Failure category |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| F01_1daycloud | `qwen3.6-35b-a3b` | `gwdg_qwen36_35b_v16_f01_dev` | `stop` | pass | 7/12 | 1 | 0.583 | `content_validation_failure` |
| F03_about_gitlab | `qwen3.6-35b-a3b` | `gwdg_qwen36_35b_v16_f03_compact_smoke` | `stop` | pass | 4/8 | 1 | 0.500 | `content_validation_failure` |
| F10_gourmania | `qwen3.6-35b-a3b` | `gwdg_qwen36_35b_v16_f10_dev` | `stop` | pass | 6/8 | 1 | 0.750 | `content_validation_failure` |
| F06_community_dynamics | `qwen3.6-35b-a3b` | `gwdg_qwen36_35b_v16_f06_dev_omit_maxtokens` | `stop` | pass | 4/10 | 1 | 0.400 | `content_validation_failure` |
| F01_1daycloud | `qwen3-omni-30b-a3b-instruct` | `gwdg_qwen3_omni_30b_v16_f01_dev_omit_maxtokens` | `length` | fail | 0/12 | 0 | 0.500 | `completion_truncation_failure` |
| F03_about_gitlab | `qwen3-omni-30b-a3b-instruct` | `gwdg_qwen3_omni_30b_v16_f03_compact_smoke` | `stop` | pass | 3/8 | 0.750 | 0.500 | `dynamic_route_or_content_failure` |
| F10_gourmania | `qwen3-omni-30b-a3b-instruct` | `gwdg_qwen3_omni_30b_v16_f10_dev_omit_maxtokens` | `stop` | pass | 5/8 | 0.750 | 0.750 | `dynamic_route_or_content_failure` |

## Interpretation

- This is a pipeline demo, not the final formal leaderboard.
- The demo shows generation, static technical gating, browser-workflow scoring, model aggregation, and explicit failure accounting.
- `qwen3.6-35b-a3b` completes all four demo items and enters scoring for all four.
- `qwen3-omni-30b-a3b-instruct` completes F03 and F10, but F01 remains a completion/truncation failure even without a client-side `max_tokens` field.
- The next thesis step is to expose this failure accounting in the main leaderboard pipeline before expanding to more items.
