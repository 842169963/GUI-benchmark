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
