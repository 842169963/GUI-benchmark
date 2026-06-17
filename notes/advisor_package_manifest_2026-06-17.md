# Advisor Review Package Manifest - 2026-06-17

Status: draft manifest for selecting files to send to the supervisor. This is
not the final package and not thesis manuscript text. It has been checked
against the cleaned meeting interpretation in
`notes/meeting_2026-06-16_supervisor_cleaned.md`.

Package name:

```text
advisor_package_2026-06-17/
```

## Mapping

| Supervisor request | Package file or folder | Current project source | Status | Note |
| --- | --- | --- | --- | --- |
| Slides shown in the meeting | `slides/track_b_progress_2026-06-12_v6.pptx` | `presentations/track_b_progress_2026-06-12_v6.pptx` | Ready to copy | Use v6 because this is the version shown to the supervisor. Optional PDF export is not required. |
| Short package overview | `README.md` | Needs to be written from current notes | Needs concise wrapper | Should explain what the package contains and which parts are preliminary. |
| Dataset source and item structure | `dataset/dataset_description.md` | `data/track_b/items/`, `data/track_b/vision2web_raw/`, `data/track_b/vision2web_pilot_manifest.json`, `notes/benchmark_item_schema.md` | Needs wrapper | The raw material exists, but the supervisor needs a direct explanation of source, subset, and item fields. |
| Dataset sample | `dataset/sample_items/` or `dataset_link.txt` | Example items under `data/track_b/items/F01_1daycloud/`, `data/track_b/items/F03_about_gitlab/`, `data/track_b/items/F06_community_dynamics/`, `data/track_b/items/F09_elections_bc/`, `data/track_b/items/F10_gourmania/` | Ready after selection | Copy a few small item folders or provide a link if the full dataset is too large. |
| Benchmark setup | `methodology/benchmark_setup.md` | `notes/track_b_benchmark_protocol.md`, `notes/benchmark_item_schema.md` | Needs wrapper | Should summarize item, generation artifact, evaluation layers, and leaderboard unit. |
| Generation protocol | `methodology/generation_pipeline.md` | `scripts/generate_track_b_ui.py`, `scripts/check_track_b_generation.py`, `data/track_b/items/*/generated/*/generation_metadata.json`, `notes/track_b_benchmark_protocol.md` | Needs concise explanation | Do not send API keys or `.env`. Include prompt/version/provider rules only if relevant. |
| Static technical metrics | `methodology/static_technical_metrics.md` | `notes/metric_specification.md`, `scripts/check_track_b_generation.py` | Mostly ready, needs cleanup | Explain gate checks and what pass/fail means. |
| Static visual metrics / checklist | `methodology/static_visual_metrics.md` | `notes/metric_specification.md`, `scripts/score_track_b_visual.py`, `scripts/run_visual_judge.py`, `scripts/prompts/LB-JUDGE-v1.md` | Needs careful framing | Current checklist needs source mapping and should be described as under validation. |
| Dynamic/browser metrics | `methodology/dynamic_browser_metrics.md` | `notes/track_b_browser_workflow_v1_experiment.md`, `scripts/run_track_b_dynamic_workflow.py`, `scripts/run_track_b_browser_workflow.js`, `data/track_b/browser_workflow_summary.json`, `data/track_b/dynamic_workflow_v9_summary.json` | Needs wrapper | Separate route simulation from real browser workflow validation. |
| Accessibility metrics | `methodology/accessibility_metrics.md` | `scripts/run_track_b_accessibility.js`, generated `accessibility_report.json` files | Optional / brief | Include only if it is part of the displayed benchmark. |
| LLM judge protocol | `methodology/llm_judge_protocol.md` | `scripts/run_visual_judge.py`, `scripts/prompts/LB-JUDGE-v1.md`, `data/track_b/visual_human_review/llm_judge_*.json` | Needs wrapper | State model, prompt variants, repeated calls, majority vote, and item-level labels. |
| Human annotation / agreement | `methodology/human_annotation_pilot.md` | `data/track_b/visual_human_review/human_vs_llm_comparison*.json`, `data/visual_human_review_extended_rater2*.json`, `scripts/compute_interrater.py`, `scripts/compare_visual_human_llm.py` | Needs cautious wording | Label as pilot reliability check, not final ground truth. |
| Generated original examples | `examples/original_generated/` | `data/track_b/items/*/generated/*/index.html`, `standard_screenshots/` | Ready after selecting examples | Include 2-3 representative examples, not every generated artifact. |
| Jitter/degraded examples | `examples/jittered_generated/` | `data/track_b/items/*/generated/*_jitter_mild/`, `data/track_b/items/*/generated/*_jitter_severe/`, `data/track_b/visual_human_review/jitter_mild_comparison.html` | Ready after selecting examples | Good evidence for quality variation and judge sensitivity. |
| Weak-model / low-quality examples | `examples/weak_model_outputs/` | Generated folders and leaderboard records under `data/track_b/items/*/generated/` and `data/track_b/leaderboard/` | Needs selection | Include only if clearly labeled as preliminary/demo. |
| Leaderboard preview | `results/leaderboard_preview.md` | `data/track_b/leaderboard/model_leaderboard_tb_gen_v16.md`, `data/track_b/leaderboard/dev_subset_v16_schema_v1_demo.md` | Ready but preliminary | Mark as demo/pilot results, not final thesis results. |
| Detailed artifact results | `results/artifact_results_sample.json` | `data/track_b/leaderboard/artifact_results_tb_gen_v16.json` | Optional | Useful if supervisor wants exact score records. |
| Open questions for supervisor | `open_questions_for_supervisor.md` | Meeting notes and current uncertainty | Needs to be written | Ask about dataset suitability, binary vs Likert, judge validation depth, and static/dynamic aggregation. |
| Email draft | `email_draft_to_supervisor.md` | Meeting notes | Optional | Useful after package contents are fixed. |

## Do Not Send

- `.env`
- `api key free gwdg.txt`
- `.git/`
- `node_modules/`
- full `archive/`
- raw paid-provider logs unless needed and checked
- private tokens, API keys, or unnecessary personal data

## Minimal Package Recommendation

If the package should be small, include only:

```text
advisor_package_2026-06-17/
  README.md
  slides/track_b_progress_2026-06-12_v6.pptx
  dataset/dataset_description.md
  dataset/sample_items/
  methodology/benchmark_setup.md
  methodology/static_technical_metrics.md
  methodology/static_visual_metrics.md
  methodology/dynamic_browser_metrics.md
  methodology/llm_judge_protocol.md
  methodology/human_annotation_pilot.md
  examples/
  results/leaderboard_preview.md
  open_questions_for_supervisor.md
```
