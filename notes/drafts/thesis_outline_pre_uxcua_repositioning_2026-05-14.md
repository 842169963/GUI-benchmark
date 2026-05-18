# Master Thesis — Overall Outline & Critical Review

## Context

Xinyang 已经完成 thesis proposal（[thesis_proposal.tex](thesis_proposal.tex)），并由 GPT 生成了一份非常详细的章节大纲（[notes/thesis_summary_outline.md](notes/thesis_summary_outline.md)，约 550 行，10 章）。老师在 [Teacher's suggestion.txt](Teacher's%20suggestion.txt) 中给出了 5 条主线建议：(1) 用现代多模态 LLM 重做 UIClip；(2) 从 pairwise 升级到多维评估；(3) 改进 LLM-as-a-judge 方法；(4) 扩展到动态/交互式 UI；(5) 设计 benchmark + leaderboard。

本计划文件做两件事：
1. **整合一份精简、可执行的整体论文大纲**（基于 GPT 大纲，但根据 proposal、Design2Code 等参考文献做了取舍和补强）。
2. **提出我的批评性意见**，特别是 scope、风险、最小可交付版本（MVT）等老师建议中没明说但我认为关键的问题。

---

## Part 0 — 用户已确认的关键决策（2026-04-29 更新）

1. **章节数**：采用 8 章版本
2. **Track B 数据源**：混合（Design2Code-HARD 主体 + 5–10 条自建 requirement）
3. **Leaderboard**：上线 Hugging Face Space（最简实现：展示不评估）
4. **Dynamic 模块**：是论文重要组成（老师明确要求），不是 add-on
5. **Track A**：**保留但缩小范围**（用户决策 2026-04-29）。理由：现在还不确定后续走向，留作 fallback 与 UIClip 锚点。**起步范围**：直接复用 UIClip 公开 pair 数据 50–100 对，**不做新的人工标注**，只让 LLM judges 跑一遍并报告与 UIClip 的差距。Track A 后期可视情况扩展或砍掉。
6. **整体策略**：**先锁定一个"大概可行"的 starting scope，开工后再裁剪**——不在动笔前过度决策。

### 关于 dynamic 实现方式（建议但未最终决定）
两种实现路径，建议**起步用方案 B（轻量），跑通后视情况决定要不要升级到方案 A**：
- **方案 A（重）**：真 computer-use agent 在浏览器中点击执行
- **方案 B（轻）**：给 LLM (DOM + screenshot + task)，让它输出 action sequence，用脚本验证 sequence 是否合理（element 存在性、selector 命中、是否到达预期 state）
- 方案 B 的好处：成本低一个量级；隔离 UI 质量与 agent 执行能力两个 noise source；失败归因清晰

### 关于 "static 和 dynamic 是否两条线" 的设计建议 ⭐

**结论：方法论上分两章，数据层面合并为同一条线。** 具体安排：

- **Track A**（screenshot only）：缩小范围版——复用 UIClip 50–100 对公开数据，不新做人工标注，作为 UIClip 数字锚点 + reproduction sanity check。后期可裁剪为 Ch5 一个小节
- **Track B**（generated executable UI）：**同一批界面同时接受 static rubric 评分 + dynamic agent 任务测试**
  - 这意味着每个 Track B item 都有两组分数：static rubric (Ch5) + dynamic task success (Ch6)
  - 由此**static-dynamic correlation 成为论文的核心新颖发现**，回答："静态 LLM judge 能否预测真实交互结果？"
  - 这正是把老师建议 2、3、4 串起来的最强论点

这种"分章不分 dataset"的设计避免了 dynamic 模块孤立、规模太小的问题，同时让两套评估互相支撑。Ch3 methodology 与 Ch7 results 都要显式强调这个配对关系。

---

## Part 1 — 完整论文大纲（8 章 + 附录，可动笔版）

> 每章包含：(1) Purpose 一句话；(2) 估算页数；(3) 完整 numbered subsections；(4) 每节写作要点；(5) Figures / Tables 清单；(6) 引用文献；(7) Cross-refs 与 out-of-scope 备注。
>
> **总页数估算**：正文约 70–90 页 + 附录 15–25 页（TU Clausthal informatics master thesis 的常见区间）。
>
> 章节标题、subsection 标题用英文（直接进 thesis）；写作要点和注释用中文。

---

### Chapter 1 — Introduction (~6–8 pages)

