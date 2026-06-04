# Track B Browser Workflow v1 Experiment

Date: 2026-06-03

## Purpose

This experiment upgrades the Track B dynamic pilot from deterministic
`route-simulation-v1` to a real-browser scripted evaluator,
`browser-workflow-v1`.

The goal is not to use an autonomous computer-use agent yet. The goal is to
test whether fixed `workflow.json` cases can be executed reproducibly in
Chromium while preserving clearer failure attribution than a full agent run.

## Implementation

Script:

- `scripts/run_track_b_browser_workflow.js`

Main behavior:

- opens each generated `index.html` in Chromium through Playwright
- starts each workflow case from the item homepage route when available
- executes visible `<a>` / `<button>` controls matching the workflow action
- uses contextual matching for ambiguous controls such as `Learn more`
- checks visible text, visible image/card/form evidence, active navigation
  state, route reachability, and console errors
- writes per-run `browser_workflow_report.json` files under each generated run
  directory

Inputs:

- benchmark-owned `workflow.json`
- generated run `index.html`
- static-gate result `gate_report.json` for deciding which runs enter the
  formal browser-workflow summary

Output summary:

- `data/track_b/browser_workflow_summary.json`

Per-run detailed reports are under `data/track_b/items/.../generated/...` and
are ignored local artifacts because `data/track_b/items/` is ignored by git.

## Results

Browser-workflow results for current static-gate-passing runs:

| Item | Run | Cases passed | Route success | Content validation | Task success |
| --- | --- | ---: | ---: | ---: | ---: |
| F01_1daycloud | `gwdg_qwen36_35b_v9_smoke` | 8/12 | 1.000 | 0.667 | 0.667 |
| F03_about_gitlab | `gwdg_qwen36_35b_v9_smoke` | 8/8 | 1.000 | 1.000 | 1.000 |
| F06_community_dynamics | `gwdg_qwen36_35b_v9_smoke_40k` | 4/10 | 1.000 | 0.400 | 0.400 |
| F09_elections_bc | `claude_sonnet45_v3_smoke` | 5/10 | 0.900 | 0.500 | 0.500 |
| F09_elections_bc | `claude_sonnet45_v4_smoke` | 5/10 | 0.900 | 0.500 | 0.500 |
| F09_elections_bc | `gwdg_qwen36_35b_v6_smoke_40k` | 5/10 | 0.900 | 0.500 | 0.500 |
| F10_gourmania | `gwdg_qwen36_35b_v9_smoke` | 7/8 | 1.000 | 0.875 | 0.875 |

## Interpretation

`browser-workflow-v1` is a stronger candidate than `route-simulation-v1` for
the formal dynamic layer because it executes the generated UI in a real browser
and validates visible DOM state.

The current results show that route reachability is usually high among
static-gate-passing runs. Most failures are content-validation failures: the
generated UI reaches a route, but the visible destination page lacks the
required text, form, card, table, sidebar, or other UI evidence.

Task success equals the case-level conjunction of action success, route success,
and content-validation success. Therefore, when route success is 1.000, task
success and content-validation success are often identical.

## Workflow Normalization Issue

F09 exposed an important workflow-design issue. One case asks the evaluator to
click `Local Forms` in the sidebar, but that sidebar control is only visible
after navigating to the local-elections page. If each case is evaluated
independently from the homepage, this case lacks its prerequisite navigation
path.

Before final scoring, workflow cases should be normalized so that every
independently scored case includes the prerequisite steps needed to make its
target control visible.

Normalization demo:

- normalized workflow file:
  `data/track_b/workflow_demos/F09_elections_bc_browser_normalized_v1.json`
- evaluator override:
  `scripts/run_track_b_browser_workflow.js --workflow <normalized-workflow>`

| Item | Run | Workflow | Route success | Content validation | Task success |
| --- | --- | --- | ---: | ---: | ---: |
| F09_elections_bc | `claude_sonnet45_v4_smoke` | original | 0.900 | 0.500 | 0.500 |
| F09_elections_bc | `claude_sonnet45_v4_smoke` | normalized demo | 1.000 | 0.500 | 0.500 |
| F09_elections_bc | `gwdg_qwen36_35b_v6_smoke_40k` | original | 0.900 | 0.500 | 0.500 |
| F09_elections_bc | `gwdg_qwen36_35b_v6_smoke_40k` | normalized demo | 1.000 | 0.500 | 0.500 |

This confirms that normalization fixes an artificial route failure caused by a
missing prerequisite path. It does not hide content failures: task success stays
at 0.500 because the destination pages still lack required visible evidence
such as the local forms table/dropdown and sidebar/content descriptions.

Workflow-case normalization was then formalized in:

- `scripts/normalize_track_b_workflow_cases.py`
- `data/track_b/workflows_normalized/normalization_summary.json`

For the current leaderboard-demo item set, the normalizer changed two items:

- `F06_community_dynamics`: added the missing `Discover events` prerequisite
  for two cases that are defined from the blogs page.
- `F09_elections_bc`: added the missing local-elections prerequisite before
  the `Local Forms` sidebar action.

After rerunning `browser-workflow-v1` with normalized workflows, all currently
eligible artifacts have `route_success_rate = 1.000`. Remaining dynamic
failures are therefore content-validation failures rather than prerequisite
path failures.

## Next Steps

- Keep `route-simulation-v1` as a lightweight baseline and diagnostic check.
- Use `browser-workflow-v1` as the candidate formal dynamic evaluator.
- Use normalized workflow cases for final browser-workflow scoring.
- Keep autonomous agent execution as a small exploratory extension after the
  scripted browser workflow evaluator is stable.
