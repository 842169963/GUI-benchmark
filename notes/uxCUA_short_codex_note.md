# Codex Note: Learn This Paper and Use It to Suggest Improvements to My Thesis Plan

## How Codex should use this file

Read this file as a compact summary of the paper:

**Training Computer Use Agents to Assess the Usability of Graphical User Interfaces**  
Main system: **uxCUA**  
Main dataset: **uxWeb**

Then read my thesis plan separately and suggest how my plan could be improved.  
Do **not** rewrite the whole plan.  
Do **not** replace my current plan with this paper.  
Use this paper only as supporting literature and methodological inspiration.

---

## 1. Core idea of the paper

The paper proposes training **computer-use agents (CUAs)** to assess GUI usability.

Instead of only judging a static UI screenshot, the agent:

1. opens an interactive GUI,
2. identifies important user goals and interaction flows,
3. uses mouse/keyboard actions to test those flows,
4. reviews the interaction trace,
5. outputs usability problems and a numerical usability score.

The key shift is:

> from static visual UI assessment to dynamic interaction-based usability assessment.

This is useful for my thesis because it shows that GUI evaluation should not only ask whether a UI looks good, but also whether users/agents can actually complete important tasks.

---

## 2. Problem and motivation

Traditional usability testing with real users or experts is effective but expensive and time-consuming.

Existing LLM/VLM-based agents can interact with websites, but the paper argues that off-the-shelf agents still struggle to give accurate usability assessments.

Main motivation:

- GUI usability depends on interaction flows, not just appearance.
- Static screenshots cannot reveal broken navigation, missing feedback, irreversible actions, confusing forms, or failed task completion.
- General-purpose VLMs/CUAs are not automatically reliable usability judges.
- Automated usability assessment needs task-specific data, interaction traces, and evaluation objectives.

---

## 3. uxWeb dataset

The paper creates **uxWeb**, a dataset of fully interactive websites with usability labels and human judgments.

Dataset construction:

1. Start from 137 real websites from Mind2Web.
2. Use a coding agent to generate standalone React.js website clones.
3. Each clone has mocked but functional user flows.
4. Each clone includes a `flows.txt` file documenting implemented user flows.
5. After quality checks, the authors obtain 879 plain website clones.
6. They inject usability defects into a subset of these sites.
7. Final dataset includes 2,586 fully interactive UIs:
   - plain website clones
   - defect-augmented versions
   - usability labels
   - human preference judgments

Important insight for my thesis:

> Synthetic but controllable UI variants can be useful for benchmarking, especially when real labeled usability data is hard to obtain.

---

## 4. Usability defect injection

The paper injects known usability defects into website clones.

The defect categories are based on Shneiderman’s 8 Golden Rules:

1. **Consistency**  
   Similar actions and terminology should behave consistently.

2. **Feedback**  
   The interface should respond clearly to user actions.

3. **Dialog closure**  
   Interaction sequences should have a clear beginning, middle, and end.

4. **Error prevention**  
   Users should be protected from serious mistakes.

5. **User control**  
   Users should feel in control and avoid unexpected behavior.

6. **Reversal / undo**  
   Actions should be reversible where possible.

7. **Memory load**  
   Users should not need to remember information across screens.

8. **Hierarchy**  
   Important task-relevant elements should be easy to find.

Important insight for my thesis:

> These categories are interaction-level usability dimensions. They can complement static visual dimensions such as layout, visual hierarchy, information organization, and aesthetics.

---

## 5. Human preference data

The paper collects designer-rated usability preferences using an arena-style comparison interface.

Key details:

- 17 participants with design background
- 30 pairs per participant
- 510 preference pairs
- participants interact with both websites before voting
- inter-rater agreement is low: Krippendorff’s alpha = 0.308

Important insight for my thesis:

> Human UI/usability judgments can be subjective. My plan should mention inter-rater agreement and avoid assuming that human labels are perfectly consistent.

---

## 6. uxCUA agent behavior

uxCUA is designed to conduct a usability test like this:

1. receives the instruction: conduct a usability test of this website;
2. has a fixed action budget, usually 50 steps;
3. lists important user goals;
4. tests at least several key flows;
5. uses realistic placeholder data when filling forms;
6. handles errors if possible;
7. reflects on the interaction history;
8. outputs usability issues;
9. gives a final usability score from 0 to 100.

The score represents the estimated probability that an average user can successfully use the website’s important flows.

Important insight for my thesis:

> A dynamic evaluation module does not need to inspect every page. It can use a limited action/task budget and focus on important flows.

---

## 7. Training method

The paper trains uxCUA in three stages.

### 7.1 Rollout generation

The base agent explores uxWeb websites and generates interaction traces.

- up to 24 traces per website
- 37,281 traces generated
- traces include screenshots, actions, model thoughts, and final scores

### 7.2 Reward assignment

The paper rewards traces based on:

1. navigation quality
2. usability score accuracy

Navigation quality uses simple measurable signals:

- same-screen ratio
- same-screen-after-clicks ratio
- unique-screen ratio
- number of steps

This helps filter poor traces where the agent loops, gets stuck, or clicks uselessly.

### 7.3 Policy update

The best traces are used to fine-tune the agent.

Key point:

> The full training setup is large and expensive. My thesis should not try to reproduce this unless the plan is explicitly changed.

---

## 8. Score calibration idea

The paper argues that a plain UI should not simply be assigned 100 and a defect-augmented UI should not simply be assigned 0.

Reason:

- even the plain UI may contain usability flaws;
- usability is relative and noisy;
- human preferences can be subjective.

Instead, the paper enforces a margin between preferred and rejected interfaces.

Important insight for my thesis:

> UI quality and usability should be treated as relative, noisy, and partially subjective. Pairwise comparison and ranking may be more realistic than absolute “perfect” scores.

---

## 9. Evaluation results

The paper compares:

- GPT-5-mini
- Kimi K2.5
- EvoCUA
- uxCUA

### Synthetic defect labels

AUC:

- GPT-5-mini: 0.436
- Kimi K2.5: 0.521
- EvoCUA: 0.381
- uxCUA: 0.632

### Human preference labels

AUC:

- GPT-5-mini: 0.592
- Kimi K2.5: 0.588
- EvoCUA: 0.522
- uxCUA: 0.607

Main conclusion:

> Off-the-shelf models and agents are not reliable enough for rigorous usability assessment. A task-specific trained agent performs better.

---

## 10. Critique quality

The paper manually inspects uxCUA’s generated usability critiques.

Precision:

- overall: 69.8%
- plain clones: 60.8%
- defect-augmented sites: 71.9%

Important insight for my thesis:

> Agent-generated critiques can be useful but are not perfectly reliable. Evaluation should measure critique quality or clearly state it as qualitative support rather than ground truth.

---

## 11. Limitations of the paper

Important limitations:

1. The dataset is mostly synthetic.
2. Real-world generalization is limited.
3. The 50-step budget cannot cover all website functions.
4. The agent is slow, around five seconds per step.
5. The agent can make mistakes humans may not make, such as missing click targets.
6. The work mainly targets fixed-resolution web interfaces.
7. Transfer to mobile apps, native desktop apps, or XR is uncertain.
8. Real-world testing needs guardrails for high-impact actions such as purchases or deletion.
9. Even if the final score matches human preference, it is unclear whether the agent used the same evidence as humans.

---

## 12. What Codex should suggest for my thesis plan

After reading my thesis plan separately, suggest improvements inspired by this paper.

Focus on the following possible suggestions:

### A. Add a clearer static vs dynamic distinction

Static evaluation:

- screenshot-based
- visual/rubric judgment
- pairwise preference
- layout, hierarchy, aesthetics, information organization

Dynamic evaluation:

- browser-based
- task-flow-based
- interaction trace
- task completion
- feedback, control, reversibility, memory load, navigation clarity

### B. Strengthen motivation for dynamic evaluation

Use this paper to argue that static UI quality assessment is incomplete because usability depends on interaction.

### C. Add a limited dynamic evaluation component

Do **not** suggest training uxCUA.

Instead suggest a lightweight version:

- render generated HTML UI in browser
- define a few task flows
- use Playwright or a simple browser agent
- check task completion through DOM state
- log steps, clicks, errors, dead clicks, and loops
- compare dynamic task success with static judge scores

### D. Suggest one additional research question

Possible RQ:

> Are static UI quality judgments predictive of dynamic task-completion success?

Codex should decide whether this should be a main RQ or an optional/secondary RQ.

### E. Suggest metrics inspired by the paper

Possible dynamic metrics:

- task success rate
- number of steps
- dead-click rate
- repeated-screen ratio
- unique-screen ratio
- navigation loop count
- error-state count
- DOM-state correctness
- mismatch between static score and dynamic success

### F. Suggest limitations to add

Possible limitations:

- static screenshots cannot fully capture usability
- dynamic agents may make non-human errors
- task coverage is limited
- human labels are subjective
- generated HTML UIs may not represent production UIs
- no trained CUA judge is built in this thesis
- real user studies remain necessary

### G. Suggest future work

Possible future work:

- train a dedicated CUA-based UI judge
- build a larger interactive UI benchmark
- extend to mobile apps
- add accessibility-specific profiles
- use video traces
- add safety guardrails
- include richer UX critique evaluation

---

## 13. Scope warnings for Codex

Do **not** recommend the following unless explicitly required by the thesis plan:

- training a new uxCUA model
- reproducing uxWeb
- building thousands of interactive websites
- conducting large-scale user studies
- making dynamic evaluation the entire thesis
- replacing static UIClip-style evaluation with agent-only evaluation

The best use of this paper is as follows:

> Use uxCUA as evidence that interaction-based usability evaluation matters, then suggest a small and feasible dynamic evaluation extension to my existing static UI evaluation plan.