**Purpose**: 让读者在 5 分钟内理解为什么这个问题值得做、本论文做了什么、以及和 UIClip 的关系。

**1.1 Motivation**
- LLM 已能产出 UI mockup + 前端代码，引 Design2Code 与 Designer Feedback 的实证数字
- GUI 质量 ≠ 视觉吸引力，还包括 usability / 任务完成 / requirement 满足
- 三类 stakeholder 都需要可信的 GUI 评估：设计师（迭代反馈）、开发者（自动化测试）、AI 研究者（模型对比）

**1.2 Problem Statement**
- 现有 screenshot-based 方法（UIClip）的三重局限：仅 pairwise / 旧模型 / 纯静态
- LLM-as-a-judge 在文本领域成熟，但在 UI 视觉领域几乎空白
- 没有一个 benchmark 同时覆盖：现代多模态 judge + 多维 rubric + requirement-driven 生成 UI + 静态-动态评估配对

**1.3 Research Questions** (preview, full statement in §3.1)
- 4 个 RQ 列表（不展开）

**1.4 Contributions**
- C1: 双 track GUI 质量评估 benchmark（Track A reproduction + Track B requirement-driven）
- C2: 4 维 GUI 质量 rubric，建立在 Nielsen / ISO 9241 上
- C3: 现代多模态 LLM judge 的系统对比（含 prompting 策略 ablation 与 position bias 分析）
- C4: ⭐ 首次实证 static rubric 评分与 dynamic 任务执行成功率的关系
- C5: 开源评估 pipeline + Hugging Face Space leaderboard

**1.5 Thesis Structure**
- 每章 1 段（~50 字）

**Figures**: Fig 1.1 整体 framework 概览（two-track + static + dynamic + leaderboard）
**Tables**: Table 1.1 Contributions ↔ Chapters 对照
**Cites**: UIClip, Designer Feedback, Design2Code, MT-Bench

**Out of scope**: 不在 introduction 中给具体数字，那放到 results。

---

### Chapter 2 — Background and Related Work (~12–15 pages)

**Purpose**: 建立概念基础并显式说明 research gap。

**2.1 GUI Quality and Usability**
- 2.1.1 Definition of GUI quality (visual + functional + interactive 三个层面)
- 2.1.2 Classical usability heuristics: Nielsen's 10, ISO 9241-11
- 2.1.3 How established usability theory informs our rubric
- *写作要点：这一节是审稿人最爱挑刺的地方，必须有理论根基。Nielsen + ISO 至少各引一处。*

**2.2 Screenshot-based UI Evaluation**
- 2.2.1 Pre-LLM era: rule-based, ML classifiers (brief)
- 2.2.2 UIClip: dataset, model, metrics, results
- 2.2.3 Limitations: pairwise-only, model age, static-only

**2.3 LLM-Generated UIs**
- 2.3.1 Design2Code: 484 webpages, prompting methods, automatic metrics (CLIP score, block-match)
- 2.3.2 Designer Feedback: pairwise rankings ~50% agreement (本论文的关键论据)
- 2.3.3 Implications: richer feedback formats matter

