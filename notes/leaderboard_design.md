# Leaderboard Design

Status: planning specification for the generator-model leaderboard.

The leaderboard ranks generator LLMs. It does not rank judge models.

Generated UI/Web app artifacts are the direct evaluation target. Artifact-level
scores are aggregated into model-level leaderboard rows.

## Main Mode: New LLM Mode

Main input:

```text
generator model API/interface
```

Fixed context:

```text
benchmark dataset + standardized prompt schema + evaluation protocol
```

Output:

```text
one model-level leaderboard row
```

Pipeline:

1. Load fixed benchmark items.
2. Apply the standardized prompt schema.
3. Generate one artifact per benchmark item.
4. Store generation metadata.
5. Run static technical scoring.
6. Render predefined routes and capture standardized screenshots.
7. Run static visual scoring on the standardized screenshots.
8. Run lightweight dynamic validation.
9. Record token usage, cost, and latency.
10. Aggregate artifact-level scores into model-level category scores.
11. Compute optional Overall Score.
12. Update leaderboard tables and plots.

## Secondary Mode: Artifact Scoring

The framework may optionally score a single uploaded HTML file or zip project.

This mode produces an artifact-level report. It is not the main leaderboard
basis unless the artifact was generated under the same fixed benchmark protocol
and includes model, prompt, item, timestamp, and generation metadata.

## Leaderboard Columns

Recommended top-level columns:

| Column | Meaning |
| --- | --- |
| Model | Generator model or model configuration. |
| Overall Score | Optional weighted score across categories. |
| Static Technical Score | Structural and requirement coverage score. |
| Static Visual Score | Standardized screenshot-based visual score. |
| Dynamic Score | Task or workflow success score. |
| Efficiency Score | Cost and latency efficiency score. |
| Average Cost per App | Mean generation/evaluation cost per artifact. |
| Average Token Usage | Mean total token usage per artifact. |

Detailed submetrics should live in model detail pages, result JSON files, or
appendix tables rather than as all top-level columns.

## Optional Overall Score

Initial optional composite:

```text
Overall Score =
0.25 * Static Technical Score
+ 0.25 * Static Visual Score
+ 0.35 * Dynamic Score
+ 0.15 * Efficiency Score
```

The leaderboard must preserve category-specific rankings because users may
prioritize different trade-offs.

## Result Aggregation

Artifact-level result:

```text
score generated artifact A from model M on benchmark item I
```

Model-level row:

```text
aggregate all artifact-level scores for model M across the fixed item set
```

Recommended model-level reporting:

- attempted item count
- valid artifact count
- failed artifact count
- provider/tool failure count
- mean category scores
- standard deviation or confidence interval if enough items are available

## Cost-Performance Reporting

The leaderboard should include cost-performance views:

- cost vs Static Technical Score
- cost vs Static Visual Score
- cost vs Dynamic Score
- cost vs Overall Score
- token usage vs score
- latency vs score

Pareto frontier plots should highlight models that are not dominated by another
model with both lower cost and higher score.

## Reliability Audit Reporting

Reliability and bias checks are audit fields, not main ranking targets.

Possible detail-page fields:

- repeated scoring consistency
- order-swap sensitivity
- rating-scale sensitivity if feasible
- judge model variance
- invalid or refusal rate

These fields support trust in the scoring protocol without turning judge-model
bias into the main thesis contribution.

## Static Screenshot Rule

Static visual leaderboard scores must come from standardized predefined-route
screenshots. Agent trace screenshots are stored only for debugging and dynamic
failure analysis.
