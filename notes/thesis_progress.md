# Thesis Progress Log

## Working Rule

- Canonical project folder: `D:\master_thesis`
- Main source file: `D:\master_thesis\thesis_proposal.tex`
- Reference file: `D:\master_thesis\references.bib`
- PDF output: `D:\master_thesis\thesis_proposal.pdf`
- Detailed edit history: `D:\master_thesis\notes\revision_log.md`

---

## 2026-05-04 — Track A formal run update

### Completed

- Added `scripts/track_a_eval.py`, a cleaner Track A evaluation script with support for `biglab/uiclip_human_data_hf`, older `img_good/img_bad` paired datasets, `.env` loading, optional `OPENAI_BASE_URL`, order-swap evaluation, and dry-run pair construction.
- Dry-run built 50 caption-matched pairs successfully.
- Smoke test ran 3 pairs / 6 calls successfully.
- Formal small run completed on 50 pairs / 100 calls.

### Result: UIClip human caption-matched pairs, GPT-4o, 50 pairs

Result file: `scripts/results/track_a_eval_gpt-4o_20260504_161730.json`

Important data note: `biglab/uiclip_human_data_hf` contains single screenshots with captions, not explicit `img_good/img_bad` pair columns. The script therefore constructs **caption-matched derived pairs** by matching `well-designed` screenshots with `poor design / bad contrast / bad proximity` screenshots that share the same normalized page description. In thesis text, describe this as derived from UIClip human caption labels, not as raw pairwise human preference labels.

| Metric | Value |
|--------|-------|
| Raw accuracy | 59/100 = **59.0%** |
| Accuracy Run1 (good=A) | 20/50 = **40.0%** |
| Accuracy Run2 (good=B) | 39/50 = **78.0%** |
| Consistency rate | 29/50 = **58.0%** |
| Position bias rate | 21/50 = **42.0%** |
| Corrected accuracy (consistent pairs only) | 19/29 = **65.5%** |
| Chose A / Chose B | 31 / 69 |

Interpretation: GPT-4o still shows a clear second-image preference on the UIClip-human-derived sample (`B` chosen 69% of the time). The Run1/Run2 gap remains large (40% vs 78%), supporting the need for order-swap. However, corrected accuracy drops to 65.5%, so the earlier 88.9% corrected pilot result should be treated as preliminary and dataset-specific.

### Next

- [ ] Manually inspect the 50 derived pairs for matching quality.
- [ ] Improve caption matching if mismatches are found.
- [ ] Scale to 100 pairs after pair quality is checked.
- [ ] Add rubric-guided prompt condition.
- [ ] Add one comparison model only after GPT-4o formal setup is stable.

## 2026-05-04 — 阶段总结 & 后续计划

### 一、已完成工作

#### 论文框架
- **8章大纲**已确定：`notes/thesis_outline.md`（含章节结构、subsection、图表清单、文献）
- **4个研究问题（RQ）**已锁定：
  - RQ1：现代多模态LLM与UIClip人工标签的pairwise对齐度
  - RQ2：从pairwise升级到多维rubric后，各维度的human-model对齐情况
  - RQ3：judging策略（zero-shot / rubric-guided / order-swap / 重复采样）的最优trade-off
  - RQ4 ⭐：Track B静态rubric评分能否预测动态交互任务的成功率
- **双轨设计**：Track A（UIClip截图对复现）+ Track B（requirement-driven生成UI + 动态评估）

#### 文献与章节草稿
| 文件 | 内容 |
|------|------|
| `references.bib` | 13条文献，含Nielsen/ISO 9241/WebArena/Mind2Web |
| `notes/draft_ch2_gap_matrix.tex` | §2.6 Research Gap叙述 + 8×7对比矩阵 |
| `notes/draft_ch3_methodology.tex` | 完整Ch3（RQ、方法、指标、映射表） |

#### 实验脚本与结果
| 脚本 | 状态 | 结果文件 |
|------|------|----------|
| `scripts/track_a_pilot.py` | ✅ 已运行 | `results/track_a_pilot_gpt-4o_*.json` |
| `scripts/track_a_order_swap.py` | ✅ 已运行 | `results/track_a_orderswap_gpt-4o_20260504_153247.json` |

#### 关键实验发现

**Pilot（随机A/B，20对）**
- 准确率：65%
- 模型选B：18/20（90%）→ 存在严重位置偏差

**Order-Swap（每对判断两次，20对）**

| 指标 | 数值 | 含义 |
|------|------|------|
| 准确率 Run1（好图在A） | **40%** | 模型多数仍选B（错误） |
| 准确率 Run2（好图在B） | **95%** | 模型选B（恰好正确） |
| 一致率 | **45%** | 仅9/20对换序后选同一张图 |
| 位置偏差率 | **55%** | 超过半数因位置改变翻转答案 |
| 修正准确率（一致对） | **88.9%** | 去偏后模型真实判断力 |

