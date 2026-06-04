# Meeting Decision Summary for Codex

## Purpose

This document summarizes the final thesis direction after integrating the Notta meeting summary and the speaker-separated meeting transcript. It should be used to update the current thesis plan, methodology, and implementation roadmap in the repository.

The current thesis should focus on a reproducible benchmark and leaderboard for evaluating LLM-generated web interfaces. The main object of evaluation is the generator model, not the judge model.

---

# 1. Final Thesis Direction

## Main Thesis Direction

The thesis should be positioned as:

**A reproducible multi-dimensional benchmark and leaderboard framework for evaluating LLM-generated web interfaces / web apps.**

The primary goal is to compare different generator LLMs on the same fixed benchmark tasks using the same prompt schema and evaluation protocol.

The thesis should not be framed mainly as:

* a generic tool for scoring arbitrary uploaded HTML files;
* a standalone judge-model comparison study;
* a pure position-bias study;
* a UIClip reproduction as the main research question.

Instead, UIClip-style reproduction or pairwise GUI judging can remain as a small baseline or sanity-check component if needed, but it should not dominate the thesis structure.

---

# 2. Primary Leaderboard Mode

## Main Input Mode: New LLM Mode

The primary leaderboard mode should be:

```text
Input: a generator LLM / model API
Fixed context: benchmark dataset + prompt schema + evaluation protocol
Output: model row in the leaderboard
```

The system should:

1. Load the fixed benchmark dataset.
2. Apply the same standardized prompt schema to every evaluated generator model.
3. Ask the model to generate web app submissions.
4. Run static technical evaluation.
5. Render the generated app locally and capture standardized screenshots.
6. Run static visual evaluation on the standardized screenshots.
7. Run dynamic validation / task-based evaluation.
8. Record token usage, cost, and latency.
9. Aggregate category scores and compute an optional overall score.
10. Add the model to the leaderboard.

## Secondary Artifact-Scoring Mode

The framework may optionally support:

* single HTML upload scoring;
* zip project upload scoring.

However, this mode is secondary. It can produce a score report for an individual artifact, but it should not be the main basis for the leaderboard unless the artifact was generated under the same benchmark protocol, with recorded model, prompt, task ID, timestamp, and generation metadata.

---

# 3. Benchmark Item Definition

A benchmark item is not a generated output. It is the fixed test specification used to evaluate generator models.

A submission artifact is the generated web app produced by a model for a benchmark item.

## Recommended Benchmark Item Schema

Each benchmark item should contain:

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

## Meaning of Each File

### requirement.md

Natural-language requirement given to the generator LLM.

### pages.json

Expected pages or routes, such as:

```json
["/", "/products", "/cart", "/checkout"]
```

### elements.json

Required elements per page, such as buttons, inputs, links, product cards, tables, forms, headings, labels, and required text.

### tasks.json

Dynamic user tasks, such as:

* add a product to the cart;
* submit a booking form;
* filter a table;
* navigate to a detail page;
* complete a checkout workflow.

### validation_rules.json

Rules used to judge whether static and dynamic requirements are satisfied.

### visual_pages.json

List of predefined pages/routes that should be rendered and screenshotted for static visual evaluation.

### metadata.json

Task category, difficulty, source, whether dynamic validation is required, and other metadata.

---

# 4. Static / Dynamic Boundary

The evaluation should clearly distinguish three categories:

```text
Static Technical Metrics
Static Visual Metrics
Dynamic Metrics
```

The general rule is:

```text
If a metric can be evaluated from code, DOM, metadata, or a standardized screenshot without executing a user task, it is static.

If a metric requires clicking, typing, navigating, submitting, waiting for state changes, or completing a workflow, it is dynamic.
```

---

# 5. Static Technical Metrics

Static technical metrics evaluate the structural and requirement-level completeness of the generated artifact.

They should check whether the required UI structure exists, but they should not be responsible for proving that a full workflow works during interaction.

## Recommended Static Technical Metrics

The leaderboard should not expose all submetrics as top-level columns. Instead, these submetrics should be aggregated into a **Static Technical Score** and shown in detail pages or appendices.

Candidate submetrics:

1. HTML completeness

   * valid HTML structure;
   * presence of body/head/script/style sections where needed;
   * generated output not obviously truncated.

2. Required element coverage

   * required elements found / total required elements.

3. Required text coverage

   * required text items found / total required text items.

4. Route declaration coverage

   * declared or recognizable required routes / total required routes.

5. Link target declaration

   * required links with valid declared targets / total required links.

6. Form field coverage

   * required input/select/textarea fields found / total required fields.

7. Selector / ID coverage

   * stable selectors or IDs available for required elements.

8. Accessibility basics

   * labels for form fields;
   * button accessible names;
   * image alt text;
   * basic ARIA or semantic structure when applicable.

9. Static requirement fidelity

   * whether the generated structure covers the required pages, components, and text.

## Important Boundary

Examples that belong to static technical evaluation:

* “Does the Add to Cart button exist?”
* “Does the cart page exist or is it declared?”
* “Is there a checkout form?”
* “Does the required label text appear?”

Examples that belong to dynamic evaluation:

* “Does clicking Add to Cart actually update the cart?”
* “Does the checkout form submit successfully?”
* “Does the app navigate to the confirmation page after submission?”

---

# 6. Static Visual Metrics

Static visual evaluation is separate from static technical evaluation.

It evaluates visual quality from standardized screenshots, not from agent trace screenshots.

## Recommended Static Visual Dimensions

Candidate submetrics:

1. Visual hierarchy
2. Information organization
3. Typography / readability
4. Contrast
5. Spacing and alignment
6. Consistency
7. Overall aesthetic quality

These should be aggregated into a **Static Visual Score**.

## Standardized Screenshot Protocol

For each generated app:

```text
1. Render the app locally.
2. Visit each predefined required page / route.
3. Capture one standardized screenshot per page using the same viewport.
4. Evaluate each screenshot using the same visual rubric.
5. Aggregate page-level visual scores into an app-level visual score.
```

Recommended fixed screenshot configuration:

* same browser engine, e.g., Chromium;
* same viewport size, e.g., 1440 × 900;
* same zoom level;
* same wait time after page load;
* same full-page or viewport-only screenshot rule.

## Difference from Agent Trace Screenshots

Standardized screenshots:

* captured from predefined pages/routes;
* same number and type of screenshots per app;
* suitable for fair visual leaderboard scoring.

Agent trace screenshots:

* captured while an agent executes a task;
* number and sequence vary by app and agent behavior;
* useful for debugging and failure analysis;
* should not be the primary input for static visual scoring.

Final rule:

```text
Static visual scores are computed from standardized screenshots of predefined pages. Agent trace screenshots are stored for dynamic failure analysis but are not used as the main visual leaderboard input.
```

---

# 7. Dynamic Metrics

Dynamic evaluation checks whether the generated web app actually works during interaction or task validation.

The initial implementation may use lightweight dynamic validation, but the metric design should remain compatible with future real computer-use agents.

## Recommended Dynamic Metrics

Top-level leaderboard column:

```text
Dynamic Score
```

Candidate submetrics:

1. Task success rate

   * successful tasks / total tasks.

2. Step success rate

   * successful steps / total steps.

3. Route execution success

   * whether the expected target page is reached after interaction.

4. Button functionality success

   * whether buttons produce the expected effect.

5. Form completion success

   * whether required forms can be filled and submitted.

6. State-change success

   * whether cart count, confirmation message, table filtering, selected item, or similar state changes occur.

7. Retry count

   * number of attempts needed before success or failure.

8. Failure localization

   * failure type: missing element, broken button, broken route, form failure, state failure, visual ambiguity, agent error, task ambiguity.

9. Robustness / pass@k

   * success over multiple attempts or runs.

---

# 8. Compatibility with Real Agent Upgrade

The dynamic metric schema should be independent of the execution backend.

Current lightweight implementation may use:

```text
DOM + screenshot + task → LLM action plan → deterministic validator
```

Future real-agent implementation may use:

```text
browser + computer-use agent → executed trace → same success oracle
```

The key idea:

```text
Change the executor, not the metric schema.
```

For example:

| Metric               | Lightweight version                   | Real-agent version                       |
| -------------------- | ------------------------------------- | ---------------------------------------- |
| Task success rate    | action plan passes validator          | agent completes task in browser          |
| Route success        | planned route matches target          | browser reaches target route             |
| Form success         | planned form actions are valid        | agent fills and submits form             |
| State-change success | validator predicts expected DOM/state | actual DOM/state changes after execution |
| Failure localization | validator error                       | trace/log/screenshot failure analysis    |

The thesis should implement the lightweight version first. Real-agent execution should be treated as an optional later upgrade or a small cross-check after the main pipeline is stable.

---

# 9. Recommended Development Scope

The implementation should proceed in stages.

## Stage 1: Minimal End-to-End Prototype

Scope:

* 2–5 benchmark web app items;
* 2–3 generator models;
* fixed prompt schema;
* generated web app artifacts;
* static technical checks;
* standardized screenshot capture;
* static visual scoring;
* lightweight dynamic validation;
* token/cost/latency tracking;
* mini leaderboard.

Goal:

* make the full pipeline work end-to-end.

## Stage 2: Expanded Thesis Experiment

If feasible:

* expand to 10–20 benchmark tasks;
* include more generator models depending on cost;
* analyze static-dynamic relationship;
* add cost-performance and Pareto plots;
* record reliability/bias audit data.

## Stage 3: Optional Real-Agent Cross-Check

After the route is stable:

* run a small subset, e.g., 5–10 items, with a real browser-based computer-use agent;
* compare real-agent results with lightweight dynamic validation;
* use agent trace screenshots only for failure analysis.

---

# 10. Leaderboard Score Design

The leaderboard should not expose every submetric as a top-level column. It should show category scores and optional overall score.

## Recommended Leaderboard Columns

```text
Model
Overall Score
Static Technical Score
Static Visual Score
Dynamic Score
Efficiency Score
Average Cost per App
Average Token Usage
```

## Detail Pages / Appendix

Detailed submetrics should be available in model detail pages, result JSON files, or appendix tables.

Examples:

* element coverage;
* route declaration coverage;
* contrast score;
* typography score;
* task success by task type;
* failure categories;
* latency;
* repeated scoring variance.

## Optional Overall Score

An initial composite score may be:

```text
Overall Score =
0.25 × Static Technical Score
+ 0.25 × Static Visual Score
+ 0.35 × Dynamic Score
+ 0.15 × Efficiency Score
```

This weighting is only an initial proposal. The thesis should also report category-specific rankings because different users may prioritize different properties.

Recommended wording:

```text
The leaderboard reports both category-specific scores and an optional composite score, because different users may prioritize visual quality, functional correctness, or cost efficiency differently.
```

---

# 11. Efficiency and Cost Metrics

The generation should not impose an artificially low output-token cap that causes incomplete UI generation.

Instead:

```text
Do not impose a hard low output-token cap.
Allow models to generate complete outputs.
Record token usage, cost, and latency as efficiency metrics.
```

Recommended efficiency submetrics:

* input tokens;
* output tokens;
* total tokens;
* estimated generation cost;
* evaluation cost;
* generation latency;
* evaluation latency;
* cost-performance ratio.

Important visualization:

* cost vs static technical score;
* cost vs static visual score;
* cost vs dynamic score;
* cost vs overall score;
* Pareto frontier.

---

# 12. Reliability / Bias Audit

Bias should not be the main thesis track for now. It should be treated as a reliability audit of LLM-based scoring.

It can be recorded during experiments and discussed in methodology, results, and threats to validity.

## Recommended Reliability / Bias Records

1. Repeated scoring consistency

   * same GUI scored multiple times.

2. Order-swap sensitivity

   * if pairwise comparisons are used, swap left/right order.

3. Rating-scale sensitivity

   * compare 1–5 vs 1–10 or verbal labels only if feasible.

4. Judge model variance

   * compare scores from different judge models if used.

5. Refusal / invalid output rate

   * how often the judge fails to return valid scores.

This should not dominate the thesis. It supports the reliability of static visual/rubric scoring.

Recommended positioning:

```text
Reliability and bias checks are used to audit the scoring protocol. They are not the primary leaderboard objective.
```

---

# 13. Revised Research Questions

The thesis should use 3 main RQs plus a reliability/bias audit.

## Recommended RQs

```text
RQ1: How can a reproducible benchmark and leaderboard be designed for evaluating LLM-generated web interfaces?

RQ2: How can static technical, static visual, dynamic task-based, and efficiency metrics be operationalized and aggregated for generated web apps?

RQ3: How are static quality scores related to dynamic task-success outcomes in LLM-generated web apps?
```

## Reliability / Bias Audit Question

```text
Reliability Audit: How stable and bias-sensitive are the LLM-based visual/rubric scores used in the evaluation pipeline?
```

Do not make judge bias a large independent chapter unless there is enough time and data.

---

# 14. Recommended Thesis Structure

## Chapter 1 — Introduction

* Motivation
* Problem statement
* Research questions
* Contributions
* Thesis structure

## Chapter 2 — Related Work

* LLM-generated UI
* GUI quality evaluation
* Static and dynamic UI testing
* LLM-as-a-judge
* Reliability and bias issues in automatic judging

## Chapter 3 — Benchmark Design and Methodology

* Benchmark scope
* New LLM leaderboard mode
* Benchmark item schema
* Prompt schema
* Generator model protocol
* Submission artifact format

## Chapter 4 — Evaluation Metrics

* Static technical metrics
* Static visual metrics
* Dynamic task metrics
* Efficiency and cost metrics
* Score aggregation
* Reliability / bias audit protocol

## Chapter 5 — Leaderboard Framework

* Add-new-LLM pipeline
* Generation module
* Rendering and screenshot module
* Scoring modules
* Result storage
* Leaderboard views
* Cost-performance plots

## Chapter 6 — Experiments and Results

* Benchmark tasks
* Generator models
* Static technical results
* Static visual results
* Dynamic results
* Overall leaderboard
* Cost-performance analysis
* Static-dynamic relationship analysis
* Reliability / bias records

## Chapter 7 — Discussion

* What static technical metrics capture
* What static visual metrics capture
* What dynamic metrics capture
* Where static and dynamic diverge
* Limitations
* Real-agent upgrade path
* Threats to validity

## Chapter 8 — Conclusion

* Summary
* Contributions
* Future work

---

# 15. Concrete Repository Tasks for Codex

Please update the repository plan and notes according to this direction.

Recommended files to create or update:

1. `notes/meeting_decision_summary_for_codex.md`

   * save this document.

2. `notes/thesis_outline.md`

   * update thesis direction and RQs;
   * move benchmark/leaderboard to the main RQ;
   * weaken UIClip reproduction / Track A as baseline or sanity check;
   * clarify New LLM leaderboard mode;
   * clarify Static Technical vs Static Visual vs Dynamic.

3. `notes/metric_specification.md`

   * create if missing;
   * define category scores and submetrics;
   * include formulas;
   * include leaderboard columns vs detail-page submetrics;
   * include dynamic metrics compatible with real-agent upgrade.

4. `notes/benchmark_item_schema.md`

   * create if missing;
   * define requirement.md, pages.json, elements.json, tasks.json, validation_rules.json, visual_pages.json, metadata.json;
   * include one example benchmark item.

5. `notes/prompt_schema.md`

   * create if missing;
   * define standardized generator prompt;
   * explicitly state no model-specific prompt tuning.

6. `notes/leaderboard_design.md`

   * create if missing;
   * define leaderboard columns;
   * define model detail page;
   * define cost-performance plots and Pareto frontier.

7. `notes/dynamic_agent_upgrade_plan.md`

   * create if useful;
   * describe lightweight validation first and real-agent upgrade later;
   * emphasize “change executor, not metric schema”.

8. `thesis/chapters/chapter3_methodology.tex`

   * update methodology to reflect the new benchmark and metric design.

9. `thesis/chapters/chapter4*.tex` or equivalent

   * if chapter files exist, ensure evaluation metrics and benchmark construction align with this plan.

Do not implement heavy real-agent execution yet. First update the plan, metrics, schemas, and methodology so the project direction is consistent.
