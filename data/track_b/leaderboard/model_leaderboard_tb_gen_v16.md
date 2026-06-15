# Track B Mini Leaderboard

Prompt filter: `TB-GEN-v16`

Generated UI/Web app artifacts are the direct evaluation target; generator models are the ranking target.

Provider failures recorded: 0

| Rank | Model | Attempted | Eligible | Failed | Completion reliability | Static Technical | Static Visual | Dynamic | Efficiency | Overall | Avg prompt tokens | Avg completion tokens | Avg total tokens | Avg latency (s) | Cost status |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | tuzi-openai/gpt-4.1-mini/TB-GEN-v16 | 1 | 1 | 0 | 1.000 | 0.923 | pending | 0.625 | pending | pending | 5028.0 | 7574.0 | 12602.0 | 82.0 | not_estimated_no_stable_price_reference |
| 2 | gwdg-openai/qwen3.6-35b-a3b/TB-GEN-v16 | 5 | 5 | 0 | 1.000 | 0.954 | pending | 0.558 | pending | pending | 21726.0 | 17588.2 | 39314.2 | 146.7 | not_estimated_no_stable_price_reference |
| 3 | gwdg-openai/qwen3-omni-30b-a3b-instruct/TB-GEN-v16 | 5 | 2 | 3 | 0.400 | 0.846 | pending | 0.500 | pending | pending | 24499.6 | 21040.2 | 45539.8 | 173.8 | not_estimated_no_stable_price_reference |

Failure summary:

| Model | Ineligibility reasons |
| --- | --- |
| gwdg-openai/qwen3-omni-30b-a3b-instruct/TB-GEN-v16 | generation_token_truncated: 3, static_technical_gate_failed: 3 |

Notes:

- Static Visual is pending until the standardized screenshots are scored with a visual rubric.
- Efficiency score remains pending, but raw token and latency fields are reported for quality-vs-efficiency comparison.
- USD cost is not estimated in this output because no stable provider price or billing reference is fixed.
- Overall remains pending while any component score is pending.
- Current demo ranking falls back to Dynamic score while Overall is pending.
