# Supervisor Brief - GUI Benchmark / Leaderboard

Status: concise review note after the 2026-06-16 meeting.

## 1. What This Package Contains

This package contains:

- the PowerPoint shown in the meeting,
- the dataset source and one normalized sample item,
- compact examples of original generated pages and one degraded/jittered page,
- representative implementation scripts and output reports,
- a preliminary leaderboard preview,
- short notes on literature support and open design questions.

## 2. Dataset

The current pilot uses a reduced subset derived from Vision2Web.

External source:

- Hugging Face: https://huggingface.co/datasets/zai-org/Vision2Web
- GitHub: https://github.com/zai-org/Vision2Web
- Paper: https://arxiv.org/abs/2603.26648

Current normalized selection:

- 14 items total,
- 10 Level 2 frontend items,
- 4 Level 1 static webpage/control items,
- Level 3 full-stack tasks excluded because they add backend/deployment/auth
  complexity outside the current thesis scope.

Included sample item:

- `dataset/sample_item_F01/requirement.md`
- `dataset/sample_item_F01/workflow.json`
- `dataset/sample_item_F01/source_meta.json`

Open question:

- Is this Vision2Web-derived subset suitable for the thesis benchmark, or is it
  too detailed/low-level for the intended evaluation goal?

## 3. Benchmark Unit

One benchmark item is the fixed task specification. It contains the requirement,
workflow actions/validations, and source metadata.

One generated artifact is one model's generated implementation for one item.
In this pilot it is usually:

- `index.html`: the generated web UI,
- `generation_metadata.json`: run metadata,
- evaluation reports such as `gate_report.json` or
  `browser_workflow_report.json`.

What `generation_metadata.json` is for:

- records which model/provider/prompt created the artifact,
- records finish reason, token counts, latency, and generation settings,
- helps detect failures such as output truncation,
- makes leaderboard rows reproducible and auditable.

It is not itself an evaluation metric. It is provenance for the generated
artifact.

## 4. Static vs Dynamic: The Boundary

Static and dynamic evaluation can both use the same `workflow.json`, but they
answer different questions.

| Layer | Main question | Example |
| --- | --- | --- |
| Static technical | Does the generated HTML contain the structure needed for evaluation? | Is there a `Contact` button/route? Is `showPage()` defined? |
| Dynamic/browser | Does clicking through the UI actually reach the expected page and content? | After clicking `Contact`, is the contact page visible and is the form present? |
| Static visual | Does a screenshot look visually organized/readable/consistent? | Does the page have clear hierarchy and no overlap? |

So static technical checks existence/structure; dynamic checks behavior after
actions; static visual checks screenshots.

## 5. Static Technical Evaluation

Purpose:

Static technical evaluation is a deterministic gate before screenshots, browser
workflows, or LLM visual judging. It checks whether the generated artifact is
structurally evaluable.

Included implementation and evidence:

- implementation copy: `implementation/check_track_b_generation.py`
- representative outputs: `examples/*/gate_report.json`
- inputs: `dataset/sample_item_F01/workflow.json`, `examples/*/index.html`,
  `examples/*/generation_metadata.json`

Current checks include:

- complete HTML document structure,
- closed `body`, `html`, `style`, and `script` tags,
- provider stop reason is not `max_tokens` or `length`,
- click-handler functions exist,
- route/page identifiers referenced by navigation controls exist,
- quoted workflow click labels appear as clickable controls where applicable,
- local image sources are not missing,
- semantic click descriptions are warnings rather than hard failures.

Concrete example:

If the generated HTML contains:

```html
<button onclick="showPage('contact')">Contact</button>
```

the static gate checks that:

- a JavaScript function `showPage` is defined;
- a page/section with `id="contact"` exists;
- the visible `Contact` control is a clickable `<button>` or `<a>`.

What this does not prove:

- It does not prove that clicking the button works in a browser.
- It does not prove that the destination page contains the required contact
  form.

Those belong to dynamic/browser evaluation.

Literature/design basis:

- This exact gate is a project-specific engineering design.
- Vision2Web motivates fixed requirements/workflows and verification targets.
- WebDevJudge and web-development evaluation work motivate separating
  implementation/technical checks from visual judging.
