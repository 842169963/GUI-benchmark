# GUI-benchmark

Master's thesis proposal workspace for GUI quality evaluation with multimodal LLMs.

## Main files

- `thesis_proposal.tex`: main LaTeX source of the proposal
- `thesis_proposal.pdf`: latest compiled PDF
- `thesis_proposal.docx`: Word export of the proposal
- `references.bib`: bibliography database

## Supporting files

- `revision_log.md`: detailed record of edits and decisions
- `thesis_progress.md`: short progress summary
- `make_docx.py`: helper script for generating the `.docx` version
- `backup/`: dated snapshots of previous proposal versions and notes

## Template files

The following files come from the journal/template setup and are kept in the repository so the project can compile reproducibly:

- `sn-jnl.cls`
- `*.bst`
- `*.sty`

## Notes on repository layout

This repository currently uses a simple flat layout:

- core writing files stay in the root directory
- historical snapshots stay in `backup/`
- LaTeX build artifacts such as `.aux`, `.log`, and `.out` are ignored via `.gitignore`

This is intentionally conservative so the LaTeX build keeps working without extra path configuration.

## Suggested future cleanup

If the repository grows, a light reorganization would be reasonable:

- keep `thesis_proposal.tex`, `references.bib`, and the latest output files in the root
- move progress notes into a `notes/` folder
- move helper scripts into a `scripts/` folder
- remove unused template sample files if they are confirmed unnecessary

