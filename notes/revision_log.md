# Revision Log

## 2026-06-12

### Deck rev 3 — synced to final freeze + adjudication findings

- Regenerated `presentations/track_b_progress_2026-06-12_v3.pptx` (v2 left in
  place, possibly open) to match the latest results. Factual corrections:
  medium anchor 0.875 → 0.75 (frozen anchors 0.50/0.75/1.0, F10 home / F01
  contact / F01 academy, slide 3); judge reframed from "awaiting confirmation"
  to FROZEN/FINAL (slides 6, 11, 12); provider claim corrected — the "tuzi
  lenient" worry was debunked as an artifact, providers are quality-equivalent,
  ChatAnywhere chosen for speed/stability (slides 7, 11). Added the
  "why author labels as gold?" defense (adjudicated-consensus anchors built and
  tested head-to-head, scored LOWER κ 0.31 vs 0.35 → author-gold retained) and
  the Goldilocks anchor refinement (moderate 0.50 beats both absence → collapse
  and a harsher 0.25 → over-correction) to the Exp 3 slide. Speaker notes gained
  the κ>0.6 explanation (objective tasks + training + countable wording, not
  yes/no; our κ≈0.3 matches subjective UI-judge literature). QA: exported PNGs
  via PowerPoint COM, slides 3/6/7/11/12 verified clean.

### Adjudicated-consensus anchors tested; author-gold retained; judge freeze FINAL

- Responding to the user's "why author labels as gold" critique, built an
  adjudicated-consensus anchor set (3 graded double-labelled pages, 5 disagreeing
  items resolved by author+friend adjudication; anchor scores 0.0625/0.625/1.0;
  sheet `anchor_adjudication_sheet.md`, new `--anchor-set adjudicated`). Full-range
  re-validation on ChatAnywhere, head-to-head on the SAME 45 pages:
  author-gold κ 0.353/0.340 vs adjudicated 0.306/0.281 → adjudicated consistently
  LOWER. Per the pre-registered rule, **author-gold default anchors RETAINED**.
  The harsh 0.0625 low exemplar over-corrects the judge; the moderate 0.50 low
  anchor calibrates better. Single-rater-gold documented as a limitation but
  empirically the consensus alternative did not improve agreement.
- Also explained/recorded (F6/F7 in jitter notes): self-preference sensitivity
  check is a planned POST-leaderboard step (re-judge GPT-family contestants with
  a cross-family judge, check ranking stability; contrast judge needs no
  certification). Dual-judge panel = future work (each member must pass human-
  ceiling cert; none qualifies now). Visual judge stays SCREENSHOT-ONLY by design
  (construct validity + avoids reopening the self-preference channel that code
  fingerprints carry + code/structure already covered by technical/accessibility
  layers).
- **Controlled add-one-low-anchor test** (clean single-variable, after the user
  correctly flagged the adjudicated test as confounded): 3 anchors vs 3+one 0.25
  low anchor, same session/pages. Control κ 0.329/0.299 vs treatment 0.228/0.198
  — adding the low anchor lowers κ ~0.10 (> ±0.05 noise), consistent across both
  raters. Full-range coverage REFUTED cleanly; the harsh-low-anchor effect is
  real. Control reproduced the original certification (within noise).
- Also explained (recorded): high-κ datasets reach κ>0.6 via objective/verifiable
  tasks + annotator training/guidelines/calibration + countable item wording —
  NOT via "yes/no" (we already use yes/no). Our κ≈0.3 ceiling matches the
  subjective UI-judge literature (MLLM-as-UI-Judge, WebDevJudge report moderate
  correlation), confirming the compare-to-human-ceiling framing.
- **VISUAL JUDGE FREEZE FINAL**: gpt-4.1-mini + strict + default graded anchors
  (0.50/0.75/1.0, author golds, 3 anchors — wider coverage tested & rejected) +
  3-rep majority vote, on ChatAnywhere.

### Visual-judge provider chosen (tuzi) — judge freeze config complete

- Re-certified the certified config (gpt-4.1-mini / strict / default graded
  anchors, only provider changed) on tuzi across the full extended set vs all
  three raters: tuzi κ = 0.369 / 0.249 / 0.462 (mean 0.360) ≈ ChatAnywhere
  0.349 / 0.251 / 0.426 (mean 0.342); both at/above the human ceiling ≈0.31.
  Judge mean 0.664 (tuzi) vs 0.682 (ChatAnywhere) — the earlier "tuzi lenient"
  worry was an artifact of the all-good original set + broken-gradient consensus
  anchors, NOT a provider property; on the discriminative set tuzi marks weak
  pages down hard.
- Framing correction: "tuzi lenient" was imprecise — no absolute ground truth,
  so lenient/strict is undefined; against humans both judge means (0.664/0.682)
  sit inside the human range (0.60–0.81) and κ is equal → providers equivalent.
- **Decision (final): production provider = ChatAnywhere.** Quality is a tie, so
  reliability/speed + cost decide: tuzi is slow and hung once (independently
  confirmed slow by Codex); ChatAnywhere is fast, stable, holds the original
  certification, and is now recharged (cost no longer a constraint). tuzi kept
  as a validated cheaper-but-slower fallback. Provider is swappable (one
  ~5-min re-validation per switch) but must be FIXED within a formal batch.
- FROZEN VISUAL JUDGE CONFIG: gpt-4.1-mini + strict + default graded anchors
  (0.50 / 0.75 / 1.00, F10 homepage / F01 contact / F01 academy, author golds)
  + 3-rep item-level majority vote, on ChatAnywhere. Anchors+golds+order frozen.
- Tooling: `--out-tag` added to run_visual_judge.py (provider-tagged outputs,
  no overwrite of certified files); call timeout 180→90 s. Certified
  ChatAnywhere extended-set files backed up as `*_chatanywhere_certified.json`.

### Supervisor-meeting deck built

- Built `presentations/track_b_progress_2026-06-12.pptx` (12 slides, English,
  Chinese speaker notes) via `presentations/build_deck.js` (pptxgenjs).
  Covers: judge config explained (strict / few-shot / 3-rep vote), r and κ
  defined with own data, literature sources for the validation bar, Exp 1
  jitter (with original/mild/severe/weak screenshots), Exp 2 human ceiling +
  certification, Exp 3 anchor sensitivity, generation-side status (TB-GEN-v16,
  W03, prompt-freeze blocker), schema v1 demo table, open items with causes,
  next steps. QA: exported slide PNGs via PowerPoint COM, fixed three layout
  collisions (slide 6 stat wrap, slide 8 title wrap, slide 10 table columns).
- Rev 2 after user review → `track_b_progress_2026-06-12_v2.pptx` (v1 was
  locked/open in PowerPoint, left untouched): experiments moved to slides 5–7
  (literature slide now follows as recap); yes-bias and temperature=0 get
  plain-language explanations; bad-anchor caption corrected (lowest ORIGINAL
  page; worse pages are jittered/weak variants, ineligible as anchors); r/κ
  slide gains worked examples; human-ceiling and reference-knowledge wording
  expanded; Exp 3 subtitle states anchors = few-shot pages; generation
  prompt-freeze blocker removed everywhere per user; schema slide gains a
  metric key (Rel./Stat./Dyn./axe weighted density); coverage and T1/T3 open
  items reworded in plain language.

### Rater correction (3 raters, 2 pairs); per-pair certification; tuzi provider

- User clarified the "second rater" was actually **two different friends**
  (A: pages 1–28, B: pages 29–56). Recomputed per pair: human-human κ =
  0.294 (author-A) and 0.324 (author-B) — two independent pairs both land at
  ≈0.3, stabilizing the ceiling estimate. gpt-4.1-mini per-pair κ =
  0.350/0.251/0.426 (mean 0.342) straddles and on average exceeds the human
  range; gemma (mean 0.246) and claude (0.242) sit below. Certification
  conclusion unchanged, now based on two human pairs. Correction recorded in
  [notes/track_b_jitter_validation.md](D:/master_thesis/notes/track_b_jitter_validation.md).
- ChatAnywhere balance exhausted (403 on 4-image few-shot payloads); user
  added a new `tuzi` provider key (`TUZI_API_KEY`/`TUZI_BASE_URL` in `.env`,
  api.tu-zi.com, OpenAI-compatible; response sometimes wrapped in `data` —
  `unwrap_openai_payload()` added to
  [scripts/run_visual_judge.py](D:/master_thesis/scripts/run_visual_judge.py)).
  Single-image probe with gpt-4.1-mini passes; anchor-sensitivity run
  (`--anchor-set alt`) relaunched via tuzi.
- **Anchor-sensitivity result**: with alt anchors lacking a truly-bad
  exemplar (span 0.69–1.0), gpt-4.1-mini collapses to yes-bias (15/16 pages
  = 1.0). Provider control (default anchors via the same tuzi key) preserves
  variance → collapse attributable to the anchors, not the provider. The
  single low-quality anchor (F10 homepage 0.50) carries the calibration.
  Frozen-config hard requirement added: anchor set must include ≥1 genuinely
  low-scoring exemplar; anchors+golds are frozen with the judge. Secondary:
  tuzi default run is lenient-shifted vs ChatAnywhere — provider switch
  requires revalidation. Details in
  [notes/track_b_jitter_validation.md](D:/master_thesis/notes/track_b_jitter_validation.md).

## 2026-06-11

### Track B leaderboard schema v1

- Added `notes/track_b_leaderboard_schema_v1.md` as the meeting-demo schema
  specification. It separates the schema container from metric formulas and
  defines artifact-level results, model-level rows, failure-aware reporting,
  applicable/not-applicable metric handling, category rankings, and pending
  metric slots.
- Rebuilt `scripts/build_track_b_dev_subset_demo.py` to output schema-aligned
  JSON/Markdown:
  - `data/track_b/leaderboard/dev_subset_v16_schema_v1_demo.json`
  - `data/track_b/leaderboard/dev_subset_v16_schema_v1_demo.md`
- The schema v1 demo includes F-series executable workflow items
  (F01/F03/F06/F10) and the W03 static-responsive probe. Dynamic metrics are
  marked not applicable for W03 rather than scored as zero.
- The model-level rows now include attempted/eligible/failed items,
  `failure_by_item`, `failure_category_counts`, completion reliability,
  category scores, raw route/content/token/latency averages, and category
  ranking fields. Overall remains pending until category weights are approved.
- Validation: `py -3 -m py_compile scripts/build_track_b_dev_subset_demo.py`
  and `py -3 scripts/build_track_b_dev_subset_demo.py` both succeeded. The
  generated JSON declares `leaderboard_schema_version =
  track-b-leaderboard-v1`.

### Second-rater data merged; inter-rater ceiling computed; judge certified at human level

- Rater2 (independent friend, blind to variants) completed the 56-page
  extended review in two browser sessions; the two complementary exports were
  merged by [scripts/compute_interrater.py](D:/master_thesis/scripts/compute_interrater.py)
  into [data/track_b/visual_human_review/visual_human_review_extended_rater2.json](D:/master_thesis/data/track_b/visual_human_review/visual_human_review_extended_rater2.json)
  (2 duplicate pages with conflicting answers kept first-session values; 2
  pages have one missing item each).
- **Human-human ceiling** (rater1 vs rater2, 894 item cells): agreement 0.697,
  **κ=0.317**, page-score r=0.521 — binary visual judgments have genuinely low
  human consensus; the judges' absolute κ must be read against this ceiling,
  not against the generic κ>0.6 textbook bar.
