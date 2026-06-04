# Metric Specification

Status: planning specification for the thesis benchmark and leaderboard.

This note defines the metric categories used to score generated UI/Web app
artifacts and aggregate them into generator-model leaderboard rows.

The direct evaluation target is the generated artifact. The leaderboard ranking
target is the generator LLM. Artifact-level scores are aggregated across fixed
benchmark items to produce model-level rankings.

## Score Categories

The leaderboard uses four category scores:

- Static Technical Score
- Static Visual Score
- Dynamic Score
- Efficiency Score

An optional Overall Score can be reported, but category-specific rankings remain
visible.

### Score normalization (shared rule)

Different layers use different measuring instruments on purpose — binary
checklists for structural/visual checks, narrow anchored scales for graded
judgements, task success rate for dynamic behavior, and tool violation counts
for accessibility. What is unified is the **output scale**: every submetric is
normalized to `[0, 1]` before aggregation, and each submetric records its
normalization formula. Common cases:

| Instrument | Raw | Normalized to [0,1] |
| --- | --- | --- |
| Binary checklist | passed / total | already 0–1 |
| Narrow scale `1..max` | value `x` | `(x - 1) / (max - 1)` |
| Task success | successful tasks / total | already 0–1 |
| Accessibility tool | passed checks / total | already 0–1 |

A category score is the mean of its normalized submetrics; the leaderboard
aggregates category scores across items into model-level rows.

## Static Technical Score

Static technical metrics evaluate whether the generated artifact structurally
covers the benchmark item without executing a user task.

Candidate submetrics:

| Submetric | Definition |
| --- | --- |
| HTML completeness | Complete document, non-truncated script/style blocks, visible body content. |
| Required element coverage | Required elements found / total required elements. |
| Required text coverage | Required text items found / total required text items. |
| Route declaration coverage | Required routes declared or recognizable / total required routes. |
| Link target declaration | Required links with declared valid targets / total required links. |
| Form field coverage | Required fields found / total required fields. |
| Selector or ID coverage | Required elements with stable selectors or IDs / total required elements. |
| Accessibility basics | Basic labels, button names, image alt text, and semantic structure. |
| Static requirement fidelity | Structural coverage of required pages, components, labels, and text. |

Recommended aggregation:

```text
Static Technical Score = mean(available static technical submetrics)
```

If a submetric is not applicable to an item, exclude it from the denominator and
record it as not applicable in the detail report.

Static technical evaluation can check that a required button exists and declares
a target. It should not claim that clicking the button completes a workflow.
That belongs to dynamic evaluation.

## Static Visual Score

Static visual metrics evaluate standardized screenshots, not source code and not
agent trace screenshots.

### Design decision (2026-06-04)

The earlier seven-dimension list was reduced for two reasons grounded in the
literature:

1. **Holistic aesthetic judgement is too subjective for a reproducible
   leaderboard metric.** LLM judges agree poorly with humans on raw aesthetic
   ratings out of the box (Beauty-in-the-Eye-of-AI reports LLM-human alignment
   far below human-human agreement before calibration). A single "overall
   aesthetic quality" score would inject high judge variance into the ranking.
   Holistic aesthetics is therefore moved to **future work**, or reported only
   as an optional, non-weighted diagnostic accompanied by human-correlation
   validation.
2. **Anything with an objective rule or formula should not be LLM-judged.**
   Contrast has a deterministic WCAG formula computable from the actual CSS
   colors; it is moved to the automated accessibility metrics (see below) and
   removed from LLM visual scoring.

The LLM judge therefore scores **four objective-leaning visual dimensions**:

| Dimension | Covers (old dims merged) | Grounding |
| --- | --- | --- |
| Layout & Visual Hierarchy | visual hierarchy + spacing/alignment | MLLM-as-UI-Judge (Visual Hierarchy); VisAWI (Simplicity) |
| Information Organization / Clarity | information organization | MLLM-as-UI-Judge (Clarity) |
| Typography & Readability | typography/readability (contrast removed) | WebDevJudge (UI Quality) |
| Visual Consistency | consistency | WebDevJudge (visual consistency); VisAWI (Craftsmanship) |

### Scoring method (binary checklist preferred)

