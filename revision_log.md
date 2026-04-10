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
- Added [thesis_progress.md](D:/master_thesis/thesis_progress.md) as a separate project-level progress record to track current scope, completed decisions, supervisor feedback already addressed, and next tasks.
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
