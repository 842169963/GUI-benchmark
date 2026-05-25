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

### 2026-05-06 literature update: dynamic usability CUA paper

Added paper note: `notes/paper_notes_dynamic_usability_cua.md`

Paper: Gao et al., "Training Computer Use Agents to Assess the Usability of Graphical User Interfaces" (arXiv:2604.26020v1, 28 Apr 2026).

Impact: this paper strongly overlaps with a broad "CUA-based dynamic usability assessment" direction. The thesis should not claim novelty for training or using CUAs to assess GUI usability in general. Instead, Track B should be positioned as the core of a multi-metric static and dynamic leaderboard for evaluating LLM-generated GUIs.

Recommended change: keep Track B, but frame RQ4 as the relationship, complementarity, and divergence between static quality scores and dynamic task-validation outcomes, not as building a new usability-assessment CUA.

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

- [x] Manually inspect the 50 derived pairs for matching quality.
- [x] Exclude 7 manually marked mismatch pairs and save clean subset.
- [x] Scale to 100 pairs after pair quality is checked.
- [x] Manually inspect the 100-pair run and produce clean subset.
- [x] Add rubric-guided prompt condition.
- [x] Add one comparison model only after GPT-4o formal setup is stable.

### Manual review update: clean 43-pair subset

Manual review marked 7/50 pairs as mismatch / needs review:
`pair_id` = 0, 15, 31, 33, 35, 41, 48.

Cleaned result file: `scripts/results/track_a_eval_gpt-4o_20260504_161730_clean43.json`

| Metric | Original 50 pairs | Clean 43 pairs |
|--------|-------------------|----------------|
| Raw accuracy | 59.0% | **61.6%** |
| Accuracy Run1 (good=A) | 40.0% | **39.5%** |
| Accuracy Run2 (good=B) | 78.0% | **83.7%** |
| Consistency rate | 58.0% | **55.8%** |
| Position bias rate | 42.0% | **44.2%** |
| Corrected accuracy | 65.5% | **70.8%** |
| Chose A / Chose B | 31 / 69 | **24 / 62** |

Interpretation: after removing clear mismatches, model accuracy improves slightly, but the core pattern remains: GPT-4o still strongly favors the second image. This strengthens the claim that the position effect is not merely an artifact of mismatched pairs.

### 100-pair run before manual cleaning

Result file: `scripts/results/track_a_eval_gpt-4o_20260506_142748.json`  
Review page: `scripts/results/track_a_eval_gpt-4o_20260506_142748_pair_review/review.html`

| Metric | Value |
|--------|-------|
| Raw accuracy | **59.5%** |
| Accuracy Run1 (good=A) | **38.0%** |
| Accuracy Run2 (good=B) | **81.0%** |
| Consistency rate | **53.0%** |
| Position bias rate | **47.0%** |
| Corrected accuracy | **67.9%** |
| Chose A / Chose B | 57 / 143 |

Interpretation: the 100-pair run reproduces the same position-bias pattern found in the 50-pair run. Manual pair-quality review is still required before treating this as the clean Track A result.

### Manual review update: clean 85-pair subset

Manual review marked 15/100 pairs as mismatch / needs review:
`pair_id` = 0, 23, 33, 41, 56, 57, 58, 87, 90, 91, 92, 94, 95, 97, 98.

Cleaned result file: `scripts/results/track_a_eval_gpt-4o_20260506_142748_clean85.json`

| Metric | Original 100 pairs | Clean 85 pairs |
|--------|--------------------|----------------|
| Raw accuracy | 59.5% | **62.4%** |
| Accuracy Run1 (good=A) | 38.0% | **38.8%** |
| Accuracy Run2 (good=B) | 81.0% | **85.9%** |
| Consistency rate | 53.0% | **52.9%** |
| Position bias rate | 47.0% | **47.1%** |
| Corrected accuracy | 67.9% | **73.3%** |
| Chose A / Chose B | 57 / 143 | **45 / 125** |

Interpretation: after manual removal of mismatched derived pairs, the alignment estimate improves, but the position-bias finding is unchanged. GPT-4o still selects the second image in 125/170 calls.

### Rubric-guided prompt comparison on clean85

Rubric-guided result file: `scripts/results/track_a_eval_openai_gpt-4o_rubric_20260506_162332.json`