- The practical reason is cost and reproducibility: cheap deterministic checks
  catch broken artifacts before expensive browser or LLM evaluation.

## 6. Static Visual Evaluation

Current workflow:

1. Generate an artifact from the item requirement.
2. Render predefined routes/pages locally.
3. Capture standardized screenshots with fixed viewport and wait conditions.
4. Ask the visual LLM judge to answer a 16-item checklist from screenshots only.
5. Aggregate item answers into page and artifact visual scores.
6. Validate judge behavior against a small human pilot before using it for a
   leaderboard column.

Included implementation/evidence:

- implementation copies:
  - `implementation/score_track_b_visual.py`
  - `implementation/visual_judge_workflow_summary.md`
- example screenshots: `examples/*/*.png`

Checklist dimensions:

- layout and visual hierarchy,
- information organization and clarity,
- typography and readability,
- visual consistency.

Current scoring:

```text
dimension_score = passed checklist items / 4
page_visual_score = mean(four dimension scores)
artifact_visual_score = mean(page scores)
```

Why binary checklist instead of Likert in the current pilot:

- Binary checklist answers give item-level agreement data and are easier to
  aggregate with Cohen's kappa.
- The design tries to reduce broad scale-use differences and central-tendency
  effects that can occur with wide Likert scales.
- CheckEval supports checklist decomposition as a reliability-oriented strategy,
  but it is from text evaluation; applying it to GUI screenshots is a
  methodological transfer, not a fully proven GUI-specific rule.
- Preston & Colman support that response-category choice affects reliability
  and discriminating power.

Important open issue:

- The supervisor's concern remains valid: subjective UI quality may not be
  naturally binary.
- Binary scoring is therefore a current pilot choice, not a final assumption.
- A Likert or pairwise sensitivity check can be added if the supervisor thinks
  it is necessary.

What "source-mapped" means:

- Each of the 16 checklist items should be mapped to a source or rationale.
- Example: "spacing and alignment" may be linked to visual hierarchy/layout
  literature; "typography readability" may be linked to UI readability or web
  design evaluation sources.
- If an item has no direct literature source, it should be labelled as a
  project-specific operationalization and justified as such.

Planned next step:

- Create a table: checklist item -> what it measures -> scoring rule ->
  literature/source or project rationale -> uncertainty.

## 7. Dynamic / Browser Evaluation

Purpose:

Dynamic evaluation checks whether workflow actions can reach the expected
route/page and whether the reached page contains expected content.

Included implementation and evidence:

- implementation copies:
  - `implementation/run_track_b_dynamic_workflow.py`
  - `implementation/run_track_b_browser_workflow.js`
- representative outputs:
  - `examples/*/dynamic_workflow_report.json`, where available
  - `examples/*/browser_workflow_report.json`, where available
  - `examples/*/browser_workflow_normalized_report.json`, where available

Two implemented layers:

| Layer | How it works | What it proves |
| --- | --- | --- |
| Route simulation | Parses generated HTML, chooses likely clickable controls, simulates route transitions, and checks text/card/form/image evidence. | Fast deterministic first-pass workflow signal. |
| Browser workflow validation | Opens the generated HTML in Chromium/Playwright, clicks real visible controls, and checks visible DOM/text afterwards. | Stronger evidence that the generated UI works in a browser. |

Future layer:

- Real agent evaluation, where an autonomous agent operates the UI from a
  high-level goal, is not required for the current benchmark design. It is a
  possible future extension only.

Why Playwright is enough for the current thesis scope:

- The current benchmark items already contain fixed workflow actions and
  validations.
- The goal is to compare generated artifacts under the same predefined checks,
  not to test whether an autonomous agent can discover its own strategy.
- Playwright/Chromium is more reproducible than a real LLM/VLM agent because it
  executes the same scripted workflow every time.
- A real agent would add a second source of uncertainty: if the task fails, it
  becomes unclear whether the generated UI is bad or the agent made a poor
  decision.

When a real agent would become necessary:

- if the thesis goal changes to open-ended user tasks;
- if workflows are given as high-level goals rather than explicit actions;
- if recovery from unexpected UI labels/layouts becomes part of the evaluation;
- if the benchmark aims to evaluate computer-use agents, not generated web
  artifacts.

