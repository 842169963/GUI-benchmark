# Track B TB-GEN-v15 Small Batch Experiment

Date: 2026-06-05

## Purpose

This experiment checks whether the F10-specific improvement from `TB-GEN-v15`
generalizes to a small Track B item batch before treating it as a frozen prompt
candidate.

Model/provider:

- `gwdg-openai/qwen3-omni-30b-a3b-instruct`

Prompt:

- `TB-GEN-v15`

Items attempted:

- `F01_1daycloud`
- `F03_about_gitlab`
- `F06_community_dynamics`
- `F09_elections_bc`
- `F10_gourmania` from the previous F10 follow-up

## Results

| Item | Run | Artifact | Static gate | Browser workflow | Main issue |
| --- | --- | ---: | ---: | ---: | --- |
| F01_1daycloud | `gwdg_qwen3_omni_30b_v15_f01_smoke` | yes | fail | 6/12, route 1.000, content 0.500 | Static gate over-treated a semantic logo click as exact text; dynamic route matching worked, but generated destination content missed required evidence. |
| F03_about_gitlab | `gwdg_qwen3_omni_30b_v15_f03_smoke` | no | n/a | n/a | Provider rejected the prompt because text plus multimodal tokens exceeded the model context limit: 78,813 > 65,536. |
| F06_community_dynamics | `gwdg_qwen3_omni_30b_v15_f06_smoke` | yes, truncated | fail | not usable, page crashed | Output hit `finish_reason=length`; generated HTML was incomplete, no images were present, and browser loading crashed. |
| F09_elections_bc | `gwdg_qwen3_omni_30b_v15_f09_smoke` | yes, truncated | fail | 0/10 | Output hit `finish_reason=length`; workflow controls and route script were incomplete. |
| F10_gourmania | `gwdg_qwen3_omni_30b_v15_f10_smoke` | yes | pass, warnings | 8/8, route/content/task 1.000 | F10 success case; remaining warnings are broken non-critical image refs and non-workflow route placeholders. |

Leaderboard output:

- `data/track_b/leaderboard/model_leaderboard_tb_gen_v15.md`

The v15 leaderboard output has 4 artifacts and only 1 eligible artifact. The
single eligible artifact is F10.

## Interpretation

`TB-GEN-v15` should not be frozen as the next general Track B generation prompt.
It fixed the F10 workflow-control failure, but it does not generalize cleanly:

- It is too verbose for complex items under the tested GWDG qwen3-omni context
  and output limits.
- It still needs a better separation between exact text click targets and
  semantic/image targets such as a logo click.
- It improves visual grounding when output completes, but for larger items the
  visual-grounding instructions cause truncation before the route script and
  required controls are complete.
- It does not guarantee the destination content evidence required by workflow
  validations.

The experiment supports creating a follow-up prompt rather than freezing v15.

## Recommended Next Prompt Direction

The next candidate should combine the v15 control-contract improvements with
bounded generation:

- Keep exact `required_element` controls for quoted/named text targets.
- Treat semantic/image targets, such as logo clicks, as route/action guidance
  rather than exact visible-text requirements.
- Reintroduce compactness, but not the v9 instruction to remove visual detail
  first.
- Require at least a small number of local images per major visual section
  instead of encouraging exhaustive image-heavy pages.
- Require explicit validation evidence text for each workflow destination page.
- Add deterministic input truncation/context policy for models with smaller
  multimodal context windows.

This points toward a `TB-GEN-v16` candidate, not a frozen v15 benchmark.