| Metric | Zero-shot clean85 | Rubric-guided clean85 |
|--------|-------------------|-----------------------|
| Raw accuracy | 62.4% | **57.1%** |
| Accuracy Run1 (good=A) | 38.8% | **20.0%** |
| Accuracy Run2 (good=B) | 85.9% | **94.1%** |
| Consistency rate | 52.9% | **25.9%** |
| Position bias rate | 47.1% | **74.1%** |
| Corrected accuracy | 73.3% | **77.3%** |
| Chose A / Chose B | 45 / 125 | **22 / 148** |

Interpretation: rubric-guided prompting did not improve reliability in this pairwise setting. It made the B-position preference stronger, reducing raw accuracy and consistency. This supports RQ3 by showing that prompt strategy effects must be measured rather than assumed.

### Cross-model check: Claude Sonnet 4.5 on clean85

Claude result file: `scripts/results/track_a_eval_chatanywhere-anthropic_claude-sonnet-4-5-20250929_zeroshot_20260519_153820.json`

Condition: zero-shot pairwise prompt, same clean85 subset, order-swap enabled.

| Metric | GPT-4o zero-shot clean85 | Claude Sonnet 4.5 zero-shot clean85 |
|--------|--------------------------|-------------------------------------|
| Raw accuracy | **62.4%** | **55.3%** |
| Accuracy Run1 (good=A) | **38.8%** | **20.0%** |
| Accuracy Run2 (good=B) | **85.9%** | **90.6%** |
| Consistency rate | **52.9%** | **29.4%** |
| Position bias rate | **47.1%** | **70.6%** |
| Corrected accuracy | **73.3%** | **68.0%** |
| Chose A / Chose B | **45 / 125** | **25 / 145** |

Interpretation: Claude Sonnet 4.5 reproduces the core Track A reliability concern and shows an even stronger second-image preference than GPT-4o on this subset. This supports treating Track A as a reduced cross-model baseline and moving the main effort to Track B.

### Track A interpretation boundary

Track A should be written as a noisy reduced reproduction rather than a definitive model-capability benchmark. The clean85 pairs are caption-matched UIClip-human-derived pairs, not raw pairwise human preferences. Manual cleaning removed obvious mismatches, but the remaining pairs may still contain weak or ambiguous quality contrasts. Therefore, the safest claim is methodological: order-swapped pairwise judging reveals severe reliability problems in this derived-pair setting. The main thesis evidence should come from Track B, where requirements, generated UIs, rubric labels, and dynamic validation are controlled by the thesis pipeline.

### 2026-05-19 Track B source update: Vision2Web

New Track B direction: use a reduced Vision2Web Level 1/Level 2 subset as the primary data source. Vision2Web is more aligned with the thesis's static-vs-dynamic question than Design2Code because it includes both visual website development and functional/agent verification signals. Design2Code remains useful as a static UI-to-code reference and backup source, but it is no longer the main Track B substrate.

Scope boundary: exclude Vision2Web Level 3 full-stack tasks. They introduce backend state, deployment, authentication, and long-horizon workflow complexity that would shift the thesis away from GUI-quality evaluation.

Pilot preparation:

