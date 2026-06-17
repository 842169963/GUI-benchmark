# Visual Judge Workflow Summary

The full repository contains the visual judge runner used for provider calls.
This minimal package includes a workflow summary instead of the provider-calling
script, to avoid shipping API-provider plumbing or environment-variable names.

Workflow:

1. Load standardized screenshots for a generated artifact.
2. Build the LB-JUDGE visual checklist prompt.
3. Send each screenshot to the multimodal judge.
4. Parse structured JSON answers for the 16 checklist items.
5. Repeat judge calls for stability where configured.
6. Apply item-level majority vote across repetitions.
7. Compute dimension, page, and artifact visual scores.
8. Compare the judge against human pilot labels using Pearson correlation and
   Cohen's kappa.

Related package file:

- `score_track_b_visual.py`

Related full-repository files:

- `scripts/run_visual_judge.py`
- `scripts/prompts/LB-JUDGE-v1.md`
- `data/track_b/visual_human_review/`
