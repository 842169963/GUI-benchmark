# Thesis Summary and Detailed Outline

## 1. Thesis Overview

**Working title:** Beyond Pairwise GUI Quality Judgments: Multi-Dimensional Evaluation with Modern Multimodal LLMs

**Current status:** The thesis proposal has been completed and compiled successfully. The proposal defines the main research direction, the evaluation tracks, the human annotation protocol, the LLM-as-a-judge methodology, and the expected benchmark and leaderboard artifact. This document turns the proposal into a practical writing blueprint for the full master thesis.

### Motivation

Large language models are increasingly used to generate interface mockups, frontend code, and interactive user interface prototypes. As this becomes more common, evaluating the quality of generated graphical user interfaces becomes a research problem in its own right. GUI quality cannot be reduced to visual attractiveness alone. It also involves layout, visual hierarchy, information organization, perceived usability, requirement satisfaction, and whether users or agents can complete intended tasks on the interface.

Existing screenshot-based approaches such as UIClip show that visual-language models can judge UI screenshots and compare interface quality. However, this line of work is limited when it relies mainly on binary pairwise comparisons, older model families, and static screenshots. The proposed thesis extends this foundation by evaluating modern multimodal LLMs as GUI judges with richer rubrics, stronger reliability analysis, requirement-driven interface generation, and a small dynamic interaction module.

### Research Problem

The central research problem is:

> Can modern multimodal large language models approximate human judgments of GUI quality beyond simple pairwise comparison, and which evaluation setup produces the most reliable and useful judgments?

This problem has three connected parts:

- How to build a benchmark that supports both screenshot-based GUI comparison and requirement-driven evaluation of generated interfaces.
- How to compare human judgments and model judgments across pairwise and rubric-based tasks.
- How static GUI quality judgments relate to dynamic task completion when computer-use agents interact with selected interfaces.

### Expected Contributions

The thesis should aim to contribute:

- A two-track GUI quality evaluation benchmark:
  - **Track A:** screenshot-based baseline using existing UI resources, mainly for visual quality, pairwise comparison, and rubric-based assessment.
  - **Track B:** requirement-driven generation track, where interfaces are produced from natural language requirements, rendered as screenshots, and kept executable for interaction tests.
- A multi-dimensional GUI evaluation rubric covering layout quality, visual hierarchy, information organization, perceived usability, requirement fidelity, and interaction quality.
- A human annotation protocol with inter-rater agreement analysis.
- A systematic comparison of LLM-as-a-judge strategies, including zero-shot prompting, few-shot prompting, rubric-guided scoring, repeated judging, order-swapped pairwise comparisons, and simple aggregation.
- A benchmark output format and lightweight leaderboard design.
- A small dynamic evaluation module using computer-use agents to test whether static quality scores predict task completion.

### Core Positioning

The main thesis contribution should remain the static GUI quality benchmark and the comparison between human and model judgments. The dynamic evaluation module should be framed as a targeted extension that tests whether static judgments connect to actual interaction performance. This keeps the thesis focused while still addressing the important limitation of screenshot-only evaluation.

## 2. Reference Map

