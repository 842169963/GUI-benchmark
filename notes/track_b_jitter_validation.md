# Track B Visual Judge Jitter Validation (Range-Restriction Check)

Date: 2026-06-10

## Why

All strict+fewshot judges cluster at Pearson r ≈ 0.51–0.60 against the single
human rater. The user hypothesized this is **range restriction**, not judge
incapacity: the dev-subset artifacts all come from one decent model with rich
inputs, so human page scores cluster at 0.875–1.00 and there is little true
variance for r to explain.

Following the UIClip idea (jitter functions injecting known design defects,
arXiv:2404.12500), we built degraded page variants with a **constructed ground
truth ordering** (original > mild > severe), so judge discrimination can be
tested via pairwise ranking accuracy with **zero new human labels**.

## Method

- [scripts/jitter_track_b_pages.py](../scripts/jitter_track_b_pages.py):
  deterministic CSS defect injection (no RNG), defect families per UIClip:
  spacing, layout/alignment, typography, color clash, contrast.
  - `JITTER-MILD-v1`: uneven section padding, slight heading misalignment, one
    undersized heading level, washed-out body text.
  - `JITTER-SEVERE-v1`: chaotic spacing, misaligned/rotated blocks, clashing
    fonts and sizes, clashing section background colors, inconsistent button
    styles, low-contrast text.
- Jittered copies written as sibling run dirs
  (`gwdg_qwen36_35b_v9_smoke_jitter_{mild,severe}`); relative resource paths
  stay valid. Visual check confirmed severe damage is obvious and mild is
  subtle.
- Same standardized screenshot protocol (1440x900, 500 ms wait,
  `capture_track_b_standard_screenshots.js`); 38/38 captured.
- Judges: `gemma-4-31b-it` (free GWDG) and `gpt-4.1-mini` (ChatAnywhere), both
  strict+fewshot — the two freeze candidates. Same 16 evaluation pages as the
  human-comparison study (3 few-shot example pages excluded everywhere, so
  pairs align with existing original-page scores).
- [scripts/compute_jitter_pairwise.py](../scripts/compute_jitter_pairwise.py):
  per-page pairs; correct = better variant scored strictly higher; tie = 0.5.

## Results

| Judge | orig vs severe | mild vs severe | orig vs mild | mean orig / mild / severe |
| --- | ---: | ---: | ---: | --- |
| gemma-4-31b-it | **0.906** (0 wrong, 3 tied) | 0.938 (0 wrong) | **0.281** (7 wrong, 9 tied) | 0.918 / **0.973** / 0.816 |
| gpt-4.1-mini | **0.906** (0 wrong, 3 tied) | 0.875 (0 wrong) | 0.500 (2 wrong, 12 tied) | 0.918 / 0.902 / **0.645** |
| claude-sonnet-4-5 | **0.938** (1 wrong, 0 tied) | 0.938 (1 wrong) | 0.313 (7 wrong, 8 tied) | 0.879 / **0.949** / 0.680 |

Claude addendum (2026-06-10, capping test): on the original 15-page set
claude-sonnet-4-5 strict+fewshot is *negatively* correlated with the single
human rater (Pearson **-0.125**, κ -0.059, agreement 0.812) — it has real
variance and varied confidence but marks *different* pages as weak than the
human did. On the jitter set it is the most decisive severe discriminator
(0.938, zero ties). Two of three judges (gemma, claude) score mild-jittered
pages *higher* than originals, strengthening the suspicion that the mild
ground-truth assumption ("any jitter = worse") is partly wrong, e.g. the even
generous padding may genuinely look fine. The human extended review will
arbitrate.

Outputs: `data/track_b/visual_jitter_validation/jitter_pairwise_*.json`.

## Interpretation

1. **Range-restriction hypothesis supported.** Both judges separate original
   from severe damage with 0.9+ accuracy and zero inversions. The moderate
   r on the original set reflects compressed true variance, not judge
   blindness. This is the key defence of the visual metric for the thesis.