Each dimension is scored by decomposing it into binary (yes/no) sub-questions
answered by the MLLM judge from the screenshot, not by asking for a raw 1–5
score. Binary checklist decomposition gives higher inter-judge agreement and
lower variance than a holistic Likert rating (CheckEval). Example for Layout &
Visual Hierarchy:

| Sub-question | Pass condition |
| --- | --- |
| Is there a clear primary element / visual focus? | yes |
| Are elements free of overlap or misalignment? | yes |
| Does alignment follow a consistent grid? | yes |
| Is spacing consistent across the page? | yes |

```text
dimension_score = passed_sub_questions / total_sub_questions   # 0–1
```

Where a dimension genuinely cannot be decomposed and a graded judgement is
needed, use a **narrow 3–5 level scale with explicit behavioral anchors**, never
a wide 1–9 scale. Wide scales suffer LLM central-tendency bias (higher variance,
lower agreement); narrow anchored scales are more reliable. A graded score `x`
on a `1..max` scale normalizes as `(x - 1) / (max - 1)`.

### Rating-scale policy

The reported scoring uses a narrow anchored scale. A wide scale (e.g. 1–9) or a
verbal-label scale is used **only** as a deliberate condition when recording
rating-scale sensitivity (see Reliability Audit), not as the production scale.

### Reliability levers (optional)

Two cheap calibration levers from the literature may be applied to the visual
judge and recorded:

- **Few-shot anchoring**: include a small number of human-scored example
  screenshots in the judge prompt to align the model's notion of good/bad.
- **Confidence filtering**: discard or flag low-confidence judgements rather
  than forcing a score; report how many judgements were retained.

### Human-correlation validation

LLM visual scores are not assumed reliable. On a small subset, the same
screenshots are scored by humans and the LLM-human correlation
(Pearson/Spearman) is reported. This validation is the evidence that the visual
score is trustworthy, and it is recorded under the Reliability Audit.

### Screenshot protocol

1. Render the generated app locally.
2. Visit every predefined route listed in `visual_pages.json`.
3. Capture one standardized screenshot per route.
4. Use the same browser engine, viewport, zoom, wait time, and screenshot rule.
5. Score every screenshot with the same visual rubric.
6. Aggregate page-level visual scores into the artifact-level Static Visual
   Score.

Recommended aggregation:

```text
page_visual_score = mean(four dimension_scores for that page)   # each 0–1
Static Visual Score = mean(page_visual_score over predefined visual pages)
```

Agent trace screenshots are stored only for debugging and dynamic failure
analysis. They are not the primary input for static visual scoring.

## Accessibility Score (automated, rule-based)

Accessibility is evaluated by a **free, local, deterministic tool**
(`axe-core` via Playwright, or Lighthouse), not by an LLM. This is cheaper than
LLM judging (no tokens), more accurate, reproducible, and immune to judge bias.
It still contributes to the leaderboard — it lives in the automated technical /
accessibility category rather than the LLM visual category.

Tool-checkable rule items include:

| Rule item | Source |
| --- | --- |
| Color contrast (text and controls) | WCAG 2.2 contrast formula on actual CSS colors |
| Image alt text present | WCAG / axe-core |
| Form controls have labels | WCAG / axe-core |
| Buttons/links have accessible names | WCAG / axe-core |
| Heading order is sensible (no skipped levels) | axe-core |
| Document language declared | axe-core |
| Correct ARIA usage | axe-core |
| Landmark regions present | axe-core |

Why contrast is not LLM-judged: the formula needs the exact foreground and
background luminance, which the tool reads from the DOM/CSS. An LLM can only
estimate colors from a screenshot, so giving it the formula does not help.

```text
Accessibility Score = passed_rule_checks / total_applicable_rule_checks   # 0–1
```

Alternatively report `1 - min(1, weighted_violations / N_elements)`. Either way
the output is normalized to `[0, 1]`.

## Dynamic Score

Dynamic metrics evaluate interaction behavior. A metric is dynamic when it
requires clicking, typing, navigating, submitting, waiting for state changes, or
validating task completion.

A task counts as successful **iff its required route is reached AND the
destination content validation passes**. Route success and content validation
are recorded separately for diagnosis, but `task_success` is their conjunction
per task.