| Reference | Main role in the thesis | Where to use it |
| --- | --- | --- |
| [UIClip: A Data-driven Model for Assessing User Interface Design](https://arxiv.org/abs/2404.12500) | Establishes the screenshot-based GUI quality assessment baseline. It shows that UI screenshots and natural language descriptions can be used for model-based assessment of design quality and visual relevance. | Introduction, Background, Dataset and Benchmark Construction, Results comparison. |
| [Improving User Interface Generation Models from Designer Feedback](https://machinelearning.apple.com/research/designer-feedback) | Motivates richer feedback structures beyond simple rankings. The paper supports the claim that designer-aligned, workflow-aware feedback can be more useful than coarse pairwise ranking data. | Introduction, Background, Human Annotation Protocol, Discussion. |
| [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685) | Provides the foundation for using strong LLMs as scalable judges and introduces key concerns such as position bias, verbosity bias, self-enhancement bias, and agreement with human preferences. | Background, Methodology, LLM-as-a-Judge Experiments, Reliability Analysis. |
| [From Generation to Judgment: Opportunities and Challenges of LLM-as-a-judge](https://arxiv.org/abs/2411.16594) | Provides a broad taxonomy of LLM-as-a-judge methods, including what is judged, how judging is performed, and how judge benchmarks are organized. | Background, Research Questions and Methodology, Prompting Strategy Design. |
| [Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge](https://arxiv.org/abs/2406.07791) | Supports the use of order-swapped pairwise comparisons and explicit position-bias analysis. It also provides concepts such as repetition stability, position consistency, and preference fairness. | Methodology, LLM-as-a-Judge Experiments, Results and Analysis. |
| [Design2Code: How Far Are We From Automating Front-End Engineering?](https://salt-nlp.github.io/Design2Code/) | Supports the feasibility of generating renderable frontend code from visual or textual UI specifications and evaluating rendered outputs. | Dataset and Benchmark Construction, Requirement-driven Track, Discussion. |
| [VisualWebArena: Evaluating Multimodal Agents on Realistic Visual Web Tasks](https://aclanthology.org/2024.acl-long.50/) | Provides methodological support for evaluating multimodal agents on visually grounded web tasks. It motivates the dynamic evaluation module with computer-use agents. | Dynamic Evaluation, Results and Analysis, Discussion. |

## 3. Proposed Research Questions

The thesis can be organized around the following research questions:

**RQ1:** How well do modern multimodal LLMs align with human judgments in pairwise GUI quality comparison?

**RQ2:** How well do multimodal LLMs align with human ratings in multi-dimensional rubric-based GUI assessment?

**RQ3:** Which judging strategies improve reliability and human alignment: zero-shot prompting, few-shot prompting, rubric-guided scoring, repeated judging, order-swapped pairwise comparisons, or aggregation?

**RQ4:** Which GUI quality dimensions are most reliably judged by humans and models?

**RQ5:** In the requirement-driven track, how well do static model judgments capture requirement fidelity?

**RQ6:** For a selected subset of interfaces, do static quality scores predict dynamic task success by computer-use agents?

These questions can be refined during the implementation stage, but they already match the proposal scope and give the thesis a clear evaluation structure.

## 4. Detailed Thesis Outline

### Chapter 1: Introduction

**Purpose:** Introduce the research problem, explain why GUI quality evaluation matters now, and position the thesis as an extension of screenshot-based GUI quality judgment toward multi-dimensional and partially dynamic evaluation.

**Main arguments to develop:**

- GUI quality affects usability, task completion, and user perception.
- Generative models now produce UI designs and frontend code, so evaluating generated interfaces is increasingly important.
- Existing screenshot-based methods are useful but limited by binary preference formats and static visual judgment.
- Modern multimodal LLMs make it possible to test richer GUI evaluation protocols.
- The thesis contributes a benchmark-oriented evaluation framework rather than only a single model comparison.

**Suggested subsections:**

- 1.1 Motivation: LLM-generated interfaces and the need for quality assessment.
- 1.2 Problem Statement: limitations of pairwise screenshot-only GUI evaluation.
- 1.3 Research Objectives: human-aligned, multi-dimensional GUI judging with multimodal LLMs.
- 1.4 Contributions: benchmark, rubric, human annotation, judge comparison, leaderboard, dynamic module.
- 1.5 Thesis Structure: short chapter-by-chapter roadmap.

**Required evidence and material:**

- Use the final proposal abstract and introduction as the basis.
- Introduce UIClip as the main prior screenshot-based baseline.
- Use Designer Feedback to motivate why simple rankings may not capture rich design quality.
- Use LLM-as-a-judge literature to motivate scalable automated evaluation.

**Likely figures or tables:**

- Figure 1: High-level overview of the thesis evaluation framework.
- Table 1: Summary of thesis contributions and corresponding chapters.

**Reference usage:**

- Cite UIClip when introducing screenshot-based GUI quality evaluation.
- Cite Designer Feedback when arguing that richer feedback and rubric-based judgments are needed.
- Cite MT-Bench/Chatbot Arena when introducing LLM-as-a-judge as a scalable evaluation paradigm.

### Chapter 2: Background and Related Work

**Purpose:** Build the conceptual foundation for the thesis and show how the project connects GUI evaluation, UI generation, human feedback, LLM-as-a-judge methods, and multimodal web agents.

**Main arguments to develop:**

- GUI quality assessment has both visual and functional dimensions.
- UIClip is a strong baseline for screenshot-based assessment but does not fully cover requirement fidelity or dynamic interaction.
- Designer-centered feedback research suggests that design evaluation benefits from richer, more structured judgments.
- LLM-as-a-judge methods provide scalable evaluation tools but require careful handling of bias and consistency.
- Design-to-code systems and web-agent benchmarks make requirement-driven and dynamic evaluation feasible.

**Suggested subsections:**

- 2.1 GUI Quality Assessment and Usability Heuristics.
- 2.2 Screenshot-based UI Evaluation and UIClip.
- 2.3 UI Generation and Designer Feedback.
- 2.4 LLM-as-a-Judge: Scoring, Ranking, Selection, and Bias.
- 2.5 Multimodal Frontend Generation and Design2Code.
- 2.6 Dynamic Web Interaction and Computer-Use Agents.
- 2.7 Research Gap.

**Required evidence and material:**

- Summarize each cited work according to its role in the thesis.
- Explain the difference between static visual evaluation and dynamic task-based evaluation.
- Identify the gap: there is no unified GUI quality benchmark in this proposal's scope that combines pairwise comparison, rubric-based scoring, requirement fidelity, model-judge reliability, and a small dynamic module.

**Likely figures or tables:**

- Table 2: Related work comparison by evaluation material, judgment type, human labels, model judges, requirement fidelity, and dynamic interaction.
- Figure 2: Relationship between static screenshot judgment, requirement-driven generation, and dynamic interaction.

**Reference usage:**

- UIClip: baseline for screenshot-based quality ranking.
- Designer Feedback: evidence that richer design feedback matters.
- MT-Bench/Chatbot Arena and LLM-as-a-Judge survey: methodology and taxonomy.
- Position Bias Study: bias and robustness concerns.
- Design2Code: feasibility of generated frontend artifacts.
- VisualWebArena: precedent for multimodal agent evaluation.

### Chapter 3: Research Questions and Methodology

**Purpose:** Convert the motivation into precise research questions, define the overall experimental design, and explain how the two tracks and evaluation modules fit together.

**Main arguments to develop:**

- The thesis is not only asking whether LLMs can judge GUIs, but also how they should be prompted, calibrated, and evaluated.
- Pairwise comparison and rubric-based assessment answer complementary questions.
- Human judgments provide the reference point, while reliability analysis determines how trustworthy the labels and model outputs are.
- The dynamic module tests whether static judgments have practical meaning for interaction.

**Suggested subsections:**

- 3.1 Research Questions.
- 3.2 Overall Study Design.
- 3.3 Track A: Screenshot-based Baseline.
- 3.4 Track B: Requirement-driven Generated Interfaces.
- 3.5 Static Evaluation Tasks: Pairwise and Rubric-based.
- 3.6 Dynamic Evaluation Module.
- 3.7 Reliability and Cost Analysis.

**Required evidence and material:**

- Formalize the research questions listed in this document.
- Define what counts as a task, item, interface, pair, rubric score, model judgment, human label, and dynamic task.
- Clarify that Track A supports screenshot-based comparison and general visual quality judgment.
- Clarify that Track B supports requirement fidelity, executable interfaces, and dynamic interaction.

**Likely figures or tables:**

- Figure 3: End-to-end methodology pipeline.
- Table 3: Research questions mapped to datasets, tasks, metrics, and expected outputs.

**Reference usage:**

- Use the LLM-as-a-Judge survey to justify the categories of judging strategies.
- Use the Position Bias Study to justify order-swapped pairwise comparisons.
- Use Design2Code and VisualWebArena to justify the feasibility of Track B and the dynamic module.

### Chapter 4: Dataset and Benchmark Construction

**Purpose:** Describe the benchmark material, how interfaces are selected or generated, how screenshots and code artifacts are stored, and how the benchmark remains extensible.

**Main arguments to develop:**

- A two-track design avoids the limitations of using only old static screenshots.
- Track A provides comparability to previous screenshot-based GUI quality assessment.
- Track B enables requirement-aligned evaluation and dynamic testing because generated interfaces remain executable.
- Standardized storage and result formats are necessary for a reusable benchmark and leaderboard.

**Suggested subsections:**

- 4.1 Benchmark Design Goals.
- 4.2 Track A: Existing Screenshot-based UI Resources.
- 4.3 Track B: Natural Language Requirements and Generated Interfaces.
- 4.4 Rendering and Screenshot Capture Pipeline.
- 4.5 Benchmark Item Format and Metadata.
- 4.6 Result Submission Format.
- 4.7 Leaderboard Design.
- 4.8 Dataset Limitations and Scope Boundaries.

**Required evidence and material:**

- Define the minimum metadata for each benchmark item: item ID, track, source, screenshot path, requirement text if applicable, generated code path if applicable, task type, and evaluation split.
- Define the two evaluation task formats:
  - Pairwise comparison: two GUI screenshots and a preference label.
  - Rubric-based scoring: one GUI plus dimension-level scores.
- For Track B, define the relationship between requirement text, generated frontend code, rendered screenshot, and possible interaction task.
- Explain how contemporary screenshots may supplement the UIClip-based material if needed.

**Likely figures or tables:**

- Figure 4: Track A and Track B data construction pipelines.
- Table 4: Benchmark item schema.
- Table 5: Leaderboard fields, including pairwise agreement, rubric correlation, dimension-level scores, task success rate, and cost.

**Reference usage:**

- UIClip supports the screenshot baseline and possible reuse of public UI resources.
- Design2Code supports the frontend generation and rendering pipeline.
- Designer Feedback can motivate using natural language requirements and generated UI variants as more realistic design evaluation material.

### Chapter 5: Human Annotation Protocol and GUI Rubric

**Purpose:** Define how human reference labels are collected, how the rubric is structured, and how annotation reliability is measured.

**Main arguments to develop:**

- Human labels are necessary because the thesis evaluates whether model judgments approximate human assessment.
- Pairwise labels are simple but limited; rubric scores provide finer diagnostic information.
- Multiple annotators per item and agreement analysis are needed to make reference labels credible.
- The rubric should remain compact enough for consistent annotation but broad enough to capture key GUI quality dimensions.

**Suggested subsections:**

- 5.1 Annotation Goals and Annotator Instructions.
- 5.2 Pairwise Comparison Protocol.
- 5.3 Rubric-based Single-interface Scoring.
- 5.4 Rubric Dimensions and Score Anchors.
- 5.5 Requirement Fidelity for Track B.
- 5.6 Interaction Quality and Dynamic Review Cases.
- 5.7 Inter-rater Reliability.
- 5.8 Pilot Annotation and Rubric Refinement.

**Required evidence and material:**

- Define the rubric dimensions:
  - Layout quality.
  - Visual hierarchy.
  - Information organization.
  - Perceived usability.
  - Requirement fidelity for Track B.
  - Interaction quality for Track B dynamic cases.
- Decide and document the ordinal scale, for example 1 to 5, with short anchors.
- Explain how ties are handled in pairwise comparison.
- Explain how human review is used for ambiguous dynamic outcomes.
- Report inter-rater agreement, likely using Krippendorff's alpha and majority labels for pairwise comparisons.

**Likely figures or tables:**

- Table 6: GUI rubric dimensions and score anchors.
- Table 7: Example annotation form.
- Table 8: Inter-rater reliability by task type and rubric dimension.

**Reference usage:**

- Designer Feedback supports the importance of structured and design-aware feedback.
- MT-Bench/Chatbot Arena supports comparing model judgments against human preferences.
- UIClip supports human-rated UI quality as a reference concept.

### Chapter 6: LLM-as-a-Judge Experiments

**Purpose:** Define and run the model-judge experiments, comparing prompting strategies, model families, and reliability conditions.

**Main arguments to develop:**

- Modern multimodal LLMs can be evaluated as GUI judges in both pairwise and rubric-based settings.
- Prompting strategy matters because model judgments can be affected by instructions, examples, candidate order, and repeated sampling.
- Order-swapped pairwise comparisons are necessary to detect positional bias.
- Aggregation may improve robustness but increases cost.

**Suggested subsections:**

- 6.1 Model Selection.
- 6.2 Pairwise Judgment Prompts.
- 6.3 Rubric-guided Scoring Prompts.
- 6.4 Few-shot Calibration Examples.
- 6.5 Repeated Judging and Self-consistency.
- 6.6 Order-swapped Pairwise Comparisons.
- 6.7 Aggregation Strategies.
- 6.8 Cost and Runtime Tracking.

**Required evidence and material:**

- Define the tested model set: representative current closed-source multimodal models, open multimodal models where feasible, and one or two weaker models as exploratory baselines.
- Define structured output requirements for model judgments.
- For pairwise comparison, compute agreement with human majority labels.
- For rubric scoring, compute rank correlation and score differences against human ratings.
- Track stability across repeated judgments and order-swapped comparisons.
- Track cost per model, per task type, and per strategy.

**Likely figures or tables:**

- Table 9: Judge models and configuration.
- Table 10: Prompting conditions.
- Figure 5: Pairwise judging prompt template.
- Figure 6: Rubric-based judging prompt template.
- Table 11: Metrics for human alignment, reliability, bias, and cost.

**Reference usage:**

- MT-Bench/Chatbot Arena provides the core precedent for LLM-as-a-judge and human agreement analysis.
- LLM-as-a-Judge survey supports the broader taxonomy of judging strategies.
- Position Bias Study supports order-swapped comparisons and position-bias metrics.

### Chapter 7: Dynamic Evaluation with Computer-Use Agents

**Purpose:** Describe the small complementary module where computer-use agents interact with selected generated interfaces and attempt short tasks.

**Main arguments to develop:**

- Static screenshots can indicate visual and perceived usability quality, but they cannot fully test interaction and task completion.
- Track B creates executable interfaces, making a controlled dynamic evaluation possible.
- Dynamic evaluation should be limited in scope so that it complements rather than replaces the main benchmark.
- Comparing static quality scores with task success can reveal where visual judgment and practical interaction diverge.

**Suggested subsections:**

- 7.1 Rationale for Dynamic Evaluation.
- 7.2 Selection of Interfaces for Dynamic Testing.
- 7.3 Task Design from Natural Language Requirements.
- 7.4 Computer-Use Agent Setup.
- 7.5 Automated Outcome Checks.
- 7.6 Human Review for Ambiguous Cases.
- 7.7 Dynamic Metrics and Failure Categories.

**Required evidence and material:**

- Define the subset of Track B interfaces used for dynamic tests.
- Derive short tasks from the original natural language requirements.
- Define automated checks such as DOM state inspection or screenshot comparison against expected end states.
- Define metrics:
  - Task completion rate.
  - Action efficiency.
  - Failure type.
  - Static-dynamic correlation.
- Separate interface-related failures from agent or script failures.

**Likely figures or tables:**

- Figure 7: Dynamic evaluation loop with agent, browser, interface, and outcome checker.
- Table 12: Dynamic task examples.
- Table 13: Failure taxonomy for dynamic evaluation.

**Reference usage:**

- VisualWebArena provides the main methodological foundation for multimodal agent evaluation on visual web tasks.
- Design2Code supports the existence of executable generated interfaces.
- The LLM-as-a-judge references can be used lightly when discussing how static judgments and dynamic outcomes are compared.

### Chapter 8: Results and Analysis

**Purpose:** Present the empirical findings and directly answer the research questions.

**Main arguments to develop:**

- The best-performing judging setup should be identified by human alignment, reliability, and cost.
- Pairwise and rubric-based results may reveal different strengths and weaknesses.
- Some rubric dimensions may be easier for models and humans to judge reliably than others.
- Position bias and repeated-judgment variability should be measured rather than assumed away.
- Dynamic evaluation may show that visually strong interfaces do not always support task completion.

**Suggested subsections:**

- 8.1 Dataset and Annotation Statistics.
- 8.2 Human Agreement Results.
- 8.3 Pairwise Model-Judge Results.
- 8.4 Rubric-based Model-Judge Results.
- 8.5 Requirement Fidelity Results for Track B.
- 8.6 Position Bias and Self-consistency.
- 8.7 Dynamic Task Completion Results.
- 8.8 Static-Dynamic Relationship.
- 8.9 Cost-Quality Trade-offs.

**Required evidence and material:**

- Report human annotation counts and reliability.
- Report agreement with human majority labels for pairwise tasks.
- Report dimension-level correlations and score differences for rubric tasks.
- Report position-bias rates from order-swapped comparisons.
- Report dynamic task completion and action efficiency.
- Compare strong, open, and weaker model behavior if included.

**Likely figures or tables:**

- Table 14: Human annotation summary.
- Table 15: Pairwise agreement by model and prompting strategy.
- Table 16: Rubric score correlation by dimension.
- Figure 8: Model performance by rubric dimension.
- Figure 9: Position-bias visualization.
- Figure 10: Static score versus dynamic task success.
- Table 17: Cost per evaluation strategy.

**Reference usage:**

- Compare results back to UIClip as the starting point for screenshot-based evaluation.
- Use MT-Bench/Chatbot Arena and Position Bias Study to interpret bias and agreement results.
- Use VisualWebArena to contextualize the dynamic task results.

### Chapter 9: Discussion

**Purpose:** Interpret the results, explain what they mean for GUI quality evaluation, and discuss limitations.

**Main arguments to develop:**

- Multimodal LLMs may be useful GUI judges, but their reliability depends on task format, prompt design, model capability, and bias controls.
- Rubric-based assessment can reveal more useful information than binary pairwise preference.
- Requirement fidelity is important for generated interfaces because visually appealing UI can still fail the original specification.
- Dynamic evaluation can expose failures that static screenshots miss.
- Benchmark design should report dimension-level scores instead of only a single aggregate ranking.

**Suggested subsections:**

- 9.1 What Makes a Reliable GUI Judge?
- 9.2 Pairwise Comparison versus Rubric-based Assessment.
- 9.3 Static Visual Quality versus Requirement Fidelity.
- 9.4 Static Quality versus Dynamic Interaction.
- 9.5 Practical Benchmark and Leaderboard Implications.
- 9.6 Threats to Validity.
- 9.7 Limitations.

**Required evidence and material:**

- Discuss internal validity: prompt sensitivity, model variability, annotation disagreement.
- Discuss external validity: dataset size, UI domain coverage, model availability, changing model capabilities.
- Discuss construct validity: whether rubric dimensions truly represent GUI quality.
- Discuss cost and reproducibility.
- Explain why the dynamic module is intentionally small and exploratory.

**Likely figures or tables:**

- Table 18: Main findings mapped to research questions.
- Table 19: Threats to validity and mitigation strategies.
- Figure 11: Recommended benchmark reporting format.

**Reference usage:**

- Designer Feedback supports the discussion that richer feedback is valuable.
- LLM-as-a-Judge survey and Position Bias Study support cautions about judge reliability.
- VisualWebArena supports the argument that dynamic evaluation is important but challenging.

### Chapter 10: Conclusion and Future Work

**Purpose:** Summarize the thesis, answer the research questions at a high level, and identify future extensions.

**Main arguments to develop:**

- The thesis provides a benchmark-oriented framework for evaluating GUI quality with modern multimodal LLMs.
- The main contribution is the combination of pairwise comparison, rubric-based assessment, human labels, model-judge reliability analysis, and requirement-driven evaluation.
- The dynamic module shows how future work can connect static interface judgments with real task completion.
- The benchmark and leaderboard can be extended as new multimodal models become available.

**Suggested subsections:**

- 10.1 Summary of Contributions.
- 10.2 Answers to Research Questions.
- 10.3 Practical Implications.
- 10.4 Future Work.

**Required evidence and material:**

- Restate the most important empirical findings without introducing new experiments.
- Mention possible future directions:
  - Larger and more diverse GUI datasets.
  - More detailed interaction tasks.
  - Code-level UI quality evaluation.
  - More advanced model aggregation or judge calibration.
  - Longitudinal leaderboard updates as models change.

**Likely figures or tables:**

- Optional final summary table: contribution, result, and future extension.

**Reference usage:**

- Use references sparingly in the conclusion. The conclusion should mainly synthesize the thesis findings and connect them back to the research problem.

## 5. Cross-Chapter Writing Notes

### Keep the Two Tracks Clear

Throughout the thesis, maintain a consistent distinction:

- **Track A: Screenshot-based baseline**
  - Main purpose: compare against existing screenshot-based GUI evaluation.
  - Primary data: UI screenshots.
  - Main tasks: pairwise comparison and rubric-based static assessment.
  - Main dimensions: layout quality, visual hierarchy, information organization, perceived usability.

- **Track B: Requirement-driven generation**
  - Main purpose: evaluate generated interfaces against original natural language requirements.
  - Primary data: requirement text, generated frontend code, rendered screenshots, executable interfaces.
  - Main tasks: rubric-based assessment, requirement fidelity, and selected dynamic interaction tests.
  - Additional dimensions: requirement fidelity and interaction quality.

### Keep Static and Dynamic Evaluation Separated but Connected

The static benchmark is the thesis core. The dynamic module should be written as a complementary extension. The key connection is not that dynamic evaluation replaces static judgment, but that it tests whether static quality scores are predictive of actual interaction outcomes.

### Keep the Benchmark Artifact Visible

The benchmark and leaderboard should not appear only in the methods chapter. They should be visible in the introduction, methodology, dataset chapter, results chapter, and discussion. The thesis should repeatedly emphasize that the project produces a reusable evaluation protocol, not only a one-time experiment.

### Keep Human Judgment Central

The thesis evaluates LLMs as GUI judges, so human annotations are the reference point. The writing should avoid implying that model judgments are automatically correct. Human agreement, model-human alignment, and model reliability should be treated as empirical questions.

## 6. Suggested Writing Order

1. Expand Chapter 2 first, because related work will clarify terminology and make the research gap sharper.
2. Draft Chapter 3 next, fixing the final research questions and methodology.
3. Write Chapters 4 and 5 together, because dataset construction and annotation design depend on each other.
4. Implement and document Chapter 6 experiments.
5. Add Chapter 7 after the Track B pipeline is stable.
6. Write Chapter 8 only after results exist.
7. Finish with Chapters 1, 9, and 10, so the introduction and conclusion match the actual findings.

## 7. Immediate Next Steps

- Turn this outline into a thesis writing tracker with chapter status, missing material, and expected figures.
- Start the related work matrix for the seven cited papers.
- Define the exact benchmark item schema and annotation form before collecting labels.
- Run a small pilot annotation to test whether the rubric dimensions are clear.
- Run a small pilot model-judge experiment before scaling to the full benchmark.
