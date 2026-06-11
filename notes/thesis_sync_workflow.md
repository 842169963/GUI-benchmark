# Thesis Sync Workflow

Status: working process note.

This note defines when to run a manuscript synchronization pass. It exists
because thesis code, notes, data, and manuscript files may be edited by multiple
agents or tools in parallel.

## When to run a sync pass

Run a thesis sync pass at the end of each substantive phase, especially after:

- a prompt version is introduced, frozen, rejected, or materially revised;
- an evaluation metric formula changes;
- a new experiment produces a result that may support a thesis claim;
- a human annotation protocol or LLM judging protocol changes;
- a supervisor-meeting decision changes the thesis direction;
- several agents have edited overlapping experiment, note, or manuscript files;
- before sending a draft, building a PDF for review, or committing a milestone.

## Sync pass checklist

1. Inspect `git status --short` and separate manuscript, notes, scripts, data,
   and generated-output changes.
2. Read `notes/revision_log.md` since the last manuscript edit and list every
   thesis-impacting change.
3. For each change, decide one of:
   - `write to manuscript now`;
   - `record in appendix only`;
   - `keep in notes until decision/data is stable`;
   - `do not report`.
4. Update thesis chapters only with claims that have a recorded basis: result
   files, scripts, notes, supervisor feedback, explicit design decisions, or
   citations.
5. Add or update prompt templates in
   `thesis/appendices/prompt_templates.tex` for thesis-impacting prompts.
6. Record the sync pass in `notes/revision_log.md`, including files changed,
   sources used, and remaining uncertainty.
7. Run a lightweight validation, at minimum a LaTeX compile or targeted syntax
   check if compile dependencies are unavailable.

## What not to do during sync

- Do not silently convert unstable notes into final result claims.
- Do not overwrite another agent's manuscript edits without reading them.
- Do not add invented background, novelty, benchmark, or result claims.
- Do not store API keys, private tokens, or unnecessary personal data in prompt
  records or appendices.

## Recommended cadence

During active experimentation, run this pass daily or after each major
experiment block. During writing-heavy periods, run it before each PDF build and
before each supervisor-facing draft.
