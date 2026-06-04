# Project Agent Instructions

These instructions apply to every agent working in this repository.

## Thesis text provenance and change recording

When adding or materially revising thesis manuscript content, do not invent
claims, facts, numbers, comparisons, or methodological justifications without a
traceable basis.

- Add an appropriate citation for literature-backed claims.
- For project-specific claims, base the text on recorded experiment outputs,
  scripts, notes, supervisor feedback, or explicit design decisions, and mention
  that basis in the relevant note or revision record.
- If a sentence is an interpretation or scope decision rather than a cited fact,
  make the reason clear in the text or record it in `notes/revision_log.md`.
- Record every substantive thesis-text change in `notes/revision_log.md`,
  including the files changed, the source or rationale used, and any remaining
  uncertainty.
- Do not add unsupported background statements, result claims, benchmark claims,
  or novelty claims merely because they sound plausible.

## Thesis-impacting prompt preservation

Prompts are part of the experimental method for this thesis. When working on
experiments or thesis text, preserve only prompts that can affect the thesis
claims, reported results, benchmark protocol, human annotation protocol, or
reproducibility.

Follow the detailed rule in `notes/prompt_preservation_policy.md`.

In short:

- Save prompts used for LLM judging, GUI generation, rubric scoring, action-plan
  elicitation, human annotation instructions, output schemas, or any ablation
  reported in the thesis.
- Do not save routine coding-assistant chats, brainstorming, language polishing,
  literature-search prompts, or operational prompts unless the thesis explicitly
  uses them as experimental material.
- For every saved prompt, record the exact prompt text, prompt identifier,
  purpose, experiment/track, model/provider, date, key parameters, output schema,
  source script/result file, and whether images, DOM snapshots, examples, or
  rubrics were included.
- Add thesis-impacting prompt templates to the thesis appendix file:
  `thesis/appendices/prompt_templates.tex`.
- When modifying a thesis-impacting prompt, create a new version identifier
  instead of silently replacing the old one.

Never store API keys, secrets, private tokens, or unnecessary personal data in
prompt records or appendices.

## Cost control for model experiments

When testing Track B generation prompts or other model-calling scripts, use the
free GWDG/SAIA API key for smoke tests first whenever it can support the task.
Only use paid or proxy providers after the prompt, gate, and pipeline have been
validated on the cheaper/free provider, unless the experiment specifically
requires that provider.
