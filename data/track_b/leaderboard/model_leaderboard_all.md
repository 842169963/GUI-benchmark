# Track B Mixed-Prompt Pipeline Summary

Prompt filter: `all`

Generated UI/Web app artifacts are the direct evaluation target; generator models are the ranking target.

Provider failures recorded: 1

| Rank | Model | Eligible artifacts | Static Technical | Static Visual | Dynamic | Efficiency | Overall | Avg total tokens | Avg latency (s) |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | gwdg-openai/qwen3-omni-30b-a3b-instruct/TB-GEN-v15 | 1 | 0.846 | pending | 1.000 | pending | pending | 46589.0 | 64.8 |
| 2 | gwdg-openai/qwen3.6-35b-a3b/TB-GEN-v9 | 4 | 0.975 | pending | 0.735 | pending | pending | 56603.8 | 92.3 |
| 3 | chatanywhere-anthropic/claude-sonnet-4-5-20250929/TB-GEN-v3 | 1 | 1.000 | pending | 0.500 | pending | pending | n/a | 103.7 |
| 4 | chatanywhere-anthropic/claude-sonnet-4-5-20250929/TB-GEN-v4 | 1 | 1.000 | pending | 0.500 | pending | pending | n/a | 100.6 |
| 5 | gwdg-openai/qwen3.6-35b-a3b/TB-GEN-v6 | 1 | 1.000 | pending | 0.500 | pending | pending | 43830.0 | 135.1 |

Notes:

- Static Visual is pending until the standardized screenshots are scored with a visual rubric.
- Efficiency is pending until a cost reference or normalization rule is fixed.
- Overall remains pending while any component score is pending.
- Current demo ranking falls back to Dynamic score while Overall is pending.
- This `all` table mixes prompt versions and is only a pipeline summary, not a fair model leaderboard.
- Use a fixed prompt filter such as `TB-GEN-v9` for same-prompt leaderboard comparisons.