- Created `notes/track_b_vision2web_pilot_plan.md` with 10 selected Level 2 frontend tasks and 4 selected Level 1 static control tasks.
- Created `scripts/prepare_track_b_vision2web_manifest.py` and generated `data/track_b/vision2web_pilot_manifest.json`.
- Created `scripts/extract_track_b_vision2web_pilot.py` to download Vision2Web archives and extract only selected task directories when ready.
- Downloaded/extracted selected Vision2Web task directories into `data/track_b/vision2web_raw/`.
- Extraction summary saved at `data/track_b/vision2web_extraction_summary.json`.
- Directory check: all 10 Level 2 `frontend` tasks have `prompt.txt`, `workflow.json`, `prototypes/`, and `resources/`; all 4 Level 1 `webpage` tasks have `workflow.json`, `prototypes/`, and `resources/` but no `prompt.txt`, which matches the dataset format.
- Created `scripts/normalize_track_b_vision2web_items.py` and normalized the 14 selected tasks into `data/track_b/items/`.
- Normalization summary saved at `data/track_b/normalization_summary.json`.
- Normalized Track B item format now contains `requirement.md`, `workflow.json`, copied `prototypes/`, copied `resources/`, `source_meta.json`, and empty `generated/` / `renders/` directories.
- Created `scripts/generate_track_b_ui.py` for first generator-model smoke tests; the first Track B generation prompt template is recorded as `TB-GEN-v1` in `thesis/appendices/prompt_templates.tex`.
- Ran a Claude Sonnet 4.5 smoke generation on `F09_elections_bc`, saved at `data/track_b/items/F09_elections_bc/generated/claude_sonnet45_smoke/`.
- Rendered Chrome desktop/mobile smoke screenshots. Desktop is non-empty; mobile shows horizontal overflow, so the next step is a stricter render gate / prompt revision before scaling to the full Track B batch.
- Added `TB-GEN-v2` to tighten Track B generation around complete HTML, same-file JavaScript handlers, workflow-required interactions, and responsive no-overflow behavior.
- Added `scripts/check_track_b_generation.py` as a static generation gate. It correctly flags the first Claude smoke run as invalid because the HTML is incomplete and `showPage` is referenced but undefined.
- Attempted to re-run `F09_elections_bc` with `TB-GEN-v2`, but the current sandbox blocked the external ChatAnywhere API call because it would send local Track B prompt inputs and prototype screenshots outside the workspace. Re-run requires explicit approval of that data transfer risk.
- After permission was opened, reran `F09_elections_bc` with revised prompts. `TB-GEN-v4` produced `data/track_b/items/F09_elections_bc/generated/claude_sonnet45_v4_smoke/` and passed all static gate checks.
- `TB-GEN-v5` was added to reduce hash-scroll side effects and tighten mobile CSS requirements, but its first ChatAnywhere call failed with HTTP 524 before an artifact was written.
- After reviewing the experimental scope, mobile/responsive behavior was moved out of the current hard gate and into future work. `TB-GEN-v6` is now the active Track B generation prompt: it keeps desktop visual fidelity and workflow-required interactions as the main requirements, allows non-workflow secondary navigation to remain placeholder-like, and treats missing real PDF downloads as a visible-content quality issue when the dataset supplies no PDF assets.
- Added GWDG/SAIA support through the OpenAI-compatible endpoint `https://chat-ai.academiccloud.de/v1` using local `GWDG_API_KEY`. The available model list was checked through `scripts/list_gwdg_models.py`. The next smoke run will use `qwen3.5-397b-a17b` first, with `qwen3.6-35b-a3b` as the fallback if the larger model is unstable or slow.
- GWDG/SAIA smoke update: `qwen3.5-397b-a17b` timed out after 360 seconds without writing an artifact. `qwen3.6-35b-a3b` succeeded only after increasing the output budget to 40k tokens. The valid artifact is `data/track_b/items/F09_elections_bc/generated/gwdg_qwen36_35b_v6_smoke_40k/`; static gate passed after recognizing `data-route-target` delegated route links. Hash route checks for `voter_registration` and `local_election_forms` passed. The rendered desktop screenshot is non-empty but starts below the header/navigation, so the next prompt revision should focus on hash-scroll behavior and output compactness before a wider batch.

## 2026-05-04 — 阶段总结 & 后续计划

### 一、已完成工作

#### 论文框架
- **8章大纲**已确定：`notes/thesis_outline.md`（含章节结构、subsection、图表清单、文献）
- **主贡献已重定位为**：multi-metric static + dynamic leaderboard for evaluating LLM-generated GUIs.
- **4个研究问题（RQ）**已更新：
  - RQ1：UIClip-style pairwise baseline 及其方法限制（position/order bias 作为控制项）
  - RQ2：LLM-generated GUI 的静态多维指标评估，以及自动/LLM评分与人工评分的对齐情况
  - RQ3：评价方法（zero-shot / rubric-guided / order-swap / 重复采样）的可靠性与成本 trade-off
  - RQ4 ⭐：Track B 静态质量指标与动态功能/任务验证结果之间的关系、互补和分歧
- **双轨设计**：Track A（UIClip-style reduced baseline）+ Track B（requirement-driven generated GUI + static/dynamic leaderboard 主线）

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
  - 明确 leaderboard 的主要对象是 generated GUI / generator model，而不是 judge model
- [ ] **Ch2草稿** `notes/draft_ch2_background.tex`
  - 整合gap matrix进完整Ch2叙述
  - §2.1 GUI Quality理论（Nielsen/ISO根基）
  - §2.2–§2.5 各节 → §2.6 Research Gap

#### Track B Pipeline（工程量最大）
- [x] Vision2Web Level 1/2筛选：先选10–20个pilot tasks，过滤无法本地渲染、依赖外部服务、或动态成功标准不清楚的项目
- [x] 明确排除Vision2Web Level 3 full-stack：backend/deployment/long-horizon workflow不进主线
- [ ] Requirement整理：复用Vision2Web的prototype/structured requirement/assets，必要时改写成统一自然语言requirement
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