Current position:

- Use Chromium/Playwright as the main dynamic validation layer.
- Mention real-agent evaluation only as future work or optional extension.

Concrete example:

From `F01_1daycloud/workflow.json`, one case asks the evaluator to click the
`"Contact"` navigation item and validate that:

- the contact page/route is reached,
- contact information is visible,
- a contact form with fields is present.

Route simulation tries to infer this from HTML. Browser workflow validation
actually opens the page and clicks the visible control.

Score meaning:

- `route_success_rate`: proportion of cases where the expected route/section is
  reached.
- `content_validation_success_rate`: proportion of expected content checks that
  pass after reaching the destination.
- task success rate: combined task level success, when available.
- A dynamic score such as `0.5` should be read only together with its
  denominator and report type.

Literature/design basis:

- Vision2Web motivates workflow-based verification for generated web artifacts.
- WebArena, Mind2Web, and VisualWebArena motivate browser/agent-style web task
  evaluation.
- The current route/content heuristics are project-specific and should be
  reported as implementation choices.

## 8. LLM Judge Protocol

Current workflow:

1. Capture standardized screenshots.
2. Human raters answer the same visual checklist on a small validation subset.
3. The LLM judge answers the checklist from screenshots.
4. The judge is run repeatedly for stability checks.
5. Item-level majority vote aggregates repeated judge outputs.
6. Agreement with humans is measured before using the judge for leaderboard
   scoring.

Current judge idea:

- screenshot-only visual judging,
- structured JSON output,
- strict/few-shot prompt variants,
- repeated calls with item-level majority vote in the frozen pilot setup.

Why this design:

- The judge is treated as a measurement instrument, not as ground truth.
- Strict prompting and few-shot anchors are used because early runs showed
  strong yes-bias.
- Repetition/majority vote is used because even temperature-zero calls varied
  on borderline pages in the pilot.

Metrics:

- Pearson's `r`: page-level correlation. It asks whether the judge and humans
  rank pages similarly.
- Cohen's `kappa`: item-level chance-corrected agreement for binary checklist
  answers. It corrects for agreement that would occur just because most items
  are often answered "yes".

Literature/design basis:

- Cohen (1960) supports kappa for nominal agreement.
- LLM-as-a-judge surveys motivate validating automated judges.
- MLLM-as-UI-Judge and WebDevJudge motivate caution for multimodal UI/web
  judging.
- Judge's Verdict motivates comparing judge-human behavior against human
  agreement patterns, but the current use is an adapted pilot criterion.

Open issue from the meeting:

- If few-shot examples currently include only final scores, they should be
  revised/tested to include all 16 item-level gold labels, because the model is
  asked to answer item-level checklist questions.

What "gold labels" means here:

- A gold label is the human reference answer for one checklist item.
- For one screenshot, gold labels mean the full set of 16 human answers:
  `L1-L4`, `O1-O4`, `T1-T4`, and `C1-C4`.
- Example: for an anchor screenshot, the prompt should ideally show not only
  `overall score = 0.50`, but also which of the 16 items are `true` or `false`.
- The final score is derived from those item-level answers, so item-level gold
  labels are more useful than only giving the model an overall score.
- This is especially important for few-shot anchors, because the model is being
  trained in-context to answer the same 16 checklist questions.

Current uncertainty:

- The exact existing few-shot prompt should be checked to confirm whether the
  anchors include item-level gold labels or only final scores.
- If they include only final scores, this should be tested as a prompt variant:
  final-score-only anchors vs item-level-gold anchors.

## 9. Human Annotation

The current human annotation is a pilot reliability check, not final ground
truth.

Limitations:

- the thesis author is not an independent annotator,
- friends are useful for a pilot but the sample is small,
- low human-human agreement limits strong claims.

Safer wording:

> The current human annotation is used as a pilot reliability check for the
> visual judging protocol. It is not claimed to provide a final ground-truth
> benchmark.

## 10. Leaderboard Design

The leaderboard aggregates artifact-level results into model-level rows.

Included implementation/evidence:

- implementation copy: `implementation/build_track_b_dev_subset_demo.py`
- preview: `results/leaderboard_preview.md`

