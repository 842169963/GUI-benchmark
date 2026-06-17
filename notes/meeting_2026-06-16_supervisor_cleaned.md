# Supervisor Meeting Notes - 2026-06-16

Status: cleaned interpretation from an automatic Buzz transcript. This file
does not claim to be a verbatim transcript. It corrects obvious ASR/Buzz errors
and records uncertain terms explicitly.

Source transcript: `D:\obs录制\6.16 meeting 2.txt`

## Main Topic

The meeting discussed the current Track B / GUI benchmark work:

- generating web interfaces from fixed requirements,
- taking standardized screenshots of generated HTML artifacts,
- evaluating screenshots with a 16-item visual checklist,
- validating an LLM-as-a-judge protocol against preliminary human annotation,
- creating jittered/degraded variants to test judge sensitivity,
- drafting static, dynamic, accessibility, and leaderboard metrics.

The supervisor did not reject the direction. The main concern was that the
benchmark setup and measurement protocol are still under-specified. The next
step is to make the dataset, checklist, judge protocol, and metric formulas
clear enough for review.

## What the Supervisor Explicitly Asked to Receive

| Requested material | Meeting basis | How to provide it |
| --- | --- | --- |
| Dataset or dataset link | The supervisor asked where the requirements come from and then asked for the dataset or a link. | Send a small dataset folder/sample or a link, plus a short dataset description. |
| Slides | The supervisor asked for the slides after noting that many concepts were compressed. | Send the actual PowerPoint shown in the meeting: `presentations/track_b_progress_2026-06-12_v6.pptx`. |
| Short explanations accompanying the slides | The supervisor asked for "a couple of explanations" because static/dynamic/judge details were unclear. | Add README plus short methodology notes, not only the PPTX. |

The supervisor did not literally request a large package with many named files.
However, the questions asked during the meeting imply that a small organized
review package is the best way to answer him.

## Questions the Package Should Answer

### Dataset

The supervisor repeatedly asked:

- What dataset is used?
- Where do the requirements come from?
- Are requirements generated, extracted, or manually written?
- How many requirements/items are used?
- What does one requirement look like?
- What screenshots, workflows, routes, assets, and validations belong to one
  item?
- Is the chosen dataset too detailed/low-level or too abstract/open-ended?

Needed package response:

- `dataset/dataset_description.md`
- `dataset/sample_items/` or `dataset_link.txt`

### Visual Checklist

The supervisor asked how the checklist items were chosen. If they were produced
with LLM help, that alone is not enough. Each item should be connected to a
source, such as UI literature, design guidelines, or existing GUI-evaluation
work.

Needed package response:

- `methodology/static_visual_metrics.md`
- ideally a checklist source table: item, meaning, scoring rule, source, and
  status.

### Binary vs Likert Scoring

The supervisor questioned whether binary yes/no scoring is natural for
subjective UI quality. He suggested considering Likert-scale or ordinal ratings
and evaluating whether LLMs and humans behave differently under binary and
Likert settings.

Important correction:

- The transcript's "licker scale" means `Likert scale`.
- The transcript's "Kipendorf/Kruhenskappa" means `Krippendorff's alpha`.

Needed package response:

- Explain that binary scoring is the current protocol.
- Mark binary vs Likert as an open validation question, not a settled fact.

### Few-Shot Judge Examples

The supervisor asked whether few-shot examples contain only an overall score or
also the 16 item-level labels. His concern was that if the model is asked to
answer item-level checklist questions, the examples should probably show
item-level gold labels too.

Needed package response:

- `methodology/llm_judge_protocol.md`
- State current prompt structure.
- Check whether the current few-shot anchors include item-level labels.
- If they do not, mark this as a required follow-up experiment.

### Majority Voting

The supervisor clarified that majority voting is not a separate prompt type. It
is a technique applied on top of a prompt configuration, such as strict prompt
or few-shot prompt. The important implementation detail is whether the API is
called multiple times and then item-level answers are aggregated.

Needed package response:

- Explain whether the current protocol uses repeated API calls.
- Explain whether aggregation is item-level majority vote or score averaging.
- Avoid presenting "strict", "few-shot", and "majority voting" as three
  parallel prompt methods unless that is exactly how the implementation works.

### Human Annotation

The supervisor said the current human annotation is preliminary:

- The thesis author is not an independent annotator.
- Friends can be useful for a pilot, but the sample is small.
- Low human-human agreement limits the strength of claims.
- The current data should not be used to prove that one final judge setup is
  objectively correct.

Needed package response:

- `methodology/human_annotation_pilot.md`
- Use cautious wording such as "pilot reliability check" rather than final
  ground truth.

### LLM Judge Alternatives

The supervisor did not require testing 20 models. He suggested checking the
literature and trying one or two additional judge methods or configurations.
Possible directions discussed or implied:

- zero-shot judge,
- strict rubric-only judge,
- few-shot judge,
- few-shot plus repeated calls/majority vote,
- multiple LLM judges,
- Likert-scale judging,
- pairwise or preference-based judging.

Needed package response:

- List current judge method.
- List 1-2 candidate follow-up methods after literature checking.
- Do not make the thesis only about LLM judge benchmarking unless that becomes
  an explicit scope decision.

### Static and Dynamic Metrics

The supervisor found the static/dynamic leaderboard metrics unclear. He asked:

- How is the static score computed?
- What does a dynamic score like 0.5 mean?
- What exact checks are performed?
- Is a browser currently used?
- Is it route simulation, browser workflow validation, or a real agent?
- How are HTML/CSS/JS errors converted into scores?

Needed package response:

- `methodology/static_technical_metrics.md`
- `methodology/dynamic_browser_metrics.md`
- clearly separate:
  - static technical gate,
  - static visual screenshot evaluation,
  - route simulation,
  - browser workflow validation,
  - future real-agent evaluation, if not yet implemented.

### Generated Examples and Variation

The supervisor asked about model-generated GUI variation and weak-model outputs.
He seemed to agree that weaker models or jittered variants can help create a
quality range, but they must be explained.

Needed package response:

- `examples/original_generated/`
- `examples/jittered_generated/`
- optionally `examples/weak_model_outputs/`
- label these examples as preliminary/demo if they are not final results.

## Corrected Terms From Buzz Transcript

| Buzz / ASR text | Intended term |
| --- | --- |
| charge / church | judge |
| visual algorithm judge | visual LLM judge / multimodal LLM judge |
| assentate judgment | automated judgment |
| survey ID | survey item / checklist item |
| typography layout color overall | likely checklist dimensions; exact final dimensions should be checked against the slide/prompt |
| yes-bills | yes bias |
| view short / future | few-shot |
| generative votes / maturity voting | repeated calls / majority voting |
| Twitter variants | jitter variants |
| licker scale | Likert scale |
| Kipendorf / Kruhenskappa | Krippendorff's alpha |
| key / K value | Cohen's kappa or kappa value, depending on context |
| data board / read board | leaderboard |
| buoy | GUI |
| QV / Q / Quen | Qwen, exact model uncertain |
| gamma | Gemma, exact model uncertain |
| 54.5 / 54 million | likely GPT-4.1-mini or another judge model, needs verification from slides/results |
| static memory / SMT judgment | static metric / static evaluation, exact phrase uncertain |
| X-QoM scan | likely axe-core accessibility scan, needs verification from code |

## Package Scope After Correcting the Transcript

The package should be small and review-oriented:

```text
advisor_package_2026-06-17/
  README.md
  slides/
    track_b_progress_2026-06-12_v6.pptx
  dataset/
    dataset_description.md
    sample_items/
  methodology/
    benchmark_setup.md
    static_technical_metrics.md
    static_visual_metrics.md
    dynamic_browser_metrics.md
    llm_judge_protocol.md
    human_annotation_pilot.md
  examples/
    original_generated/
    jittered_generated/
  results/
    leaderboard_preview.md
  open_questions_for_supervisor.md
```

Do not send the full repository.

## Immediate Action Items

1. Send v6 PowerPoint, not v7.
2. Prepare a short dataset description and dataset sample/link.
3. Add concise explanations for benchmark setup, static/dynamic metrics, and
   LLM judge protocol.
4. Mark visual checklist source mapping as incomplete if not yet verified.
5. Mark current human annotation and leaderboard values as preliminary.
6. Ask the supervisor specifically for feedback on dataset suitability and
   metric design before expanding the benchmark further.

## Remaining Uncertainties

- The exact generator model names should be verified from
  `generation_metadata.json` files and the v6 slides.
- The exact judge model called "54.5" in the transcript should be verified from
  the judge result filenames or slide text.
- The exact 16 visual checklist items should be taken from the actual prompt or
  scoring script rather than the Buzz transcript.
- The current implementation of repeated judging should be checked to determine
  whether it uses item-level majority voting, score averaging, or both.
