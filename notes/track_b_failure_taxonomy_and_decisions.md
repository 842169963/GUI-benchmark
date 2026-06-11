# Track B Failure Taxonomy and Decisions

Date: 2026-06-10

## Purpose

This note turns the repeated Track B debugging issues into explicit benchmark
failure categories and experiment decisions. The goal is to stop treating every
failed generated page as a prompt bug. Some failures are legitimate model or
provider outcomes and should be recorded by the leaderboard instead of patched
away.

## Current Scope Decision

Track B remains a fixed-item benchmark for generated executable web interfaces.
The benchmark asks each generator model to produce an `index.html` artifact for
the same item context and evaluates the result with the same checks.

The benchmark is not an open-ended UI repair system. It should not keep changing
the prompt until every model passes every item.

## Failure Categories

### F0: Provider Failure

Definition:

- The provider call fails before a usable artifact is written.
- Examples: HTTP 500, HTTP 503, timeout, unsupported model, context-length
  rejection before generation.

Leaderboard handling:

- Count as an attempted item.
- Record `provider_failure_count`.
- No static/dynamic score is computed because no artifact exists.

Examples already observed:

| Case | Prompt | Model/provider | Evidence | Decision |
| --- | --- | --- | --- | --- |
| F09 repeated GWDG HTTP 500 | `TB-GEN-v9` | GWDG `qwen3.6-35b-a3b` | revision log 2026-05-27 | Provider-level failure, not UI-quality failure. |
| F02 read timeout | `TB-GEN-v9` | GWDG `qwen3.6-35b-a3b` | `notes/track_b_benchmark_protocol.md` | Provider-level failure. |
| F03 context overflow | `TB-GEN-v15` | GWDG `qwen3-omni-30b-a3b-instruct` | `notes/track_b_v15_small_batch_experiment.md` | Capacity/context failure; fixed by compact input, not by item-specific prompt tuning. |

### F1: Completion / Truncation Failure

Definition:

- A generated artifact exists, but it is incomplete or structurally truncated.
- Typical evidence: `finish_reason=length`, missing `</body></html>`, unclosed
  `<style>` or `<script>`, incomplete route script, or static gate truncation
  errors.

Leaderboard handling:

- Count as an attempted item and generated artifact.
- Exclude from eligible dynamic/visual scoring if the static technical gate
  fails.
- Record `truncation_failure_count` and completion-token metadata.

Examples already observed:

| Case | Prompt | Model/provider | Evidence | Decision |
| --- | --- | --- | --- | --- |
| F06/F09 v15 | `TB-GEN-v15` | GWDG `qwen3-omni-30b-a3b-instruct` | `notes/track_b_v15_small_batch_experiment.md` | v15 is not a general prompt; do not freeze it. |
| F01 v16, 20k cap | `TB-GEN-v16` | GWDG `qwen3-omni-30b-a3b-instruct` | `gwdg_qwen3_omni_30b_v16_f01_dev` | 20k-capped sensitivity result only. |
| F01 v16, no `max_tokens` | `TB-GEN-v16` | GWDG `qwen3-omni-30b-a3b-instruct` | `gwdg_qwen3_omni_30b_v16_f01_dev_omit_maxtokens` | Still incomplete after 41,740 completion tokens; record as model/provider completion failure on F01. |
| F10 v16, 20k cap | `TB-GEN-v16` | GWDG `qwen3-omni-30b-a3b-instruct` | `gwdg_qwen3_omni_30b_v16_f10_dev` | Previous failure was cap-sensitive. |
| F10 v16, no `max_tokens` | `TB-GEN-v16` | GWDG `qwen3-omni-30b-a3b-instruct` | `gwdg_qwen3_omni_30b_v16_f10_dev_omit_maxtokens` | Completes and passes static gate; use omitted max-token policy for future OpenAI-compatible runs. |

### F2: Static Technical Gate Failure

Definition:

- The artifact is complete, but the static gate finds structural defects that
  make downstream scoring unreliable.
