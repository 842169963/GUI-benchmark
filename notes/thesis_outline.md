# Master Thesis Outline

## Current Thesis Direction

The thesis is a reproducible multi-dimensional benchmark and leaderboard
framework for evaluating LLM-generated web interfaces and web apps.

The direct evaluation target is the generated UI/Web app artifact. The
leaderboard ranking target is the generator LLM. Artifact-level scores are
aggregated into model-level leaderboard rows.

The main benchmark mode is New LLM mode:

```text
Input: generator model API/interface
Fixed context: benchmark dataset + standardized prompt schema + evaluation protocol
Output: one leaderboard row for the generator model
```

Single HTML or zip-project scoring can exist as a secondary artifact report
mode, but it is not the main thesis leaderboard basis unless the artifact was
generated under the fixed benchmark protocol and includes complete generation
metadata.

## Scope Decisions

- Primary artifact contribution: fixed benchmark dataset, standardized prompt
  schema, scoring protocol, result format, and leaderboard design.
- Primary empirical contribution: measuring how static technical, static
  visual, dynamic, and efficiency signals characterize generated web apps, and
  how static scores relate to dynamic task success.
- Track A/UIClip is retained only as a small baseline or sanity check. It is not
  the main research question or primary contribution.
- Judge models, human review, and LLM-as-a-judge prompts are scoring
  instruments. They are not the leaderboard ranking target.
- Judge bias is treated as a reliability audit of scoring, not as a standalone
  thesis track.
- Heavy autonomous real-agent execution is out of scope for the immediate
  implementation. The dynamic metric schema should remain compatible with a
  future real-agent executor, but the first implementation uses route
  simulation and browser-workflow validation.
- Mobile and native app evaluation are future work unless explicitly added
  later. The current benchmark focuses on web interfaces and web apps.

## Research Questions

### RQ1: Benchmark and Leaderboard Design

How can a reproducible benchmark and leaderboard be designed for evaluating
LLM-generated web interfaces?

This question defines the fixed benchmark dataset, benchmark item schema,
standardized generation prompt, generated artifact format, evaluation protocol,
metadata requirements, and model-level aggregation strategy.

### RQ2: Metric Operationalization and Aggregation

How can static technical, static visual, dynamic task-based, and efficiency
metrics be operationalized and aggregated for generated web apps?

This question defines the category scores and their submetrics:

- Static Technical Score
- Static Visual Score
- Dynamic Score
- Efficiency Score
- optional Overall Score

Category-specific rankings remain visible because different users may care more
about visual quality, functionality, or cost efficiency.

### RQ3: Static-Dynamic Relationship

How are static quality scores related to dynamic task-success outcomes in
LLM-generated web apps?

This question uses the same generated artifacts for both static and dynamic
evaluation. It analyzes correlations and mismatch cases, such as visually strong
interfaces that fail tasks or visually plain interfaces that support the
workflow reliably.

### Reliability Audit

How stable and bias-sensitive are the LLM-based visual/rubric scores used in
the evaluation pipeline?

This audit records repeated scoring consistency, order-swap sensitivity for
pairwise comparisons when used, rating-scale sensitivity if feasible, judge
model variance, and invalid or refusal rates. It supports the scoring protocol
but does not become the main thesis question.

## Benchmark Object Model

### Benchmark Item

A benchmark item is the fixed test specification. It is not a generated output.
It contains the requirement, expected pages/routes, required elements, tasks,
validation rules, visual screenshot targets, and metadata.

Recommended item files:

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

### Generated Artifact

A generated artifact is the web app produced by a generator model for one
benchmark item. The artifact is the direct evaluation target.

Minimum generated artifact:

```text
generated/<item_id>/<model_run_id>/
  index.html
  generation_metadata.json
  optional local assets
```

### Model-Level Leaderboard Row

The leaderboard aggregates artifact-level scores across benchmark items into one
row per generator model or model configuration.

Recommended top-level columns:

- Model
- Overall Score
- Static Technical Score
- Static Visual Score
- Dynamic Score
- Efficiency Score
- Average Cost per App
- Average Token Usage

## Metric Categories

### Static Technical Metrics

Static technical metrics evaluate whether the generated artifact structurally
covers the benchmark item without executing a user task.

Examples:

- HTML completeness
- required element coverage
- required text coverage
- route declaration coverage
- link target declaration
- form field coverage
- selector or ID coverage
- accessibility basics
- static requirement fidelity

Static technical evaluation may check whether an Add to Cart button exists, but
it should not claim that clicking the button updates the cart. That belongs to
dynamic evaluation.

### Static Visual Metrics

Static visual evaluation uses standardized predefined-route screenshots. It
does not use screenshots collected from agent traces as the main visual scoring
input.

Candidate dimensions:

- visual hierarchy
- information organization
- typography and readability
- contrast
- spacing and alignment
- consistency
- aesthetic quality

Screenshot protocol:

1. Render the generated app locally.
2. Visit each predefined page or route listed in `visual_pages.json`.
3. Capture one standardized screenshot per page using the same browser,
   viewport, zoom, wait rule, and full-page/viewport rule.