2. **Neither judge reliably detects mild defects.** gpt-4.1-mini mostly ties
   (12/16) — insensitive but not wrong. gemma is **inverted**: it scored mild-
   jittered pages *higher* than originals on 7/16 pages (mild mean 0.973 >
   original 0.918) — a validity failure on subtle differences.
3. **gpt-4.1-mini responds to severity more proportionally** (severe mean
   0.645 vs gemma's 0.816), has no inversion, and also had the higher human
   correlation (r=0.602 vs 0.565). The freeze recommendation therefore shifts
   from free gemma to **gpt-4.1-mini strict+fewshot**, with gemma documented
   as the free fallback.
4. **Caveat on the mild ground truth**: "any jitter = worse" is weakest for
   mild damage (e.g. generous even padding may genuinely look fine), so the
   orig-vs-mild number is a sensitivity indicator, not a strict error rate.
   The severe contrast is the headline evidence.

## Extended human validation result (2026-06-10, evening)

The user annotated all 56 extended pages (19 mild, 19 severe, 18 weak-model;
quasi-blind, per-page default-accept/-reject protocol). Key outcomes
(`data/track_b/visual_jitter_validation/extended_validation_summary.json`):

1. **Mild ground truth refuted by the human rater.** Across 18 page triples the
   human never scored original > mild (0 of 18; 7 ties, 11 mild-higher; subset
   means: mild 0.987 vs original 0.889). The "any jitter = worse" assumption is
   wrong for JITTER-MILD-v1 — its changes (extra padding, softened text) read
   as neutral-to-better. **Consequence: gemma/claude "inversions" on mild were
   human-aligned behavior, not validity failures; the orig-vs-mild pairwise
   accuracies in the table above must NOT be read as error rates.**
2. **Severe ground truth confirmed** (original > severe in 15/18, mild > severe
   in 17/18; severe mean 0.576). Weak-model pages span the real low end
   (mean 0.344).
3. **Range restriction resolved — full-range correlations (62 pages):**

| Judge | Pearson r (full) | κ (item) | agreement | means (human 0.710) | weak-subset r |
| --- | ---: | ---: | ---: | --- | ---: |
| gemma-4-31b-it | **0.694** | 0.294 | 0.753 | 0.858 (lenient) | 0.172 |
| gpt-4.1-mini | 0.615 | **0.360** | 0.744 | **0.738 (calibrated)** | **0.393** |
| claude-sonnet-4-5 | 0.505 | 0.263 | 0.731 | 0.822 | 0.192 |

4. Residual degenerate behavior: on the qwen3-omni weak run gemma scored all
   five pages identically (0.6875) and gpt-4.1-mini scored all five 0.125 —
   uniform output on out-of-distribution broken pages persists for both minis;
   claude kept real variance there.
5. Protocol caveat to report: the extended session used the per-page
   default-accept/-reject buttons while the original session used per-item
   clicks; the mild subset's very high mean may be partly protocol leniency.
   Cross-session comparisons (original vs mild) carry this confound; within-
   session comparisons (mild/severe/weak) do not.

## Three-cause decomposition of the mild result (2026-06-11, user reflection)

The user's own post-hoc review of the original-vs-mild comparison page
identified three co-acting causes for "mild scored >= original", each a
documented measurement phenomenon with citable literature (candidates recorded
here; add to references.bib only when cited in thesis text, per the
cite-only-if-used rule):

1. **Perturbation near the perceptual threshold (JND).** Several mild changes
   (#8a8a8a body text, 14px heading offset at 1440x900) sit near or below the
   just-noticeable difference for the viewing conditions. Candidate refs:
   Weber/Fechner JND (any perception textbook treatment); visual JND surveys
   (e.g. Wu et al., "A Survey of Visual Just Noticeable Difference
   Estimation").
2. **Binary-scale floor effect (granularity).** A yes/no item only flips when
   a defect crosses the "clearly violated" line; sub-threshold defects are
   absorbed. Psychometrics: reliability/validity deteriorate sharply from 3 to
   2 response categories, and finer scales detect subtler differences
   (Preston & Colman 2000, "Optimal number of response categories in rating
   scales"; arXiv:2502.02846 on response categories and measurement error).
   This is the deliberate CheckEval-style tradeoff: binary buys inter-judge
   reliability at the cost of fine-grained sensitivity — acceptable because
   the leaderboard ranks medium-to-large quality gaps.
3. **Rater attention fluctuation / fatigue.** The user reports defaulting to
   All-Yes on pages that looked unchanged; sustained-vigilance degradation in
   annotation is well documented in crowdsourcing human-factors work (e.g.
   Kazai et al., "An analysis of human factors and label accuracy in
   crowdsourcing relevance judgments").

Also recorded: the user *saw* the heading offsets but attributed them to
generation flaws rather than injected perturbation — under the blind protocol
this is correct behavior (rate what is visible regardless of cause), so it is
evidence the protocol worked, not an error.

Status: recorded in notes only; NOT yet in the thesis manuscript. Goes into
the reliability/limitations subsection of the methodology or results chapter
when that section is written, with the citations above added to
references.bib at that point.

## Test-retest stability of the judge (2026-06-11)

Question from the user: should the judge score multiple times and average?
Previous protocol was **one call per page at temperature=0**. Measured
test-retest over 3 repetitions of gpt-4.1-mini strict+fewshot on the 16
original pages (rep1 = today's earlier run, rep2/3 fresh):

- 5/16 pages changed score across reps; mean page-score spread 0.074, max
  **0.4375** (F10 cookbooks: 0.9375 / 0.625 / 0.5); item-level flip rate 9.0%.
- Temperature=0 does NOT make the API deterministic (provider-side MoE
  routing/batching nondeterminism) — the single-run r=0.602 itself fluctuates:
  per-rep r vs human = 0.602 / 0.627 / 0.503; 3-rep item-level majority vote
  r = 0.563.
- **Protocol consequence for the freeze**: the frozen judge config must
  specify **3 repetitions with item-level majority vote** — not because it
  raises mean correlation (it doesn't; it lands mid-pack) but because it
  shrinks the run-to-run variance of every reported score and removes
  single-run luck from model rankings. Cost: 3x judge calls, still cents per
  artifact.
- Distinction recorded: repetition reduces *variance* only; systematic bias
  (yes-bias, leniency) is addressed by the strict+fewshot calibration, and
  judge-ensemble panels (PoLL-style) remain future work.
- Reliability-audit field "repeated scoring consistency" is now filled with
  measured data. Files: `llm_judge_gpt-4.1-mini_strict_fewshot_rep{1,2,3}.json`.

### Per-page/per-item breakdown of the instability (recordable bias patterns)

- **All 5 unstable pages are F10_gourmania pages** (scores in the 0.4–0.9
  band); every F01/F03 page (clearly good, scores ~1.0) was identical across
  all 3 reps. The judge's variance is **heteroscedastic**: near-zero on clear
  pages, large on borderline pages. Consequence: single-run scores are least
  trustworthy exactly where leaderboard rankings are contested — which is the
  argument for the 3-rep majority protocol.
- **Minority-vote direction skews lenient**: of 23 flipped (page,item) cells,
  16 resolve to false under majority vote — the stray run tends to be the one
  saying *true*. Residual yes-bias resurfaces as occasional lenient slips
  under uncertainty; majority voting filters it.
- **Noise items vs bias items**: T4 font-consistency flips most (4 pages),
  then L1/C1/C4 (3 each) — these are judgment-call items on borderline pages
  (noise). L4 spacing-consistency never flips yet systematically disagrees
  with the human — that is stable miscalibration (bias), not noise. The audit
  can therefore separate which checklist items need wording fixes (L4) from
  which just need vote aggregation (T4).

## Status / next

- Judge freeze decision: evidence now favors `gpt-4.1-mini` strict+fewshot;
  awaiting user confirmation.
- After freeze: copy LB-JUDGE-v1 base/strict/fewshot prompts verbatim into
  `thesis/appendices/prompt_templates.tex`; wire the frozen judge into the
  leaderboard pipeline; then implement Technical coverage submetrics.
- The jitter tooling is reusable for calibrating few-shot anchors without
  human labels (future option).
