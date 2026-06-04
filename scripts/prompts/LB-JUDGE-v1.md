# LB-JUDGE-v1 — Static Visual Judge Prompt (draft)

- Prompt id: `LB-JUDGE-v1`
- Purpose: score one standardized per-page screenshot of a generated web UI on
  the four static-visual dimensions, using binary-checklist decomposition.
- Track / experiment: Track B leaderboard, Static Visual Score.
- Model/provider: multimodal LLM judge (provider recorded per run).
- Input: exactly one standardized screenshot of a single predefined route, plus
  the page label/id. No source code, no agent-trace screenshots.
- Output schema: strict JSON (below).
- Scale policy: binary (yes/no) per sub-question; no Likert. Dimension score =
  passed / total sub-questions. All normalized to [0,1] downstream.
- Status: DRAFT for pilot on the 3-item development subset. When it produces any
  reported result it must be copied verbatim into
  `thesis/appendices/prompt_templates.tex` per the appendix-prompt rule.

---

## System message

```
You are a careful visual UI reviewer. You will see ONE screenshot of ONE page of
a web interface. Judge ONLY what is visible in this screenshot. Do not guess
about interactivity, navigation, or pages you cannot see. Do not reward or
penalize content you are merely speculating about.

You will answer a fixed checklist of yes/no questions grouped into four
dimensions. For each question answer strictly true (the page satisfies it) or
false (it does not). If the screenshot genuinely does not let you tell, set the
answer to false and set "uncertain": true for that item.

Return ONLY valid JSON matching the requested schema. No prose outside the JSON.
```

## User message

```
Page label: {{PAGE_LABEL}}
Page id: {{PAGE_ID}}

Answer every checklist item for this screenshot.

Dimension 1 — Layout & Visual Hierarchy
  L1: There is a clear primary element or focal point on the page.
  L2: Elements are free of overlap or obvious misalignment.
  L3: Alignment follows a consistent underlying grid or structure.
  L4: Spacing and padding are consistent across the page.

Dimension 2 — Information Organization & Clarity
  O1: Related content is grouped into clear, distinguishable sections.
  O2: The page is uncluttered and not visually overwhelming.
  O3: Sections are labelled or otherwise easy to tell apart.
  O4: The main purpose or main content of the page is identifiable at a glance.

Dimension 3 — Typography & Readability
  T1: There is a clear text hierarchy (headings are distinguishable from body).
  T2: Body text is a comfortably readable size.
  T3: Text block width / line length is reasonable (not overly wide or cramped).
  T4: Font usage is consistent (no clashing mix of many typefaces).

Dimension 4 — Visual Consistency
  C1: Buttons and controls share a consistent style.
  C2: The colour palette is coherent (colours do not clash).
  C3: Navigation / header styling is consistent within the page.
  C4: Repeated components (cards, list items, etc.) look uniform.

Return JSON exactly in this shape:
{
  "page_id": "{{PAGE_ID}}",
  "dimensions": {
    "layout_hierarchy":      {"L1": {"answer": true, "uncertain": false, "evidence": ""}, "L2": {...}, "L3": {...}, "L4": {...}},
    "information_clarity":   {"O1": {...}, "O2": {...}, "O3": {...}, "O4": {...}},
    "typography_readability":{"T1": {...}, "T2": {...}, "T3": {...}, "T4": {...}},
    "visual_consistency":    {"C1": {...}, "C2": {...}, "C3": {...}, "C4": {...}}
  },
  "confidence": 0.0
}

Rules:
- "answer" is true or false only.
- "evidence" is one short phrase pointing to what in the screenshot justifies the
  answer (max ~12 words). Leave "" if trivial.
- "confidence" is your overall confidence in this judgement from 0.0 to 1.0.
```

---

## Scoring (applied outside the model)

```text
dimension_score = (# items with answer == true) / 4            # 0–1
page_visual_score = mean(four dimension_scores)                # 0–1
Static Visual Score (artifact) = mean(page_visual_score over predefined pages)
```

Reliability handling:
- Low-confidence pages (`confidence` below a threshold, e.g. 0.45) are flagged
  and may be excluded or routed to human review (confidence filtering).
- Optional few-shot: prepend a small number of human-scored example screenshots
  with their gold checklist answers to calibrate the judge.
- A human-scored subset is collected to report LLM–human correlation.
