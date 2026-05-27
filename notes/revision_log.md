# Revision Log

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

### Leaderboard metric design draft

- Created [notes/leaderboard_metric_design.md](D:/master_thesis/notes/leaderboard_metric_design.md) to record the working design of the GUI-quality leaderboard metric system.
- Captured both the original 3-layer / 11-indicator draft (Technical pre-check + 6 static Likert dimensions + 4 dynamic indicators, mapped to ISO 9241-11, ISO/IEC 25010, WCAG 2.2, Lavie & Tractinsky, VisAWI, WebQual, UIClip, UI-Bench, FrontendBench, ArtifactsBench) and the revised 4-layer proposal that (a) merges the 6 static dimensions to 3 anchored Likert dimensions (Functional Completeness, Layout & Hierarchy, Visual Quality), (b) moves Basic Accessibility off the Likert scale to rule-based `axe-core` / Lighthouse checks, (c) defines an explicit composite aggregation `0.4 * static + 0.2 * a11y + 0.4 * dynamic` with all four numbers reported, and (d) adds pairwise comparison + Elo as a robustness check alongside Likert.
- Recorded the open questions (weighting, composite hyper-parameters, reference step count availability, minimum submissions per item for Elo) and a pilot plan that includes a FC / LH / VQ correlation analysis to test whether the three-dimension merge is empirically justified.
- The MLLM-as-judge prompt for the three anchored Likert dimensions and the pairwise comparison is **not yet written**. When written, it must be saved verbatim to [thesis/appendices/prompt_templates.tex](D:/master_thesis/thesis/appendices/prompt_templates.tex) with an explicit prompt id (e.g. `LB-JUDGE-v1`), per the project's appendix-prompt rule.
