# Prompt Preservation Policy

This policy decides which prompts must be preserved for the thesis and how they
must be recorded. It is intentionally selective: preserve prompts that affect
research validity, not every chat message.

## Core Rule

Save a prompt when changing or omitting it could change a thesis result, a
reported metric, a benchmark protocol, an annotation protocol, or a
reproducibility claim.

## Must Save

Save the exact text and metadata for:

- LLM-as-a-judge prompts for pairwise comparison, rubric scoring, ranking, or
  preference selection.
- GUI generation prompts used to create Track B interfaces.
- Dynamic evaluation prompts, including action-plan elicitation from screenshot,
  DOM, and task descriptions.
- Human annotation instructions, calibration examples, score anchors, and
  annotation form wording.
- Output-format instructions and JSON schemas when they constrain model
  responses used in metrics.
- Few-shot examples, rubrics, system/developer messages, image-order labels, DOM
  excerpts, or other context included with an experimental prompt.
- Any prompt variant used in an ablation, pilot, formal run, or reported
  comparison.

## Usually Do Not Save

Do not preserve routine prompts unless they become part of the method:

- Coding-assistant chats used to edit scripts or LaTeX.
- Literature search, summarisation, brainstorming, or wording-polish prompts.
- Planning, debugging, or project-management prompts.
- One-off exploratory prompts whose outputs are not used in experiments,
  benchmark construction, annotation, or thesis claims.

## Required Metadata

Every saved prompt record should include:

- Prompt ID, for example `TA-PAIR-ZS-v1`, `TA-PAIR-RUBRIC-v1`,
  `TB-GEN-v1`, or `TB-DYN-PLAN-v1`.
- Track and task: Track A, Track B, annotation, dynamic validation, etc.
- Purpose: what result or protocol this prompt supports.
- Exact prompt text, including line breaks.
- Message structure: system/developer/user roles when applicable.
- Non-text inputs: image order, screenshot labels, DOM snapshot, task text,
  examples, rubrics, assets, or schemas.
- Model/provider and exact model identifier.
- Date/time and timezone of use.
- Parameters: temperature, seed, max tokens, top-p, repetitions, order-swap
  status, viewport if relevant.
- Source files: script path, result JSON path, generated data path, or appendix
  location.
- Version note: what changed compared with the previous prompt version.

## Storage Locations

Use all relevant storage layers:

- Source implementation: keep reusable templates in scripts or a dedicated
  prompt/template file.
- Result artifacts: write the actual prompt used into result JSON metadata.
- Thesis appendix: add thesis-impacting prompt templates to
  `thesis/appendices/prompt_templates.tex`. The appendix should prioritize
  final, formal-run, reported-ablation, or otherwise central reproducibility
  templates. Superseded pilot versions may be summarized in a version table
  instead of reproduced in full, provided the exact historical prompts remain
  recoverable from source files, result metadata, notes, or version control.
- Notes: when useful, mention new prompt versions in `notes/revision_log.md` or
  the relevant experiment progress note.

## Versioning Rule

Do not silently overwrite prompts that have already been used in a run. Create a
new prompt ID or version suffix, and keep the old prompt recoverable. If a result
file used an older prompt, leave its metadata unchanged.

## Privacy and Safety

Never save API keys, authentication tokens, private credentials, or unnecessary
personal data. If a prompt contains sensitive content that is not required for
reproducibility, redact it and state the redaction clearly.