Why these row fields exist:

| Field | Reason |
| --- | --- |
| attempted | Counts how many artifacts were generated/evaluated for the model. |
| eligible | Separates artifacts that are valid enough to compare from failed attempts. |
| failed | Makes generation/evaluation failures visible instead of silently dropping them. |
| failure categories | Explains whether a failure came from truncation, provider issues, static gate failure, or dynamic failure. |
| completion reliability | Measures how often the model produces an evaluable artifact. |
| static technical | Captures structural/evaluability checks. |
| static visual | Captures screenshot visual quality after judge validation. |
| dynamic | Captures workflow route/content success. |
| accessibility | Captures rule-based accessibility checks, e.g. axe/WCAG. |
| efficiency | Records tokens/latency so quality can be compared with cost/runtime. |
| overall | Left pending because category weights are a value judgment. |

Design principles:

- failures are not silently dropped;
- `not applicable` is different from score `0`;
- category scores remain visible so one overall number does not hide the
  failure mode;
- overall weighting should be decided after supervisor feedback.

Literature/design basis:

- Vision2Web motivates benchmark-style evaluation over fixed web tasks.
- The exact leaderboard schema is project-specific. It is designed for
  auditability and failure transparency rather than copied from one paper.

## 11. Final Benchmark Scope

There are two possible end states for the benchmark.

### Option A: Controlled Thesis Evaluation Pipeline

This is the safer thesis scope.

The thesis author runs selected models under controlled conditions:

- fixed dataset/subset,
- fixed generation prompt/version,
- fixed provider/model settings where possible,
- fixed static technical gate,
- fixed screenshot protocol,
- fixed visual judge protocol,
- fixed browser workflow validation,
- fixed leaderboard aggregation.

The thesis reports reproducible model comparisons and carefully explains
failures, limitations, and pilot judge validation.

### Option B: API-Key Leaderboard Workflow

This is a possible future or prototype direction.

An external user provides:

- provider/model name,
- API key or endpoint,
- optional generation settings.

The benchmark system then automatically:

- loads fixed benchmark items,
- sends generation prompts,
- saves generated artifacts and metadata,
- runs static technical checks,
- captures screenshots,
- runs visual judging,
- runs browser workflow validation,
- aggregates leaderboard rows.

This would make the benchmark easier for external users, but it adds additional
engineering and methodological issues:

- API key handling,
- provider/rate-limit instability,
- cost control,
- security,
- reproducibility across providers and dates,
- whether external users should also be allowed to submit pre-generated HTML
  artifacts.

Current proposed framing:

- For the thesis, prioritize Option A: controlled evaluation pipeline.
- Present Option B as a future leaderboard/prototype direction unless the
  supervisor wants the public API-key workflow to become part of the core
  thesis contribution.

Question for supervisor:

- Should the final benchmark be framed primarily as a controlled thesis
  evaluation pipeline, or should the API-key-based leaderboard workflow be part
  of the main thesis scope?

## 12. Generated Examples

This minimal package includes compact examples:

- `examples/original_qwen_F01/`: unchanged original Qwen-generated artifact.
- `examples/original_qwen_F10/`: unchanged original Qwen-generated artifact with
  browser report and screenshot.
- `examples/original_gpt4omini_F10/`: unchanged original GPT-4o-mini artifact.
- `examples/original_claude_F09/`: unchanged original Claude artifact with
  browser workflow report.
- `examples/jitter_severe_F01/`: severe jitter/degraded variant.

The full local project contains more Qwen, Claude, GPT, and jitter examples.

## 13. Main Questions for Feedback

1. Is the dataset/subset suitable?
2. Are the static technical checks appropriate as a deterministic gate?
3. Is the static/dynamic/browser split clear and methodologically acceptable?
4. Is binary checklist scoring acceptable, or should Likert/pairwise be added?
5. Are the current checklist dimensions appropriate if source-mapped?
6. How much LLM judge validation is enough for the thesis scope?
7. Should the final benchmark be framed as a controlled thesis pipeline, or as
   an API-key-based leaderboard workflow?
8. What should enter the final leaderboard aggregation, and what should remain
   separate category scores?
