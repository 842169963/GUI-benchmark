# Track A Results Memo

## Purpose

Track A is a UIClip-style baseline. It does not make position bias the main thesis topic. Its role is to establish how a modern multimodal LLM behaves on simple screenshot pairwise GUI quality judging before the thesis moves to rubric-based and dynamic evaluation.

## Data

Main dataset: `biglab/uiclip_human_data_hf`.

Important limitation: this dataset stores single screenshots with captions, not explicit pairwise preference rows. Pairs are derived automatically by matching screenshots with the same normalized page description where one caption indicates `well-designed` and the other indicates `poor design`, `bad contrast`, or `bad proximity`.

Thesis wording: **caption-matched UIClip-human-derived pairs**.

## Current Main Result

Result file: `scripts/results/track_a_eval_gpt-4o_20260506_142748_clean85.json`

Condition: zero-shot pairwise prompt, GPT-4o, order-swap enabled.

| Metric | Value |
|--------|-------|
| Pairs after manual cleaning | 85 |
| Total model calls | 170 |
| Raw accuracy | 62.4% |
| Accuracy when good image is A | 38.8% |
| Accuracy when good image is B | 85.9% |
| Consistency rate | 52.9% |
| Position bias rate | 47.1% |
| Corrected accuracy on consistent pairs | 73.3% |
| Chose A / Chose B | 45 / 125 |

## Interpretation

The result shows moderate alignment between GPT-4o and UIClip-derived GUI quality labels. Simple pairwise judging is fragile: the model chooses the second image far more often than the first. This supports order-swapping as a necessary methodological control, while motivating the thesis move beyond pairwise comparison toward rubric-guided and multidimensional evaluation.

## Thesis Use

- RQ1: modern-model baseline on UIClip-style GUI quality judging.
- RQ3: evidence that single-order pairwise evaluation is unreliable and judging strategy matters.
- Bridge to Track B: pairwise screenshots provide limited information, motivating rubric scoring and dynamic task evaluation.

## Relation to Position-Bias Literature

Shi et al. (2025), *Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge*, already establishes position bias as a general reliability issue in LLM-as-a-judge settings. The Track A result should therefore not be framed as the thesis's main novelty or as a new discovery of position bias.

The thesis contribution is narrower and domain-specific: it shows that the same methodological risk appears in **multimodal GUI screenshot quality judging**, including UIClip-style pairwise comparison, and that a rubric-guided prompt does not automatically fix it. This motivates using order-swap as a control and supports the move beyond pairwise judgments toward multidimensional GUI evaluation.

## Prompt Strategy Comparison

The rubric-guided prompt was run on the same clean85 pair set.

Rubric result file: `scripts/results/track_a_eval_openai_gpt-4o_rubric_20260506_162332.json`

| Metric | Zero-shot clean85 | Rubric-guided clean85 |
|--------|-------------------|-----------------------|
| Raw accuracy | 62.4% | **57.1%** |
| Accuracy when good image is A | 38.8% | **20.0%** |
| Accuracy when good image is B | 85.9% | **94.1%** |
| Consistency rate | 52.9% | **25.9%** |
| Position bias rate | 47.1% | **74.1%** |
| Corrected accuracy on consistent pairs | 73.3% | **77.3%** |
| Chose A / Chose B | 45 / 125 | **22 / 148** |

Interpretation: rubric guidance did not improve pairwise reliability in this setup. It increased the model's tendency to choose the second image, lowering raw accuracy and consistency. This is useful for RQ3: more detailed judging instructions are not automatically better and must be evaluated empirically.

## Next Experiment

Possible next step: test whether a stronger anti-position-bias instruction or structured JSON output reduces the B-position preference, but avoid over-expanding Track A before starting the Track B rubric pipeline.
