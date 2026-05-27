# Leaderboard Metric Design

Working notes for the GUI-quality leaderboard metric system used by this
thesis. Records both the original draft and the revised proposal so the
design rationale and trade-offs are visible in the final write-up.

Status: **draft** — not yet implemented in any scorer. Decisions here
should be validated by a small pilot before being committed to the
methodology chapter or to any leaderboard run.

## 1. Original draft (rejected as-is)

Three layers:

- **Technical pre-check** — Renderability / Build Success (pass/fail).
- **Static (1–5 Likert, 6 dimensions)** —
  Requirement Alignment, Content Completeness,
  Layout & Visual Hierarchy, Visual Aesthetics,
  Consistency & Professionalism, Basic Accessibility.
- **Dynamic** — Task Success / Effectiveness (pass/fail or success
  rate), Interaction Correctness (pass/fail per check),
  Runtime Stability (pass/fail / error count),
  Interaction Efficiency (steps / time / normalised score).

Source mapping: ISO 9241-11, ISO/IEC 25010, WCAG 2.2,
Lavie & Tractinsky 2004, VisAWI (Moshagen & Thielsch), WebQual,
UIClip, UI-Bench, FrontendBench, ArtifactsBench.

### Concerns with the original draft

1. **Static-dimension overlap.** Layout & Visual Hierarchy, Visual
   Aesthetics, and Consistency & Professionalism are likely to be
   highly correlated when scored by an MLLM judge. Six Likert
   dimensions will probably collapse to 2–3 latent factors and add
   unnecessary judge variance.
2. **Absolute 1–5 Likert with MLLM-as-judge is fragile.** Anchor drift
   between calls is a known issue (UI-Bench specifically motivates
   pairwise + Elo for this reason). Likert can stay, but should be
   anchored and complemented by a pairwise robustness check.
3. **Basic Accessibility does not belong on a 1–5 scale.** WCAG 2.2 is
   rule-based; using `axe-core` / Lighthouse is more defensible and
   reproducible than asking an MLLM to score accessibility 1–5.
4. **Requirement Alignment vs. Content Completeness overlap.** A judge
   will conflate "does it match the spec" with "is everything there".
5. **No aggregation rule.** Eleven metrics with no defined combination
   means the leaderboard cannot rank submissions.
6. **Dynamic metrics need a concrete protocol.** Task Success and
   Interaction Correctness require defined test scripts; this should
   reference FrontendBench-style scripted assertions.

## 2. Revised proposal

Four layers. Goal: do not let an MLLM judge anything that can be
automated; merge overlapping dimensions; define an aggregation rule.

### Layer 0 — Technical Pre-check (gate, pass/fail)

A submission that fails this gate is excluded from the leaderboard and
is not scored further.

| Indicator | Check |
| --- | --- |
| Build / Render Success | Build completes without errors and DOM renders |
| No Fatal Console Errors | No uncaught exceptions in the first 5 s of load |

### Layer 1 — Static Quality (MLLM-as-judge, 3 anchored Likert dimensions)

The original six static dimensions are merged to three. Each dimension
is scored 1–5 with explicit anchor descriptions written into the judge
prompt (see Section 4). The pairwise Elo from Section 3 is reported
alongside as a robustness check.

| Dimension | Covers | 1 | 3 | 5 |
| --- | --- | --- | --- | --- |
| Functional Completeness | Requirement Alignment + Content Completeness | ≥50 % of required elements missing | Most elements present, 1–2 missing or wrong | All required elements present and semantically correct |
| Layout & Hierarchy | Layout & Visual Hierarchy | Overlap, misalignment, no hierarchy | Readable but information hierarchy unclear | Clear grid alignment, hierarchy obvious at a glance |
| Visual Quality | Visual Aesthetics + Consistency & Professionalism | Clashing colours, inconsistent typography and styling | Mostly consistent style with rough details | Polished and consistent, product-grade visual quality |

### Layer 2 — Accessibility (rule-based, automated, not MLLM-judged)

Run `axe-core` (or Lighthouse) and report:

| Sub-indicator | Measure |
| --- | --- |
| WCAG 2.2 Violations | Counts at critical / serious / moderate / minor severity |
| Accessibility Score | `1 - min(1, weighted_violations / N_elements)` normalised to `[0, 1]` |

### Layer 3 — Dynamic / Functional (scripted, FrontendBench-style)

Each item ships with predefined Playwright / Puppeteer scripts. All four
metrics are normalised to `[0, 1]` so they aggregate cleanly.

| Indicator | Measure | Aggregation |
| --- | --- | --- |
| Task Success Rate | Per-task final assertion outcome | passed tasks / total tasks |
| Interaction Correctness | Per-step sub-assertions (state change after click, etc.) | passed assertions / total assertions |
| Runtime Stability | Console errors / unhandled rejections during interaction | `1 / (1 + error_count)` |
| Interaction Efficiency | Steps / time relative to reference implementation | `min(1, ref_steps / actual_steps)` |

### Aggregation

```
if pre_check == fail:
    excluded
else:
    static_score   = mean(FC, LH, VQ)        # 1–5
    a11y_score     = 1 - weighted_violations # 0–1
    dynamic_score  = mean(TSR, IC, RS, IE)   # 0–1

    composite = 0.4 * normalise(static_score)
              + 0.2 * a11y_score
              + 0.4 * dynamic_score
```

Report **all four** numbers in the thesis: static, a11y, dynamic, and
the composite. Reporting only the composite hides per-axis differences
and makes ablations harder to interpret.

## 3. Robustness check: pairwise comparison

In addition to the absolute Likert scoring above, the same MLLM judge
runs a pairwise comparison between submissions on the same item for the
three static dimensions. Pairwise results are aggregated into an Elo
score. The thesis reports correlation between the Likert composite and
the Elo ranking as a reliability check, following UI-Bench precedent.

## 4. Judge prompt status

The MLLM-as-judge prompt for the three anchored Likert dimensions and
for the pairwise comparison **is not yet written**. When it is written,
it must be saved verbatim to
`thesis/appendices/prompt_templates.tex` per the project's
appendix-prompt rule (see `memory/feedback_save_experiment_prompts.md`)
and assigned an explicit prompt id (e.g. `LB-JUDGE-v1`).

## 5. Open questions before pilot

- Should the static composite weight FC, LH, VQ equally, or should
  Functional Completeness be weighted more heavily because it tracks
  requirement satisfaction?
- Should the composite weights `(0.4, 0.2, 0.4)` be motivated from an
  external source (e.g. ISO 25010 sub-characteristic prioritisation) or
  treated as a hyper-parameter and sensitivity-tested?
- For Interaction Efficiency, does the dataset already ship a reference
  step count per task, or does it need to be added to the benchmark
  metadata?
- How many submissions per item are needed before pairwise Elo is
  meaningful, and is the planned pilot large enough to compute it?

## 6. Pilot plan (next step)

1. Pick 3–4 Track B items already passing the static gate (e.g.
   `F03_about_gitlab`, `F09_elections_bc`, `F10_gourmania`).
2. Collect 2–3 generated submissions per item from different generator
   models.
3. Run the MLLM judge with the anchored Likert prompt on all
   submissions; record per-dimension scores.
4. Run pairwise comparison on the same submissions; compute Elo.
5. Run `axe-core` on each submission.
6. Run the existing scripted dynamic checks where available.
7. Compute correlation matrix across FC, LH, VQ to test whether the
   three-dimension merge is justified. If two dimensions correlate at
   `r > 0.9` across submissions, consider merging further.
8. Decide whether to lock the four-layer system into the methodology
   chapter or revise.
