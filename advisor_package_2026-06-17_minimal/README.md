# GUI Benchmark Review Package - Minimal Version

Please start with `supervisor_brief.md`. It answers the main questions from the
2026-06-16 meeting in one file.

## What Is Included

| File/folder | What it is |
| --- | --- |
| `supervisor_brief.md` | Main explanation: dataset, benchmark setup, static/dynamic metrics, LLM judge, human annotation, final benchmark scope, and open questions. |
| `slides/track_b_progress_2026-06-12_v6.pptx` | PowerPoint version shown in the meeting. |
| `dataset/dataset_description.md` | Dataset source, links, subset, and one included sample item. |
| `dataset/sample_item_F01/` | One concrete benchmark item: requirement, workflow, source metadata. |
| `examples/` | Five compact examples: original Qwen, GPT-4o-mini, Claude pages, plus one severe jitter page. |
| `implementation/` | Copies of the core scripts for static gate, dynamic/browser workflow, visual judge, and leaderboard aggregation. |
| `results/leaderboard_preview.md` | Preliminary leaderboard demo. |
| `literature_and_citations.md` | Short citation audit for the current design reasons. |
| `repository_link.txt` | Supplementary GitHub remote link. |

## Reading Order

1. `supervisor_brief.md`
2. `dataset/dataset_description.md`
3. `literature_and_citations.md`
4. `slides/track_b_progress_2026-06-12_v6.pptx`

The examples and leaderboard are supporting material only.

## Caveat

The current leaderboard values, LLM judge validation, and human annotation are
preliminary. They are included for review of the method, not as final thesis
results.
