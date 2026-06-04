# Meeting Decision Summary for Codex

Status: condensed repository-facing summary of the June 2026 supervisor
discussion. The raw meeting notes remain outside the committed thesis plan.

## Final Direction

The thesis is a reproducible multi-dimensional benchmark and leaderboard
framework for evaluating LLM-generated web interfaces and web apps. The direct
evaluation target is the generated web artifact. The leaderboard ranking target
is the generator LLM or generator-model configuration.

The thesis should not be framed mainly as a generic arbitrary-HTML scoring
tool, a standalone judge-model comparison study, a position-bias study, or a
UIClip reproduction. UIClip-style pairwise judgement may remain as a small
baseline or sanity check.

## Main Leaderboard Mode

Primary mode: New LLM mode.

```text
Input: generator model API/interface
Fixed context: benchmark dataset + standardized prompt schema + evaluation protocol
Output: one model-level leaderboard row
```

The pipeline loads fixed benchmark items, applies the same prompt schema,
generates artifacts, stores metadata, runs static technical checks, captures
standardized screenshots, runs static visual scoring, runs dynamic validation,
records token/cost/latency data, and aggregates artifact-level scores into
model-level leaderboard rows.

Single HTML or zip-project scoring can exist as a secondary artifact-report
mode, but it is not the main leaderboard basis unless generated under the same
fixed benchmark protocol with complete generation metadata.

## Benchmark Items

A benchmark item is the fixed test specification, not a generated output.
Recommended item shape:

```text
benchmark_item/
  requirement.md
  pages.json
  elements.json
  tasks.json
  validation_rules.json
  visual_pages.json
  metadata.json
```

Generated artifacts store model, provider, prompt ID, timestamp, token usage,
latency, cost, and finish reason separately from the fixed item.

## Metric Categories

The active metric categories are:

- Static Technical Score
- Static Visual Score
- Dynamic Score
- Efficiency Score

An optional Overall Score can be reported, but category-specific scores remain
visible because users may prioritize visual quality, functional correctness, or
cost efficiency differently.

Dynamic metrics should be independent of the execution backend. The first
implementation can use deterministic route simulation or browser-workflow
validation. A later real-agent executor should reuse the same task-success and
failure-taxonomy schema.

## Research Questions

RQ1: How can a reproducible benchmark and leaderboard be designed for
evaluating LLM-generated web interfaces?

RQ2: How can static technical, static visual, dynamic task-based, and
efficiency metrics be operationalized and aggregated for generated web apps?

RQ3: How are static quality scores related to dynamic task-success outcomes in
LLM-generated web apps?

Reliability audit: How stable and bias-sensitive are the LLM-based visual or
rubric scores used in the evaluation pipeline?

## Repository Implications

The active planning documents are:

- `notes/thesis_outline.md`
- `notes/benchmark_item_schema.md`
- `notes/metric_specification.md`
- `notes/prompt_schema.md`
- `notes/leaderboard_design.md`

Thesis-impacting prompts must still be versioned and preserved according to
`notes/prompt_preservation_policy.md`.
