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