**2.4 LLM-as-a-Judge**
- 2.4.1 MT-Bench / Chatbot Arena: foundation
- 2.4.2 EMNLP'25 survey: taxonomy of judge types
- 2.4.3 Position bias study (IJCNLP-AACL'25): position consistency, repetition stability
- 2.4.4 What transfers from text to multimodal/UI? (open question this thesis addresses)

**2.5 Multimodal Web Agents and Dynamic UI Evaluation**
- 2.5.1 VisualWebArena: setup, agent, metrics
- 2.5.2 Brief mention: WebArena, Mind2Web (1 段)
- 2.5.3 Computer-use agents (Claude/GPT Operator): capabilities & current failure modes
- *写作要点：诚实承认 agent 仍然不稳定，这就是为什么本论文用 Plan B（action plan elicitation）而不是真 agent execution。*

**2.6 Research Gap**
- 一段 narrative，再用一张矩阵 table 强化
- 矩阵列：[work] × [evaluation material / judgment type / multidim / human labels / requirement fidelity / dynamic interaction]
- 行：UIClip / Designer Feedback / MT-Bench / VisualWebArena / Design2Code / **This thesis**

**Figures**: Fig 2.1 Taxonomy of GUI evaluation paradigms（static vs dynamic, pairwise vs rubric）
**Tables**: Table 2.1 Related-work comparison matrix
**Cites**: 全部 references.bib + Nielsen 1994 + ISO 9241-11 (待补)

---

### Chapter 3 — Research Questions and Methodology (~8–10 pages)

**Purpose**: 把动机正式化为可测试 RQ，并给出 end-to-end 实验设计。

**3.1 Research Questions**
- 完整 4 RQ 措辞（每个 RQ 含 1–2 个 sub-question）：
  - **RQ1** (Track A, reproduction): How well do modern multimodal LLMs align with UIClip's original pairwise human labels, and how does this compare to UIClip's reported model performance?
  - **RQ2** (Track A + B, multidim): When moving from pairwise comparison to multi-dimensional rubric scoring, what is the human-model alignment per dimension, and which dimensions are most reliably judged?
  - **RQ3** (judge methodology): Among prompting strategies (zero-shot, rubric-guided), reliability conditions (order-swap, repeated sampling), and across model families, which configurations achieve the best alignment-cost trade-off?
  - **RQ4** ⭐ (static-dynamic linkage): For Track B executable interfaces, do static rubric scores predict the success rate of LLM-derived action plans on derived tasks? Which rubric dimensions correlate most with dynamic task success?

**3.2 Overall Study Design**
- 3.2.1 Two-track architecture (rationale recap)
- 3.2.2 Static-dynamic pairing principle: Track B 每个 item 同时收到 static rubric + dynamic plan validation
- 3.2.3 Reference labels: UIClip 原始标签 (Track A) + 自做人工标注 (Track B)
- 3.2.4 Reproducibility 承诺: model IDs, dates, prompts, seeds, random shuffles 全部记录

**3.3 Track A: Reduced Reproduction**
- Data: 50–100 UIClip pairs
- Tasks: pairwise comparison
- Reference: UIClip 原标签
- Purpose: numerical anchor，不做新标注

**3.4 Track B: Requirement-driven Generated UIs**
- Data sources: Design2Code-HARD (~50–60 selected) + 5–10 self-built requirements
- Generation: 2–3 generator models per requirement → 100–200 generated UIs（pilot 后定）
- Tasks: rubric scoring + dynamic action plan validation
- Reference: human rubric scores + automated dynamic outcomes

**3.5 Static Evaluation Methodology**
- 3.5.1 Pairwise judging (Track A)
- 3.5.2 Rubric scoring (Track A 部分 + Track B 全部)
- 3.5.3 Prompting conditions: zero-shot / rubric-guided
- 3.5.4 Reliability conditions: order-swap (must), repeated sampling 3× (must)

**3.6 Dynamic Evaluation Methodology (Plan B)**
- 3.6.1 Approach choice: Plan B (action plan elicitation) over Plan A (full agent execution)，理由见 §6.2
- 3.6.2 Task derivation 流程
- 3.6.3 Action plan validation: deterministic script
- 3.6.4 Plan A 列入 future work

**3.7 Metrics**
- Human-model agreement: Cohen's κ (pairwise), Krippendorff's α (rubric)
- Rubric correlation: Spearman ρ per dimension
- Position bias rate (order-swap)
- Self-consistency rate (repeated sampling)
- Plan success rate (dynamic)
- Static-dynamic correlation
- API cost per evaluation

**3.8 RQ ↔ Methods Map**

**Figures**: Fig 3.1 End-to-end pipeline; Fig 3.2 Static-dynamic pairing schema
**Tables**: Table 3.1 RQ × Track × Task × Metric × Artifact 对照

---

### Chapter 4 — Benchmark Construction and Human Annotation Protocol (~12–15 pages)

**Purpose**: 详细定义数据如何来、如何存、如何标注、如何评估标注质量。

**4.1 Benchmark Design Goals**
- Reproducibility, extensibility, track separation, leaderboard 兼容

**4.2 Track A Construction**
- 4.2.1 Source: UIClip 公开 repo
- 4.2.2 Sampling: random + balanced（覆盖原数据集多个类别）
- 4.2.3 Item storage: `track_a/{pair_id}/{img_a.png, img_b.png, label.json}`
- 4.2.4 No new annotation; reuse UIClip ground-truth labels

**4.3 Track B Construction**
- 4.3.1 Requirement source 1: Design2Code-HARD curation
  - 从 80 examples 筛选 ~50 个，过滤掉 dynamic-impossible 的页面
  - 把 reference HTML 反向写成自然语言 requirement（半自动 + 人工修订）
- 4.3.2 Requirement source 2: 5–10 self-built (form-heavy + mobile UI 优先)
- 4.3.3 Generator models: 2–3 个（与 judge 模型可重叠也可不重叠，决策记录在 §5.1）
- 4.3.4 Rendering pipeline: Playwright headless → screenshot + DOM dump
- 4.3.5 Item storage: `track_b/{item_id}/{requirement.md, generated.html, screenshot.png, dom.json, generator_meta.json}`

**4.4 Benchmark Item Schema and Submission Format**
- JSON spec（完整版进 Appendix C）
- Result format spec：用于 HF Space leaderboard
- 一个 minimal example item shown inline

**4.5 GUI Quality Rubric**
- 4.5.1 Design rationale（grounded in §2.1）
- 4.5.2 Four starting dimensions（pilot 后可调）：
  - **D1 Visual Structure**：layout、alignment、spacing、visual hierarchy（合并原 6 维的 layout + hierarchy）
  - **D2 Information Clarity**：grouping、labeling、可读性、可推断的可用性（合并原 organization + perceived usability）
  - **D3 Requirement Fidelity** (Track B only)：界面是否实现了 requirement 中的所有元素与功能
  - **D4 Interaction Quality** (Track B only, dynamic)：界面在交互流程中的响应、状态转换、反馈是否合理
- 4.5.3 Scoring scale: 1–5 ordinal，每维度有 5 个简短 anchor
- 4.5.4 Anchor descriptions（完整表格见 Appendix B）
- 4.5.5 Pilot 后调整规则：α < 0.4 的维度强制重新设计或合并

**4.6 Human Annotation Protocol**
- 4.6.1 Annotator recruitment：起步 plan = 同学/HCI lab 3 人，备份 = Prolific（待定，见 Part 3 决策）
- 4.6.2 Annotator instructions（完整版进 Appendix B）
- 4.6.3 Pairwise form (Track A 不需要新标注，本节主要为 Track B 服务，标 Track B item 之间的 pairwise 选 1 子集)
- 4.6.4 Rubric form (Track B)
- 4.6.5 Tie handling、ambiguity escalation 流程

**4.7 Inter-rater Reliability**
- 目标：α ≥ 0.5 acceptable, ≥ 0.7 good
- 不达标处理：rubric 重新设计 → re-pilot
- Majority voting 用于得出 reference label

**4.8 Pilot Annotation**
- 4.8.1 Pilot set: 10 Track B items × 3 annotators
- 4.8.2 Pilot results: per-dimension α
- 4.8.3 Refinements applied
- 4.8.4 Final rubric (post-pilot)

**Figures**: Fig 4.1 Track A & Track B 数据 pipeline; Fig 4.2 Annotation 表单截图; Fig 4.3 Item directory layout
**Tables**: Table 4.1 Rubric dimensions + anchors; Table 4.2 Item schema; Table 4.3 Pilot α values

---

### Chapter 5 — LLM-as-a-Judge Experiments (~10–12 pages)

**Purpose**: 定义并执行模型评判实验，回答 RQ1, RQ2, RQ3 的方法论部分。

**5.1 Model Selection**
- 2 closed-source: Claude (Sonnet/Opus latest)、GPT-4o 或继任
- 1 open: Qwen-VL 或 LLaVA-NeXT
- 1 weaker baseline: 较小 multimodal 模型（验证 model capability ↔ judge quality 关系）
- 完整记录：model ID、API version、调用日期

**5.2 Prompting Conditions**
- 5.2.1 Zero-shot（pairwise + rubric）
- 5.2.2 Rubric-guided：显式给出维度定义 + 锚点 + JSON 输出 schema
- 5.2.3 Few-shot (time-permitting)：1–2 个 worked example
- 5.2.4 通用：所有 prompt 强制 structured JSON output；JSON 解析失败 retry 上限 3 次

**5.3 Reliability Conditions**
- 5.3.1 Order-swap (must)：pairwise 任务每对评 2 次（A,B 与 B,A），计算 position consistency
- 5.3.2 Repeated sampling (must)：每个 item × condition × model 跑 3 次（temperature > 0）
- 5.3.3 Aggregation (time-permitting)：majority vote (pairwise) / score average (rubric)

**5.4 Track A: UIClip Reproduction**
- 5.4.1 Setup: 上述模型在 Track A 50–100 对上跑 zero-shot pairwise
- 5.4.2 Direct comparison: 与 UIClip 原文报告数字对比
- 5.4.3 这一节是论文与老工作连接的"科学锚点"

**5.5 Track B Static: Rubric Scoring**
- 5.5.1 Setup: 全部 Track B items × 全部 models × {zero-shot, rubric-guided}
- 5.5.2 Reference: §4 中的 human majority scores
- 5.5.3 Per-dimension correlation 计算

**5.6 Cost and Runtime Tracking**
- 每个 (model, condition, item) 三元组记录 cost + latency
- 用 batch API where available（Claude / Gemini / OpenAI 都支持）

**5.7 Implementation Details**
- 代码结构: `src/judges/`, `src/eval/`, `src/datasets/`
- 完整 prompt templates 进 Appendix A

**Figures**: Fig 5.1 Pairwise prompt template; Fig 5.2 Rubric prompt template
**Tables**: Table 5.1 Model lineup; Table 5.2 Condition × Model matrix; Table 5.3 Cost summary

**Out of scope**: 实际数字结果在 Ch7。

---

### Chapter 6 — Dynamic Evaluation with Computer-Use Agents (~8–10 pages)

**Purpose**: 在 Track B 同一批 UI 上做 dynamic 评估，与 Ch5 配对回答 RQ4。

**6.1 Rationale**
- 静态截图无法评估交互
- Static rubric 是否能预测交互成功率，是论文核心新颖发现
- Track B 界面可执行，使配对实验成为可能

**6.2 Approach: Plan B (Action Plan Elicitation)**
- 6.2.1 Why not Plan A (full agent execution): agent + UI 两个 noise source 叠加，归因困难，成本高
- 6.2.2 Plan B definition: 给 LLM (DOM + screenshot + task)，让它输出 action sequence (JSON)
- 6.2.3 Validation: 确定性脚本检查 sequence 可行性
- 6.2.4 Plan A 在 §8.7 列入 future work

**6.3 Task Derivation**
- 6.3.1 Protocol: 每个 Track B requirement → 1–2 个 short task with unambiguous success criterion
- 6.3.2 Task examples table
- 6.3.3 Task 由作者定义，由 1 人交叉检查；不能自动派生

**6.4 Action Plan Elicitation**
- 6.4.1 Prompt template (full in Appendix A)
- 6.4.2 Output schema: ordered list of `{action_type, target_selector, value?}`
- 6.4.3 Action types: click / type / select / scroll / submit
- 6.4.4 Same model lineup as §5.1（保证可比）

**6.5 Validation Script**
- 6.5.1 Element existence check（每个 selector 是否在 DOM 中）
- 6.5.2 Selector resolution（unique match）
- 6.5.3 Optional state transition check（form submit 后是否有目标 element）
- 6.5.4 Plan success criterion: 全部 actions resolvable 且达到 target state

**6.6 Failure Taxonomy**
- F1 UI failure: element missing / 布局破坏 / 必要 handler 缺失
- F2 Plan failure: LLM 给错 selector 或 action sequence
- F3 Ambiguity: UI 可用但 task 描述歧义
- F4 Tool/script failure: validation 脚本本身的 bug
- 模糊 case 由 1 人 review 决定归类

**6.7 Static-Dynamic Pairing Data**
- 每个 Track B item 产出 4-tuple: `(item_id, rubric_vector, plan_success_rate, failure_categories)`
- 这是 §7.5 的 RQ4 直接输入

**Figures**: Fig 6.1 Dynamic pipeline; Fig 6.2 Example action plan + validation outcome
**Tables**: Table 6.1 Task examples; Table 6.2 Failure taxonomy with examples

**Cites**: VisualWebArena (作 Plan A 的对比), Design2Code (Track B 数据基础)

---

### Chapter 7 — Results and Analysis (~12–15 pages)

**Purpose**: 实证回答 4 个 RQ，组织顺序按 RQ 而非 task。

**7.1 Dataset and Annotation Statistics**
- Track A 数量；Track B 数量；human annotator 数；标注时长
- Per-dimension IRR (α)
- Cost summary

**7.2 RQ1: Pairwise Modern Models vs UIClip**
- Per-model agreement with UIClip labels
- 与 UIClip 报告数字直接对比表
- 解读：现代模型是否真的更好，差距多少

**7.3 RQ2: Multidimensional Rubric Alignment**
- Per-dimension Spearman correlation (model × dimension heatmap)
- 哪些维度模型表现最好，哪些最差
- D3 (Requirement Fidelity) 与 D4 (Interaction Quality) 的特殊讨论

**7.4 RQ3: Strategy Ablation**
- Zero-shot vs rubric-guided：alignment 提升多少
- Order-swap：position consistency 数字
- Repeated sampling：self-consistency 数字
- Cost vs alignment trade-off

**7.5 RQ4: Static-Dynamic Correlation ⭐**
- Scatter: rubric (D1+D2 平均) vs plan success rate
- Per-dimension correlation table
- 哪些 static 维度预测 dynamic 最好
- Diverging cases 定性分析（visually appealing but task-failed; cluttered but task-success）

**7.6 Cost-Quality Trade-off**
- 每个 (model, strategy) 的 cost vs alignment 散点

**7.7 Qualitative Error Analysis**
- 4–6 个 typical case 截图 + 分析
- Cases: cluttered UI but high task success; visually appealing UI but task fails; model rates high humans rate low; vice versa

**Figures**: Fig 7.1 Model × Dimension heatmap; Fig 7.2 Static-dynamic scatter; Fig 7.3 Position bias bars; Fig 7.4 Cost-quality plot; Figs 7.5+ Qualitative case screenshots
**Tables**: Table 7.1 Dataset stats; Table 7.2 RQ1 numerics + UIClip comparison; Table 7.3 RQ2 per-dim correlations; Table 7.4 RQ3 ablation; Table 7.5 RQ4 correlations; Table 7.6 Cost summary

---

### Chapter 8 — Discussion, Limitations and Conclusion (~8–10 pages)

**Purpose**: 综合解读结果，明示 limitations，指 future work，收尾。

**8.1 What Makes a Reliable GUI Judge?**
- 综合 RQ1–RQ3 给出实践建议（哪个 model + 哪个 strategy combination 是 best practice）

**8.2 Pairwise vs Rubric vs Requirement Fidelity**
- 三种 task format 各自的强项与失效场景

**8.3 The Static-Dynamic Gap**
- RQ4 结果的含义
- 当 LLM judge 作为 usability proxy 时该信什么、不该信什么

**8.4 Practical Benchmark and Leaderboard Implications**
- HF Space 部署 summary
- 别人如何 extend benchmark / submit results

**8.5 Threats to Validity**
- Internal: prompt sensitivity, model variance, annotator bias
- External: 数据规模、UI 领域覆盖
- Construct: 4 维 rubric 是否真代表 GUI quality
- Reproducibility: model versioning, API drift

**8.6 Limitations**
- Track A reduced scope（只用 50–100 对，没新标注）
- Plan B 不是真 agent execution
- Annotator pool 有限
- 仅静态截图 + DOM，未涵盖动效与可访问性

**8.7 Future Work**
- 更大 Track B
- Plan A: full agent execution
- Code-level UI quality (无障碍、性能)
- Judge calibration / fine-tuning
- 长期 leaderboard 维护机制

**8.8 Conclusion**
- Restate contributions
- 高层回答每个 RQ
- Closing paragraph

**Figures**: Fig 8.1 Benchmark reporting recommendation
**Tables**: Table 8.1 Findings ↔ RQs; Table 8.2 Threats × mitigations

---

### Appendices

- **A: Full prompt templates** (~5–10 pages) — pairwise / rubric / action plan elicitation 完整版
- **B: Annotation guidelines** (~3–5 pages) — instructions, anchor 完整描述, edge case 处理
- **C: Benchmark item schema** (~1–2 pages) — JSON spec for Track A & Track B & result format
- **D: Selected human-annotated examples** (~2–3 pages) — 6–8 个 representative items + scores
- **E: Model output samples** (~2–3 pages) — 每模型每 condition 1–2 个原始 output
- **F: Leaderboard implementation notes** (~1–2 pages) — HF Space 代码结构、submission flow
- **G: Reproducibility checklist** (~1 page) — model IDs, dates, seeds, code repo URL

---

### 章节间依赖与写作顺序提示

```
Ch2 (基础知识) ──┐
                 ├──► Ch3 (RQ + 方法) ──► Ch4 (数据 + 标注) ──► Ch5 (静态实验) ──┐
                 │                                                                 ├──► Ch7 (结果) ──► Ch8 (讨论)
                 └─────────────────────────────────────────────► Ch6 (动态实验) ──┘
                                                                                   │
                                                                                   └──► Ch1 (Intro 最后写)
```

**Pilot annotation (§4.8) 是关键里程碑**：α 不达标必须改 rubric 然后重跑，会反向影响 Ch3 与 Ch4。建议 pilot 跑完再去打磨 Ch3 的 RQ 措辞。

---

## Part 2 — 我的批评性意见与建议（重点读这里）

### 意见 1 ⭐ 必须显式做"UIClip reproduction"作为基线
老师建议的第一条是 **"reproduce (parts of) the original setup"**。GPT 大纲里把它隐含到了 Ch5 实验里，但**没有专门小节**。我强烈建议在 §5.4 单列一节，明确说明：
- 用现代 GPT/Claude/Gemini 在 UIClip 原始 pairwise 任务上跑一遍
- 报告与原论文的差距（数字层面的对比）
- 这一节是连接老论文与本论文最直接的"科学锚点"，也最容易被审稿人看到价值

### 意见 2 ⭐⭐ Scope 警告：当前设计对 master thesis 偏大（dynamic 已确认必做后，更需收缩其他部分）
用户已确认 dynamic + HF Space leaderboard 都是必做项，这意味着**其他部分的 scope 必须收紧**，否则不可能按时交付。建议：
- **Track A**：使用 UIClip 现有公开数据，不再自建当代截图集（节省人工标注成本）
- **Track B 规模**：50–80 个 generated UI 即可（Design2Code-HARD 80 个为上限参考）
- **模型数**：3 个闭源 + 1 个开源 + 1 个 weaker baseline，不要更多
- **Prompting 策略**：zero-shot, rubric-guided, order-swap, repeated 这 4 个为必做；few-shot 和 aggregation 列为"时间允许时做"
- **HF Space**：MVP 版本即可（gradio 静态展示 + 下载结果文件），不必做在线评估
- **关键时间节点**：建议 Ch4 数据 + 标注必须在论文写作期前 1/3 时间完成，否则后续都没法做

### 意见 3 Track B（生成 pipeline）的工程量被低估
- Design2Code 论文用了 484 个手工筛选的 webpage、84 种 HTML 标签、平均 158 个 tag。要让本论文 Track B 有意义，至少需要：
  - 20–50 条 requirement（自己写或改编）
  - 每条 requirement × 3–5 个 generator 模型 → 60–250 个 generated UI
  - 每个都要渲染、截图、保留可执行版本
- 建议：**直接复用 Design2Code-HARD（80 examples）作为 reference + requirement source**，不要自己从头构造，省下大量工程时间。reference 文件夹里已经有这篇论文，可以引用其方法。

### 意见 4 Human annotation 的预算与招募现实问题
- 6 维 × 5 分 + pairwise，单 item 人工时间 ≈ 3–5 分钟
- 如果要 200 items × 3 annotators = 600 次标注 ≈ 30–50 小时人工
- 建议：
  - 在 Ch4 显式给出**预算/招募来源**（同学、Prolific、TU Clausthal HCI 实验室？）
  - Pilot 阶段（10–20 items）必须先做，IRR 不达标就调 rubric
  - **Design2Code 用了 Prolific @ $16/hour, 5 annotators per item**，可作为参考

### 意见 5 缺少基础 usability 文献的引用
当前 references.bib 中没有 **Nielsen heuristics**、**ISO 9241**、或 HCI 教科书级别的可用性框架。审稿人很可能问："你的 rubric 6 维基于什么理论？" 建议在 Ch2.1 加入：
- Nielsen 1994 《Usability Engineering》或 10 Heuristics
- ISO 9241-11 (usability definition)
- 可选：Norman《Design of Everyday Things》

### 意见 6 RQ 数量过多，建议从 6 → 4
GPT 大纲的 6 个 RQ 里 RQ4（"哪些维度最可靠"）和 RQ5（"requirement fidelity"）实际上是 RQ2 的子问题。合并后 4 个 RQ 更紧凑，论文结构也更清晰。

### 意见 7 Leaderboard 上 HF Space 的最简实现路径
用户确认要上线 HF Space。为了控制工程量，建议采用**只展示、不在线评估**的设计：
- HF Space 用 Gradio 做一个静态 dashboard：读取 repo 中的 `results.json` 渲染表格 + 各维度 bar chart
- 用户提交新模型结果的方式 = 提交 PR 到 GitHub repo + 一个标准化的 `result.json`
- Space 自动从 GitHub 拉最新结果重新渲染
- **不要**在 Space 上跑模型推理（成本不可控、安全风险大）
- 这种"submission via PR"模式参考 LMSys Chatbot Arena leaderboard 早期版本，1–2 周可完成

### 意见 8 章节合并建议（已纳入上面 outline）
- 原 Ch4 (Dataset) + Ch5 (Annotation) → **新 Ch4**（数据和标注协议本来就需要 co-design）
- 原 Ch9 (Discussion) + Ch10 (Conclusion) → **新 Ch8**（master thesis 一般不分两章）
- 这样从 10 章压到 8 章，对 60–80 页的 master thesis 更合适

### 意见 9 写作顺序建议（与 GPT 大纲一致，重申一下）
1. 先写 Ch2（related work matrix 是定盘星）
2. Ch3 RQ + methodology（写完后让导师审一次，避免后期返工）
3. Ch4 dataset & annotation（**强烈建议在这一步就跑完 pilot annotation**，否则 rubric 会反复改）
4. Ch5 实验（同时开始 cost tracking）
5. Ch6 dynamic（看时间裁剪）
6. Ch7 results
7. 最后写 Ch1 + Ch8（introduction 和 conclusion 必须基于真实结果而不是空想）

### 意见 10 风险与缓解
| 风险 | 概率 | 影响 | 缓解 |
| --- | --- | --- | --- |
| Track B 生成质量太差，rubric 区分度不够 | 中 | 中 | 复用 Design2Code-HARD；保留 human-curated UI 作 control |
| Annotator 招募失败 | 中 | 高 | 提前与导师/同学敲定；准备 Prolific 备份预算 |
| API 成本超支（多模型 × 多策略 × 重复采样） | 高 | 中 | 实验前估算成本上限；用 Claude/Gemini 的 batch API；先小样本 pilot |
| Computer-use agent 不稳定 | 高 | 低（dynamic 是 add-on） | 缩小 dynamic 子集；明确报告 agent failure rate |
| 模型在论文写作期间下线/更新 | 中 | 中 | 记录每次实验的 exact model ID + date；保存原始输出 |

---

## Part 3 — 仍需 Xinyang 决策的问题

主要决策已在 Part 0 确认。剩余尚未确定：

1. **Annotation 资源**：是否能保证 ≥3 个 annotator？预算从哪里来（同学/Prolific/HCI lab）？
2. **Rubric 维度**：保留当前 6 维，还是允许 pilot 后调整为 4–5 维？
3. **Track B 自建那 5–10 条 requirement 覆盖什么场景**？建议：mobile UI（Design2Code 主要是桌面 web），或者 form-heavy 任务界面（更利于 dynamic agent 任务设计）。
4. **Dynamic agent 选择**：用 VisualWebArena 的 agent 实现，还是直接调用 Anthropic computer use API / OpenAI Operator？后者代码量小但 API 成本高。

---

## Part 4 — Critical Files

- [thesis_proposal.tex](thesis_proposal.tex) — proposal 源文件，必须与新大纲一致
- [references.bib](references.bib) — 需要补充 Nielsen / ISO 9241 等基础文献
- [notes/thesis_summary_outline.md](notes/thesis_summary_outline.md) — GPT 详细版大纲（保留作 reference）
- [notes/revision_log.md](notes/revision_log.md) — 每次结构变更要记录
- [reference/degin2code front-end automatedv3.pdf](reference/degin2code%20front-end%20automatedv3.pdf) — Track B pipeline 的方法论模板

## Part 5 — Verification Plan

本计划本身不涉及代码运行。一旦 Xinyang 同意大纲方向，下一步的"端到端验证"包括：
1. 起草 Ch2 related work matrix（1 页 table），让导师审过
2. 写 Ch3 RQ 终稿，与导师确认
3. 跑 pilot annotation（10–20 items, 3 annotators），验证 IRR ≥ 0.5
4. 跑 pilot LLM-as-judge experiment（1 模型 × 1 策略 × 20 items），验证 prompt 模板可用
5. 估算总 API 成本和人工成本，写入 thesis progress log

---

*Plan authored 2026-04-29. 大纲与意见基于 thesis_proposal.tex（v2026-04-10）、Teacher's suggestion.txt、notes/thesis_summary_outline.md、references.bib、reference/Design2Code 论文。*