Candidate submetrics:

| Submetric | Definition |
| --- | --- |
| Task success rate | Successful tasks / total tasks. |
| Step success rate | Successful steps / total steps. |
| Route execution success | Interactions reach the expected route or page. |
| Button functionality success | Buttons produce the expected effect. |
| Form completion success | Required forms can be filled and submitted. |
| State-change success | Expected DOM or UI state changes occur. |
| Retry count | Attempts needed before success or terminal failure. |
| Failure localization | Failure type recorded for failed tasks. |
| Robustness/pass@k | Success over repeated attempts or executions. |

Recommended first aggregation:

```text
Dynamic Score = task_success_rate
```

Supporting submetrics should be reported in detail files and used for diagnosis.
If the experiment later includes a stable executor with richer per-step data,
the dynamic score may be expanded to a weighted mean, but the thesis should
state that change explicitly.

The current implementation may use deterministic route simulation or
browser-workflow validation. Route simulation checks route/content evidence from
the generated artifact, while browser-workflow validation opens the artifact in
Chromium, executes workflow clicks with Playwright, and validates visible
destination content. A future implementation may use a browser-based
computer-use agent. The metric schema should stay stable: change the executor,
not the metric schema.

## Efficiency Score

Efficiency metrics characterize resource usage and cost.

Candidate submetrics:

| Submetric | Definition |
| --- | --- |
| Input tokens | Prompt/context tokens used for generation. |
| Output tokens | Completion tokens used for generation. |
| Total tokens | Input plus output tokens. |
| Generation cost | Estimated provider cost for generation. |
| Evaluation cost | Estimated provider/tool cost for scoring. |
| Generation latency | Wall-clock generation time. |
| Evaluation latency | Wall-clock scoring time. |
| Cost-performance ratio | Cost compared with category or overall score. |

The evaluation should avoid presenting any fixed truncating output-token cap as
the final policy. If a provider requires a maximum output setting, choose a
setting high enough to allow complete outputs where feasible and record actual
usage, cost, latency, and failures.

One possible normalized efficiency score is:

```text
Efficiency Score = 1 - min(1, cost_per_app / cost_reference)
```

The reference cost should be defined before formal runs. Until that reference is
stable, report raw tokens, cost, and latency alongside category scores.

## Optional Overall Score

Initial optional composite:

```text
Overall Score =
0.25 * Static Technical Score
+ 0.25 * Static Visual Score
+ 0.35 * Dynamic Score
+ 0.15 * Efficiency Score
```

This weighting is a starting proposal and should be treated as a hyper-parameter
to be sensitivity-tested, not a justified final value. The thesis must also
report category-specific rankings and cost-performance plots because users may
prioritize different trade-offs.

Open design note: cost is primarily a **Pareto-plot axis** (cost vs. quality),
so including an Efficiency Score *inside* the weighted Overall risks
double-counting cost (once in the ranking, once on the plot axis). Whether
Efficiency stays a weighted Overall component or becomes purely a Pareto axis is
deferred to the formal-spec stage.

## Reliability Audit Metrics

Reliability and bias checks audit the scoring protocol. They are **not** a
separate research direction in this thesis and do not require dedicated study
effort. The scope is limited to **recording biases as they appear during the
evaluation runs** and applying known controls when they do (order-swap,
individual rather than batched judging, narrow anchored scale). A larger
systematic bias study (position / scale / anchoring / cross-model) is noted only
as an optional future extension that the supervisor suggested; it is out of
scope for the main thesis.

Candidate audit fields recorded alongside runs:

- repeated scoring consistency
- order-swap sensitivity for pairwise comparisons when used
- rating-scale sensitivity if feasible
- judge model variance
- invalid or refusal rate
- LLM-human correlation on the small visual-validation subset

These fields are reported separately from generator-model quality.

## Aggregation Level

Artifact-level result:

```text
(item_id, model_run_id, static_technical_score, static_visual_score,
 dynamic_score, efficiency_score, optional_overall_score)
```

Model-level leaderboard row:

```text
mean artifact-level scores across fixed benchmark items for one generator model
```

Aggregation should report the number of attempted items, valid artifacts, failed
artifacts, and provider/tool failures so that model rankings are interpretable.