**结论**：GPT-4o存在纯粹的"第二张图偏好（recency bias）"，11个偏差对全部是同一模式（Run1选B错，Run2选B对）。这直接证明order-swap去偏的必要性（支撑RQ3），同时模型本身具有真实的视觉辨别能力（修正准确率88.9%）。

---

### 二、后续执行计划

#### 近期实验（Track A 正式版）
- [ ] 切换到 `biglab/uiclip_human_data_hf`（UIClip官方人工标签数据集）
- [ ] 规模扩展：20对 → 50–100对
- [ ] 多模型对比：Claude Sonnet + Gemini Flash + GPT-4o，统一order-swap框架
- [ ] rubric-guided条件：增加rubric-guided prompt，测量对齐提升幅度

#### 论文写作（可与实验并行）
- [ ] **Ch4草稿** `notes/draft_ch4_benchmark.tex`
  - Track A/B数据pipeline说明
  - 4维Rubric（D1–D4）+ 1–5分锚点完整表格
  - 标注协议、IRR目标（α≥0.5）、Pilot标注设计
- [ ] **Ch2草稿** `notes/draft_ch2_background.tex`
  - 整合gap matrix进完整Ch2叙述
  - §2.1 GUI Quality理论（Nielsen/ISO根基）
  - §2.2–§2.5 各节 → §2.6 Research Gap

#### Track B Pipeline（工程量最大）
- [ ] Design2Code-HARD筛选：80个example中挑选~50个，过滤dynamic-impossible页面
- [ ] Requirement反向提取：reference HTML → 自然语言requirement（半自动+人工修订）
- [ ] 生成UI：2–3个generator模型（GPT-4o/Claude）各自生成HTML
- [ ] 渲染pipeline：Playwright headless → screenshot + DOM dump

#### 人工标注
- [ ] 招募标注员：≥3人（同学/HCI lab）
- [ ] Pilot标注：10个Track B items × 3人 → 计算Krippendorff's α，目标≥0.5
- [ ] 正式标注：Track B全集，majority vote得出reference label

#### 动态评估（Ch6）
- [ ] 任务设计：每个Track B item推导1–2个交互任务（明确成功标准）
- [ ] Plan B脚本：LLM输入(DOM + screenshot + task) → 输出action sequence JSON
- [ ] Validation脚本：DOM selector检查 + state transition验证

#### 收尾
- [ ] HF Space Leaderboard：Gradio静态dashboard，读取results.json渲染表格
- [ ] Ch7 Results + Ch8 Discussion/Conclusion（基于真实结果写）
- [ ] Ch1 Introduction（最后写，数字确定后）

---

## 2026-04-10

### Current status

- The proposal source has been restored after an accidental overwrite from an older local version.
- The current PDF builds successfully from `D:\master_thesis`.
- The abstract is visible again in the compiled PDF.
- The current title is:
  `Beyond Pairwise GUI Quality Judgments: Multi-Dimensional Evaluation with Modern Multimodal LLMs`

### Proposal scope at the moment

- Main focus:
  screenshot-based GUI quality evaluation
- Main methodological elements:
  pairwise comparison, rubric-based assessment, human annotation, and LLM-as-a-judge strategies
- Additional artifact:
  benchmark + lightweight leaderboard
- Dynamic component:
  a small complementary evaluation module with computer-use agents

### Key decisions already made

- Use only `D:\master_thesis` as the canonical working directory.
- Do not rely on the desktop folder as the main editable version.
- Keep concrete paper names such as `UIClip` out of the abstract.
- Keep standard field terms such as `rubric-based assessment`, `zero-shot prompting`, and `rubric-guided scoring` in the abstract where useful.
- Treat dynamic evaluation as an extension, not as the main thesis focus.

### Supervisor feedback already addressed

- Clarified the meaning of order-swapped pairwise comparisons.
- Added benchmark / leaderboard as an explicit deliverable.
- Added a limited dynamic evaluation extension with computer-use agents.
- Revised the abstract to be more self-contained.

### Immediate next tasks

- Review remaining supervisor comments one by one.
- Check whether the benchmark / leaderboard wording should be tightened further.
- Decide whether the dynamic evaluation description should stay at its current level or be narrowed further.
- Continue recording every confirmed change in `notes/revision_log.md`.

### Lessons learned

- After important edits, keep a clean compiled PDF and source snapshot.
- Avoid overwriting the main file after a failed local build.
- When something looks wrong in the PDF, verify both the source file and the compiled output before editing further.