- **Judge certification (Judge's Verdict two-step)**: gpt-4.1-mini
  strict+fewshot reaches κ=0.350/0.334 vs the two raters — **at/above the
  human-human ceiling, symmetric across raters** → certified human-like.
  gemma (0.293/0.221) and claude (0.286/0.194) are below the ceiling and
  asymmetric (track rater1 idiosyncratically — likely few-shot-anchor overlap).
- New finding recorded: **reference-knowledge effect** — rater1 (knows the
  prototypes) scored weak-model pages 0.344 vs naive rater2's 0.686; rater
  framing shifts absolute scores while preserving within-rater ordering.
  Mild-jitter refutation replicated by rater2 (mild mean 0.957).
- Details in [notes/track_b_jitter_validation.md](D:/master_thesis/notes/track_b_jitter_validation.md);
  summary JSON `data/track_b/visual_jitter_validation/interrater_summary.json`.
- Consequence: the visual-judge freeze recommendation (gpt-4.1-mini
  strict+fewshot, 3-rep majority vote) is now **literature-standard certified**;
  awaiting the user's formal freeze confirmation to execute appendix prompts,
  leaderboard wiring, and Technical coverage submetrics.

### Thesis manuscript synchronization pass after multi-agent experiment edits

- Ran a focused sync pass because recent Track B files were edited across
  Claude Code and Codex sessions while the thesis chapter files had not been
  updated since 2026-06-04/05.
- Updated [thesis/chapters/chapter3_methodology.tex](D:/master_thesis/thesis/chapters/chapter3_methodology.tex):
  - added the current versioned-generation protocol around `TB-GEN-v16`
    compact input packing, prompt-ID governance, and the OpenAI-compatible
    `max_tokens` omission policy;
  - replaced the outdated accessibility pass-ratio wording with the frozen
    severity-weighted violation-density formula from
    [notes/metric_specification.md](D:/master_thesis/notes/metric_specification.md);
  - refined the failure taxonomy to separate provider failures, completion /
    truncation failures, dynamic route failures, and dynamic content-validation
    failures, based on
    [notes/track_b_failure_taxonomy_and_decisions.md](D:/master_thesis/notes/track_b_failure_taxonomy_and_decisions.md);
  - expanded the reliability-audit text to cover the 16-item human/LLM visual
    checklist, Cohen's kappa, score degeneracy, strict/few-shot calibration,
    jittered screenshots, weak-model artifacts, and the caveat that mild
    perturbations are not a guaranteed error oracle, based on
    [notes/track_b_jitter_validation.md](D:/master_thesis/notes/track_b_jitter_validation.md).
- Updated [thesis/appendices/prompt_templates.tex](D:/master_thesis/thesis/appendices/prompt_templates.tex)
  with thesis-impacting Track B visual prompt/protocol records:
  `LB-JUDGE-v1-base`, `LB-JUDGE-v1-strict`,
  `LB-JUDGE-v1-strict-fewshot`, and `HUMAN-VISUAL-v1`. Basis:
  [scripts/run_visual_judge.py](D:/master_thesis/scripts/run_visual_judge.py)
  and [scripts/build_visual_human_review.py](D:/master_thesis/scripts/build_visual_human_review.py).
- Added [notes/thesis_sync_workflow.md](D:/master_thesis/notes/thesis_sync_workflow.md)
  to define when to run future sync passes and how to decide whether recent
  code/data/notes changes should be written to the manuscript, appendix, or
  left in notes.
- Remaining uncertainty: the production visual judge is still not stated as a
  final frozen choice in the manuscript; current evidence favors
  `gpt-4.1-mini` strict+fewshot, but the notes still record this as awaiting
  user confirmation.
- Validation: `pdflatex -interaction=nonstopmode -halt-on-error
  master_thesis.tex` succeeded from `thesis/` and produced
  `thesis/master_thesis.pdf`. LaTeX still reports existing overfull/underfull
  box warnings in tables/verbatim prompt blocks.

### Track B W-series static/responsive probe

- Ran one Vision2Web Level 1 W-series item, `W03_eventbrite`, to check how the
  current `TB-GEN-v16` pipeline behaves on static responsive webpage tasks
  rather than F-series dynamic workflow tasks.
- Command policy: `TB-GEN-v16`, compact input, GWDG `qwen3.6-35b-a3b`,
  `--max-tokens none`. Run directory:
  `data/track_b/items/W03_eventbrite/generated/gwdg_qwen36_35b_v16_w03_static_omit_maxtokens/`.
- Result: generation stopped normally (`finish_reason=stop`) with 10,120 prompt
  tokens, 16,525 completion tokens, 26,645 total tokens, and 206.35 seconds
  latency. The static gate passed with zero errors and zero warnings.
- Captured standardized screenshots with
  `scripts/capture_track_b_standard_screenshots.js --full-page`; screenshot
  coverage is 3/3 for the W03 desktop/tablet/mobile viewport routes. Manifest:
  `data/track_b/items/W03_eventbrite/generated/gwdg_qwen36_35b_v16_w03_static_omit_maxtokens/standard_screenshots/manifest.json`.
- Interpretation: W-series items exercise a different branch of Track B. They
  are static/responsive visual-layout tasks (`use_for_dynamic=false`), so they
  should feed static visual/responsive evaluation rather than route/content
  dynamic workflow scoring. Do not merge W03 into the current F-series dynamic
  leaderboard without separate metric treatment.

### Judge test-retest instability found; freeze protocol gains 3-rep majority vote

- Measured repeated-scoring consistency (user question: average multiple
  judge runs?): 3 reps of gpt-4.1-mini strict+fewshot on the 16 original
  pages at temperature=0. Result: 5/16 pages changed, max page-score swing
  0.4375, 9% item flip rate; per-rep r vs human 0.602/0.627/0.503 — the API
  is not deterministic at temperature=0 (MoE routing/batching).
- Decision: the frozen judge protocol will require **3 repetitions +
  item-level majority vote** (variance reduction, not bias correction; bias
  is handled by strict+fewshot calibration; judge panels = future work).
- Details in [notes/track_b_jitter_validation.md](D:/master_thesis/notes/track_b_jitter_validation.md);
  rep files `llm_judge_gpt-4.1-mini_strict_fewshot_rep{1,2,3}.json`.
- Also built shareable single-file review pages for the second rater
  (`review_extended_rater2_embedded.html`, 13MB, base64-embedded screenshots;
  `--rater`/`--embed` options added to
  [scripts/build_visual_human_review.py](D:/master_thesis/scripts/build_visual_human_review.py)),
  plus an original-vs-mild comparison page
  ([scripts/build_jitter_comparison.py](D:/master_thesis/scripts/build_jitter_comparison.py))
  and the three-cause decomposition of the mild result (JND / binary floor
  effect / rater fatigue) with candidate citations.

### Extended human review completed; full-range validation computed

- User annotated all 56 extended pages (19 jitter-mild, 19 jitter-severe, 18
  weak-model F10) via `review_extended.html` (quasi-blind, shuffled, per-page
  All-Yes/All-No default-then-correct protocol). Export stored as
  [data/track_b/visual_human_review/visual_human_review_extended.json](D:/master_thesis/data/track_b/visual_human_review/visual_human_review_extended.json).
- Ran all three strict+fewshot judges on the three weak-model runs (new
  `llm_judge_*_strict_fewshot_<weak_run>.json` files; example-page exclusion
  drops 01_homepage, so 5 pages per weak run).
- New [scripts/compute_extended_validation.py](D:/master_thesis/scripts/compute_extended_validation.py)
  → `data/track_b/visual_jitter_validation/extended_validation_summary.json`.
- **Findings** (details appended to
  [notes/track_b_jitter_validation.md](D:/master_thesis/notes/track_b_jitter_validation.md)):
  - Human refutes the mild ground truth (0/18 original>mild; mild mean 0.987)
    → gemma/claude mild "inversions" were human-aligned, not failures.
  - Severe ordering confirmed (15/18); weak pages span the low end (0.344).
  - Full range (62 pages): gemma r=0.694/κ=0.294; gpt-4.1-mini r=0.615/
    κ=0.360, best-calibrated mean, best weak-subset r=0.393; claude r=0.505.
    Range-restriction hypothesis confirmed: r rose from ~0.5–0.6 to ~0.69, κ
    from 0.07–0.17 to 0.29–0.36 once the quality range was unrestricted.
  - Residual uniform-output degeneracy on out-of-distribution broken pages for
    both minis (gemma all-0.6875, 4.1-mini all-0.125 on the qwen3-omni run).
- Protocol caveat recorded: extended session used default-accept/-reject
  buttons, original session per-item clicks; cross-session (original vs mild)
  comparisons carry this confound.
- Pending: final judge freeze decision (recommendation gpt-4.1-mini
  strict+fewshot: best κ, best calibration, best on real weak pages — the
  leaderboard-relevant subset; gemma best raw full-range r but lenient and
  weakest on weak pages). After freeze: appendix prompts, leaderboard wiring,
  Technical coverage submetrics.

## 2026-06-10

### Pre-freeze validation per literature standards (Claude capping test, kappa, extended human set)

Context: literature check (Design2Code 5-annotator majority protocol;
MLLM-as-UI-Judge multi-rater crowdsourcing, judges accurate only on large
score gaps; LLM-judge surveys requiring chance-corrected agreement, κ>0.6)
showed our validation was below field standards (1 rater, 15 pages, raw
agreement only). Executed the agreed pre-freeze checklist:

- Added **Cohen's κ** to [scripts/compare_visual_human_llm.py](D:/master_thesis/scripts/compare_visual_human_llm.py).
  Result: raw item agreement ~0.85 collapses to κ=0.173 (gemma) / 0.067
  (gpt-4.1-mini) on the range-restricted original set — the "high agreement"
  was base-rate inflation; must not be reported as primary evidence.
- **Claude capping test** (claude-sonnet-4-5 via ChatAnywhere, strict+fewshot,
  prompt unchanged): on originals Pearson **-0.125** (κ -0.059) — real variance
  and varied confidence, but flags *different* pages than the human. On jitter
  pairs it is the most decisive severe discriminator (0.938, zero ties).
  Cross-judge summary: ALL judges pass coarse discrimination (orig-vs-severe
  ≈0.91–0.94); ALL fail subtle discrimination; gemma and claude *invert* on
  mild. Trying more judges cannot resolve the freeze decision — more human
  data is the only arbiter.
- Captured standardized screenshots for three real weak-model F10 artifacts
  (same TB-GEN-v9 prompt: qwen3-omni, internvl3.5, gpt-4o-mini).
- Extended [scripts/build_visual_human_review.py](D:/master_thesis/scripts/build_visual_human_review.py)
  with `--extended`: built `review_extended.html` (56 pages = 19 jitter-mild +
  19 jitter-severe + 18 weak-model), **run names hidden + deterministic
  shuffle (quasi-blind)**, separate localStorage key and export name.
- Mild-jitter caveat strengthened: 2 of 3 judges scored mild-jittered pages
  *higher* than originals — the "any jitter = worse" assumption may be partly
  wrong for mild; the human extended review arbitrates.
- **Next / blocking**: user annotates the 56-page extended set (priority:
  jitter-mild), exports `visual_human_review_extended.json`; then recompute
  full-range r and κ and make the judge freeze decision. Inter-rater κ
  (second human rater) deferred to scale-up phase.

### Paid-judge comparison (gpt-4o-mini, gpt-4.1-mini) vs free gemma

- Edited [scripts/run_visual_judge.py](D:/master_thesis/scripts/run_visual_judge.py):
  added a `--provider {gwdg,chatanywhere}` option (endpoint + key loading from
  `.env`, fixed a UTF-8-BOM parsing issue). **Prompt wording unchanged** — no
  new prompt version. Backup:
  `archive/backup/run_visual_judge_2026-06-10_before-paid-provider.py`.
- Ran the LB-JUDGE comparison harness on the same 19/16 dev screenshots:
  - `gpt-4o-mini` base: all pages 1.000, zero variance — **the paid model has
    the same yes-bias** as all four free GWDG vision models.
  - `gpt-4o-mini` strict: all pages exactly 0.9375, zero variance — a **new
    degenerate mode**: mechanically marks exactly one item false per page
    ("token fault-finding"), superficially obeying the strict instruction while
    still having no discriminative power.
  - `gpt-4o-mini` strict+fewshot: real variance, Pearson **0.514**, item
    agreement 0.838 (below free gemma's 0.565/0.871).
  - `gpt-4.1-mini` strict+fewshot: Pearson **0.602**, item agreement 0.854,
    mean 0.912 vs human 0.917 (well calibrated) — best so far, but within noise
    of gemma at n=15.
- Outputs: `data/track_b/visual_human_review/llm_judge_gpt-4o-mini*.json`,
  `llm_judge_gpt-4.1-mini_strict_fewshot.json`, and per-condition
  `human_vs_llm_comparison_*.json` copies (the unsuffixed comparison file now
  holds the latest run; named copies disambiguate).
- **Interpretation**: all three strict+fewshot judges cluster at r≈0.51–0.60,
  so the alignment ceiling is the task/labels (single rater, n=15, ~90%-true
  base rate), not model price tier. L4 (spacing consistency) is systematically
  under-marked by every judge (gemma, 4o-mini, 4.1-mini) — an item-level
  wording/standard issue, not a model issue.
- Pending decision: freeze the production judge (free gemma strict+fewshot vs
  paid gpt-4.1-mini). Once frozen, all LB-JUDGE prompt variants (base, strict,
  fewshot) must go verbatim into
  [thesis/appendices/prompt_templates.tex](D:/master_thesis/thesis/appendices/prompt_templates.tex)
  because the three-condition comparison will be reported in the reliability
  section.

### Jitter validation: range-restriction hypothesis confirmed, judge preference flipped

- User hypothesis: the r≈0.51–0.60 ceiling is **range restriction** (all dev
  artifacts are good, human scores cluster 0.875–1.00), not judge incapacity.
- Built a UIClip-style validation (details in
  [notes/track_b_jitter_validation.md](D:/master_thesis/notes/track_b_jitter_validation.md)):
  [scripts/jitter_track_b_pages.py](D:/master_thesis/scripts/jitter_track_b_pages.py)
  injects deterministic CSS defects (JITTER-MILD-v1 / JITTER-SEVERE-v1) into the
  dev-subset artifacts → constructed ground truth (original > mild > severe) →
  same screenshot protocol → pairwise ranking accuracy via
  [scripts/compute_jitter_pairwise.py](D:/master_thesis/scripts/compute_jitter_pairwise.py),
  no new human labels needed.
- Added `--run` option to [scripts/run_visual_judge.py](D:/master_thesis/scripts/run_visual_judge.py)
  (prompt wording unchanged).
- Results (16 pairs each): both judges hit **0.906 with zero inversions** on
  original-vs-severe — the moderate r on originals is compressed variance, not
  blindness. On original-vs-mild, gpt-4.1-mini mostly ties (insensitive), but
  gemma **inverts** (scores mild-jittered pages higher than originals, 7/16) —
  a validity failure on subtle differences.
- **Judge freeze recommendation flipped to `gpt-4.1-mini` strict+fewshot**
  (no inversion, proportional severity response 0.918/0.902/0.645, higher
  human r=0.602); gemma stays as the documented free fallback. Decision
  awaiting user confirmation.
- Caveat recorded: the mild ground-truth assumption ("any jitter = worse") is
  weak; orig-vs-severe is the headline evidence.

### Accessibility normalization formula frozen

- Backup: `archive/backup/metric_specification_2026-06-10_before-accessibility-formula-freeze.md`.
- Edited [notes/metric_specification.md](D:/master_thesis/notes/metric_specification.md):
  replaced the pass-ratio leaderboard formula (clustered 0.91–0.98, no
  discriminative power) with severity-weighted violation density:
  `1 - min(1, (1*minor + 2*moderate + 4*serious + 8*critical) / (pass_nodes + violation_nodes))`.
  Weights 1/2/4/8 are a recorded convention (axe-core gives ordinal impact
  only). All inputs already exist in `accessibility_report.json`, so historical
  reports can be re-scored without re-running. Pass ratio demoted to a
  diagnostic field. Formula frozen before formal batches, same discipline as
  the generation-prompt freeze policy.

## 2026-06-05

### Track B static gate relaxed; prompt freeze policy added

Context: the Track B generation prompt kept churning (`TB-GEN-v1`..`v16`) because
every gate failure was treated as a prompt-wording problem. Diagnosis: the static
gate's exact-visible-text requirement for workflow controls was forcing the
prompt to micromanage exact strings (`GitLab Duo`, `View Recipe`), and each fix
regressed another item.

- Backup: `archive/backup/check_track_b_generation_2026-06-05_before-gate-relaxation.py`.
- Edited [scripts/check_track_b_generation.py](D:/master_thesis/scripts/check_track_b_generation.py):
  - Added `normalize_label()` and `label_matches_clickable()` (normalized +
    bidirectional-containment fuzzy matching) and an `attrs_make_clickable()`
    helper (refactored out of `has_working_clickable`).
  - Demoted `workflow_clickable_labels_present` and `workflow_clickables_not_inert`
    from **error** to **warning**, and switched them to fuzzy matching. The hard
    gate now blocks only on structural/capacity failures (incomplete doc, unclosed
    body/style/script truncation, `finish_reason in {length,max_tokens}`, undefined
    onclick functions, workflow `showPage` routes without matching section ids).
  - Authority for workflow-control routing/content correctness moves to the
    dynamic browser workflow check (`run_track_b_browser_workflow.js`).
- Regression-verified on existing artifacts: F03 `..v16_f03_compact_smoke` now
  **passes** (was a hard exact-label fail); F10 `..v15_f10_smoke` still passes;
  F06/F09 `..v15..` still **fail but only on real truncation errors**, not labels.
- Added [notes/track_b_prompt_freeze_policy.md](D:/master_thesis/notes/track_b_prompt_freeze_policy.md):
  root-cause separation (capacity vs instruction-following vs exact-string), the
  gate-change record, an explicit **freeze criterion** on the F01/F03/F10 dev
  subset, and anti-overfitting rules (no single-item tuning, one change per
  version, record-don't-patch).
- Rationale: a benchmark must measure task completion, not verbatim string
  reproduction; exact-text gating destroyed leaderboard discriminative power and
  drove the prompt churn.
- Not yet done: re-score a `TB-GEN-v16` dev-subset batch under the relaxed gate
  to decide whether to freeze v16 as the baseline. The appendix table in
  `thesis/appendices/prompt_templates.tex` may need a note that the static gate is
  structural-only once the freeze decision is made.

## 2026-06-04

### Provider model catalog for experiment keys

- Added [notes/provider_model_catalog_2026-06-04.md](D:/master_thesis/notes/provider_model_catalog_2026-06-04.md) to record provider-documented model names for the configured GWDG/SAIA and ChatAnywhere keys without storing any secret values.
- Sources used: GWDG Chat AI model documentation, GWDG SAIA API documentation, ChatAnywhere GitHub README, and ChatAnywhere API/model-list documentation.
- Rationale: avoid wasting time and provider quota by probing model names through generation calls; keep model choices traceable for Track B smoke tests and future reported runs.
- Added the experiment-cost decision that GWDG/SAIA remains the default for tests; when it is rate-limited, quota-limited, timing out, or otherwise unavailable, fallback to ChatAnywhere should start with low-cost models (`gpt-4o-mini`, `gpt-4.1-mini`, or `gpt-5-mini`) and record the fallback trigger in run metadata.
- Remaining uncertainty: provider model availability can change after 2026-06-04, and ChatAnywhere's own model-list page warns that its table may lag upstream provider changes.

### Metric-spec revision after supervisor-meeting follow-up discussion

Source: discussion grounding in `Meeting Summary/` plus literature search
(VisAWI Moshagen & Thielsch; Lavie & Tractinsky 2004; MLLM-as-a-UI-Judge
arXiv:2510.08783; WebDevJudge arXiv:2510.18560; CheckEval arXiv:2403.18771;
Beauty-in-the-Eye-of-AI arXiv:2604.03417; Position-Bias-in-Rubric-Based-Judge
arXiv:2602.02219). These references are recorded here as rationale; they will be
added to `references.bib` only when actually cited in thesis chapter text, per
the user's "cite only if used" instruction.

- Backups: `archive/backup/metric_specification_2026-06-04_before-visual-layer-revision.md` and `archive/backup/track_b_vision2web_pilot_plan_2026-06-04_before-dev-subset-note.md`.
- Edited [notes/metric_specification.md](D:/master_thesis/notes/metric_specification.md):
  - Reduced the Static Visual layer from seven dimensions to **four objective-leaning, LLM-judged dimensions** (Layout & Visual Hierarchy, Information Organization/Clarity, Typography & Readability, Visual Consistency), each grounded in cited instruments.
  - Switched the visual scoring method to **binary-checklist decomposition** (CheckEval rationale: lower variance, higher agreement than holistic Likert); narrow 3–5 anchored scale only where a graded judgement is unavoidable; wide 1–9 scale reserved as a rating-scale-sensitivity condition only.
  - Moved **holistic aesthetic quality to future work** (LLM-human aesthetic alignment is weak without calibration); optional non-weighted diagnostic with human-correlation validation.
  - Moved **contrast and other rule-based accessibility checks to a new automated Accessibility Score** computed by `axe-core`/Lighthouse (free, local, deterministic, no LLM tokens), still counted in the leaderboard. Documented why contrast must not be LLM-judged.
  - Added a shared **score-normalization rule** (all submetrics → [0,1] with per-instrument formulas) and clarified the Static Visual layer is a single layer with multiple instruments.
  - Tightened the **dynamic task-success definition**: a task succeeds iff route reached AND destination content validation passes.
  - Added optional **reliability levers** (few-shot anchoring, confidence filtering) and an **LLM-human visual-correlation validation** step.
  - Added an **Overall-Score caution** that cost is primarily a Pareto axis and weights are an un-justified hyper-parameter to be sensitivity-tested.
  - Reframed the **Reliability Audit** as lightweight recording only (per user decision): biases are recorded as they appear with known controls applied; a systematic bias study is an optional, out-of-scope future extension.
- Edited [notes/track_b_vision2web_pilot_plan.md](D:/master_thesis/notes/track_b_vision2web_pilot_plan.md): added an explicit **development subset (3 items: F01, F03, F10) vs scale-up set (10 items)** split, per the supervisor's "develop on a tiny set first" advice.
- Not yet done: `LB-JUDGE-v1` visual-judge prompt (four-dimension checklist + anchors) is still unwritten; when written it must go verbatim into [thesis/appendices/prompt_templates.tex](D:/master_thesis/thesis/appendices/prompt_templates.tex).

### Methodology chapter aligned to revised metric spec

- Backup: `archive/backup/chapter3_methodology_2026-06-04_before-visual-layer-revision.tex`.
- Edited [thesis/chapters/chapter3_methodology.tex](D:/master_thesis/thesis/chapters/chapter3_methodology.tex) so the manuscript matches the revised metric spec:
  - Rewrote the **Static Visual Score** subsection to the four objective-leaning dimensions + binary-checklist scoring + narrow-anchored-scale rule, with holistic aesthetics deferred to future work and contrast removed.
  - Added a new **Accessibility Score** subsection (automated `axe-core`/Lighthouse, still in the leaderboard) and removed "accessibility basics" from the Static Technical submetric list to avoid duplication.
  - Added an **Overall-Score hyper-parameter / cost-double-counting** caution.
  - Provenance (per AGENTS.md): traceable to [notes/metric_specification.md](D:/master_thesis/notes/metric_specification.md); design-claim citations added (see below).
- Added five bibliography entries to [thesis/references.bib](D:/master_thesis/thesis/references.bib): `visawi`, `lavie2004aesthetics`, `mllmuijudge`, `webdevjudge`, `checkeval`, and cited them in the Static Visual subsection. Clean rebuild (`bibtex` + `latexmk`) with zero undefined citations.
  - **TODO (metadata)**: `mllmuijudge` (arXiv:2510.08783) and `webdevjudge` (arXiv:2510.18560) currently use placeholder author fields; replace with the real author lists before final submission. Classic HCI entries (`visawi`, `lavie2004aesthetics`) and `checkeval` have standard metadata.

### LB-JUDGE-v1 visual judge prompt drafted

- Created [scripts/prompts/LB-JUDGE-v1.md](D:/master_thesis/scripts/prompts/LB-JUDGE-v1.md): first draft of the static-visual judge prompt. Scores one standardized per-page screenshot via 16 binary checklist items (4 per dimension) over the four visual dimensions, returns strict JSON, includes confidence for confidence-filtering. Scale policy is binary-only (no Likert).
- Not yet wired into a scorer script and not yet run. When it produces any reported result it must be copied verbatim into [thesis/appendices/prompt_templates.tex](D:/master_thesis/thesis/appendices/prompt_templates.tex) with id `LB-JUDGE-v1`.

### Bib author metadata completed

- Replaced the placeholder author fields in [thesis/references.bib](D:/master_thesis/thesis/references.bib) with the real author lists found via search: `mllmuijudge` (Luera, Rossi, Dernoncourt, et al., arXiv:2510.08783) and `webdevjudge` (Chunyang Li, Yilun Zheng, Xinting Huang, et al., arXiv:2510.18560).

### Accessibility scorer (axe-core) implemented and run

- Installed `axe-core` (npm) and created [scripts/run_track_b_accessibility.js](D:/master_thesis/scripts/run_track_b_accessibility.js): opens the generated `index.html` in Chromium (Playwright), injects axe-core, runs the WCAG 2 A/AA rule set in-page, and writes a normalized `accessibility_report.json`. Score = pass_nodes / (pass_nodes + violation_nodes). Free, local, deterministic, no API tokens.
- Ran it on the 3-item development subset (`gwdg_qwen36_35b_v9_smoke`): F01 0.913, F03 0.9845, F10 0.9259. All violations were colour-contrast — exactly the WCAG check moved off the LLM judge.

### Trial leaderboard aggregation

- Created [scripts/build_trial_leaderboard.py](D:/master_thesis/scripts/build_trial_leaderboard.py) and wrote [data/track_b/trial_leaderboard_2026-06-04.json](D:/master_thesis/data/track_b/trial_leaderboard_2026-06-04.json).
- **Tentative** Overall weights (hyper-parameters, to be sensitivity-tested, NOT final): Technical 0.20, Visual 0.25, Accessibility 0.15, Dynamic 0.40. Efficiency kept as a Pareto axis, not in the composite (avoids double-counting cost).
- Visual is still null (LB-JUDGE-v1 not run), so only a provisional Overall over the available quality categories (renormalized) is reported. Model-level provisional (excl. visual) for `qwen3.6-35b-a3b`: technical 1.00, accessibility 0.941, dynamic 0.847, provisional Overall 0.907. Technical currently uses gate pass/fail as a placeholder until coverage submetrics are computed.

### Accessibility coverage breadth + human visual-review page

- Enhanced [scripts/run_track_b_accessibility.js](D:/master_thesis/scripts/run_track_b_accessibility.js) to also record passed-rule list, incomplete rules, and inapplicable-rule count, and re-ran the 3 dev items. Finding: all violations are `color-contrast` (serious); 17--19 applicable rules pass per page and 43--45 are inapplicable (simple pages without forms/tables/frames). Interpretation: for this content type the Accessibility category is currently dominated by contrast and has low discriminative breadth; consider items with forms/tables to exercise more rules, or report it as a focused contrast/structure diagnostic.
- Created [scripts/build_visual_human_review.py](D:/master_thesis/scripts/build_visual_human_review.py) → [data/track_b/visual_human_review/review.html](D:/master_thesis/data/track_b/visual_human_review/review.html): a self-contained page presenting each of the 19 standardized dev-subset screenshots with the same 16 binary checklist items, live per-page scoring, localStorage autosave, and JSON export in the LB-JUDGE-v1 shape for human-vs-LLM comparison.

### First human-vs-LLM visual judge comparison (key finding)

- Human review collected (18/19 pages answered; `04_gitlab_duo` left null): [data/track_b/visual_human_review/visual_human_review.json](D:/master_thesis/data/track_b/visual_human_review/visual_human_review.json). Human mean page score 0.889 with real spread (page scores 0.50--1.00).
- Created [scripts/run_visual_judge.py](D:/master_thesis/scripts/run_visual_judge.py) (LB-JUDGE-v1 comparison variant, flat boolean answers + confidence) and ran it on all 19 screenshots via GWDG/SAIA free model `internvl3.5-30b-a3b`: [data/track_b/visual_human_review/llm_judge_internvl3.5-30b-a3b.json](D:/master_thesis/data/track_b/visual_human_review/llm_judge_internvl3.5-30b-a3b.json).
- Created [scripts/compare_visual_human_llm.py](D:/master_thesis/scripts/compare_visual_human_llm.py) → [data/track_b/visual_human_review/human_vs_llm_comparison.json](D:/master_thesis/data/track_b/visual_human_review/human_vs_llm_comparison.json).
- **Finding**: the free InternVL model answered `true` to all 16 items on all 19 pages (mean 1.000, zero variance, confidence 0.90--0.95) -- a degenerate yea-saying judge. Raw item agreement is 0.889 but this is a base-rate artifact (the human is also mostly-true); Pearson on page scores is undefined because the LLM has no variance, so it cannot discriminate good from weak pages and is unusable as a leaderboard scorer as-is. The LLM never marked false on exactly the discriminative items where the human did (O2 uncluttered, T3 line length, T2 text size, L2 alignment). This reproduces the WebDevJudge cautionary result and validates the human-correlation requirement.
- Implications/next steps to try: stronger judge model (GPT-4o/Claude, needs paid key); prompt forcing a critical stance with required evidence for each `false`; few-shot calibration including failure examples; possibly comparative/forced-quota judging. Recorded as a reliability finding, not a separate research direction.

### Cross-model + strict-prompt follow-up (visual judge)

- Queried the live GWDG model list; only four vision-capable models exist (`internvl3.5-30b-a3b`, `qwen3-omni-30b-a3b-instruct`, `gemma-4-31b-it`, `medgemma-27b-it`); the email's Qwen2.5-VL-72B is no longer served.
- **Base prompt, all three usable vision models give the identical degenerate output**: every page scored 1.000, zero variance (internvl, qwen3-omni, gemma). The yes-bias is robust across models, not a single-model fluke.
- Added a `--variant strict` fault-finding prompt to [scripts/run_visual_judge.py](D:/master_thesis/scripts/run_visual_judge.py) and re-ran:
  - `gemma-4-31b-it` strict: yes-bias broken -- now has real variance (LLM mean 0.879), but judgments do not track the human (item agreement 0.787, Pearson on page scores = -0.184 over 17 pages, i.e. ~0 / slightly negative). 1 page failed JSON parse.
  - `internvl3.5-30b-a3b` strict: still all 1.000, ignores the strict instruction entirely.
- **Conclusion (revised after few-shot)**: free GWDG vision models default to yes-bias; strict prompting removes the all-yes symptom (gemma) but alone gives uncorrelated noise; some models ignore it (internvl).

### Ruling out non-model causes + few-shot calibration

- Ruled out image-resolution confound: all standardized screenshots are 1440x900 (above-the-fold viewport), not giant downscaled full-page captures, so the judge sees the same images the human saw.
- Added a `--fewshot` mode to [scripts/run_visual_judge.py](D:/master_thesis/scripts/run_visual_judge.py): prepends 3 curated human-labelled example screenshots (mix of weak/strong: F10 homepage 0.50, F01 contact 0.75, F01 academy 1.00) as image+gold-answer turns; those 3 pages are excluded from evaluation.
- `gemma-4-31b-it` strict + few-shot (15 eval pages): **Pearson on page scores jumps from -0.184 to +0.565**; item agreement 0.871; LLM mean 0.912 vs human 0.917 (well-calibrated). So the failure was largely prompt/calibration, not raw capability: a free 31B model + strict prompt + 3 examples reaches moderate human alignment.
- Net narrative for the reliability section: (1) yes-bias is the default across free vision models; (2) a strict fault-finding prompt is necessary but not sufficient; (3) few-shot calibration with human-labelled examples recovers moderate alignment (r=0.565, n=15, single rater) even on a free model. A paid judge and more/independent human labels are the path to stronger alignment.

### Thesis text provenance rule added

- Updated [AGENTS.md](D:/master_thesis/AGENTS.md) with a repository-wide rule for thesis manuscript edits: new or materially revised thesis content must have either a citation, a traceable project source, or an explicit rationale.
- The rule requires substantive thesis-text changes to be recorded in this revision log with changed files, source/rationale, and remaining uncertainty.
- Motivation: user instruction that thesis additions should not be invented and should be source-marked or reasoned, with a record kept for reproducibility and writing discipline.

### Methodology clarification for pilot results and artifact-scoring modes

- Updated [chapter3_methodology.tex](D:/master_thesis/thesis/chapters/chapter3_methodology.tex) to clarify that controlled thesis experiments require full generation metadata, while public artifact-scoring mode can accept a submitted executable artifact with minimal optional metadata for diagnostic reports.
- Added the current Track B static technical gate basis: complete HTML, non-truncated style/script blocks, defined click handlers, declared routes, workflow-required controls, and quoted-label versus semantic-click handling.
- Added a dynamic-validation clarification that `browser-workflow-v1` is still a pilot implementation used to validate the protocol and identify workflow-design issues, not final thesis-result evidence until the item set, workflow normalization, and reporting rules are fixed.
- Source/rationale: based on [notes/track_b_benchmark_protocol.md](D:/master_thesis/notes/track_b_benchmark_protocol.md), [notes/track_b_browser_workflow_v1_experiment.md](D:/master_thesis/notes/track_b_browser_workflow_v1_experiment.md), and the user decision that pilot browser-workflow and mini-leaderboard results should not be prematurely written as final thesis results.

## 2026-04-08

- Abstract wording updated in [thesis_proposal.tex](D:/master_thesis/thesis_proposal.tex) to clarify the evaluation method:
  `order-swapped pairwise comparisons, where the order of candidates is reversed to detect positional bias`.
- Purpose of the change: respond to supervisor feedback asking what the earlier wording meant and make the method description more explicit.

## 2026-04-09

- Added benchmark and leaderboard language to the abstract in [thesis_proposal.tex](D:/master_thesis/thesis_proposal.tex).
- Added a short motivation paragraph explaining why screenshot-based evaluation alone is not sufficient and why dynamic interaction should be treated as a complementary dimension.
- Added a new `Benchmark and Leaderboard Design` subsection to describe the benchmark structure, extensibility to new models, and a lightweight leaderboard or dashboard artifact.
- Added a new `Dynamic Evaluation with Computer-Use Agents` subsection to position dynamic evaluation as a small complementary extension rather than the main benchmark.
- Updated the `Evaluation` section to include dynamic metrics such as task completion rate, action efficiency, and qualitative failure analysis, and to mention benchmark extensibility.
- Revised the abstract to remove citation-dependent special terms such as `UIClip`, and replaced more technical wording with more self-contained phrasing suitable for an abstract without references.
- Further simplified abstract wording by replacing method-heavy terms such as `rubric-based assessment`, `zero-shot prompting`, and `rubric-guided scoring` with more self-contained descriptions.
- Rewrote the opening and closing logic of the abstract so that it no longer begins with `Earlier work...`, and instead states the problem, contribution, and static-versus-dynamic evaluation relation more directly.
- Refined the abstract again to restore appropriate field-standard method terms such as `rubric-based assessment`, `zero-shot prompting`, and `rubric-guided scoring`, while still avoiding citation-dependent paper names such as `UIClip`.
- Fixed the front-matter build issue by restoring the correct `abstract/keywords -> maketitle` order and verifying a clean rebuild from scratch. This resolved the missing abstract and removed the stale `Contributing authors` line from the rebuilt PDF.

## 2026-04-10

- Restored [thesis_proposal.tex](D:/master_thesis/thesis_proposal.tex) after an accidental overwrite from an older local version during a failed local build attempt.
- Reinstated the agreed title, abstract wording, benchmark/leaderboard extension, dynamic computer-use-agent extension, and the subsection-based `Planned Approach` structure.
- Removed stale front-matter content from the overwritten version, including the old email-driven author block and outdated abstract text.
- Added [thesis_progress.md](D:/master_thesis/notes/thesis_progress.md) as a separate project-level progress record to track current scope, completed decisions, supervisor feedback already addressed, and next tasks.
- Created a dated backup snapshot in `D:\master_thesis\backup\` covering the current source, PDF, bibliography, revision log, and progress log.
- Revised the final paragraph of the introduction so that it now reflects the two-track benchmark design more accurately, rather than describing the project as primarily screenshot-based.
- Revised the requirement-driven track description in `Datasets and Evaluation Material` to make the generation scope smaller and clearer.
- Replaced the earlier `code artifact`-style wording with a more direct explanation that runnable front-end code supports both browser-based interaction tests and checks of requirement satisfaction.
- Created a second dated backup snapshot after the introduction and dataset-section revisions, stored in `D:\master_thesis\backup\` with the suffix `2026-04-10_after_intro_dataset_revision`.

## 2026-04-10 (Introduction revision)

- Revised the Introduction section in response to supervisor comment ("For such aspects it is particularly important to employ something like CUA for automated task completion").
- Paragraph 1: added a closing sentence emphasizing that GUI quality also concerns interaction and task completion, not just visual appearance.
- Paragraph 2 (UIClip): replaced the old "open questions" framing with a new structure that acknowledges UIClip's strength for visual/usability evaluation, then highlights its limitation regarding interactive task completion, and introduces computer-use agents (CUA) as the relevant dynamic assessment method.
- Removed the standalone paragraph about screenshot limitations (previously paragraph 4), since the point is now integrated into paragraphs 1 and 2.
- Final paragraph: added a scope-setting sentence clarifying the main focus (screenshot-based benchmark + leaderboard) and the complementary dynamic evaluation module with CUA.
- Backup saved as `backup/thesis_proposal_2026-04-10_intro-revision.tex`.

## 2026-04-10 (Section 2.1 + linked revisions — responding to supervisor dataset feedback)

**Supervisor comment**: "This is not a good idea because it will restrict the evaluation possibilities drastically ... It is better to base the dataset on natural language requirements. In addition, it restricts the evaluation only to visual aspects, but maybe using the code for evaluation might also be interesting."

**Background research**: Studied all three cited papers in depth (UIClip, Designer Feedback / RLDF, LLM-as-a-Judge) to inform the revision. Key insights: UIClip is screenshot-only with acknowledged limitations for dynamic/interactive evaluation; the Designer Feedback paper uses NL descriptions → LLM-generated HTML as a core pipeline and found that simple ranking feedback has only ~50% agreement; the LLM-as-a-Judge paper provides methodological foundations for judging strategies.

**Changes made**:

- **Section 2.1 (Datasets and Evaluation Material)**: Rewrote to introduce a dual-track dataset structure:
  - Track A: existing UIClip screenshot resources as an established baseline for pairwise and rubric-based evaluation.
  - Track B (new): NL requirement-driven generation — collect UI descriptions, use multiple LLMs to generate HTML, render as screenshots. Produces runnable code for dynamic evaluation and enables requirement-alignment assessment.
  - Added a closing paragraph explaining how the two tracks together broaden evaluation beyond screenshot-only.
- **Introduction (paragraph 3)**: Strengthened the designer feedback citation by adding the key finding that simple pairwise rankings reached only ~50% evaluator agreement, further motivating the need for richer evaluation structures (rubric-based scoring, requirement-aligned judgment).
- **Section 2.6 (Dynamic Evaluation)**: Explicitly linked the dynamic module to the requirement-driven track — LLM-generated HTML can be rendered in a browser, and interaction tasks are derived from the original NL descriptions. Added a sentence about whether requirement alignment in static evaluation predicts successful dynamic interaction.
- **Section 3 (Evaluation)**: Added a sentence about an additional evaluation dimension for the requirement-driven track: measuring how well model judgments capture whether a generated interface satisfies its original NL description.
- **Decision**: Code-level evaluation (suggested by supervisor as "interesting") is acknowledged as a future possibility in Section 2.1 but not incorporated into the current evaluation framework, to keep scope manageable.
- Backup saved as `backup/thesis_proposal_2026-04-10_pre-2.1-revision.tex` (pre-edit) and `backup/thesis_proposal_2026-04-10_post-2.1-revision.tex` (post-edit).

## 2026-04-10 (Add citations + requirement fidelity dimension)

**Motivation**: Following feasibility analysis of the three core changes (Track B, CUA dynamic eval, requirement alignment), two new supporting citations were identified and incorporated. The requirement fidelity rubric dimension was also formally added to Section 2.3.

**New references added to `references.bib`**:
- `design2code`: Si et al., "Design2Code: How Far Are We From Automating Front-End Engineering?", ACL 2024. Cited in Section 2.1 to support the feasibility of generating renderable front-end code from UI descriptions.
- `visualwebarena`: Koh et al., "VisualWebArena: Evaluating Multimodal Agents on Realistic Visual Web Tasks", ACL 2024. Cited in Section 2.6 to provide methodological precedent for using multimodal agents to perform goal-directed tasks on visual web interfaces.

**Section 2.1**: Added in-text citation of `design2code` with one supporting sentence.

**Section 2.3 (Multi-dimensional GUI Rubric)**: Added a fifth rubric dimension — **Requirement fidelity** (Track B only) — measuring the degree to which a generated interface realizes the elements, structure, and functionality specified in the original NL description. Added a follow-up sentence clarifying that this dimension applies exclusively to Track B and uses the original description as a reference for judgment.

**Section 2.6 (Dynamic Evaluation)**: Added in-text citation of `visualwebarena` with one supporting sentence.

**Compile**: Full pdflatex + bibtex + pdflatex × 2 — successful, 5 pages, no errors.
- Backup: `backup/thesis_proposal_2026-04-10_add-refs.tex/.pdf`, `backup/references_2026-04-10_add-refs.bib`.

## 2026-04-10 (Rubric update — responding to supervisor comments on Section 2.3)

**Supervisor comments**:
1. "GUI dynamics" — rubric should include a dimension covering dynamic/interactive behavior.
2. "This should also be only an initial list, there might be more dimensions that are relevant." — list should be explicitly marked as open to expansion.

**Changes made**:

- **Section 2.3**: Added a sixth rubric dimension — **Interaction quality** (Track B only) — covering responsiveness to user actions, appropriateness of feedback and state transitions, and overall smoothness of the interactive experience. This directly addresses the "GUI dynamics" comment. Explicitly linked this dimension to the dynamic evaluation module in Section 2.6.
- **Section 2.3**: Added an explicit sentence after the itemized list: "This list represents an initial set of dimensions; additional dimensions may emerge during pilot annotation and will be incorporated if they prove reliable and informative." This directly addresses the "initial list" comment.
- Restructured the explanatory paragraph after the list to clearly distinguish: the first four dimensions (static screenshot), requirement fidelity (Track B, description-based), and interaction quality (Track B, dynamic evaluation via CUA).

**Compile**: Successful, 5 pages, no errors.
- Backup: `backup/thesis_proposal_2026-04-10_rubric-update.tex/.pdf`.

## 2026-04-10 (Section 2.4 literature review framing and supporting citations)

**Supervisor comment**: "Should also include a literature research to first of all investigate which other LLM-as-a-judge techniques exist that are potentially applicable ..."

**Changes made**:

- **References**: Added two new LLM-as-a-judge citations to `references.bib`:
  - `li-etal-2025-generation`: Li et al., "From Generation to Judgment: Opportunities and Challenges of LLM-as-a-judge", EMNLP 2025. Used as a survey-style reference for the broader space of judge techniques.
  - `shi-etal-2025-judging`: Shi et al., "Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge", IJCNLP-AACL 2025. Used to support positional-bias analysis in pairwise judging.
- **Section 2.4 (Prompting and Judging Strategies)**: Rewrote the opening of the subsection so that the strategy set is no longer presented as an ad hoc list. It now states that strategy selection will be informed by an initial literature review of LLM-as-a-judge methods.
- **Section 2.4 citations**: Added in-text support for three parts of the subsection:
  - `llm_judge` for foundational pairwise judging and judge bias,
  - `li-etal-2025-generation` for broader judge-taxonomy framing,
  - `shi-etal-2025-judging` for order-swapped pairwise comparisons and positional-bias mitigation.
- **Scope preserved**: Kept the experimental strategy set itself unchanged (zero-shot, few-shot, rubric-guided, repeated judging, order-swapped pairwise comparisons, aggregation), but reframed these as representative strategies chosen after the literature review.

## 2026-04-10 (Reference style cleanup for new LLM-as-a-judge citations)

**Motivation**: After adding two new LLM-as-a-judge references for Section 2.4, the bibliography became visually inconsistent because the new entries used full ACL-style metadata while the rest of the proposal used a shorter compact style.

**Changes made**:

- **`references.bib`**: Shortened `li-etal-2025-generation` and `shi-etal-2025-judging` to match the style of the existing bibliography.
- Replaced full author lists with compact `and others` formatting so that the bibliography renders as `et al.`.
- Replaced long conference names with abbreviated venue names (`Proc. EMNLP`, `Proc. IJCNLP-AACL`).
- Removed pages, address, publisher, DOI, and URL fields from these two entries to keep the proposal bibliography concise and visually uniform.

**Verification**:
- Confirmed that Section 2.4 still cites all three intended sources: `llm_judge`, `li-etal-2025-generation`, and `shi-etal-2025-judging`.

## 2026-04-10 (Light response to supervisor side note on weaker models)

**Supervisor note**: It could be interesting to also test substantially weaker models and compare their behavior to stronger proprietary models.

**Change made**:

- **Section 3 (Evaluation)**: Added one short exploratory sentence after the opening model-selection sentence. The new sentence states that, if feasible, one or two smaller or weaker multimodal models may be included in order to examine how judge quality varies with model capability.

**Rationale**:
- This responds to the supervisor's suggestion without turning weaker-model comparison into a core deliverable or expanding the scope of the proposal too much.

**Backup**:
- Saved a new snapshot after this change in `D:\master_thesis\backup\` with the suffix `2026-04-10_after_weaker_model_note` for the source, PDF, bibliography, revision log, and progress log.

## 2026-04-10 (Content compression and repetition cleanup)

**Motivation**: The proposal still contained several places where the same structure or contribution was summarized multiple times. The goal of this revision was to reduce repetition without changing the scope or methodological content.

**Changes made**:

- **Introduction**: Compressed the closing thesis-summary paragraph into a single sentence. It still states the benchmark/leaderboard contribution, the two-track design, and the dynamic module, but without repeating the full structure in two separate sentences.
- **Planned Approach**: Removed the opening "six main components" overview sentence because the subsection structure already makes the methodology clear.
- **Section 2.1 (Datasets and Evaluation Material)**: Merged the explanation of runnable front-end code, browser-based interaction tests, and requirement checking into a single compact sentence. Removed the extra concluding sentence that restated the purpose of the two-track design.
- **Section 2.3 (Multi-dimensional GUI Rubric)**: Shortened the explanatory paragraph after the rubric list. The revised text now keeps only the essential distinctions between static dimensions and Track-B-specific dimensions, with a shorter link to the dynamic module.
- **Section 3 (Evaluation)**: Merged the first two paragraphs so that accuracy, reliability, and computational cost are presented more compactly. Removed the sentence that repeated benchmark extensibility, since that point is already covered in the benchmark/leaderboard subsection.

**Result**:
- Full rebuild successful.
- Page count reduced from 6 pages to 5 pages.

## 2026-04-10 (Section 2.2 clarified for dynamic evaluation)

**Motivation**: The Human Annotation Protocol previously described only screenshot-based annotation, which created ambiguity about how the dynamic module would be validated and how its results would connect back to the main thesis question.

**Changes made**:

- **Section 2.2 (Human Annotation Protocol)**: Revised the static annotation description slightly for concision and consistency with the rest of the proposal.
- Added a new closing paragraph explaining that the dynamic module will rely primarily on automated task-completion metrics rather than full manual scoring.
- Clarified the role of limited human review in the dynamic module:
  - to verify ambiguous task outcomes,
  - to distinguish interface-related failures from agent or evaluation-script errors,
  - and to support a small qualitative categorization of major interaction failures.
- Explicitly connected this human review to the thesis objective of understanding where static quality judgments and dynamic task performance diverge.

## 2026-04-10 (Abstract and Evaluation sync — full-paper consistency pass)

**Problem**: After multiple rounds of edits to the body (dual-track dataset, 6 rubric dimensions, literature review step, weaker models), the abstract and Evaluation section had fallen out of sync with the current body text.

**Inconsistencies fixed**:

1. **Abstract — dataset description**: Replaced "screenshot-based evaluation set" with the dual-track structure: "a screenshot-based baseline drawn from existing UI resources, and a requirement-driven track in which interfaces are generated from natural language descriptions."
2. **Abstract — rubric dimensions**: Expanded from 4 dimensions to 6, listing the original four and adding "for generated interfaces -- requirement fidelity and interaction quality."
3. **Abstract — literature review**: Added "the work begins with a literature review of LLM-as-a-judge techniques to identify applicable strategies, followed by a systematic comparison of approaches."
4. **Evaluation last paragraph**: Replaced "support UIClip-style evaluation" with "can serve as judges of GUI quality" — the scope now extends well beyond UIClip-style screenshot comparison.

**Compile**: Successful, 6 pages, no errors.
- Backup: `backup/thesis_proposal_2026-04-10_abstract-sync.tex/.pdf`.

## 2026-04-29

- Added [thesis_outline.md](D:/master_thesis/notes/thesis_outline.md) as the canonical 8-chapter thesis outline for the full master thesis (supersedes the GPT-generated `thesis_summary_outline.md` for execution; that file is kept as reference).
- Outline integrates: teacher's 5 suggestions (Teacher's suggestion.txt), the proposal's two-track design, Design2Code methodology (reference/), and a critical review of which suggestions to keep, downsize, or reframe.
- Key design decisions captured in the outline:
  - 8 chapters (was 10 in GPT version): merged Dataset+Annotation into Ch4; merged Discussion+Conclusion into Ch8.
  - 4 RQs (was 6): static-dynamic correlation (RQ4) elevated as core novelty.
  - Track A retained but reduced: 50–100 UIClip pairs reused, no new annotation.
  - Track B: Design2Code-HARD ~50 + 5–10 self-built requirements (form-heavy / mobile UI).
  - Rubric reduced from 6 to 4 starting dimensions: Visual Structure, Information Clarity, Requirement Fidelity, Interaction Quality (subject to pilot).
  - Model lineup: 2 closed-source + 1 open + 1 weaker baseline.
  - Prompting strategies must-do: rubric-guided + order-swap; few-shot/aggregation deferred.
  - Dynamic evaluation uses Plan B (LLM action plan elicitation + script validation) instead of full computer-use agent execution. Plan A listed as future work to keep noise sources separable.
  - HF Space leaderboard: minimal Gradio dashboard reading `results.json`, submission via PR. No online inference.
- Backup: `backup/thesis_outline_2026-04-29_initial.md`.

## 2026-04-30

### references.bib — Added usability theory and web agent references

Added 6 new BibTeX entries to support Ch2 of the full thesis, organized under section comments:

**Ch2.1 — GUI Quality & Usability Theory** (was completely missing):
- `nielsen1994usability` — Nielsen, *Usability Engineering*, Morgan Kaufmann, 1994. Grounds the rubric in established HCI theory.
- `nielsen1990heuristic` — Nielsen & Molich, *Heuristic Evaluation of User Interfaces*, CHI 1990. Original 10 heuristics paper.
- `iso9241-11` — ISO 9241-11:2018, *Ergonomics of Human-System Interaction: Usability: Definitions and Concepts*. Formal usability definition.
- `norman2013design` — Norman, *The Design of Everyday Things*, Basic Books, 2013 (revised ed.). Optional supporting reference.

**Ch2.5 — Multimodal Web Agents** (was missing non-VisualWebArena references):
- `webarena` — Zhou et al., *WebArena*, ICLR 2024. Foundational web-agent benchmark.
- `mind2web` — Deng et al., *Mind2Web*, NeurIPS 2023. Generalist web agent with element-level annotations.

BibTeX compile: clean (no errors). Backup: `backup/references_2026-04-30_before-usability-refs.bib`.

### 2026-04-30 — Draft Ch2.6 Research Gap Matrix

Created `notes/draft_ch2_gap_matrix.tex`: LaTeX draft of §2.6 (Research Gap).
Includes:
- Three-paragraph narrative identifying the three main gaps (no modern LLM judge for UI / no rubric-based UI assessment / static vs dynamic never validated)
- Comparison table (8 prior works × 7 dimensions): multi-dim rubric / modern LLM judge / bias analysis / human labels / requirement fidelity / dynamic eval / benchmark artifact
- All 13 references.bib keys correctly cited

### 2026-04-30 — Draft Ch3 Methodology

Created `notes/draft_ch3_methodology.tex`: complete LaTeX draft of Chapter 3 (Research Questions and Methodology).
Contents:
- §3.1: 4 RQs with formal English wording and rationale
- §3.2: Overall study design (two-track architecture, static-dynamic pairing principle)
- §3.3: Track A (UIClip 50–100 pairs, no new annotation)
- §3.4: Track B (Design2Code-HARD ~50 + 5–10 self-built, generation + rendering pipeline)
- §3.5: Static evaluation methodology (model selection, zero-shot vs rubric-guided, order-swap, repeated sampling)
- §3.6: Dynamic evaluation methodology (Plan B: action plan elicitation + DOM validation, failure taxonomy F1–F4)
- §3.7: Metrics (κ, Spearman ρ, position-bias rate, self-consistency, plan-success rate, static-dynamic correlation, API cost)
- §3.8: RQ↔method mapping table

### 2026-05-06 — Draft Ch4 Benchmark Construction

Created `notes/drafts/draft_ch4_benchmark.tex`: complete LaTeX draft of Chapter 4 (Benchmark Construction and Human Annotation Protocol). Estimated 12–15 pages.

Sections:
- §4.1 Benchmark Design Goals (reproducibility, extensibility, track separation, leaderboard compatibility)
- §4.2 Track A: UIClip Reproduction Subset — documents caption-matched derived pair construction, the manual cleaning that yielded the 43-pair canonical set (excluding ids 0, 15, 31, 33, 35, 41, 48), and the on-disk item layout
- §4.3 Track B: Requirement-Driven Generated Interfaces — Design2Code-HARD curation (~50) + 5–10 self-authored requirements; generation by 2–3 LLMs; Playwright headless rendering at fixed viewports (1280×800 desktop, 390×844 mobile)
- §4.4 Item Schema and Result Submission Format — common schema + track-specific blocks; submission JSON consumed by HF Space leaderboard
- §4.5 GUI Quality Rubric — 4 dimensions (D1 Visual Structure, D2 Information Clarity, D3 Requirement Fidelity, D4 Interaction Quality) grounded in Nielsen heuristics + ISO 9241-11; 1–5 ordinal scale; abbreviated anchor table for scores 1/3/5; post-pilot adjustment rule (α < 0.4 triggers redesign)
- §4.6 Human Annotation Protocol — 3 peer annotators, 30-min calibration session, Track B rubric form + small Track B pairwise subset, escalation procedure
- §4.7 Inter-Rater Reliability — Krippendorff α targets (≥0.7 good, ≥0.5 acceptable, <0.5 redesign); median across annotators as reference label
- §4.8 Pilot Annotation — 10 items × 3 annotators × 4 dimensions = 120 ratings; placeholder table for post-pilot α

Appendix references: full anchor table → Appendix B; JSON schema → Appendix C; leaderboard implementation → Appendix F.

Cross-references: forward to §5.1 (model lineup), Chapter 5 (experiments), Chapter 6 (dynamic eval), Chapter 7 (results).

## 2026-05-04

### Track A — Order-Swap Experiment: GPT-4o, 20 pairs

**Script**: `scripts/track_a_order_swap.py`
**Dataset**: `biglab/jitteredwebsites-merged-224-paraphrased-paired` (algorithmically labelled pairs)
**Result file**: `scripts/results/track_a_orderswap_gpt-4o_20260504_153247.json`

**Methodology**: Each pair judged twice.
- Run 1: good image shown as A (position 1), bad image shown as B (position 2) → correct answer = "A"
- Run 2: bad image shown as A, good image shown as B → correct answer = "B"
- Consistent = model picks the same underlying image both times

**Results**:

| Metric | Value |
|--------|-------|
| Accuracy Run1 (good=A) | 8/20 = **40.0%** |
| Accuracy Run2 (good=B) | 19/20 = **95.0%** |
| Consistency rate | 9/20 = **45.0%** |
| Position bias rate | 11/20 = **55.0%** |
| Corrected accuracy (consistent pairs only) | 8/9 = **88.9%** |

**Per-pair breakdown of the 11 biased pairs** (pairs 3–7, 13, 15–19):
- All 11 showed the identical pattern: Run1=B (wrong, good was A), Run2=B (correct, good was B)
- Model chose the *second image* in every single case — pure recency/position-B bias

**Pair 2 anomaly**: Consistent but *wrong* — model chose A both times when good was A in Run1 (wrong) and good was B in Run2 (also wrong). The model preferred the bad image consistently, not biased by position.

**Interpretation**:
1. **Severe B-position (recency) bias**: GPT-4o overwhelmingly prefers the second image shown. Run2 accuracy (95%) vs Run1 accuracy (40%) — a 55-percentage-point gap driven entirely by which position holds the good image.
2. **Consistency rate 45%**: Only 9 of 20 pairs elicit the same underlying image choice when order is flipped — more than half are position-driven.
3. **Corrected accuracy 88.9%**: When the model IS consistent, it almost always picks the good image. This shows genuine visual discrimination ability that is masked by positional preference.
4. **Implication for raw pilot accuracy (65%)**: The earlier pilot randomly assigned images to A/B positions (seed=42). About half the time the good image was in position B, giving partial credit. The 65% figure is therefore a mix of real discrimination and position luck — not a reliable accuracy estimate.

**Thesis relevance**:
- Directly supports **RQ3** (judging strategies): quantifies why order-swap is a necessary debiasing step.
- The 40%/95% asymmetry is the clearest possible demonstration that single-order pairwise evaluation is unreliable for GPT-4o.
- The corrected accuracy (88.9%) will be used as the debiased capability estimate in §7.4 (Strategy Ablation).
- This pattern — strong recency bias, but high corrected accuracy — is consistent with the position bias literature cited in the thesis (shi-etal-2025-judging).

## 2026-05-04

### Track A — Formalized Evaluation Script and UIClip Human Caption-Matched Run

**Script**: `scripts/track_a_eval.py`  
**Dataset**: `biglab/uiclip_human_data_hf`  
**Result file**: `scripts/results/track_a_eval_gpt-4o_20260504_161730.json`  
**Model call route**: `OPENAI_BASE_URL=https://api.chatanywhere.tech/v1` recorded in result metadata

**Important data note**: `biglab/uiclip_human_data_hf` contains single images with captions, not explicit `img_good/img_bad` pair columns. The script constructs derived pairs by matching screenshots with the same normalized page description where one caption contains `well-designed` and the other contains `poor design`, `bad contrast`, or `bad proximity`. This should be described as **caption-matched derived pairs**, not as raw pairwise human preference labels.

**Run setup**:
- 50 matched pairs
- Order-swap enabled
- 100 total multimodal judge calls
- Prompt: zero-shot pairwise visual design preference

**Results**:

| Metric | Value |
|--------|-------|
| Raw accuracy | 59/100 = **59.0%** |
| Accuracy Run1 (good=A) | 20/50 = **40.0%** |
| Accuracy Run2 (good=B) | 39/50 = **78.0%** |
| Consistency rate | 29/50 = **58.0%** |
| Position bias rate | 21/50 = **42.0%** |
| Corrected accuracy (consistent pairs only) | 19/29 = **65.5%** |
| Chose A / Chose B | 31 / 69 |

**Interpretation**:
1. The second-image preference remains visible in a larger UIClip-human-derived sample: GPT-4o chose B in 69% of the 100 calls.
2. The Run1/Run2 asymmetry persists: 40% when the good image is first, 78% when the good image is second.
3. Unlike the earlier 20-pair jittered pilot, corrected accuracy is only moderate (65.5%). This suggests that caption-matched UIClip human pairs are harder/noisier, and the stronger 88.9% pilot result should be treated as preliminary rather than a stable capability estimate.
4. Next step: manually inspect the 50 derived pairs and improve matching if needed before scaling to 100 pairs or adding more models.

### Manual Pair Review — Clean 43-Pair Subset

Manual review of the HTML pair-review page marked 7/50 pairs as mismatch / needs review:
`pair_id` = 0, 15, 31, 33, 35, 41, 48.

The filtered result file is:
`scripts/results/track_a_eval_gpt-4o_20260504_161730_clean43.json`

| Metric | Clean value |
|--------|-------------|
| Raw accuracy | 53/86 = **61.6%** |
| Accuracy Run1 (good=A) | 17/43 = **39.5%** |
| Accuracy Run2 (good=B) | 36/43 = **83.7%** |
| Consistency rate | 24/43 = **55.8%** |
| Position bias rate | 19/43 = **44.2%** |
| Corrected accuracy (consistent pairs only) | 17/24 = **70.8%** |
| Chose A / Chose B | 24 / 62 |

After removing clear mismatches, the key finding remains: GPT-4o strongly favors the second image. The improved corrected accuracy suggests that some noise came from imperfect derived-pair construction, but the position-bias effect is not explained away by those mismatches.

### Manual Pair Review — Clean 85-Pair Subset

Manual review of the 100-pair HTML page marked 15/100 pairs as mismatch / needs review:
`pair_id` = 0, 23, 33, 41, 56, 57, 58, 87, 90, 91, 92, 94, 95, 97, 98.

The filtered result file is:
`scripts/results/track_a_eval_gpt-4o_20260506_142748_clean85.json`

| Metric | Clean value |
|--------|-------------|
| Raw accuracy | 106/170 = **62.4%** |
| Accuracy Run1 (good=A) | 33/85 = **38.8%** |
| Accuracy Run2 (good=B) | 73/85 = **85.9%** |
| Consistency rate | 45/85 = **52.9%** |
| Position bias rate | 40/85 = **47.1%** |
| Corrected accuracy (consistent pairs only) | 33/45 = **73.3%** |
| Chose A / Chose B | 45 / 125 |

The clean 85-pair subset strengthens the Track A pattern: removing mismatches improves the capability estimate, but the B-position preference remains almost unchanged.

### Track A — Rubric-Guided Prompt on Clean85

**Script**: `scripts/track_a_eval.py`  
**Result file**: `scripts/results/track_a_eval_openai_gpt-4o_rubric_20260506_162332.json`  
**Pair set**: same clean85 subset as the zero-shot run  
**Condition**: rubric-guided pairwise prompt with order-swap

| Metric | Zero-shot clean85 | Rubric-guided clean85 |
|--------|-------------------|-----------------------|
| Raw accuracy | 62.4% | **57.1%** |
| Accuracy Run1 (good=A) | 38.8% | **20.0%** |
| Accuracy Run2 (good=B) | 85.9% | **94.1%** |
| Consistency rate | 52.9% | **25.9%** |
| Position bias rate | 47.1% | **74.1%** |
| Corrected accuracy | 73.3% | **77.3%** |
| Chose A / Chose B | 45 / 125 | **22 / 148** |

**Interpretation**: the rubric-guided prompt worsened pairwise reliability despite giving more explicit evaluation criteria. It increased the B-position preference substantially. This is important for RQ3: prompt engineering is not monotonically beneficial, and GUI judge strategies require empirical validation.

## 2026-05-06

### Literature Update — Dynamic Usability Assessment with Computer Use Agents

Read and summarized Gao et al., "Training Computer Use Agents to Assess the Usability of Graphical User Interfaces" (`literature/papers/Training Computer Use Agents to Assess the Usability of Graphical User Interfaces1.pdf`).

Created note: `notes/paper_notes_dynamic_usability_cua.md`.

Key finding for thesis direction:

- The paper already proposes a large-scale CUA-based dynamic usability assessment system.
- It builds `uxWeb` with 2,586 interactive UIs, injects usability defects, collects designer preferences, and trains `uxCUA`.
- It reports uxCUA outperforming larger baselines on usability scoring, with AUC 0.632 on synthetic defect labels and 0.607 on human preferences.
- Therefore, this thesis should not claim novelty for general CUA-based usability assessment.

Direction adjustment:

- Keep Track B, but reposition it as a lightweight benchmark linking static multimodal GUI rubric judgments with dynamic task-validation outcomes.
- Do not train a CUA.
- Use this paper as major related work and as justification for a smaller, methodology-focused thesis scope.

## 2026-05-14

- Repositioned [thesis_outline.md](D:/master_thesis/notes/thesis_outline.md) after re-reading uxCUA (Gao et al. 2026, arXiv:2604.26020) via the new compact summary in [notes/uxCUA_short_codex_note.md](D:/master_thesis/notes/uxCUA_short_codex_note.md).
- Primary novelty axis confirmed as **benchmark + leaderboard for GUI judge evaluation** (Teacher suggestion #5), with **RQ4 static->dynamic correlation** as the empirical centerpiece. Recorded as Part 0 bullet 7.
- Ch1.4 Contributions reordered: C1 = public benchmark + HF Space leaderboard (artifact contribution); C5 = static-dynamic linkage study (empirical centerpiece). Old C1-C5 demoted/merged.
- Ch1.1 Motivation: added explicit "positioning vs uxCUA" paragraph (complementary, not competing — uxCUA = model, this thesis = benchmark infrastructure).
- Ch2.1.2 / Ch4.5.1: added Shneiderman's 8 Golden Rules as a third theoretical grounding alongside Nielsen and ISO 9241-11; linked D4 Interaction Quality to Shneiderman's feedback / dialog closure / error prevention / reversal categories (same theoretical basis as uxCUA's defect taxonomy).
- Ch2.5: added new sub 2.5.4 "Trained CUAs for usability assessment (uxCUA)" with uxWeb stats, training pipeline, reported AUC, and contrast statement.
- Ch2.6 Research-gap matrix: added two new columns (public benchmark+leaderboard, judge-method comparison) and a new uxCUA row; highlighted the "This thesis" row's unique triple intersection.
- Ch3.1 RQ4: rewrote with sharper wording carried over from [notes/paper_notes_dynamic_usability_cua.md](D:/master_thesis/notes/paper_notes_dynamic_usability_cua.md).
- Ch3.6 + Ch6.2: added explicit Plan B vs Plan A (uxCUA-style) contrast paragraph with cost/noise-source justification.
- Ch6: added new subsection 6.8 "Plan A Navigation Pilot (cross-check)" — 5-10 Track B items, uxCUA-inspired navigation metrics (unique-screen ratio, dead-click rate, loop count, etc.), 1 table + 1 scatter. Ch6 page estimate raised from 8-10 to 10-12.
- Ch8.6 Limitations: added 3 new items (untrained judge / subjective human labels with alpha=0.308 reference / Plan B vs Plan A semantic gap).
- Ch8.7 Future Work: rewrote with three uxCUA-aware directions starred (trained CUA judge for this benchmark / mobile+desktop GUI extension / full Plan A scale-up).
- Decisions reconfirmed this session: web only (no mobile experiments); Plan B remains main dynamic approach; Plan A retained only as small §6.8 pilot.
- Updated [proposal/references.bib](D:/master_thesis/proposal/references.bib): added entries `shneiderman2016designing` (book) and `uxcua2026` (arXiv).
- Pre-edit snapshot saved at [notes/drafts/thesis_outline_pre_uxcua_repositioning_2026-05-14.md](D:/master_thesis/notes/drafts/thesis_outline_pre_uxcua_repositioning_2026-05-14.md).
- Plan file: [.claude/plans/uxcua-short-codex-note-training-compute-mutable-parnas.md](C:/Users/stephenxxy/.claude/plans/uxcua-short-codex-note-training-compute-mutable-parnas.md).
- Next steps (per plan §Verification): (1) cross-reference uxCUA mentions in the edited outline; (2) send updated Contributions block + RQ4 + §6.8 to supervisor for sign-off on the benchmark-novelty repositioning; (3) optionally locate the canonical arXiv id for uxCUA and replace placeholder `2604.26020` in references.bib if discrepancy is found.

## 2026-05-14 (patch — 7 corrections from code-review feedback)

Applied 7 targeted corrections to `thesis_outline.md` after reviewing inline annotation feedback:

1. **Part 0 #7** — Softened "uxCUA 已实质性覆盖建议 #1–#4" to a more accurate statement: uxCUA strongly overlaps with the *dynamic CUA usability assessment* direction only; UIClip reproduction, LLM-as-a-judge ablation, and judge-agnostic leaderboard (#5) remain open.
2. **Ch2.6 matrix** — Fixed factual error: uxCUA *did* build uxWeb dataset/benchmark. Corrected to: "trained-CUA usability-assessment dataset/benchmark, but not a judge-agnostic GUI-evaluation leaderboard for comparing arbitrary multimodal LLM judge methods."
3. **C5 (Ch1.4)** — Removed "First empirical study"; replaced with "A focused empirical study … To our knowledge …" to reduce claim risk.
4. **Ch6 title** — Renamed from "Dynamic Evaluation with Computer-Use Agents" to "Dynamic Task Validation for Executable Generated Interfaces" to avoid framing collision with uxCUA and better reflect Plan B's approach.
5. **§6.8** — Downgraded from committed section to "TIME-PERMITTING OPTIONAL cross-check"; added explicit status note to prevent scope inflation; page estimate adjusted to 9–11 pages.
6. **Part 0 §"static and dynamic"** — Changed "dynamic agent 任务测试" to "dynamic task validation / action-plan validation" for terminology consistency with Plan B.
7. **Part 3 item 4** — Updated "Dynamic agent 选择" open question to reflect current status: the only remaining decision is whether to run the optional §6.8 Plan A pilot.

## 2026-05-21

### Prompt preservation policy and appendix established

- Created `notes/prompt_preservation_policy.md` — defines which prompts must be saved (result/protocol-affecting only), required metadata fields, versioning rule, and storage locations.
- Created `AGENTS.md` at repo root — concise standing instruction for all agents (including Codex) to follow the prompt preservation policy.
- Created `thesis/appendices/prompt_templates.tex` with `\chapter{Prompt Templates and Experimental Metadata}` containing:
  - `TA-PAIR-ZS-v1`: zero-shot pairwise visual design prompt (gpt-4o + claude-sonnet-4-5)
  - `TA-PAIR-RUBRIC-v1`: rubric-guided pairwise prompt (gpt-4o)
  - Both entries now include full metadata (models, parameters, dates, source lines, result file paths).
- Wired appendix into `thesis/master_thesis.tex` via `\appendix` + `\include{appendices/prompt_templates}`, positioned after `\bibliography{}` (standard thesis convention).
- Appendix prompt text verified to match `scripts/track_a_eval.py:44-68` exactly.

## 2026-05-19

### Track B source update — Vision2Web replaces Design2Code-HARD as main substrate

- Reframed Track B around a reduced **Vision2Web Level 1 / Level 2** subset because Vision2Web directly supports the thesis's static-vs-dynamic GUI-quality question: static visual website generation plus interaction/function-oriented verification.
- Demoted Design2Code-HARD from the main Track B data source to a static UI-to-code related-work reference and reserve source for simple reproduction cases.
- Explicitly excluded Vision2Web Level 3 full-stack tasks from the main scope because backend state, deployment, authentication, and long-horizon workflow requirements would turn the thesis into a full-stack agent benchmark rather than a GUI-quality evaluation benchmark.
- Updated [notes/thesis_outline.md](D:/master_thesis/notes/thesis_outline.md), [thesis/chapters/chapter3_methodology.tex](D:/master_thesis/thesis/chapters/chapter3_methodology.tex), and [notes/drafts/draft_ch4_benchmark.tex](D:/master_thesis/notes/drafts/draft_ch4_benchmark.tex) to reflect the new Track B data-source decision.
- Added `vision2web` BibTeX entries to [thesis/references.bib](D:/master_thesis/thesis/references.bib) and [proposal/references.bib](D:/master_thesis/proposal/references.bib).

## 2026-05-25

### Leaderboard scope clarified as generator ranking

- Confirmed the main leaderboard object as generated GUI submissions aggregated by generator model, not judge models.
- Updated [notes/thesis_outline.md](D:/master_thesis/notes/thesis_outline.md) so `RQ2` focuses on static multi-metric comparison of generated submissions and `RQ3` focuses on reproducible generation/evaluation protocol rather than judge-method reliability.
- Updated [thesis/chapters/chapter3_methodology.tex](D:/master_thesis/thesis/chapters/chapter3_methodology.tex) to demote LLM-as-a-judge from thesis object to optional scoring instrument / audit signal.
- Updated [thesis/chapters/chapter2_background_related_work.tex](D:/master_thesis/thesis/chapters/chapter2_background_related_work.tex) to frame judge-model bias as a limitation of automated scoring, not as the central research contribution.
- Updated [notes/track_b_vision2web_pilot_plan.md](D:/master_thesis/notes/track_b_vision2web_pilot_plan.md) to require same-prompt generator comparisons and to mark the current Claude `TB-GEN-v4` artifact as a smoke result rather than the fair comparison baseline against Qwen `TB-GEN-v6`.

### Compact Track B prompt smoke tests

- Added `--prompt-id` support to [scripts/generate_track_b_ui.py](D:/master_thesis/scripts/generate_track_b_ui.py) so `TB-GEN-v6`, `TB-GEN-v7`, and `TB-GEN-v8` can remain reproducible without silently replacing old prompt versions.
- Created `TB-GEN-v7` to test whether compact prompt wording can avoid ChatAnywhere HTTP 524 without increasing `max_tokens`. Claude generated an artifact at `max_tokens=20000`, but static gate failed because `Local Forms` was implemented as an inert `div`.
- Created `TB-GEN-v8` with exact workflow-label-to-route mappings and explicit `<a>` / `<button>` requirements. Claude and GWDG/SAIA Qwen fallback both generated valid `F09_elections_bc` artifacts at `max_tokens=20000`, and both passed `scripts/check_track_b_generation.py`.
- Updated [thesis/appendices/prompt_templates.tex](D:/master_thesis/thesis/appendices/prompt_templates.tex) with full `TB-GEN-v7` and `TB-GEN-v8` prompt templates and metadata.
- Added a project cost-control note to [AGENTS.md](D:/master_thesis/AGENTS.md): use the free GWDG/SAIA API key for future model-call smoke tests before paid/proxy providers whenever feasible.

## 2026-05-27

### Track B output-budget smoke test

- Added `TB-GEN-v9`, `TB-GEN-v10`, and `TB-GEN-v11` support to [scripts/generate_track_b_ui.py](D:/master_thesis/scripts/generate_track_b_ui.py), including automatic per-item workflow-control map derivation for v10/v11.
- Ran `TB-GEN-v10` on `F03_about_gitlab` with GWDG/SAIA `qwen3.6-35b-a3b` at `max_tokens=40000`. The run stopped normally with 15,213 completion tokens after 167.00 seconds, so the larger cap did not force a 40k output and did remove truncation risk. The static gate still failed because no exact clickable `GitLab Duo` label appeared, indicating a label-policy/prompt-format issue rather than an output-budget issue.
- Fixed [scripts/check_track_b_generation.py](D:/master_thesis/scripts/check_track_b_generation.py) workflow-label extraction so quoted click labels and `related to ...` actions are handled consistently with the generation prompt extractor.
- Updated [notes/track_b_vision2web_pilot_plan.md](D:/master_thesis/notes/track_b_vision2web_pilot_plan.md) with the v8-v11 smoke-test table, including completion tokens, elapsed time, and finish reason.
- Created `TB-GEN-v12` with a machine-checkable `visible_text`, `route_id`, and `required_element` workflow-control contract. `F03_about_gitlab` with GWDG/Qwen, 40k max tokens, and `--max-resources 60` stopped normally after 13,353 completion tokens, but still failed the gate because `GitLab Duo` appeared as non-clickable text while the clickable route label was renamed to alternatives such as `Product` or `See what's new`.
- Created `TB-GEN-v13` with a required workflow-control navigation block intended to be copied verbatim into the page header. Both GWDG/Qwen attempts with 40k max tokens and `--max-resources 60` failed with HTTP 500 before writing artifacts.
- Recorded the pilot decision to stop broad prompt iteration for the exact `GitLab Duo` label case. The next step is to freeze a practical prompt candidate, currently `TB-GEN-v9`, and adjust the gate so exact visible-label matching is hard only for explicitly quoted workflow labels; semantically phrased controls should be judged by route/interaction success with exact-label mismatch recorded as a diagnostic warning.
- Restored `TB-GEN-v9` as a selectable generator prompt in [scripts/generate_track_b_ui.py](D:/master_thesis/scripts/generate_track_b_ui.py) and saved its full template in [thesis/appendices/prompt_templates.tex](D:/master_thesis/thesis/appendices/prompt_templates.tex), because it is now the practical Track B baseline prompt.
- Updated [scripts/check_track_b_generation.py](D:/master_thesis/scripts/check_track_b_generation.py) so exact visible-label matching is an error only for quoted workflow labels. Non-quoted semantic click targets, such as `logo at the top of the page`, are now recorded as diagnostic warnings rather than hard smoke-test failures.
- Ran a frozen `TB-GEN-v9` cross-item smoke check with GWDG/SAIA `qwen3.6-35b-a3b` at `max_tokens=20000`: `F01_1daycloud` generated successfully, stopped normally after 11,129 completion tokens in 91.95 seconds, and passed the revised static gate with one semantic-label warning. Existing `F03_about_gitlab` and `F10_gourmania` v9 artifacts were re-gated and both passed. Two `F09_elections_bc` v9 attempts failed with GWDG HTTP 500 before writing artifacts, so they are recorded as provider-level failures, not generated-UI failures.
- Added [scripts/run_track_b_dynamic_workflow.py](D:/master_thesis/scripts/run_track_b_dynamic_workflow.py), a deterministic dependency-free route-simulation evaluator for Track B generated HTML. It uses the original `workflow.json` actions and validations, but reports route success separately from content-validation success so navigation failures are not conflated with destination-content failures.
- Ran the route-simulation evaluator on the three `TB-GEN-v9` static-gate-passing artifacts and wrote reports next to each artifact as `dynamic_workflow_report.json`, with the summary in [data/track_b/dynamic_workflow_v9_summary.json](D:/master_thesis/data/track_b/dynamic_workflow_v9_summary.json). Results: `F01_1daycloud` 9/12 cases, route success 1.000, content validation 0.750; `F03_about_gitlab` 8/8 cases, route success 1.000, content validation 1.000; `F10_gourmania` 7/8 cases, route success 1.000, content validation 0.875. Remaining failures are content-validation issues or checks that require a browser/CSS-state rule, such as active navigation highlighting.

### Leaderboard metric design draft

- Created [notes/leaderboard_metric_design.md](D:/master_thesis/notes/leaderboard_metric_design.md) to record the working design of the GUI-quality leaderboard metric system.
- Captured both the original 3-layer / 11-indicator draft (Technical pre-check + 6 static Likert dimensions + 4 dynamic indicators, mapped to ISO 9241-11, ISO/IEC 25010, WCAG 2.2, Lavie & Tractinsky, VisAWI, WebQual, UIClip, UI-Bench, FrontendBench, ArtifactsBench) and the revised 4-layer proposal that (a) merges the 6 static dimensions to 3 anchored Likert dimensions (Functional Completeness, Layout & Hierarchy, Visual Quality), (b) moves Basic Accessibility off the Likert scale to rule-based `axe-core` / Lighthouse checks, (c) defines an explicit composite aggregation `0.4 * static + 0.2 * a11y + 0.4 * dynamic` with all four numbers reported, and (d) adds pairwise comparison + Elo as a robustness check alongside Likert.
- Recorded the open questions (weighting, composite hyper-parameters, reference step count availability, minimum submissions per item for Elo) and a pilot plan that includes a FC / LH / VQ correlation analysis to test whether the three-dimension merge is empirically justified.
- The MLLM-as-judge prompt for the three anchored Likert dimensions and the pairwise comparison is **not yet written**. When written, it must be saved verbatim to [thesis/appendices/prompt_templates.tex](D:/master_thesis/thesis/appendices/prompt_templates.tex) with an explicit prompt id (e.g. `LB-JUDGE-v1`), per the project's appendix-prompt rule.

## 2026-05-28

### Track B benchmark protocol draft

- Created [notes/track_b_benchmark_protocol.md](D:/master_thesis/notes/track_b_benchmark_protocol.md) as the current supervisor-discussion draft for Track B. It fixes the benchmark as a fixed-item protocol rather than an open-ended UI scenario evaluator, defines the submission unit as an executable UI artifact, and separates benchmark-owned item context (screenshots, requirements, workflows, assets, route expectations, validation rules) from user/model submissions.
- Documented the current three implemented Track B layers: static technical gate, dynamic route success, and content validation success. The note also records why route and content should remain separate, current `TB-GEN-v9` pilot results, and discussion questions for whether visual-quality and accessibility layers should be part of the main leaderboard or auxiliary diagnostics.
- Updated [notes/leaderboard_metric_design.md](D:/master_thesis/notes/leaderboard_metric_design.md) so it no longer reads as if the broader four-layer visual/a11y/dynamic composite is already the implemented baseline. It now points to the smaller three-layer protocol as the current Track B baseline and keeps the broader metric system as an open candidate.
- Extended the frozen `TB-GEN-v9` GWDG/Qwen pilot beyond the initial passing items. `F05_balancingbirthbaby` generated a complete artifact (`finish_reason=stop`, 19,683 completion tokens, 179.02s) but failed the static gate because of an undefined `toggle()` handler and a missing exact `Classes & Events` clickable label; dynamic route/content scores were 0.400/0.500. `F06_community_dynamics` at 20k hit `finish_reason=length` and failed the static gate, while the 40k sensitivity run stopped normally with 11,384 completion tokens, passed the static gate, and scored route/content 1.000/0.400. `F02_401trucksource` timed out after the 360s GWDG read timeout before artifact creation.
- Updated [data/track_b/dynamic_workflow_v9_summary.json](D:/master_thesis/data/track_b/dynamic_workflow_v9_summary.json), [notes/track_b_benchmark_protocol.md](D:/master_thesis/notes/track_b_benchmark_protocol.md), and [notes/track_b_vision2web_pilot_plan.md](D:/master_thesis/notes/track_b_vision2web_pilot_plan.md) with these expanded-pilot results. The expanded batch strengthens the protocol distinction between provider failures, static-gate failures, route success, and content-validation success.

### Appendix prompt-template prune

- Pruned [thesis/appendices/prompt_templates.tex](D:/master_thesis/thesis/appendices/prompt_templates.tex): the Track B section had grown to six full prompt verbatims (`TB-GEN-v6/v7/v8/v9/v12/v13`), most of which were smoke-test diagnostics that never produced reported thesis metrics.
- Verified with grep across `thesis/` that **no thesis chapter cites any specific `TB-GEN` version**; all version references live in `notes/` and the appendix itself. Therefore only the prompt that produces reported artifacts needs full text.
- Kept full text for: `TA-PAIR-ZS-v1` and `TA-PAIR-RUBRIC-v1` (reported Track A results), and `TB-GEN-v9` (frozen practical baseline per the 2026-05-27 pilot decision; produces the reported Track B pilot/leaderboard artifacts).
- Removed the full `\subsection` verbatim blocks for `TB-GEN-v6`, `v7`, `v8`, `v12`, and `v13`. These remain summarized in the version-history table (Table `tab:track-b-generation-prompt-history`) and recoverable in full from the source template in [scripts/generate_track_b_ui.py](D:/master_thesis/scripts/generate_track_b_ui.py), per-run `generation_metadata.json`, and the revision log — consistent with the appendix's own inclusion rule (only result-/reproducibility-affecting prompts get full text).
- Rewrote the version-history intro paragraph and updated the table "Status in appendix" column accordingly (`Summarized only` for the removed versions; `Full text below` for `TB-GEN-v9`).
- Confirmed no dangling `\ref` to deleted labels (`prompt-tb-gen-v6/7/8/12/13`).
- Clean rebuild: `latexmk -pdf -interaction=nonstopmode -halt-on-error master_thesis.tex` → exit 0, no errors.
- Backup: `archive/backup/prompt_templates_2026-05-28_before-appendix-prune.tex`.

## 2026-06-05

### Track B model capability table

- Added [scripts/probe_model_capabilities.py](D:/master_thesis/scripts/probe_model_capabilities.py), a low-cost provider/model smoke-probe helper. Its default behavior lists provider models; optional `--chat-smoke` asks for `OK` only so high requested output caps can be tested without forcing long generation.
- Added [data/track_b/model_capabilities/model_capability_table_2026-06-05.json](D:/master_thesis/data/track_b/model_capabilities/model_capability_table_2026-06-05.json) to separate published token limits, local observed metadata, and provider error messages for current Track B candidate models.
- Ran a minimal GWDG smoke probe and saved [data/track_b/model_capabilities/model_capability_smoke_gwdg_2026-06-05.json](D:/master_thesis/data/track_b/model_capabilities/model_capability_smoke_gwdg_2026-06-05.json). It used one requested output token for `qwen3.6-35b-a3b` and `qwen3-omni-30b-a3b-instruct`, confirming both currently respond without spending a long generation budget.
- Updated [notes/provider_model_catalog_2026-06-04.md](D:/master_thesis/notes/provider_model_catalog_2026-06-04.md) with the 2026-06-05 token-limit interpretation. Basis: local `generation_metadata.json` files, the F03 `qwen3-omni` 65,536-token rejection log, and published OpenAI/Anthropic/Gemini model-limit documentation. Remaining uncertainty: several GWDG-hosted model hard limits are not exposed by the endpoint and must be treated as observed lower bounds, not exact maxima.

### Track B v16 compact input policy

- Added `TB-GEN-v16` and compact input packing to [scripts/generate_track_b_ui.py](D:/master_thesis/scripts/generate_track_b_ui.py). The new policy keeps legacy input for old prompt ids, but `TB-GEN-v16` uses a deduplicated route/evidence workflow summary, exact-vs-semantic workflow target separation, ranked resource paths, and prototype image downscaling before API upload.
- Added the full `TB-GEN-v16` template and metadata to [thesis/appendices/prompt_templates.tex](D:/master_thesis/thesis/appendices/prompt_templates.tex), marking it as a candidate rather than a frozen baseline.
- Created [notes/track_b_v16_input_compression.md](D:/master_thesis/notes/track_b_v16_input_compression.md). Dry-run basis: F03 prompt text changed from 18,878 characters for `TB-GEN-v15` legacy input to 13,424 characters for `TB-GEN-v16` compact input; F03 prototype images will be downscaled from 6,632--8,000 px tall full-page screenshots to 3,000 px longest side for compact runs. Remaining uncertainty: compact input may still lose some multi-step workflow nuance and needs a real smoke run before use in leaderboard comparisons.
- Ran F03 `TB-GEN-v16` compact smoke tests with two GWDG models. Both `qwen3.6-35b-a3b` and `qwen3-omni-30b-a3b-instruct` generated complete, non-truncated artifacts (`finish_reason=stop`) with about 16k prompt tokens, showing that compact input fixes the prior F03 qwen3-omni input-limit failure. After correcting the evaluator so `button or link related to GitLab Duo` is treated as a semantic target rather than a hard exact visible label, both artifacts pass the static gate with one semantic warning. Normalized browser workflow scores are: `qwen3.6-35b-a3b` 4/8, route 1.000, content 0.500; `qwen3-omni-30b-a3b-instruct` 3/8, route 0.750, content 0.500. Basis: `gate_report.json` and `browser_workflow_normalized_report.json` in the two generated F03 v16 run directories. Conclusion: create a new `TB-GEN-v17` if strengthening semantic route/evidence guarantees; do not silently edit v16.

## 2026-06-10

### Track B v16 dev-subset freeze check

- Ran the remaining `TB-GEN-v16` development-subset checks for
  `F01_1daycloud` and `F10_gourmania` with two free GWDG/SAIA reference models:
  `qwen3.6-35b-a3b` and `qwen3-omni-30b-a3b-instruct`. The existing F03 v16
  compact smoke runs from 2026-06-05 were reused.
- Added generated artifacts and reports under:
  - `data/track_b/items/F01_1daycloud/generated/gwdg_qwen36_35b_v16_f01_dev/`
  - `data/track_b/items/F10_gourmania/generated/gwdg_qwen36_35b_v16_f10_dev/`
  - `data/track_b/items/F01_1daycloud/generated/gwdg_qwen3_omni_30b_v16_f01_dev/`
  - `data/track_b/items/F10_gourmania/generated/gwdg_qwen3_omni_30b_v16_f10_dev/`
- Wrote normalized browser workflow reports for the new F01/F10 runs so they
  are comparable with the existing F03 normalized reports.
- Updated `notes/track_b_v16_input_compression.md` with the result table and
  interpretation. Basis: each run's `generation_metadata.json`,
  `gate_report.json`, and `browser_workflow_normalized_report.json`.
- Result summary: `qwen3.6-35b-a3b` produced complete artifacts for F01/F03/F10
  and passed the relaxed static gate on all three; normalized workflow scores
  were 7/12, 4/8, and 6/8. `qwen3-omni-30b-a3b-instruct` passed F03 but hit
  `finish_reason=length` for F01 and F10 at `max_tokens=20000`, so it does not
  satisfy the current two-reference-model freeze criterion.
- Remaining uncertainty: this does not yet prove that v16's prompt wording is
  insufficient, because the qwen3-omni failures are capacity/truncation failures.
  The next decision is whether to rerun qwen3-omni with a documented larger
  output cap, or use a second reference model whose capacity is sufficient under
  the fixed v16 compact input profile.

### Track B max-token policy correction

- Corrected `scripts/generate_track_b_ui.py` so OpenAI-compatible providers
  (`openai`, `gwdg-openai`) can be called with `--max-tokens none` / `omit` /
  `null`, which omits the `max_tokens` field from the request payload. Previous
  behavior always sent the script default `max_tokens=20000` unless another
  integer was supplied.
- Kept Anthropic-compatible requests conservative: `anthropic` and
  `chatanywhere-anthropic` still require an explicit integer `max_tokens`
  setting because their API path expects one.
- Updated `notes/track_b_v16_input_compression.md` to mark the 2026-06-10
  qwen3-omni F01/F10 failures as 20k-capped sensitivity results, not as evidence
  for an uncapped/no-`max_tokens` generation policy.
- Basis: earlier notes and methodology already state that the evaluation should
  avoid presenting a fixed truncating output-token cap as the final policy
  (`notes/metric_specification.md`, `thesis/chapters/chapter3_methodology.tex`,
  and `notes/thesis_outline.md`). Validation: `py -3 -m py_compile
  scripts/generate_track_b_ui.py` and a `--max-tokens none --dry-run` command
  both passed.

### Track B qwen3-omni no-`max_tokens` rerun

- Re-ran the qwen3-omni `TB-GEN-v16` F01/F10 dev-subset cases with
  `--max-tokens none`, using new run names:
  `gwdg_qwen3_omni_30b_v16_f01_dev_omit_maxtokens` and
  `gwdg_qwen3_omni_30b_v16_f10_dev_omit_maxtokens`.
- F01 still failed structurally with `finish_reason=length`, but completion
  tokens increased from 20,000 to 41,740, confirming that the request no longer
  used the script's 20k cap and that the remaining failure is provider/model
  output behavior for this item.
- F10 changed from capped `finish_reason=length` to `finish_reason=stop`,
  passed the relaxed static gate with three warnings, and kept the same
  normalized workflow score pattern (5/8, route 0.750, content 0.750).
- Updated `notes/track_b_v16_input_compression.md` with the capped-vs-omitted
  comparison table. Basis: each run's `generation_metadata.json`,
  `gate_report.json`, and `browser_workflow_normalized_report.json`.
- Conclusion: omit `max_tokens` for future OpenAI-compatible Track B generation
  when accepted by the provider. `TB-GEN-v16` still does not meet the current
  two-reference-model freeze criterion with qwen3-omni, because F01 remains
  incomplete without a client-side output cap.

### Track B failure taxonomy and convergence decision

- Added `notes/track_b_failure_taxonomy_and_decisions.md` to consolidate the
  repeated Track B debugging issues into benchmark categories and explicit
  decisions.
- Defined five failure categories: provider failure, completion/truncation
  failure, static technical gate failure, dynamic route failure, and content
  validation failure.
- Recorded concrete cases already observed, including F03 qwen3-omni context
  overflow, F09/F02 provider failures, F10 qwen3-omni cap sensitivity, and F01
  qwen3-omni no-`max_tokens` truncation after 41,740 completion tokens.
- Decision: stop prompt tuning for F01/qwen3-omni. Treat it as a model/provider
  completion failure under the fixed v16 prompt rather than an unresolved prompt
  bug.
- Next engineering step: build a small failure-aware v16 dev-subset demo table
  from existing F01/F03/F10 runs before doing more generation.

### Track B v16 dev-subset pipeline demo

- Added `scripts/build_track_b_dev_subset_demo.py`, a narrow aggregation script
  for the supervisor-meeting demo. It does not run new generation or scoring; it
  reads existing v16 F01/F03/F10 artifacts, gate reports, and normalized browser
  workflow reports.
- Generated:
  - `data/track_b/leaderboard/dev_subset_v16_failure_demo.json`
  - `data/track_b/leaderboard/dev_subset_v16_failure_demo.md`
- Demo scope: `TB-GEN-v16`, compact input, items `F01_1daycloud`,
  `F03_about_gitlab`, and `F10_gourmania`; model/config rows for
  `qwen3.6-35b-a3b` and `qwen3-omni-30b-a3b-instruct`.
- Demo result: `qwen3.6-35b-a3b` generated 3/3 artifacts, passed static gate
  3/3, and has average route/content/task scores 1.000/0.611/0.611.
  `qwen3-omni-30b-a3b-instruct` generated 3/3 artifacts, passed static gate
  2/3, has one truncation failure, and has eligible-artifact average
  route/content/task scores 0.750/0.625/0.500.
- Updated `notes/track_b_failure_taxonomy_and_decisions.md` to mark the
  failure-aware demo artifact as implemented. Validation: `py -3 -m py_compile
  scripts/build_track_b_dev_subset_demo.py` and `py -3
  scripts/build_track_b_dev_subset_demo.py` both succeeded.

### Track B F06 v16 demo extension

- Ran one additional normalized demo item, `F06_community_dynamics`, with
  `TB-GEN-v16`, compact input, GWDG `qwen3.6-35b-a3b`, and `--max-tokens none`.
  Run directory:
  `data/track_b/items/F06_community_dynamics/generated/gwdg_qwen36_35b_v16_f06_dev_omit_maxtokens/`.
- Result: generation stopped normally (`finish_reason=stop`), with 28,901
  prompt tokens, 28,353 completion tokens, and 213.87 seconds latency. The
  relaxed static gate passed with zero errors and zero warnings.
- Normalized browser workflow result: 4/10 cases, route success 1.000, content
  validation 0.400, task success 0.400. Interpretation: this is an eligible
  artifact with strong route behavior but weak destination-content evidence.
- Updated `scripts/build_track_b_dev_subset_demo.py` and regenerated
  `data/track_b/leaderboard/dev_subset_v16_failure_demo.json` and `.md` so the
  meeting demo now covers four normalized items for `qwen3.6-35b-a3b`
  (F01/F03/F06/F10) and three items for qwen3-omni (F01/F03/F10).

### Tuzi OpenAI-compatible provider smoke test

- Added Tuzi support as `tuzi-openai` in:
  - `scripts/probe_model_capabilities.py`
  - `scripts/generate_track_b_ui.py`
  - `scripts/run_visual_judge.py`
  - `.env.example`
- Basis: Tuzi is used as an OpenAI-compatible provider with
  `TUZI_BASE_URL=https://api.tu-zi.com/v1`; no API key value was recorded.
- Model-list and tiny chat smoke:
  `py -3 scripts/probe_model_capabilities.py --provider tuzi-openai --model
  gpt-4.1-mini --chat-smoke --output-cap 1`.
  Output:
  `data/track_b/model_capabilities/model_capability_smoke_tuzi-openai_20260612_002229.json`.
  Result: `/models` returned HTTP 200 with 748 model IDs; `gpt-4.1-mini`
  returned HTTP 200, `finish_reason=stop`, 12 prompt tokens, 2 completion
  tokens, and 1.874 seconds latency.
- Track B generation smoke:
  `py -3 scripts/generate_track_b_ui.py --item F10_gourmania --provider
  tuzi-openai --model gpt-4.1-mini --prompt-id TB-GEN-v16 --input-profile
  compact --max-prototypes 1 --max-tokens 12000 --run-name
  tuzi_gpt41mini_v16_f10_smoke`.
  Result: generation stopped normally (`finish_reason=stop`) after 81.97
  seconds with 5,028 prompt tokens, 7,574 completion tokens, and 12,602 total
  tokens.
- Static gate:
  `py -3 scripts/check_track_b_generation.py --item F10_gourmania --run
  tuzi_gpt41mini_v16_f10_smoke`, saved as
  `data/track_b/items/F10_gourmania/generated/tuzi_gpt41mini_v16_f10_smoke/gate_report.json`.
  Result: passed with zero error failures and one warning for a missing local
  image source.
- Standard screenshot capture:
  `node scripts/capture_track_b_standard_screenshots.js --item F10_gourmania
  --run tuzi_gpt41mini_v16_f10_smoke --full-page`.
  Result: captured 1/1 detected route.
- Dynamic workflow:
  `py -3 scripts/run_track_b_dynamic_workflow.py --item F10_gourmania --run
  tuzi_gpt41mini_v16_f10_smoke`.
  Result: 5/8 cases, route success 1.000, content validation 0.625, task
  success 0.625.
- Updated `notes/provider_model_catalog_2026-06-04.md` and
  `data/track_b/model_capabilities/model_capability_table_2026-06-05.json` with
  Tuzi configuration, observed model availability, smoke results, and the
  current provider-use order: GWDG/SAIA first; Tuzi `gpt-4.1-mini` as the first
  low-cost paid/proxy fallback; ChatAnywhere standard models as the next
  fallback; ChatAnywhere `-ca` variants only for explicitly labelled low-cost
  experiments.
- Pricing basis and uncertainty: ChatAnywhere publishes per-model token prices
  in its documentation. Tuzi's public page describes price/routing groups, but
  the local `/models` response does not expose per-model price fields, so Tuzi
  cost estimates for reported runs should use the current account billing page
  or transaction record at the time of the run.
- Validation: `py -3 -m json.tool
  data/track_b/model_capabilities/model_capability_table_2026-06-05.json` and
  `py -3 -m py_compile scripts/probe_model_capabilities.py
  scripts/generate_track_b_ui.py scripts/run_visual_judge.py` both succeeded.

### Track B raw efficiency reporting in leaderboard builders

- Updated `scripts/build_track_b_dev_subset_demo.py` and
  `scripts/build_track_b_mini_leaderboard.py` to surface raw efficiency fields
  in leaderboard outputs: average prompt tokens, completion tokens, total
  tokens, latency, completion reliability, failed artifact count, and cost
  status.
- Basis: existing `generation_metadata.json` files already record prompt,
  completion, total token usage, finish reason, and elapsed seconds. The
  provider catalog records that exact USD costs should not be inferred without
  a stable provider price or account billing reference.
- Decision: use `raw_only_no_usd_reference` for the current efficiency status.
  `efficiency_score`, `average_cost_usd`, and `overall_score` remain null until
  a stable cost reference or billing source is fixed. This avoids presenting
  proxy/GWDG/Tuzi costs as precise comparable USD values.
- Scope boundary: no visual-judge files or adjudicated-anchor outputs were
  modified. Accessibility weighted-density implementation remains a separate
  future task.