- Examples: undefined `onclick` handler, workflow route id missing, broken route
  script.

Leaderboard handling:

- Count as attempted and generated.
- Not eligible for final dynamic/visual scoring unless the failure is explicitly
  downgraded to a warning by a documented gate-policy change.

Examples already observed:

| Case | Prompt | Model/provider | Evidence | Decision |
| --- | --- | --- | --- | --- |
| F05 v9 undefined `toggle()` | `TB-GEN-v9` | GWDG `qwen3.6-35b-a3b` | `notes/track_b_benchmark_protocol.md` | Static technical failure. |
| Earlier exact-label failures | v8-v15 variants | mixed | `notes/track_b_prompt_freeze_policy.md` | Exact visible-label matching was over-strict; now warning, not hard error. |

### F3: Dynamic Route Failure

Definition:

- The artifact passes the static gate, but browser workflow actions do not reach
  the expected route or section.

Leaderboard handling:

- Eligible artifact.
- Route failure lowers `route_success_rate` and task success.

Examples already observed:

| Case | Prompt | Model/provider | Evidence | Decision |
| --- | --- | --- | --- | --- |
| F03 v16 qwen3-omni GitLab Duo route | `TB-GEN-v16` | GWDG `qwen3-omni-30b-a3b-instruct` | `notes/track_b_v16_input_compression.md` | Dynamic route limitation; record in route score. |
| F10 v16 qwen3-omni no `max_tokens` | `TB-GEN-v16` | GWDG `qwen3-omni-30b-a3b-instruct` | `browser_workflow_normalized_report.json` | Static-valid artifact, but route score remains 0.750. |

### F4: Content Validation Failure

Definition:

- The workflow reaches the expected route, but the destination lacks required
  visible evidence from `workflow.json` validations.

Leaderboard handling:

- Eligible artifact.
- Content failure lowers `content_validation_success_rate` and task success.
- This is a normal generated-UI quality result, not a provider failure.

Examples already observed:

| Case | Prompt | Model/provider | Evidence | Decision |
| --- | --- | --- | --- | --- |
| F01 v16 qwen3.6 | `TB-GEN-v16` | GWDG `qwen3.6-35b-a3b` | 7/12 workflow cases, route 1.000, content 0.583 | Eligible but content evidence incomplete. |
| F03 v16 qwen3.6 | `TB-GEN-v16` | GWDG `qwen3.6-35b-a3b` | 4/8 workflow cases, route 1.000, content 0.500 | Eligible but content evidence incomplete. |
| F10 v16 qwen3.6 | `TB-GEN-v16` | GWDG `qwen3.6-35b-a3b` | 6/8 workflow cases, route 1.000, content 0.750 | Eligible but not perfect. |

## Why the Repeated Experiments Did Not "Solve" F01

The repeated experiments uncovered different root causes, not one single bug:

1. Early prompts mixed visual fidelity, route contracts, exact click labels, and
   content evidence in one instruction, so each prompt revision fixed one item
   and regressed another.
2. The old static gate over-treated semantic targets as exact labels, which
   pushed prompt changes toward brittle wording instead of measuring workflow
   success. This has now been corrected.
3. Some failures were context/input-size failures. Compact input fixed the F03
   qwen3-omni context overflow.
4. Some failures were output-budget failures. F10 qwen3-omni v16 passed after
   omitting `max_tokens`.
5. F01 qwen3-omni remains a completion/truncation failure even after omitting
   `max_tokens`, reaching 41,740 completion tokens without a complete document.
   This is now evidence of model/provider instability for that item under the
   current fixed prompt, not an unresolved prompt bug.

The benchmark should report this. It should not keep tuning the prompt to make
one model pass one item.

## Current Demo Status

A small demo already exists, but it is not yet the final public-facing demo.

Implemented:

- generated HTML artifact folders
- static technical gate reports
- browser workflow reports
- mini leaderboard aggregation script
- model-level JSON/Markdown leaderboard outputs

Existing demo note:

- `notes/track_b_mini_leaderboard_demo.md`

Existing demo outputs:

