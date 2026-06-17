# Literature and Citation Status

This is a short citation audit for the current PPT/design choices.

| Design choice / claim | Citation status | Notes |
| --- | --- | --- |
| Use Vision2Web-derived tasks | Supported | Cite Vision2Web: https://arxiv.org/abs/2603.26648 |
| Screenshot-based visual UI judging | Supported generally | Cite UIClip, MLLM-as-UI-Judge, WebDevJudge. |
| Four visual dimensions | Supported at dimension level | Map to MLLM-as-UI-Judge, WebDevJudge, VisAWI, Lavie & Tractinsky. |
| 16-item binary checklist | Partly supported | Cite CheckEval for checklist decomposition; still need UI-item source mapping. |
| Binary vs Likert tradeoff | Needs cautious framing | Cite Preston & Colman 2000; keep Likert/pairwise as open sensitivity check. |
| Cohen's kappa | Supported | Cite Cohen 1960. |
| Range restriction explanation for low r | Supported statistically, project-specific empirically | Cite Sackett & Yang 2000; phrase as pilot evidence. |
| Jitter/defect injection | Partly supported | Cite UIClip as inspiration; exact CSS jitter is project-specific. |
| Judge certification against human ceiling | Partly supported | Cite Judge's Verdict as method analogy; do not overclaim final proof. |
| Accessibility checks | Supported | Cite axe-core/WCAG if used in final method. |
| Static technical gate details | Mostly project-specific | Literature motivates deterministic artifact checks, but the exact checks are engineering decisions from this pipeline. |
| Dynamic browser workflow | Supported conceptually | Vision2Web supports workflow verification; WebArena/Mind2Web/VisualWebArena support browser-task evaluation. Current route/content heuristics are project-specific. |
| Leaderboard schema | Mostly project-specific | Designed for auditability: attempted/eligible/failed, failure categories, n/a vs zero, visible category scores. |

## Wording to Soften

Use these safer versions:

- Instead of "certified human-level judge": "passes the current pilot reliability criterion."
- Instead of "the low r was the data, not the judge": "pilot evidence suggests restricted score range contributed to the low r."
- Instead of "frozen production judge": "frozen for the next controlled evaluation batch, pending supervisor feedback."
- Instead of "known quality ordering" for all jitter variants: "severe jitter and weak-model outputs create clearer quality gaps; mild jitter remains a sensitivity case."

## Useful References

- Vision2Web: https://arxiv.org/abs/2603.26648
- UIClip: https://dl.acm.org/doi/10.1145/3654777.3676408
- CheckEval: https://arxiv.org/abs/2403.18771
- MLLM as a UI Judge: https://arxiv.org/abs/2510.08783
- WebDevJudge: https://arxiv.org/abs/2510.18560
- Judge's Verdict: https://arxiv.org/abs/2510.09738
- Cohen 1960: https://doi.org/10.1177/001316446002000104
- Sackett & Yang 2000: https://doi.org/10.1037/0021-9010.85.1.112
- Preston & Colman 2000: https://doi.org/10.1016/S0001-6918(99)00050-5
- axe-core docs: https://www.deque.com/axe/core-documentation/api-documentation/
- WebArena: https://arxiv.org/abs/2307.13854
- Mind2Web: https://arxiv.org/abs/2306.06070
- VisualWebArena: https://arxiv.org/abs/2401.13649
