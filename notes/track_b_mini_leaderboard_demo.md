# Track B Mini Leaderboard Demo

Date: 2026-06-04

## Purpose

This demo checks that the Track B leaderboard pipeline can run end to end on
the current generated artifacts.

The demo is intentionally small. It is not the final thesis leaderboard. Its
purpose is to verify the data flow:

1. generated `index.html`
2. static technical gate
3. browser-workflow dynamic evaluation
4. artifact-level result record
5. model/config-level aggregation
6. Markdown leaderboard table

## Files

Builder:

- `scripts/build_track_b_mini_leaderboard.py`

Generated demo outputs:

- `data/track_b/leaderboard/artifact_results_all.json`
- `data/track_b/leaderboard/model_leaderboard_all.json`
- `data/track_b/leaderboard/model_leaderboard_all.md`
- `data/track_b/leaderboard/artifact_results_tb_gen_v9.json`
- `data/track_b/leaderboard/model_leaderboard_tb_gen_v9.json`
- `data/track_b/leaderboard/model_leaderboard_tb_gen_v9.md`

## Current Demo Scope

The direct evaluation target is each generated UI/Web app artifact. The
leaderboard aggregation target is the generator model/configuration.

Fair model comparison requires the same prompt and the same benchmark item set.
The `all` output is therefore only a pipeline smoke/demo summary because it
mixes prompt versions. The same-prompt output for the current pilot is
`model_leaderboard_tb_gen_v9.md`; however, it currently contains only one
model/configuration row, so it demonstrates aggregation but not a real
multi-model ranking yet.

Current included components:

- static technical score from `gate_report.json`
- browser dynamic score from `browser_workflow_normalized_report.json` when
  available, otherwise `browser_workflow_report.json`
- token/latency metadata when available

Pending components:

- static visual/UX rubric score
- efficiency/cost score
- final overall composite score

Because visual and efficiency scores are pending, the current Markdown table
uses dynamic score as the temporary ranking fallback.

## Current All-Run Pipeline Demo Result

| Rank | Model/config | Eligible artifacts | Static technical | Dynamic |
| ---: | --- | ---: | ---: | ---: |
| 1 | `gwdg-openai/qwen3.6-35b-a3b/TB-GEN-v9` | 4 | 0.975 | 0.735 |
| 2 | `chatanywhere-anthropic/claude-sonnet-4-5-20250929/TB-GEN-v3` | 1 | 1.000 | 0.500 |
| 3 | `chatanywhere-anthropic/claude-sonnet-4-5-20250929/TB-GEN-v4` | 1 | 1.000 | 0.500 |
| 4 | `gwdg-openai/qwen3.6-35b-a3b/TB-GEN-v6` | 1 | 1.000 | 0.500 |

Interpretation: the all-run table shows that the pipeline can aggregate
artifact-level results into model/config-level rows. It does not claim that the
top row is the best GUI generator because prompt versions are mixed and visual
quality and efficiency are not scored yet.

## Same-Prompt Leaderboard Status

The same-prompt `TB-GEN-v9` output is the appropriate leaderboard format for a
fair comparison:

- `data/track_b/leaderboard/model_leaderboard_tb_gen_v9.md`

At the moment it contains only `gwdg-openai/qwen3.6-35b-a3b/TB-GEN-v9` with
four eligible artifacts. Same-prompt second-model smoke tests were attempted on
`F10_gourmania` and are recorded in:

- `data/track_b/leaderboard/same_prompt_second_model_attempts.json`

The attempted second models did not produce an eligible leaderboard row:

- `gwdg-openai/qwen3-omni-30b-a3b-instruct/TB-GEN-v9` produced an artifact but
  failed the static technical gate because required workflow click labels were
  missing.
- `gwdg-openai/internvl3.5-30b-a3b/TB-GEN-v9` produced an artifact but failed
  the same static technical gate.
- `openai/gpt-4o-mini/TB-GEN-v9` through the configured OpenAI-compatible
  endpoint produced an artifact but failed the same static technical gate.
- `openai/gpt-4.1-mini/TB-GEN-v9` through the configured OpenAI-compatible
  endpoint failed with HTTP 503 before artifact creation.
- `openai/gpt-5.2/TB-GEN-v9` was started while checking stronger GPT options
  and terminated before artifact creation for cost control.
- `chatanywhere-anthropic/claude-3-haiku-20240307/TB-GEN-v9` failed before
  artifact creation because the configured endpoint did not support that model.
- `gwdg-openai/qwen3-coder-30b-a3b-instruct/TB-GEN-v9` failed before artifact
  creation because it was not usable as a multimodal generation model for this
  task.
- `chatanywhere-anthropic/claude-sonnet-4-5-20250929/TB-GEN-v9` timed out
  before artifact creation.
- Gemini was not attempted because no Gemini/Google API key was present in the
  current environment.

This means the same-prompt leaderboard format is ready, and failed attempts are
traceable, but the demo is not yet a real multi-model ranking. To turn it into a
comparison, at least one additional generator must pass the static gate on the
same `TB-GEN-v9` prompt and the same selected benchmark items.

The repeated static-gate failure on `F10_gourmania` is informative: different
models produce complete HTML, but often render the recipe section title and
recipe name as non-clickable visual content instead of exact `<a>` or `<button>`
workflow controls. This points to a prompt/control-contract issue for this item,
not to token truncation or missing route JavaScript.

## Workflow-Case Normalization Status

Workflow-case normalization is implemented for the current leaderboard-demo item
set:

- `scripts/normalize_track_b_workflow_cases.py`
- `data/track_b/workflows_normalized/normalization_summary.json`

For the current selected items, normalization changes `F06_community_dynamics`
and `F09_elections_bc`. After rerunning browser-workflow with normalized
workflows, all eligible artifacts have route success 1.000; remaining dynamic
failures are content-validation failures.

## F10 Prompt Diagnostic Status

Follow-up file:

- `notes/track_b_f10_prompt_v14_v15_experiment.md`

`TB-GEN-v14` and `TB-GEN-v15` were created for an F10-specific diagnostic after
the same-prompt second-model smoke tests showed poor visual quality and repeated
workflow-control failures. `TB-GEN-v15` produced an eligible F10 artifact with
`gwdg-openai/qwen3-omni-30b-a3b-instruct`:

- static gate: pass, with warnings
- browser workflow: 8/8 cases, route/content/task success all 1.000
- image use: 46 local `<img>` references

This does not make the mixed-prompt `all` table a fair leaderboard. It shows
that a stricter visual-grounded prompt and a corrected gate extraction rule can
fix the F10 workflow-control failure. Fair model comparison still requires the
same prompt and same item set.

## Next Improvements

- Add static visual/UX rubric scoring on standardized screenshots.
- Define an efficiency normalization rule if cost/latency should affect the
  leaderboard.
- Replace dynamic-score fallback ranking with the final composite once all
  components are available.
