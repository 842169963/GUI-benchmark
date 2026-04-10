# Thesis Progress Log

## Working Rule

- Canonical project folder: `D:\master_thesis`
- Main source file: `D:\master_thesis\thesis_proposal.tex`
- Reference file: `D:\master_thesis\references.bib`
- PDF output: `D:\master_thesis\thesis_proposal.pdf`
- Detailed edit history: `D:\master_thesis\notes\revision_log.md`

## 2026-04-10

### Current status

- The proposal source has been restored after an accidental overwrite from an older local version.
- The current PDF builds successfully from `D:\master_thesis`.
- The abstract is visible again in the compiled PDF.
- The current title is:
  `Beyond Pairwise GUI Quality Judgments: Multi-Dimensional Evaluation with Modern Multimodal LLMs`

### Proposal scope at the moment

- Main focus:
  screenshot-based GUI quality evaluation
- Main methodological elements:
  pairwise comparison, rubric-based assessment, human annotation, and LLM-as-a-judge strategies
- Additional artifact:
  benchmark + lightweight leaderboard
- Dynamic component:
  a small complementary evaluation module with computer-use agents

### Key decisions already made

- Use only `D:\master_thesis` as the canonical working directory.
- Do not rely on the desktop folder as the main editable version.
- Keep concrete paper names such as `UIClip` out of the abstract.
- Keep standard field terms such as `rubric-based assessment`, `zero-shot prompting`, and `rubric-guided scoring` in the abstract where useful.
- Treat dynamic evaluation as an extension, not as the main thesis focus.

### Supervisor feedback already addressed

- Clarified the meaning of order-swapped pairwise comparisons.
- Added benchmark / leaderboard as an explicit deliverable.
- Added a limited dynamic evaluation extension with computer-use agents.
- Revised the abstract to be more self-contained.

### Immediate next tasks

- Review remaining supervisor comments one by one.
- Check whether the benchmark / leaderboard wording should be tightened further.
- Decide whether the dynamic evaluation description should stay at its current level or be narrowed further.
- Continue recording every confirmed change in `notes/revision_log.md`.

### Lessons learned

- After important edits, keep a clean compiled PDF and source snapshot.
- Avoid overwriting the main file after a failed local build.
- When something looks wrong in the PDF, verify both the source file and the compiled output before editing further.
