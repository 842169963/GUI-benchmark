# GUI-benchmark

Master's thesis proposal workspace for GUI quality evaluation with multimodal LLMs.

## Repository layout

- `thesis_proposal.tex`: main LaTeX source of the proposal
- `thesis_proposal.pdf`: latest compiled PDF
- `thesis_proposal.docx`: Word export of the proposal
- `references.bib`: bibliography database
- `thesis_proposal annotation.pdf`: supervisor-annotated review copy
- `backup/`: dated snapshots of previous proposal versions and notes
- `notes/`: progress notes and revision history
- `scripts/`: helper scripts

## Notes and scripts

- `notes/revision_log.md`: detailed record of edits and decisions
- `notes/thesis_progress.md`: short progress summary
- `scripts/make_docx.py`: helper script for generating the `.docx` version

## Template files

The following files come from the journal/template setup and are kept in the repository so the project can compile reproducibly:

- `sn-jnl.cls`
- `*.bst`
- `*.sty`

## Why some files stay in the root

The repository keeps the main writing and LaTeX template files in the root on purpose. This makes the project easier to compile without extra path configuration. Build artifacts such as `.aux`, `.log`, and `.out` are ignored via `.gitignore`.
