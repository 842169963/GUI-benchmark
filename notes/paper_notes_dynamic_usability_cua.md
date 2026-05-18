# Paper Note: Training Computer Use Agents to Assess GUI Usability

Paper: Gao et al., "Training Computer Use Agents to Assess the Usability of Graphical User Interfaces"  
Version in local library: arXiv:2604.26020v1, 28 Apr 2026  
Local file: `literature/papers/Training Computer Use Agents to Assess the Usability of Graphical User Interfaces1.pdf`

## What The Paper Does

This paper is highly relevant to the thesis dynamic-evaluation direction. It trains a computer use agent, uxCUA, to assess GUI usability by interacting with websites and predicting a numerical usability score.

Main contributions:

- Builds `uxWeb`, a large-scale dataset of 2,586 fully interactive website UIs.
- Generates synthetic website clones from Mind2Web-style sites.
- Injects known usability defects based on usability principles.
- Collects designer preference labels for a subset of site pairs.
- Trains `uxCUA`, a computer use agent based on EvoCUA, to explore interfaces and output usability scores.
- Evaluates against proprietary and open models, including GPT-5-mini, Kimi K2.5, and EvoCUA.

## Key Details

Dataset:

- 879 plain synthetic website clones.
- 1,707 defect-augmented websites.
- 2,586 total interactive UIs.
- 510 designer-rated preference pairs spanning 428 unique plain clones.
- Inter-rater agreement is low: Krippendorff's alpha = 0.308, confirming high subjectivity in design/usability evaluation.

Training:

- Agent explores UI through screenshots and mouse/keyboard actions.
- Maximum interaction budget: 50 steps.
- Generates interaction rollouts, filters low-quality traces, then fine-tunes a CUA.
- Uses outcome supervision rather than directly supervising a single "correct" usability trace.

Evaluation:

- Primary metric: AUC over predicted usability scores.
- uxCUA outperforms larger baselines.
- On synthetic defect labels, uxCUA AUC = 0.632.
- On human preference labels, uxCUA AUC = 0.607.
- GPT-5-mini and other baselines remain near chance, especially on known defect labels.

## What This Means For This Thesis

This paper overlaps strongly with the original Track B ambition of using computer-use agents for dynamic usability assessment. The thesis should not frame "using CUAs to assess GUI usability dynamically" as the main novelty anymore.

However, it does not make the thesis obsolete. The thesis can pivot its novelty to a narrower and more feasible question:

> Can lightweight static rubric scores from multimodal LLM judges predict dynamic interaction outcomes, and how do pairwise, rubric, and dynamic evaluation signals relate on the same generated UI benchmark?

This differs from Gao et al. because:

- They train a new CUA model; this thesis should not train a CUA.
- They create a large synthetic website usability dataset; this thesis should build a smaller benchmark focused on generated UIs.
- They predict numerical usability scores after full interaction; this thesis can compare static rubric scores with lightweight dynamic task success or action-plan validation.
- They focus on usability assessment agents; this thesis focuses on evaluation methodology and the relationship between static and dynamic GUI quality signals.

## Recommended Thesis Repositioning

Do not abandon the thesis. Modify Track B framing:

Old framing:

> Dynamic evaluation of generated UIs with GUI agents.

Better framing:

> A lightweight benchmark linking static multimodal GUI quality judgments with dynamic task-oriented validation for generated interfaces.

Track B should become a correlation/relationship study, not a CUA-training study.

Recommended RQ4 wording:

> For generated executable UIs, to what extent do static rubric scores from multimodal LLM judges predict dynamic task-validation outcomes, and which rubric dimensions are most predictive?

## How To Cite / Use It

Use this paper in:

- Chapter 2: related work on dynamic UI evaluation and CUA-based usability assessment.
- Chapter 3: justify why this thesis uses a lightweight Plan B rather than training a CUA.
- Chapter 6: contrast thesis dynamic evaluation with uxCUA-style full computer-use-agent usability assessment.
- Chapter 8: limitations and future work.

Key positioning sentence:

> Recent work has shown that trained computer-use agents can assess GUI usability through interactive exploration. In contrast, this thesis does not train a usability agent; it studies whether lightweight static LLM-based GUI judgments provide signals that relate to dynamic task outcomes on generated interfaces.
