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

All category scores should be normalized to `[0, 1]` before aggregation.

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

Candidate dimensions:

| Dimension | Definition |
| --- | --- |
| Visual hierarchy | Important content is visually prioritized and scannable. |
| Information organization | Related information is grouped and page structure is understandable. |
| Typography/readability | Text size, weight, line length, and contrast support reading. |
| Contrast | Foreground/background and key controls have sufficient visual separation. |
| Spacing/alignment | Layout spacing and alignment are consistent and not cluttered. |
| Consistency | Repeated components, navigation, colors, and typography are coherent. |
| Aesthetic quality | The interface appears polished and appropriate for the domain. |

Screenshot protocol:

1. Render the generated app locally.
2. Visit every predefined route listed in `visual_pages.json`.
3. Capture one standardized screenshot per route.
4. Use the same browser engine, viewport, zoom, wait time, and screenshot rule.
5. Score every screenshot with the same visual rubric.
6. Aggregate page-level visual scores into the artifact-level Static Visual
   Score.

Recommended aggregation:

```text
page_visual_score = mean(visual dimensions for that page)
Static Visual Score = mean(page_visual_score over predefined visual pages)
```

Agent trace screenshots are stored only for debugging and dynamic failure
analysis. They are not the primary input for static visual scoring.

## Dynamic Score

Dynamic metrics evaluate interaction behavior. A metric is dynamic when it
requires clicking, typing, navigating, submitting, waiting for state changes, or
validating task completion.

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

The current implementation may use lightweight workflow or action-plan
validation. A future implementation may use a browser-based computer-use agent.
The metric schema should stay stable: change the executor, not the metric
schema.

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

This weighting is a starting proposal. The thesis must also report
category-specific rankings and cost-performance plots because users may
prioritize different trade-offs.

## Reliability Audit Metrics

Reliability and bias checks audit the scoring protocol. They are not the main
leaderboard objective.

Candidate audit metrics:

- repeated scoring consistency
- order-swap sensitivity for pairwise comparisons when used
- rating-scale sensitivity if feasible
- judge model variance
- invalid or refusal rate

These metrics should be reported separately from generator-model quality.

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
