# Track B Generation Prompt Freeze Policy

Date: 2026-06-05

## Why this note exists

The Track B generation prompt churned from `TB-GEN-v1` through `v16` because
every gate failure was treated as a prompt-wording problem. Each tightening
fixed one item and regressed another (see
[track_b_v15_small_batch_experiment.md](track_b_v15_small_batch_experiment.md)
and [track_b_v16_input_compression.md](track_b_v16_input_compression.md)). This
note fixes the governance so the prompt can stop moving.

## Root-cause separation (do not fix all three by editing the prompt)

Track B failures fall into three classes with different fixes:

1. **Capacity / truncation** (F03 context overflow; F06/F09 `finish_reason=length`).
   Fix via input budget (compact input profile) and provider-specific output-budget
   policy. For OpenAI-compatible providers, prefer omitting `max_tokens` when the
   provider accepts it; if a provider requires a cap, use a documented setting
   high enough for complete outputs where feasible. **Never change prompt wording
   to fix truncation.**
2. **Instruction-following floor** (a weak model ignores or paraphrases a
   control). This is a *model* property and is a legitimate leaderboard result,
   not a prompt bug.
3. **Exact-string reproduction** (destination heading/evidence text). This was an
   over-strict *gate* requirement, now relaxed (see below), not a prompt problem.

## Gate change (2026-06-05): static gate is structural, dynamic check is authority

`scripts/check_track_b_generation.py` previously hard-failed (`error`) artifacts
whose `<a>/<button>` text did not *exactly* reproduce each workflow label
(`workflow_clickable_labels_present`, `workflow_clickables_not_inert`). That is
what forced the prompt to micromanage exact strings and caused the
`GitLab Duo` / `View Recipe` reversals.

Changed so that:

- Those two checks are now **warnings**, not errors.
- Matching is **normalized + bidirectional containment** (tolerates case,
  whitespace, punctuation, and trailing affordance glyphs), via
  `normalize_label()` / `label_matches_clickable()`.
- The **hard gate now only blocks on structural/capacity failures**: incomplete
  document, unclosed body/style/script (truncation), `finish_reason in {length,
  max_tokens}`, undefined onclick functions, and workflow `showPage` routes
  without matching section ids.

Authority for "does the workflow control actually route and reach the right
content" moves to the **dynamic browser workflow check**
(`scripts/run_track_b_browser_workflow.js`), which already does semantic route
matching and produces the route/content/task scores used by the leaderboard.

Rationale: a benchmark must measure **task completion**, not **verbatim string
reproduction**. Exact-text gating destroyed leaderboard discriminative power and
drove the prompt churn.

### Regression evidence (relaxed gate, same artifacts)

| Item / run | Before | After | Note |
| --- | --- | --- | --- |
| F03 `gwdg_qwen36_35b_v16_f03_compact_smoke` | fail (exact `GitLab Duo`) | **pass**, 1 warning | exact-label failure → warning |
| F10 `gwdg_qwen3_omni_30b_v15_f10_smoke` | pass | pass, 2 warnings | unchanged good case |
| F09 `gwdg_qwen3_omni_30b_v15_f09_smoke` | fail | **fail** (truncation only) | real capacity failure still blocked |
| F06 `gwdg_qwen3_omni_30b_v15_f06_smoke` | fail | **fail** (truncation only) | real capacity failure still blocked |

Backup: `archive/backup/check_track_b_generation_2026-06-05_before-gate-relaxation.py`.

## Freeze criterion (when to stop editing the prompt)

The generation prompt is **frozen as the leaderboard baseline** when, on the
development subset **F01 / F03 / F10**, all of the following hold:

1. **>=2 reference models** each produce a *complete, non-truncated* artifact
   that passes the relaxed static gate (errors = 0).
2. Every remaining gate **warning** is attributable to **model capability or a
   benign cosmetic difference**, not to prompt ambiguity (i.e., a careful human
   reading the prompt would produce a passing control).
3. The compact input profile keeps every dev-subset item under the smallest
   reference model's context limit.

Once met, that prompt id becomes the frozen baseline. **After freezing, all
further variation is recorded as model variation, not patched into the prompt.**
A genuinely new finding spawns a new versioned prompt id (`TB-GEN-v17`, ...) with
its own appendix entry and its own batch run — never a silent edit to the frozen
baseline.

## Anti-overfitting rules

- **Never tune the prompt to pass a single item.** v15 was overfit to F10 and did
  not generalize. Judge a prompt only by aggregate dev-subset behavior.
- **One change per version.** Do not bundle capacity, control-contract, and
  visual-grounding changes in one prompt revision; you lose the ability to
  attribute which change helped.
- **Record, do not patch.** A weak model failing the gate is a leaderboard data
  point. Patching the prompt until it passes contaminates the benchmark.

## Status

- Gate relaxation: **done** (2026-06-05).
- Freeze decision: **pending** a `TB-GEN-v16` (or successor) dev-subset batch
  re-scored under the relaxed gate. The F03 evidence above suggests v16 may now
  clear criterion 1 for F03; F01 and F10 still need a clean re-run before
  freezing.
