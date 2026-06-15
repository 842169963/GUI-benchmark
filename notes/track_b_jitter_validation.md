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

## Inter-rater reliability and judge certification (2026-06-11)

**CORRECTION (2026-06-12)**: what was first recorded as "one friend in two
browser sessions" was actually **two different independent raters** (user
clarification): friend A rated pages 1–28, friend B rated pages 29–56, both
blind to variants. The pooled "rater2" numbers below remain valid as
"author vs an independent rater" aggregates, but the per-pair split (added
below) is the methodologically correct view and is what the thesis should
report. The study therefore has **three raters and two valid human pairs**
(A-B overlap is only 2 pages — unusable).

A second, independent rater (friend of the author; blind to which pages were
jittered/weak; same 56-page extended set, same per-page default-then-correct
protocol) completed the review in two browser sessions; exports merged by
[scripts/compute_interrater.py](../scripts/compute_interrater.py) (2
conflicting duplicate pages kept first-session answers; 2 pages have one
missing item each). Results
(`data/track_b/visual_jitter_validation/interrater_summary.json`):

**Human-human ceiling (rater1 vs rater2, 56 pages / 894 item cells):**
item agreement 0.697, **Cohen's κ = 0.317**, page-score Pearson 0.521.
Binary visual-aesthetic judgments have genuinely low human consensus — the
"low" absolute κ of the judges is a property of the task, not a judge defect.

**Judges vs each rater (same extended pages, n=47):**

| Judge | κ vs rater1 | κ vs rater2 | r vs rater1 | r vs rater2 |
| --- | ---: | ---: | ---: | ---: |
| gpt-4.1-mini | **0.350** | **0.334** | 0.560 | 0.531 |
| gemma-4-31b | 0.293 | 0.221 | 0.695 | 0.374 |
| claude-sonnet-4-5 | 0.286 | 0.194 | 0.534 | 0.289 |