- `data/track_b/leaderboard/model_leaderboard_all.md`
- `data/track_b/leaderboard/model_leaderboard_tb_gen_v9.md`
- `data/track_b/leaderboard/model_leaderboard_tb_gen_v15.md`

Why it still feels unfinished:

- The fair same-prompt leaderboard had only one strong eligible model row.
- Visual and efficiency scores are still pending or partially frozen.
- Failure counts are not yet surfaced clearly in the Markdown leaderboard, so
  failed attempts feel like debugging debris rather than benchmark results.

## Convergence Plan

### Step 1: Stop Prompt Tuning for F01/qwen3-omni

Decision:

- Do not create a new prompt only to make qwen3-omni pass F01.
- Record F01/qwen3-omni as an F1 completion/truncation failure.

Reason:

- The no-`max_tokens` rerun already tests the main output-cap hypothesis.
- Further item-specific tuning would overfit the prompt and weaken the
  benchmark's model-comparison validity.

### Step 2: Freeze Evaluation Handling Before More Generation

Required change:

- Update leaderboard aggregation so attempted items, generated artifacts,
  provider failures, truncation failures, static-gate pass rate, route score,
  and content score are visible in one table.

Reason:

- This turns failed model runs into readable benchmark outcomes.
- It also creates the small demo that is currently missing: a table showing not
  only scores, but why some artifacts are ineligible.

### Step 3: Build a Minimal Demo Around Existing Runs

Recommended demo scope:

- Items: `F01`, `F03`, `F10`
- Prompt: `TB-GEN-v16`
- Models/configs:
  - `qwen3.6-35b-a3b`
  - `qwen3-omni-30b-a3b-instruct`

Expected demo message:

- qwen3.6 completes all three dev items and enters scoring.
- qwen3-omni completes F03 and F10 without client-side `max_tokens`, but still
  fails F01 by truncation/completion.
- The leaderboard can represent this as attempted/completed/gated/dynamic
  outcomes instead of hiding it.

Reason:

- This is enough for a small, defensible demo.
- It demonstrates the benchmark pipeline and a meaningful failure taxonomy
  without requiring a perfect multi-model ranking.

### Step 4: Only Then Choose Whether to Add a Second Strong Model

Options:

- Add one paid/proxy model for the same F01/F03/F10 v16 subset.
- Or keep the demo as qwen3.6 vs qwen3-omni and frame it as a pipeline/failure
  taxonomy demo, not a final leaderboard.

Decision rule:

- If the thesis needs a real ranking table, add one stronger second model.
- If the immediate need is supervisor progress/demo, do not spend more time on
  generation. Improve the leaderboard table and screenshots instead.

## Immediate Demo Artifact

Status: implemented on 2026-06-10.

Generated files:

- `data/track_b/leaderboard/dev_subset_v16_failure_demo.json`
- `data/track_b/leaderboard/dev_subset_v16_failure_demo.md`

The demo table uses existing v16 F01/F03/F06/F10 artifacts and reports:

- attempted items
- generated artifacts
- truncation failures
- static-gate pass count
- eligible artifacts
- average route success
- average content success
- artifact-level failure category

This is the current meeting-ready benchmark + leaderboard pipeline demo.

## Next Engineering Task

Implement the minimal demo table:

- Extend `scripts/build_track_b_mini_leaderboard.py` or create a narrow
  `scripts/build_track_b_failure_demo.py`.
- Input: existing v16 F01/F03/F10 run folders.
- Output:
  - `data/track_b/leaderboard/dev_subset_v16_failure_demo.json`
  - `data/track_b/leaderboard/dev_subset_v16_failure_demo.md`
- Columns:
  - model/config
  - attempted items
  - generated artifacts
  - provider failures
  - truncation failures
  - static-gate pass count
  - eligible artifacts
  - average route success
- average content success
- note

This is now implemented by `scripts/build_track_b_dev_subset_demo.py`. The next
engineering step is to merge this failure accounting into the general
leaderboard builder so future larger batches get the same visibility.
