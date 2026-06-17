# Track B Mini Leaderboard

Prompt filter: `TB-GEN-v16`

Generated UI/Web app artifacts are the direct evaluation target; generator models are the ranking target.

Provider failures recorded: 0

| Rank | Model | Provider | Prompt | Attempted | Eligible | Failed | Completion reliability | Static Technical | Static Visual | Dynamic | Efficiency | Overall | Avg prompt tokens | Avg completion tokens | Avg total tokens | Avg latency (s) | Cost status |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | `gpt-4.1-mini` | `tuzi-openai` | `TB-GEN-v16` | 1 | 1 | 0 | 1.000 | 0.923 | pending | 0.625 | pending | pending | 5028.0 | 7574.0 | 12602.0 | 82.0 | not_estimated_no_stable_price_reference |
| 2 | `qwen3.6-35b-a3b` | `gwdg-openai` | `TB-GEN-v16` | 5 | 5 | 0 | 1.000 | 0.954 | pending | 0.558 | pending | pending | 21726.0 | 17588.2 | 39314.2 | 146.7 | not_estimated_no_stable_price_reference |
| 3 | `qwen3-omni-30b-a3b-instruct` | `gwdg-openai` | `TB-GEN-v16` | 5 | 2 | 3 | 0.400 | 0.846 | pending | 0.500 | pending | pending | 24499.6 | 21040.2 | 45539.8 | 173.8 | not_estimated_no_stable_price_reference |

Failure summary:

| Model | Provider | Ineligibility reasons |
| --- | --- | --- |
| `qwen3-omni-30b-a3b-instruct` | `gwdg-openai` | generation_token_truncated: 3, static_technical_gate_failed: 3 |

## Category Rankings

Each ranking uses the same model rows above. Quality metrics are higher-is-better; raw efficiency metrics are lower-is-better.

### Completion reliability

| Rank | Model | Provider | Value |
| ---: | --- | --- | ---: |
| 1 | `gpt-4.1-mini` | `tuzi-openai` | 1.000 |
| 2 | `qwen3.6-35b-a3b` | `gwdg-openai` | 1.000 |
| 3 | `qwen3-omni-30b-a3b-instruct` | `gwdg-openai` | 0.400 |

### Static technical

| Rank | Model | Provider | Score |
| ---: | --- | --- | ---: |
| 1 | `qwen3.6-35b-a3b` | `gwdg-openai` | 0.954 |
| 2 | `gpt-4.1-mini` | `tuzi-openai` | 0.923 |
| 3 | `qwen3-omni-30b-a3b-instruct` | `gwdg-openai` | 0.846 |

### Dynamic task

| Rank | Model | Provider | Score |
| ---: | --- | --- | ---: |
| 1 | `gpt-4.1-mini` | `tuzi-openai` | 0.625 |
| 2 | `qwen3.6-35b-a3b` | `gwdg-openai` | 0.558 |
| 3 | `qwen3-omni-30b-a3b-instruct` | `gwdg-openai` | 0.500 |

### Average total tokens

| Rank | Model | Provider | Tokens |
| ---: | --- | --- | ---: |
| 1 | `gpt-4.1-mini` | `tuzi-openai` | 12602.0 |
| 2 | `qwen3.6-35b-a3b` | `gwdg-openai` | 39314.2 |
| 3 | `qwen3-omni-30b-a3b-instruct` | `gwdg-openai` | 45539.8 |

### Average latency

| Rank | Model | Provider | Seconds |
| ---: | --- | --- | ---: |
| 1 | `gpt-4.1-mini` | `tuzi-openai` | 82.0 |
| 2 | `qwen3.6-35b-a3b` | `gwdg-openai` | 146.7 |
| 3 | `qwen3-omni-30b-a3b-instruct` | `gwdg-openai` | 173.8 |

Notes:

- Static Visual is pending until the standardized screenshots are scored with a visual rubric.
- Efficiency score remains pending, but raw token and latency fields are reported for quality-vs-efficiency comparison.
- USD cost is not estimated in this output because no stable provider price or billing reference is fixed.
- Overall remains pending while any component score is pending.
- Current demo ranking falls back to Dynamic score while Overall is pending.