**Certification (Judge's Verdict two-step, arXiv:2510.09738):**
gpt-4.1-mini strict+fewshot passes both steps: (1) correlation filter
(full-range r=0.615 vs rater1); (2) human-likeness — its κ with EACH rater
(0.350/0.334) meets or exceeds the human-human κ (0.317), and symmetrically so.
gemma and claude sit below the ceiling and are asymmetric (they idiosyncratically
track rater1, suggesting overlap with the few-shot anchors' author rather than
general human perception). **gpt-4.1-mini is at the human ceiling — the freeze
is now literature-standard certified, not just pilot-grade.**

**Per-pair split (3 raters, 2026-06-12):**

| Pair | κ | r (page score) | n pages | note |
| --- | ---: | ---: | ---: | --- |
| author vs friend A | 0.294 | 0.629 | 30 | A lenient: mean 0.808 vs author 0.650 |
| author vs friend B | 0.324 | 0.499 | 28 | means 0.598 vs 0.625 |
| friend A vs friend B | n/a | n/a | 2 | overlap too small |

Human-pair κ range: **0.294–0.324** (mean ≈0.31). Judges per pair:

| Judge | vs author | vs friend A | vs friend B | mean |
| --- | ---: | ---: | ---: | ---: |
| gpt-4.1-mini | 0.350 | 0.251 | **0.426** | **0.342** |
| gemma-4-31b | 0.293 | 0.228 | 0.216 | 0.246 |
| claude-sonnet-4-5 | 0.286 | 0.264 | 0.177 | 0.242 |

Refined certification: gpt-4.1-mini's three judge-human agreements straddle
the human-pair range with mean 0.342 ≥ human mean 0.309 — within/above the
human distribution (the closest small-n approximation of Judge's Verdict's
z-score test). gemma and claude sit consistently below the human mean.
Certification conclusion unchanged, now grounded in two human pairs instead
of one.

Additional findings:

- **Mild refutation replicated**: rater2's mild mean 0.957 (rater1 0.987) —
  both humans see mild-jittered pages as near-perfect.
- **Reference-knowledge effect on weak pages**: rater1 (author, knows the
  prototypes) scored weak-model pages 0.344; rater2 (naive) scored them 0.686.
  Knowing what the page SHOULD look like halves the perceived quality of weak
  artifacts. Implication for the protocol: the production judge sees only the
  screenshot (naive condition); record that human-validation raters' framing
  (with/without reference) materially shifts absolute scores, though ordering
  (mild > severe > ... within rater) is preserved.

## Per-item inter-rater breakdown and anchor-sensitivity check (2026-06-11)

Per-item human-human agreement (rater1 vs rater2, 56 pages) answers the user's
checklist-ambiguity concern with a twist:

- The items the user suspected as overlapping (C1/C4, O4/L1) are indeed
  **redundant within a rater** (rater1 gives identical answers on C1==C4 86%,
  O4==L1 89% of pages) but are among the **highest** inter-rater items
  (C1 κ=0.591 — best in set; C4 0.416; L1 0.409). Redundancy is benign for the
  aggregate (adds reliability, survey-style).
- The genuinely problematic items are **T1 (text hierarchy, κ=0.065)** and
  **T3 (line length, κ=0.072)** — near-zero human consensus; O1 (0.179) and
  T4 (0.211) also weak. Typography judgments lack a shared standard between
  raters. Per freeze discipline these are documented now and earmarked for a
  fully re-validated LB-JUDGE-v2 (e.g. T3 → countable "body lines exceed ~100
  characters"), NOT patched into the frozen v1.

Anchor-sensitivity experiment (does swapping the 3 few-shot anchor pages move
the judge?): `--anchor-set alt` added to run_visual_judge.py (picks
lowest/median/highest non-default pages from the rater1 original review →
F10 tips 0.69 / F01 company 0.94 / F10 cookbooks 1.0; note narrower quality
span than default 0.50–1.0 because no other truly-bad original page exists).
First run blocked by ChatAnywhere balance exhaustion (403 on 4-image few-shot
payloads after ~250 vision calls); completed 2026-06-12 via the user's new
`tuzi` provider key (api.tu-zi.com, OpenAI-compatible).

### Anchor-sensitivity result (2026-06-12): the bad exemplar is load-bearing

- **Alt anchors (no truly-bad example, span 0.69–1.0)**: gpt-4.1-mini
  collapses back to yes-bias — 15/16 pages scored 1.0, one 0.875, ≈zero
  variance.
- **Provider control (default anchors, same tuzi provider)**: variance
  preserved (F10 pages 0.69–0.94, F01/F03 ≈1.0) — same qualitative shape as
  the certified ChatAnywhere runs, though somewhat more lenient on F10
  (within/near the measured run-to-run noise band).
- **Attribution**: same provider + same prompt, only anchors differ → the
  collapse is caused by the anchor change. The few-shot calibration's active
  ingredient is almost entirely the single LOW-quality exemplar (F10 homepage,
  human 0.50, many false golds) demonstrating that answering false is
  expected. The strict wording alone does not sustain criticism.
- **Frozen-config consequence**: the anchor set is a load-bearing part of the
  judge configuration. Hard requirement recorded: **anchors must include at
  least one genuinely low-scoring page with substantial false gold answers**.
  Anchor pages and their gold labels are frozen alongside model/prompt/reps.
- Secondary flag: provider identity matters too (tuzi default-anchor run is
  lenient-shifted vs ChatAnywhere) — switching API provider for the same
  model name requires revalidation before formal batches.
- Untested variant (future work): equally-spanning but different anchors
  (e.g. a human-labelled weak-model page as the bad exemplar) to separate
  "needs a bad example" from "needs THIS bad example".

### Consensus-anchor follow-up (2026-06-12): gradient, not just a bad example

Built `--anchor-set consensus`: anchors drawn from the 56 double-labelled
extended pages where author and the independent rater agree on >=13/16 items;
golds = author answers. First implementation picked low/median/high by LIST
INDEX and collapsed the judge back to all-1.0 yes-bias — because the
consensus-eligible pool skews high (14 of 25 pages = 1.0), so the index-median
anchor was itself 1.0, leaving no partial-failure exemplar (anchors
0.125/1.0/1.0). Fixed to pick by TARGET SCORE BAND (≈0.15 / ≈0.60 / 1.0,
preferring highest inter-rater agreement within band) → anchors
0.125 (internvl tips) / 0.625 (jitter-severe pricing) / 1.0 (academy).
With the graded set, variance is restored (gpt-4.1-mini originals: min 0.25,
max 1.0, not collapsed). **Refined rule: the anchor set needs a graded
low/genuine-mid/high triple; a single catastrophic example is insufficient —
the middle partial-failure exemplar carries the calibration.** The broken
index-median selection is recorded as a cautionary result.

Provider caveat reconfirmed: on tuzi the consensus run is more lenient than the
ChatAnywhere certified runs (most originals 1.0 vs ChatAnywhere's spread) — the
lenient shift is a tuzi provider effect, independent of anchors. Also tuzi
**hung for ~2h** on the full 2-model x 6-run sweep (sustained image load),
completing only 2 of 12 runs before the process died. Provider reliability +
the lenient shift mean the production provider/anchor set must be re-certified
together before the formal batch. (Stale broken-gradient file
`llm_judge_gpt-4.1-mini_strict_fewshot_consensusanchor_jitter_mild.json` from
the first sweep should be regenerated.)
- Files: `llm_judge_gpt-4.1-mini_strict_fewshot_altanchor.json`,
  `llm_judge_gpt-4.1-mini_strict_fewshot_tuzi_control.json` (canonical file
  restored from the certified ChatAnywhere rep1).

## Consolidated reliability findings (for thesis Reliability/Limitations section)

This subsection gathers the visual-judge reliability results into the form the
thesis should cite. All are recorded findings, NOT yet written into the
manuscript; citations go to references.bib only when used (cite-only-if-used).

### F1. Yes-bias is the default failure mode of MLLM visual judges

With a plain checklist prompt, every vision model tested — 4 free GWDG models
(internvl3.5-30b, qwen3-omni-30b, gemma-4-31b, medgemma) AND paid gpt-4o-mini —
answered TRUE on all 16 items for all pages: mean 1.000, zero variance. The
bias is universal across model family and price tier, not a weak-model artifact.
A strict fault-finding prompt removes the all-true symptom but, alone, gives
agreement uncorrelated with humans (gemma r=-0.18); gpt-4o-mini under strict
shows a subtler degenerate mode (mechanically one false per page, score fixed
at 0.9375, still zero discriminative variance). Reproduces the WebDevJudge /
MLLM-as-UI-Judge cautions; validates the mandatory human-correlation check.
**This is the headline reliability result and must be reported.**

### F2. The active calibration ingredient is a GRADED anchor set

Few-shot calibration, not prompt wording or model scale, is what aligns the
judge — and within few-shot, the load-bearing part is anchor *coverage of the
quality range*. Two independent collapse experiments prove it: (a) removing the
low exemplar (alt anchors, span 0.69–1.0) → yes-bias returns (15/16 pages 1.0);
(b) an anchor triple with no genuine middle (0.125/1.0/1.0 from an index-median
selection bug) → also collapses. A graded low/mid/high triple restores variance.
This matches the LLM-judge calibration literature: provide "examples of low,
medium, and high-quality responses and their corresponding scores"
([Evidently AI LLM-judge guide]; [LangChain LLM-as-judge]), and ICL
coverage-based demonstration selection (arXiv:2305.14907). Anchor selection
rule adopted: pick by target score band (≈0.15 / ≈0.60 / 1.0), prefer
highest inter-rater agreement for reliable golds; minimum 3 (one per band),
optionally 2/band if re-validating. Anchors + gold labels + order are frozen
as part of the judge config (order sensitivity: Lu et al., Fantastically
Ordered Prompts).

### F3. Anchor set vs validation set are distinct (sizes both satisfied)

Few-shot anchors (3, in-prompt, excluded from scoring) are separate from the
human-labelled validation set used to measure agreement (literature: 30–50
expert-annotated examples). Our 56-page extended set satisfies the validation-
set guidance; the 3 anchors are disjoint from it.

### F4. κ is acutely range-dependent — always report it on a spanning set

The SAME judge gives κ≈0.10 on the original-19 set (all good pages, base-rate
inflation) but κ≈0.34–0.42 on the full extended range. A low κ measured on a
homogeneous set is a measurement-window artifact, not judge incapacity. Any
reported κ must state the score distribution of the set it was computed on.

### F5. Open / future-work items (do NOT patch into frozen v1)

- T1 (text hierarchy) and T3 (line length) have near-zero human-human κ
  (0.065 / 0.072): no shared human standard → reword for LB-JUDGE-v2.
- Consensus (two-rater-gold) anchors are methodologically cleaner than the
  certified single-rater default anchors but are NOT yet validated at full
  range; adopting them requires one full-range re-validation, then freeze.
  Risk to avoid: repeated re-tuning on the same 56-page set = validation-set
  overfitting. Freeze discipline applies to the judge as it does to the
  generation prompt.
- Provider identity shifts absolute scores (tuzi lenient vs ChatAnywhere);
  certified config is default-anchors on ChatAnywhere. Switching provider
  requires re-validation.
- gpt-5-mini is better calibrated (less saturation, mean nearer human) but
  ~6x slower (reasoning model, ~25 s/page) → impractical for large formal
  batches; a cost/latency-vs-quality datapoint, not a freeze candidate.

### Adjudicated-consensus anchor test (2026-06-12) — author-gold RETAINED

Addressing the user's valid critique ("why are the author's labels the gold?"),
we built an adjudicated-consensus anchor set: 3 graded consensus pages (low
F10/05_tips, mid F03/06_pricing severe, high F01/02_academy mild) whose
disagreeing items were resolved by author+friend adjudication (5 items total;
golds → anchor scores 0.0625 / 0.625 / 1.0). Re-validated full-range on
ChatAnywhere vs both raters, head-to-head on the SAME 45 pages:

| Anchor gold | κ vs author | κ vs friend |
| --- | ---: | ---: |
| author-gold (certified default 0.50/0.75/1.0) | **0.353** | **0.340** |
| adjudicated-consensus (0.0625/0.625/1.0) | 0.306 | 0.281 |

Adjudicated is consistently LOWER → by the pre-registered rule (adopt only if
≥ author-gold) the **certified author-gold default anchors are RETAINED and
frozen**. Interpretation: the adjudicated low exemplar (0.0625, a genuinely
terrible weak-model page) is too harsh and over-corrects the judge toward
severity, slightly reducing human agreement; the moderate 0.50 low anchor
calibrates better. Net: single-rater-gold is documented as a limitation, but
empirically a consensus alternative did NOT improve agreement — so author-gold
is retained on evidence, not convenience. Files:
`llm_judge_gpt-4.1-mini_strict_fewshot_adjudicatedanchor_*.json`;
adjudication sheet `anchor_adjudication_sheet.md`.

### Controlled add-one-low-anchor test (2026-06-12) — full-range coverage REFUTED cleanly

The adjudicated test above was confounded (3 changes at once, possibly within
noise). To isolate the user's "cover the full score range with a low anchor"
hypothesis, ran a single-variable controlled test: certified 3 anchors
(0.50/0.75/1.0) UNCHANGED vs the same 3 PLUS one ~0.25 low anchor
(F01/05_digital_cards jitter_severe, author gold), everything else identical,
both fresh in the same session (noise-matched). Same 46 pages:

| Config | κ vs author | κ vs friend |
| --- | ---: | ---: |
| control: 3 anchors (0.50/0.75/1.0) | 0.329 | 0.299 |
| treatment: 4 anchors (+0.25 low) | 0.228 | 0.198 |

Adding the low anchor LOWERS κ by ~0.10 on both raters — beyond the ±0.05
run-to-run noise band, consistent across raters → a real effect, not noise.
The control reproduces the original certification (0.329 vs orig 0.349 vs
author, within noise), confirming the treatment drop is genuine.

**Conclusion (clean controlled experiment): adding this low anchor HURTS
agreement — verified, but mechanism corrected.** Full 2×2 contingency
(judge×author, N=736 item cells): control [383/122/97/134] κ=0.3288; treatment
[416/169/64/87] κ=0.2284 — reproduced by two independent code paths
(pairwise and contingency-table marginals); raw tables are auditable with any
kappa calculator.

**Mechanism correction (found while verifying the data, 2026-06-12):** an
earlier note claimed the harsh low anchor "over-corrects toward severity." The
contingency table REFUTES this — the 4-anchor judge said Yes MORE often (585 vs
505), i.e. it became more LENIENT, and the κ drop comes from extra judge-Yes /
human-No disagreements (122→169). Why adding a low (bad-page) exemplar makes
the judge more lenient is NOT explained by a single run; the robust, verified
claim is only "adding this anchor lowered κ by ~0.10 (> ±0.05 noise)", and the
mechanistic story is withdrawn. (Same caveat applies to the adjudicated-replace
result above: its "0.0625 over-corrects" rationale is likewise not supported and
should be read as "lowered κ", mechanism unknown.)

**The certified 3-anchor set (0.50/0.75/1.0, author gold) is retained and the
freeze is FINAL.** Thesis-usable: "wider anchor coverage was tested in a
single-variable controlled experiment and significantly reduced human
agreement (Δκ≈−0.10 > noise); a compact 3-anchor calibration is used."
Files: `llm_judge_..._default_lowaddanchor_*.json`, `..._ctrl2.json`.

### F6. Self-preference bias — planned sensitivity check (post-leaderboard)

The frozen judge is gpt-4.1-mini (GPT family); the leaderboard's contestant
generators include GPT-family models, so there is a theoretical self-preference
risk (a judge favouring its own family's outputs). Planned reliability step,
run AFTER the formal leaderboard exists (needs real cross-family contestant
artifacts):

- Re-judge the GPT-family contestants' artifacts (or a subset) with a
  DIFFERENT-family judge (free gemma now; Gemini if a key becomes available)
  and check whether the GPT contestants' RANKING shifts systematically.
- Stable ranking → self-preference not material → report "checked, no material
  effect". Systematic drop of GPT contestants under the cross-family judge →
  bias is real → mitigate (panel / adjust).
- The contrast judge does NOT need to pass the human-ceiling certification: it
  is used only as a cross-family ranking contrast, not as ground truth (lower
  bar than a production judge).
- Prior expectation: effect likely small because the judge sees rendered
  SCREENSHOTS, which carry a weak self-recognition signal vs text generation —
  but verify, do not assume.

### F7. Dual-judge / panel (PoLL) — future work

Averaging a cross-family panel (e.g. GPT + Gemini) would reduce single-family
bias and per-model variance, BUT is not a free add-on: (1) every panel member
must individually pass the human-ceiling certification (gemma/claude failed it;
Gemini untested and no key yet), else averaging a below-ceiling judge drags the
panel's human-agreement DOWN; (2) the averaged panel is a new configuration that
must be certified as a unit; (3) ~2x cost/latency per artifact. No qualifying
second judge is available now, so the panel is deferred. A qualifying judge can
be added later WITHOUT re-certifying gpt-4.1-mini (certify the new candidate
against the same human data; if it passes, form and certify the panel).

### Provider re-certification on tuzi (2026-06-12) — RESOLVES provider choice

Re-ran the CERTIFIED config (gpt-4.1-mini, strict, DEFAULT graded anchors —
only the provider changed) on the full extended set via tuzi, compared to all
three raters. Files: `*_tuzi.json`; ChatAnywhere certified backups
`*_chatanywhere_certified.json`.

| Provider | κ vs author | κ vs friend A | κ vs friend B | mean | judge mean score |
| --- | ---: | ---: | ---: | ---: | ---: |
| ChatAnywhere (certified) | 0.349 | 0.251 | 0.426 | 0.342 | 0.682 |
| tuzi | 0.369 | 0.249 | 0.462 | **0.360** | 0.664 |

- tuzi is **statistically indistinguishable from (slightly above)** ChatAnywhere
  and likewise at/above the human-pair ceiling (≈0.31). Provider equivalence
  confirmed for the certified default-anchor config.
- **The earlier "tuzi is lenient" concern does NOT hold on the discriminative
  set**: judge mean 0.664 ≈ ChatAnywhere 0.682, and tuzi marks weak pages down
  hard (qwen3-omni weak run all 0.125). The earlier lenient appearance was an
  artifact of (a) the all-good original page set and (b) the broken-gradient
  consensus anchors — not a provider property.
- **Framing correction**: "tuzi is lenient" was imprecise — without absolute
  ground truth, lenient-vs-strict is undefined. Against the human reference both
  judges are fine: judge means (tuzi 0.664, ChatAnywhere 0.682) both fall inside
  the human range (author 0.65, friend A 0.81, friend B ≈0.60), and their κ is
  equal. Neither provider is biased relative to humans; they are equivalent.
- **Decision (final, 2026-06-12): production provider = ChatAnywhere.** Rationale:
  judge quality is equivalent (κ tie), so the choice falls to reliability/speed
  and cost. tuzi is slow and hung once under load (confirmed independently slow
  in a Codex session); ChatAnywhere is fast, was stable during certification,
  holds the original certification, and the user has recharged it (cost no longer
  a constraint). tuzi is retained as a **validated, cheaper-but-slower fallback**.
  Provider is a swappable component: switching later only requires one
  re-validation run (~5 min on the extended set + κ), but the provider must be
  held FIXED within any single formal batch for score comparability.

## Status / next

- Judge freeze decision: evidence now favors `gpt-4.1-mini` strict+fewshot;
  awaiting user confirmation.
- After freeze: copy LB-JUDGE-v1 base/strict/fewshot prompts verbatim into
  `thesis/appendices/prompt_templates.tex`; wire the frozen judge into the
  leaderboard pipeline; then implement Technical coverage submetrics.
- The jitter tooling is reusable for calibrating few-shot anchors without
  human labels (future option).
