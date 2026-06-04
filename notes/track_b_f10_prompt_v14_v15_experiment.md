# Track B F10 Prompt v14/v15 Follow-Up

Date: 2026-06-04

## Purpose

This follow-up checks whether the poor F10 `gpt-4o-mini` output and repeated
static-gate failures were caused by missing inputs, weak model behavior, an
overly compact prompt, or overly strict gate extraction.

The item is:

- `F10_gourmania`

The provider used for the successful cheap/free follow-up smoke was:

- `gwdg-openai/qwen3-omni-30b-a3b-instruct`

## Diagnosis

The inputs were present. The generation prompt included prototype screenshots
and local resource paths, including recipe, cookbook, logo, and video images.
The poor `openai_gpt4omini_v9_f10_smoke` page did not omit images because the
input lacked them; it omitted them because `TB-GEN-v9` strongly encouraged a
minimal compact implementation and the cheap model followed that bias.

The original static gate also over-extracted clickable labels for F10. For the
action:

```text
Click the recipe card named "Gefilte Fish" in the "FAVOURITE HOLIDAY RECIPES" section
```

the gate treated both quoted strings as hard clickable targets. This was too
strict. `Gefilte Fish` is the click target; `FAVOURITE HOLIDAY RECIPES` is
section context.

## Gate Changes

Updated script:

- `scripts/check_track_b_generation.py`

Changes:

- Extract only the actual click target from workflow actions.
- Treat workflow route-target problems as hard errors.
- Treat non-workflow `showPage()` calls to missing route IDs as warnings.
- Add warnings for local image use and missing local image sources.

After this change, the old `openai_gpt4omini_v9_f10_smoke` still fails because
`Gefilte Fish` is implemented as a clickable `<div>`, not as an `<a>` or
`<button>`. It no longer fails because of the section heading.

## Prompt Changes

New prompt templates:

- `TB-GEN-v14`
- `TB-GEN-v15`

Template source:

- `scripts/generate_track_b_ui.py`

Appendix records:

- `thesis/appendices/prompt_templates.tex`

`TB-GEN-v14` removes the strong compactness bias from `TB-GEN-v9`, requires
local images, and uses the machine-checkable `workflow_controls` contract
instead of the older broad `workflow_labels` list.

`TB-GEN-v14` improved image use, but still failed static gate:

- static gate: failed
- image use: substantially improved
- remaining hard failures:
  - non-contract `showPage()` route IDs
  - `Gefilte Fish` still appeared as a title while the actual link text was
    `View Recipe`

`TB-GEN-v15` tightens v14 by:

- forbidding `showPage()` with route IDs outside `window.__TRACK_B_ROUTES`
- requiring the clickable element's own visible text to exactly match
  `visible_text`
- explicitly forbidding replacements such as `View Recipe`

## Results

Run:

- `data/track_b/items/F10_gourmania/generated/gwdg_qwen3_omni_30b_v15_f10_smoke/`

Static gate:

- report: `data/track_b/items/F10_gourmania/generated/gwdg_qwen3_omni_30b_v15_f10_smoke/gate_report.json`
- passed: true
- failed errors: 0
- failed warnings: 2
- warnings:
  - non-workflow route IDs: `my_food_line`, `newsletter`, `recipes`
  - missing local image sources: social icons and `Hamentaschen.jpg`

Browser workflow:

- report: `data/track_b/items/F10_gourmania/generated/gwdg_qwen3_omni_30b_v15_f10_smoke/browser_workflow_report.json`
- passed cases: 8/8
- route success rate: 1.000
- content validation success rate: 1.000
- task success rate: 1.000

Efficiency metadata:

- prompt tokens: 39,946
- completion tokens: 6,643
- total tokens: 46,589
- elapsed seconds: 64.83
- finish reason: `stop`

Leaderboard demo output:

- `data/track_b/leaderboard/model_leaderboard_tb_gen_v15.md`

## Interpretation

This experiment shows that F10 was not blocked by missing input assets. The
main issues were:

- `TB-GEN-v9` biased weaker models toward text-only minimal pages.
- The old gate over-treated workflow context phrases as hard clickable labels.
- The model needed a stricter, machine-checkable control contract to keep
`Gefilte Fish` itself as the clickable label.

`TB-GEN-v15` is not directly comparable with `TB-GEN-v9` leaderboard rows. It
is a prompt diagnostic showing how the protocol can be improved for future
same-prompt runs.

Remaining limitations:

- The generated artifact still has broken non-critical image references.
- Some non-workflow navigation items still point at missing routes and are only
  warnings.
- Static visual/UX scoring is still pending and should remain separate from
  workflow content validation.
