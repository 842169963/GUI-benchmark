# Track B TB-GEN-v16 Input Compression

Date: 2026-06-05

## Purpose

`TB-GEN-v15` passed the F10 smoke case but did not generalize to the small
batch. The main failure modes were repeated/verbose workflow input, incorrect
handling of semantic visual click targets such as logo clicks, and context or
output pressure on larger items.

This note records the follow-up input-packing change before running a new
generation batch.

## Implementation

Changed:

- `scripts/generate_track_b_ui.py`
- `thesis/appendices/prompt_templates.tex`

New prompt/input version:

- `TB-GEN-v16`

New input profile:

- `compact`

The default `auto` behavior keeps legacy input for old prompt ids and switches
to compact input for `TB-GEN-v16`.

## What Changed

Workflow input:

- Old behavior: insert the full formatted `workflow.json`.
- New compact behavior: insert a route-level workflow summary:
  - exact-text click controls remain in the machine-checkable
    `required_element` contract;
  - semantic/visual click targets, such as a logo click, are listed separately
    as route guidance rather than exact visible-text requirements;
  - validations are deduplicated and grouped by destination `route_id`.

Resource input:

- Old behavior: list resource paths in sorted filesystem order.
- New compact behavior: rank resources by image type, route/control/requirement
  term overlap, and visual filename hints such as `logo`, `hero`, `banner`,
  `thumbnail`, or `video`.
- Compact runs default to at most 60 listed resource paths.

Prototype image input:

- Old behavior: attach original prototype screenshots.
- New compact behavior: for compact runs, downscale attached prototype images
  before API upload so the longest side is at most 3000 px. Original files on
  disk are unchanged.

Route inference:

- Adjusted workflow-control route inference so home routes can be selected for
  logo clicks, explicit HOME labels, and back/return-home actions. This fixes
  the F01-style `logo at the top of the page` issue and F06-style navigation
  back to the homepage.

## Dry-Run Checks

F03 prompt text size:

| Item | Prompt | Input profile | Lines | Words | Characters |
| --- | --- | --- | ---: | ---: | ---: |
| F03_about_gitlab | `TB-GEN-v15` | legacy | 380 | 1972 | 18878 |
| F03_about_gitlab | `TB-GEN-v16` | compact | 189 | 1536 | 13424 |

This reduces the text prompt by about 29%. The larger expected reduction for
F03 comes from image downscaling, because the original F03 prototype screenshots
are very tall full-page captures.

F03 compact image sizes with `image_max_side=3000`:

| Prototype | Original size | Sent size |
| --- | ---: | ---: |
| `company.jpg` | 1920 x 7735 | 744 x 3000 |
| `customers.jpg` | 1920 x 6719 | 857 x 3000 |
| `gitlab_duo.jpg` | 1511 x 8000 | 566 x 3000 |
| `homepage.jpg` | 1864 x 8000 | 699 x 3000 |
| `platform.jpg` | 1920 x 6632 | 868 x 3000 |
| `pricing.jpg` | 1577 x 8000 | 591 x 3000 |

Route checks:

- F01 `Click the logo at the top of the page` is now a semantic/visual target
  routed to `home`, not an exact visible-text control.
- F06 `Discover events` remains routed to `blogs`.
- F06 `Dynamics 365 Community` navigation and breadcrumb links are routed to
  `homepage`.

## Interpretation

This change is an input-policy normalization, not a leaderboard scoring change.
It should make the generation prompt fairer by giving every model the same
deduplicated route/evidence summary and the same downscaled prototype inputs.

It does not guarantee better UI quality. The next empirical check should run a
small `TB-GEN-v16` smoke batch, preferably starting with the free GWDG
`qwen3.6-35b-a3b` model because it previously accepted larger F03 prompts.

## Remaining Uncertainty

- The compact workflow summary may still miss nuance from multi-step workflows.
- Downscaled screenshots preserve route-level visual structure but may reduce
  fine text readability on very tall pages.
- `TB-GEN-v16` is a candidate prompt/input policy, not a frozen leaderboard
  baseline.

## F03 Smoke Results

Date: 2026-06-05

Item:

- `F03_about_gitlab`

Prompt/input:

- `TB-GEN-v16`
- `input_profile=compact`
- `workflow_text_format=compact_route_evidence_v1`
- `resource_paths_in_prompt_count=60`
- `omitted_resource_count=49`
- prototype image upload longest side: 3000 px

Runs:

| Model | Run | Finish | Prompt tokens | Completion tokens | Static gate | Browser workflow |
| --- | --- | --- | ---: | ---: | --- | --- |
| `qwen3.6-35b-a3b` | `gwdg_qwen36_35b_v16_f03_compact_smoke` | `stop` | 16,261 | 13,115 | pass, 1 semantic warning | 4/8 cases, route 1.000, content 0.500 |
| `qwen3-omni-30b-a3b-instruct` | `gwdg_qwen3_omni_30b_v16_f03_compact_smoke` | `stop` | 16,180 | 15,600 | pass, 1 semantic warning | 3/8 cases, route 0.750, content 0.500 |

Static gate interpretation after evaluator correction:

- `GitLab Duo` comes from the workflow phrase `button or link related to
  GitLab Duo`, so exact visible text is not a hard requirement. The gate records
  missing exact clickable `GitLab Duo` as a semantic warning rather than an
  error.

Browser workflow failure pattern:

- Platform, Pricing, and Company route clicks worked in both artifacts.
- In the `qwen3.6-35b-a3b` artifact, the semantic matcher selected
  `AI-Assisted Development` with `href="#gitlab_duo"` for the GitLab Duo
  action, so route success is 1.000.
- In the `qwen3-omni-30b-a3b-instruct` artifact, no sufficiently related
  GitLab Duo route/link candidate was found from the homepage, so route success
  remains 0.750.
- Some content validations failed because generated pages did not preserve exact
  expected heading/evidence text such as `The most comprehensive AI-powered
  DevSecOps Platform`, `Get started with GitLab`, and `About GitLab`.

Interpretation:

- Compact input solved the prior F03 qwen3-omni input-limit failure. The same
  item that previously exceeded the 65,536-token context limit now generated
  successfully with about 16k prompt tokens.
- `TB-GEN-v16` is still not sufficient as a leaderboard candidate because
  content-validation evidence is incomplete, and one model still lacks a
  semantic GitLab Duo route entry from the homepage.
- The next prompt should strengthen route/evidence guarantees without requiring
  semantically phrased targets such as `related to GitLab Duo` to be the exact
  visible button text. If implemented, this should be a new prompt version
  (for example `TB-GEN-v17`) rather than a silent change to `TB-GEN-v16`.
