# Track B Benchmark Protocol Draft

Status: draft for supervisor discussion.

This note fixes the current working protocol for Track B so that prompt
engineering, submission format, and evaluation layers are not mixed together.
It is intentionally narrower than an open-ended UI evaluation system.

## Scope

Track B evaluates generated executable web interfaces on a fixed set of
representative benchmark items. It does not evaluate arbitrary open-ended user
scenarios.

Each benchmark item contains item-specific material:

- reference screenshots or prototype screenshots
- normalized requirement text
- `workflow.json` actions and validations
- local assets/resources
- route identifiers and expected route behavior
- evaluator rules derived from the workflow and route contract

This fixed-item design makes submissions comparable across generator models:
each model receives the same item context and is evaluated against the same
item-specific checks.

## Submission Unit

The leaderboard submission unit is the generated executable UI artifact for a
specific benchmark item.

Required submission files:

- `index.html`
- local assets, if the generated UI needs files outside `index.html`

Minimal optional metadata:

- model name
- submission name or run id
- free-text notes

Detailed generation metadata such as provider, prompt id, max output tokens,
completion tokens, finish reason, and elapsed time is required for the thesis
experiment logs when I run controlled model comparisons, but it should not be a
hard requirement for public leaderboard users because external submitters may
not have access to consistent token or runtime accounting.

Users do not submit the requirement, workflow, validation rules, or reference
screenshots. These belong to the benchmark item and are fixed by the benchmark
system.

## Evaluation Layers

The current practical protocol uses three core layers.

### Layer 0: Static Technical Gate

Purpose: determine whether a generated HTML artifact is valid enough to enter
evaluation.

Current checks:

- complete HTML document with closing body/html tags
- non-truncated style/script blocks
- no provider `finish_reason` indicating token truncation
- `onclick` handlers refer to defined functions
- `showPage(...)` route ids exist as HTML ids
- workflow-required quoted click labels exist as working `<a>` or `<button>`
- semantic click descriptions are recorded as warnings rather than hard exact
  label failures

Output: pass/fail plus diagnostic warnings.

### Layer 1: Dynamic Route Success

Purpose: test whether workflow actions can reach the expected route or section.

Current evaluators:

- `scripts/run_track_b_dynamic_workflow.py`, `route-simulation-v1`
- `scripts/run_track_b_browser_workflow.js`, `browser-workflow-v1`

The route-simulation evaluator parses the generated HTML, identifies clickable
workflow controls, simulates route transitions through `data-route-target`, and
records whether the final route matches the route implied by the action. The
browser-workflow evaluator opens the generated HTML in Chromium, executes
workflow clicks with Playwright, and records the resulting visible route.

Output:

- `route_success_rate`
- per-case route success/failure reason

### Layer 2: Content Validation Success

Purpose: test whether the reached route contains the content evidence required
by the original `workflow.json` validations.

Current evaluators:

- `scripts/run_track_b_dynamic_workflow.py`, `route-simulation-v1`
- `scripts/run_track_b_browser_workflow.js`, `browser-workflow-v1`

The current route-simulation implementation uses deterministic
HTML/text/DOM-structure heuristics, such as:

- quoted heading/text presence
- image/grid counts
- form-field counts
- card-like element counts
- branding/logo text or image-alt evidence

The browser-workflow evaluator applies the same validation intent after real
browser interaction and can check visible text, DOM state, image/card/form
counts, and active navigation state.

Output:

- `content_validation_success_rate`
- per-validation pass/fail reason

## Why Route and Content Are Separate

Route success and content validation measure different failure modes.

Route success answers:

> Did the required interaction take the user to the expected page or section?

Content validation answers:

> Once there, does the page contain the required content or UI evidence?

Keeping them separate avoids misleading results. For example, a generated UI
may correctly navigate to `gitlab_duo`, but fail a content check for visible
branding or pricing information. That should be recorded as a content failure,
not as a navigation failure. Conversely, a page may contain relevant content
somewhere, but fail because the required click target does not route to it.

## Current Pilot Results

Frozen prompt/model setting:

- prompt: `TB-GEN-v9`
- provider/model: GWDG/SAIA `qwen3.6-35b-a3b`
- output budget: `max_tokens=20000`

| Item | Run | Max tokens | Static gate | Route success | Content validation | Task success | Notes |
| --- | --- | ---: | --- | ---: | ---: | ---: | --- |
| F01_1daycloud | `gwdg_qwen36_35b_v9_smoke` | 20000 | pass | 1.000 | 0.750 | 0.750 | Valid pilot artifact. |
| F03_about_gitlab | `gwdg_qwen36_35b_v9_smoke` | 20000 | pass | 1.000 | 1.000 | 1.000 | Valid pilot artifact. |
| F10_gourmania | `gwdg_qwen36_35b_v9_smoke` | 20000 | pass | 1.000 | 0.875 | 0.875 | Valid pilot artifact. |
| F05_balancingbirthbaby | `gwdg_qwen36_35b_v9_smoke` | 20000 | fail | 0.400 | 0.500 | 0.200 | Diagnostic artifact only: missing exact workflow label and undefined `toggle()`. |
| F06_community_dynamics | `gwdg_qwen36_35b_v9_smoke` | 20000 | fail | 1.000 | 0.400 | 0.400 | Diagnostic artifact only: token-truncated at 20k and missing route handler. |
| F06_community_dynamics | `gwdg_qwen36_35b_v9_smoke_40k` | 40000 | pass | 1.000 | 0.400 | 0.400 | 40k cap removes truncation/static failure but content validation remains low. |

Provider-level failure:

- `F02_401trucksource`, `TB-GEN-v9`, GWDG/SAIA `qwen3.6-35b-a3b`,
  `max_tokens=20000`: read timeout after 360 seconds, no artifact.

Interpretation: static-gate-failing runs are diagnostic and should not enter
final leaderboard scoring. Among static-gate-passing runs, route success is
currently strong, while content validation separates high-fidelity artifacts
from artifacts that route correctly but lack the required destination content.
The `F06` 20k/40k comparison shows that output-budget settings can affect
whether a model produces a complete, statically valid artifact.

## Not Yet Final

The current browser-workflow evaluator is enough for a reproducible pilot
layer, but it is not a full autonomous computer-use agent.

Remaining work:

- Expand browser/DOM/CSS assertions for cases that route simulation cannot
  check robustly.
- Decide whether the final leaderboard should include only the three core
  layers above, or add static visual quality and accessibility layers.
- Decide whether route/content dynamic scores should be reported separately or
  also combined into a single dynamic score.
- Define how many fixed benchmark items are needed for a stable leaderboard.
- Decide which metadata fields are required for controlled thesis experiments
  versus optional for public submissions.

## Supervisor Discussion Questions

1. Is the fixed-item design acceptable, explicitly excluding arbitrary
   open-ended UI scenarios?
2. Are the three core layers sufficient for the main Track B leaderboard:
   static technical gate, route success, and content validation?
3. Should static visual quality remain a separate MLLM/human rubric layer, or
   should Track B focus mainly on executable UI functionality?
4. Should accessibility be included in the main leaderboard or reported only as
   auxiliary diagnostics?
5. Is it acceptable that public users submit only executable UI artifacts while
   the benchmark system owns requirements, workflows, screenshots, and
   validation rules?
