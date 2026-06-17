# Implementation Files

These are copies of the core scripts from the full local repository. They are
included so the evaluation descriptions in `supervisor_brief.md` can be checked
against concrete implementation files.

| Script | Layer |
| --- | --- |
| `check_track_b_generation.py` | Static technical gate/checks. |
| `run_track_b_dynamic_workflow.py` | Deterministic route-simulation workflow evaluator. |
| `run_track_b_browser_workflow.js` | Chromium/Playwright browser workflow evaluator. |
| `score_track_b_visual.py` | Static visual score aggregation with repeated judge calls. |
| `visual_judge_workflow_summary.md` | Summary of the external-provider visual judge workflow. The full provider-calling script is not included in this minimal package because it contains provider plumbing and environment-variable names. |
| `build_track_b_dev_subset_demo.py` | Preliminary leaderboard/schema aggregation demo. |

The full project repository contains the complete run history and additional
experiments. This package only includes representative copies for review.
