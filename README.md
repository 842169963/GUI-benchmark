# Master Thesis Workspace

This repository is organized as two separate LaTeX writing projects:
the finished thesis proposal and the developing thesis manuscript.

## Main Folders

- `proposal/`: proposal source, proposal PDF, Word export, annotated PDF, bibliography, and the Springer template files needed to compile the proposal.
- `thesis/`: formal thesis manuscript source, compiled thesis PDF, chapter files, and thesis bibliography.
- `notes/`: outlines, revision logs, supervisor feedback, progress notes, and original draft snippets.
- `literature/`: paper PDFs and reading material.
- `archive/`: dated backups and previous snapshots.
- `scripts/`: helper scripts.

## Compile Targets

- Proposal: open `proposal/thesis_proposal.tex` and build it in VS Code.
- Thesis body: open `thesis/master_thesis.tex` and build it in VS Code.

The chapter files under `thesis/chapters/` contain root-file comments, so building from a chapter file should still compile `thesis/master_thesis.tex`.

## Current Thesis Draft

The thesis body currently contains:

- `thesis/chapters/chapter1_introduction.tex`: placeholder introduction.
- `thesis/chapters/chapter2_background_related_work.tex`: integrated research-gap draft.
- `thesis/chapters/chapter3_methodology.tex`: integrated methodology draft.

The original generated draft snippets are preserved under `notes/drafts/`.