4. Score each screenshot with the same visual rubric.
5. Aggregate page-level scores into an artifact-level Static Visual Score.

Agent trace screenshots may be stored for debugging and dynamic failure
analysis only.

### Dynamic Metrics

Dynamic metrics evaluate task behavior that requires interaction or validated
workflow execution.

Candidate submetrics:

- task success rate
- step success rate
- route execution success
- button functionality success
- form completion success
- state-change success
- retry count
- failure localization
- robustness or pass@k

The first implementation may use deterministic route simulation or
browser-workflow validation with Playwright. The metric schema should also
support a future browser-based real-agent executor. The intended rule is:
change the executor, not the metric schema.

### Efficiency Metrics

Efficiency metrics track resource usage and cost:

- input tokens
- output tokens
- total tokens
- generation cost
- evaluation cost
- generation latency
- evaluation latency
- cost-performance ratio

The evaluation protocol should avoid presenting any fixed truncating
output-token cap as the final policy. If a provider requires a maximum output
setting, it should be high enough for complete outputs where feasible, and the
actual token usage, cost, latency, and failure mode should be recorded.

## Optional Overall Score

The initial optional composite is:

```text
Overall Score =
0.25 * Static Technical Score
+ 0.25 * Static Visual Score
+ 0.35 * Dynamic Score
+ 0.15 * Efficiency Score
```

This score is a reporting convenience, not a replacement for category-specific
rankings. The thesis should report category scores and discuss trade-offs.

## Thesis Structure

### Chapter 1: Introduction

- Motivation: LLMs can generate web interfaces, but quality must be evaluated
  beyond visual appeal.
- Problem statement: no compact reusable benchmark and leaderboard combines
  fixed generation tasks, static technical checks, standardized visual scoring,
  dynamic task validation, and efficiency reporting.
- Research questions.
- Contributions.
- Thesis structure.

### Chapter 2: Related Work

- LLM-generated UI and UI-to-code benchmarks.
- GUI quality evaluation and usability theory.
- Screenshot-based UI assessment, including UIClip.
- Static and dynamic web/UI testing.
- LLM-as-a-judge and reliability risks.
- Computer-use agents and dynamic UI evaluation, positioned as related work and
  future upgrade path rather than the immediate executor.

### Chapter 3: Benchmark Design and Methodology

- Benchmark scope and fixed-item design.
- Artifact-level evaluation and model-level leaderboard aggregation.
- New LLM mode.
- Benchmark item schema.
- Standardized prompt schema.
- Rendering and standardized screenshot protocol.
- Static technical, static visual, dynamic, and efficiency evaluation design.
- Reliability audit protocol.

### Chapter 4: Evaluation Metrics

- Formal metric definitions.
- Category score formulas.
- Optional overall score.
- Reliability and bias audit metrics.
- Aggregation from artifact-level to model-level results.

### Chapter 5: Leaderboard Framework

- Add-new-LLM pipeline.
- Generation module.
- Rendering and screenshot module.
- Scoring modules.
- Result storage.
- Leaderboard views.
- Cost-performance plots and Pareto frontier.

### Chapter 6: Experiments and Results

- Benchmark items used.
- Generator models evaluated.
- Static technical results.
- Static visual results.
- Dynamic results.
- Overall and category-specific leaderboard.
- Cost-performance analysis.
- Static-dynamic relationship analysis.
- Reliability audit records.

### Chapter 7: Discussion

- What each metric category captures.
- Where static and dynamic metrics agree or diverge.
- Practical benchmark and leaderboard implications.
- Limitations.
- Threats to validity.
- Real-agent upgrade path.

### Chapter 8: Conclusion

- Summary of findings.
- Contributions.
- Future work.

## Development Roadmap

### Stage 1: Minimal End-to-End Prototype

Scope:

- 2-5 benchmark web app items
- 2-3 generator models
- fixed prompt schema
- generated artifacts
- static technical checks
- standardized screenshot capture
- static visual scoring
- lightweight dynamic validation
- token, cost, and latency tracking
- mini leaderboard

Goal: make the full pipeline work end to end.

### Stage 2: Thesis Experiment

If feasible:

- expand to 10-20 benchmark tasks
- include more generator models depending on cost
- analyze static-dynamic relationships
- report category-specific rankings and optional overall ranking
- add cost-performance and Pareto plots
- record reliability audit data

### Stage 3: Optional Real-Agent Cross-Check

Only after the main pipeline is stable:

- run a small subset with a browser-based computer-use agent
- compare real-agent traces with lightweight dynamic validation
- use trace screenshots only for debugging and failure analysis

## Prompt Preservation Note

Prompts used for formal GUI generation, static visual/rubric scoring, dynamic
action-plan elicitation, output schemas, or human annotation instructions must
be versioned and preserved according to `notes/prompt_preservation_policy.md`.

Routine planning prompts and coding-assistant instructions are not stored in the
appendix unless the thesis explicitly uses them as experimental material.
