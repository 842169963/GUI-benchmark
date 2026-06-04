# Prompt Schema

Status: planning specification for standardized generator prompts.

The generation prompt is part of the benchmark protocol. For any direct model
comparison, all generator models receive the same benchmark item context and the
same prompt schema.

## Main Input

The main leaderboard input is a generator model API/interface.

For each evaluated generator model, the pipeline applies the fixed benchmark
dataset and standardized prompt schema, generates artifacts, scores those
artifacts, and aggregates artifact-level scores into a model-level leaderboard
row.

## Prompt Invariance Rule

No model-specific prompt tuning is allowed within a comparison batch.

Allowed:

- one fixed prompt schema per experiment condition
- documented prompt versions
- ablation conditions with explicit prompt IDs
- provider-specific transport formatting only when it does not change semantic
  prompt content

Not allowed:

- rewriting the task for one model because it performs poorly
- adding examples for one model but not another
- changing route, validation, or asset instructions per model
- silently replacing a prompt version after generated artifacts have been
  produced

## Recommended Generator Prompt Slots

A generator prompt should include these slots:

```text
Prompt ID
System role / generator role
Output format requirements
Allowed files and asset rules
Viewport and rendering assumptions
Benchmark item ID
Requirement text
Expected pages/routes
Required elements
Dynamic tasks or workflows
Validation rules
Visual pages or prototype screenshot order
Local resource paths
Metadata expectations
```

The exact final prompt text used in a formal or reported experiment must be
versioned and preserved according to `notes/prompt_preservation_policy.md`.

## Output Requirements

For the current Track B style of generated web app, the prompt should request:

- a complete executable web artifact
- inline or locally available code only, depending on the artifact format
- no network dependency unless the benchmark explicitly allows it
- deterministic route or page behavior where required
- visible required content and controls
- metadata stored by the pipeline, not embedded secrets or credentials

The prompt should prioritize complete, evaluable artifacts over decorative
detail.

## Token and Cost Policy

The evaluation protocol should avoid presenting any fixed truncating
output-token cap as the final policy.

If a provider requires a maximum output setting, choose a value high enough to
allow complete outputs where feasible. Record the actual values:

- input tokens
- output tokens
- total tokens
- finish reason
- latency
- estimated cost
- provider/model identifier
- timestamp

Token usage and cost are efficiency metrics. They should not be hidden, and they
should not be used as a low artificial cap that prevents some models from
producing complete interfaces.

## Prompt Preservation

Save thesis-impacting prompts when they affect reported results, metrics,
benchmark protocol, annotation protocol, output schemas, or reproducibility.

This includes:

- GUI generation prompts
- LLM-as-a-judge prompts
- LLM-based dynamic validation prompts, if dynamic validation later uses an
  LLM-generated plan or oracle
- human annotation instructions
- output schemas that constrain model responses used in metrics

Routine planning prompts and coding-assistant prompts are not stored in the
thesis appendix unless the thesis explicitly uses them as experimental material.

## Metadata Fields

Each generated artifact should record:

```json
{
  "prompt_id": "TB-GEN-vX",
  "model": "model-name",
  "provider": "provider-name",
  "timestamp": "ISO-8601 timestamp",
  "parameters": {
    "temperature": 0.2,
    "max_output_tokens": "provider setting if applicable"
  },
  "usage": {
    "input_tokens": 0,
    "output_tokens": 0,
    "total_tokens": 0
  },
  "latency_seconds": 0,
  "estimated_cost_usd": 0,
  "finish_reason": "stop"
}
```

The provider setting is logged for reproducibility, but the thesis should not
present a fixed truncating cap as the final evaluation policy.
