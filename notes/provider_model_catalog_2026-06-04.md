# Provider Model Catalog for Local Experiment Keys

Checked on 2026-06-04. This note records model names from provider-maintained
documentation so Track B generation runs do not need to probe models one by one.
No API keys or secret values are recorded here.

## Local environment mapping

| Local env setting | Provider/use | Base URL |
| --- | --- | --- |
| `GWDG_API_KEY`, `GWDG_BASE_URL` | GWDG Chat AI / SAIA OpenAI-compatible API | `https://chat-ai.academiccloud.de/v1` |
| `OPENAI_API_KEY`, `OPENAI_BASE_URL` | ChatAnywhere OpenAI-compatible API | `https://api.chatanywhere.tech/v1` |
| `ANTHROPIC_API_KEY`, `ANTHROPIC_BASE_URL` | ChatAnywhere Anthropic-style or OpenAI-compatible proxy endpoint currently configured in this project | `https://api.chatanywhere.org/v1` |
| `TUZI_API_KEY`, `TUZI_BASE_URL` | Tuzi OpenAI-compatible API | `https://api.tu-zi.com/v1` |

## Sources

- GWDG Chat AI available-models page: https://docs.hpc.gwdg.de/services/ai-services/chat-ai/models/index.html
- GWDG SAIA API documentation: https://docs.hpc.gwdg.de/services/ai-services/saia/index.html
- ChatAnywhere GitHub repository README: https://github.com/chatanywhere/GPT_API_free
- ChatAnywhere API documentation, model list/pricing page: https://docs.chatanywhere.tech/doc-2694962
- ChatAnywhere API documentation, `GET /v1/models`: https://docs.chatanywhere.tech/api-92222074
- Tuzi API web console/documentation entry: https://api.tu-zi.com/
- Tuzi public API landing page: https://apihead.tu-zi.com/

## GWDG / SAIA

The SAIA API documentation says API users can list available models via
`GET https://chat-ai.academiccloud.de/v1/models`, but the following API model
names are explicitly listed in the documentation. Use these names first for
scripted runs.

| API model name | Notes from provider docs |
| --- | --- |
| `deepseek-r1-distill-llama-70b` | Open-weight text/reasoning model hosted by GWDG. |
| `meta-llama-3.1-8b-instruct` | GWDG describes this as its standard lightweight recommended model. |
| `openai-gpt-oss-120b` | Open-weight OpenAI GPT-OSS model hosted by GWDG. |
| `qwen3.5-122b-a10b` | Qwen model; docs describe vision-capable multimodal use. |
| `qwen3.5-397b-a17b` | Larger Qwen MoE model; docs describe vision-capable multimodal use. |
| `qwen3.6-35b-a3b` | Qwen MoE model used in this project for Track B smoke runs. |
| `qwen3-30b-a3b-instruct-2507` | Qwen instruct model. |
| `qwen3-coder-30b-a3b-instruct` | Qwen coding-specialized model. |
| `qwen3-omni-30b-a3b-instruct` | Qwen multimodal/omni model. |
| `qwen3-embedding-4b` | Embedding model listed in the SAIA API model-name table. |

Additional GWDG-hosted open-weight models appear on the Chat AI model page, but
were not all shown in the SAIA API model-name table during this check:

- DeepSeek R1
- Devstral 2
- Gemma 4
- GLM-4.7
- InternVL 3.5 30B A3B
- Llama 3.1 8B Instruct
- Mistral Large Instruct 3 675B Instruct 2512
- GPT OSS 120B
- Qwen 3 30B A3B Instruct 2507
- Qwen 3 Coder 30B A3B Instruct
- Qwen 3 Omni 30B A3B Instruct
- Qwen 3.5 122B A10B
- Qwen 3.5 397B A17B
- Qwen 3.6 35B A3B
- OpenGPT-X Teuken 7B Instruct Research
- E5 Mistral 7B Instruct Embeddings

The Chat AI page also lists external provider models, including Anthropic Claude
Sonnet 4.6 and OpenAI GPT-5/GPT-4.1 families. The SAIA documentation states
that OpenAI external models are not generally available for API usage, so these
should not be assumed usable with the project GWDG API key unless access is
confirmed separately.

## ChatAnywhere

ChatAnywhere's README says the project supports common model families including
`gpt`, `deepseek`, `claude`, `gemini`, `grok`, `qwen`, `kimi`, and `minimax`.
It also states that the free API key supports `deepseek`, `gpt-3.5-turbo`,
embedding models, `gpt-4o` series, and `gpt-5` series. The full pricing/model
page warns that its list may lag provider changes, so use the table below as a
documented provider source, not as a guarantee of runtime availability.

### Chat and reasoning models listed as supported

| Family | Supported model names from ChatAnywhere docs/README |
| --- | --- |
| GPT-5 / GPT-4 / OpenAI chat | `gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini`, `gpt-5.4-mini-2026-03-17`, `gpt-5.4-nano`, `gpt-5.4-nano-2026-03-17`, `gpt-5.4-2026-03-05`, `gpt-5.2`, `gpt-5.2-2025-12-11`, `gpt-5.2-chat-latest`, `gpt-5.2-pro`, `gpt-5.2-pro-2025-12-11`, `gpt-5.1`, `gpt-5.1-2025-11-13`, `gpt-5.1-chat-latest`, `gpt-5.1-codex`, `gpt-5-search-api`, `gpt-5`, `gpt-5-codex`, `gpt-5-pro`, `gpt-5-mini`, `gpt-5-nano`, `gpt-5-chat-latest`, `gpt-4.1`, `gpt-4.1-2025-04-14`, `gpt-4.1-mini`, `gpt-4.1-mini-2025-04-14`, `gpt-4.1-nano`, `gpt-4.1-nano-2025-04-14`, `gpt-oss-20b`, `gpt-oss-120b`, `gpt-3.5-turbo`, `gpt-3.5-turbo-1106`, `gpt-3.5-turbo-0125`, `gpt-3.5-turbo-16k`, `gpt-3.5-turbo-instruct`, `gpt-4o-search-preview`, `gpt-4o-search-preview-2025-03-11`, `gpt-4o-mini-search-preview`, `gpt-4o-mini-search-preview-2025-03-11`, `gpt-4`, `gpt-4o`, `gpt-4o-2024-11-20`, `gpt-4o-mini`, `gpt-4-0613` |
| OpenAI reasoning | `o3`, `o3-2025-04-16`, `o4-mini`, `o4-mini-2025-04-16`, `o3-mini` |
| ChatAnywhere `-ca` variants | `gpt-5.4-ca`, `gpt-5.5-ca`, `gpt-5.4-mini-ca`, `gpt-5.4-nano-ca`, `gpt-5-codex-ca`, `gpt-5.1-codex-ca`, `gpt-5.2-codex-ca`, `gpt-5.2-ca`, `gpt-5.2-chat-latest-ca`, `gpt-5.1-ca`, `gpt-5.1-chat-latest-ca`, `gpt-5-ca`, `gpt-5-mini-ca`, `gpt-5-nano-ca`, `gpt-5-chat-latest-ca`, `gpt-4.1-ca`, `gpt-4.1-mini-ca`, `gpt-4.1-nano-ca`, `gpt-4-ca`, `gpt-4o-ca`, `gpt-4o-mini-ca` |
| DeepSeek | `deepseek-v3.2`, `deepseek-v3.2-thinking`, `deepseek-v3-2-exp`, `deepseek-v3.1-250821`, `deepseek-v3.1-think-250821`, `deepseek-reasoner`, `deepseek-r1`, `deepseek-r1-250528`, `deepseek-v3`, `deepseek-chat` |
| Claude | `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-sonnet-4-6-thinking`, `claude-opus-4-6`, `claude-opus-4-6-thinking`, `claude-opus-4-5-20251101`, `claude-opus-4-5-20251101-thinking`, `claude-haiku-4-5-20251001`, `claude-haiku-4-5-20251001-thinking`, `claude-sonnet-4-5-20250929`, `claude-sonnet-4-5-20250929-thinking`, `claude-opus-4-1-20250805`, `claude-opus-4-1-20250805-thinking` |
| Gemini | `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-flash-nothinking`, `gemini-2.5-flash-lite`, `gemini-3-pro-preview`, `gemini-3-flash-preview`, `gemini-3-flash-preview-nothinking`, `gemini-3.1-pro-preview`, `gemini-3.1-flash-lite-preview` |
| Grok | `grok-4`, `grok-4-fast` |
| Qwen | `qwen3.5-plus`, `qwen3.5-397b-a17b`, `qwen3-max-2026-01-23`, `qwen3-235b-a22b`, `qwen3-235b-a22b-instruct-2507`, `qwen3-coder-plus`, `qwen3-coder-480b-a35b-instruct` |
| Kimi / GLM / MiniMax | `kimi-k2.5`, `glm-4.7`, `glm-5`, `minimax-m2.1`, `minimax-m2.5` |

`gpt-3.5-turbo-ca` is explicitly listed as not supported in the ChatAnywhere
pricing/model page and should be avoided.

### Image, audio, and embedding models listed as supported

| Type | Supported model names from ChatAnywhere docs/README |
| --- | --- |
| Image generation/editing | `gpt-image-2-ca`, `gpt-image-1.5`, `gpt-image-1`, `gpt-image-1-mini`, `dall-e-3`, `dall-e-3-hd`, `dall-e-2`, `gemini-2.5-flash-image-preview`, `gemini-3-pro-image-preview`, `gemini-3.1-flash-image-preview` |
| Text-to-speech / transcription | `tts-1`, `tts-1-hd`, `gpt-4o-mini-tts`, `Whisper`, `gpt-4o-mini-transcribe`, `gpt-4o-transcribe` |
| Embeddings | `text-embedding-ada-002`, `text-embedding-3-small`, `text-embedding-3-large` |

`gpt-image-2` without the `-ca` suffix is listed as not supported in the
ChatAnywhere pricing/model page.

## Tuzi

Tuzi is configured as an OpenAI-compatible provider in the local scripts under
the provider name `tuzi-openai`. The default base URL is
`https://api.tu-zi.com/v1`; the scripts send chat requests to
`/chat/completions`.

Local smoke test on 2026-06-12:

- `scripts/probe_model_capabilities.py --provider tuzi-openai --model
  gpt-4.1-mini --chat-smoke --output-cap 1` succeeded.
- The Tuzi `/models` endpoint returned HTTP 200 and 748 available model IDs for
  this account.
- `gpt-4.1-mini` returned HTTP 200 with `finish_reason=stop` in 1.874 seconds,
  using 12 prompt tokens and 2 completion tokens.

Track B generation smoke test on 2026-06-12:

- Command: `scripts/generate_track_b_ui.py --item F10_gourmania --provider
  tuzi-openai --model gpt-4.1-mini --prompt-id TB-GEN-v16 --input-profile
  compact --max-prototypes 1 --max-tokens 12000 --run-name
  tuzi_gpt41mini_v16_f10_smoke`.
- Result: generation stopped normally (`finish_reason=stop`) after 81.97
  seconds, with 5,028 prompt tokens, 7,574 completion tokens, and 12,602 total
  tokens.
- Static gate passed with zero error failures and one warning: one generated
  local image reference did not exist.
- Standard screenshot capture succeeded for the single detected route.
- Dynamic workflow simulation passed 5/8 cases, with route success 1.000,
  content validation success 0.625, and task success 0.625.

Pricing note: Tuzi's public landing page describes several routing/price
groups, including a very low-cost default group and more expensive fast/stable
or original-price groups. The local `/models` response used in this project did
not expose per-model price fields, so reported cost estimates for Tuzi runs
should use the provider's current billing page or account transaction record at
the time of the run, not infer a precise price from the model list alone.

## Practical defaults for this thesis project

- Cheapest/free smoke-test path: use GWDG/SAIA first when the task fits an
  available GWDG-hosted model, per the project cost-control rule.
- Current GWDG model already used in Track B smoke runs: `qwen3.6-35b-a3b`.
- Conservative GWDG fallback for fast text smoke tests: `meta-llama-3.1-8b-instruct`.
- First paid/proxy fallback for low-cost Track B generation: Tuzi
  `gpt-4.1-mini`, because it is now locally confirmed to support both tiny chat
  smoke tests and a compact `TB-GEN-v16` F10 generation. Keep it as a smoke and
  development fallback until at least two or three items have been checked.
- Fallback rule for tests: when GWDG/SAIA is rate-limited, quota-limited,
  timing out, or otherwise unavailable, switch to a paid/proxy provider only
  with a low-cost model first. Current order:
  1. GWDG/SAIA `qwen3.6-35b-a3b` for cheap/free smoke tests.
  2. Tuzi `gpt-4.1-mini` for low-cost paid/proxy generation smoke tests.
  3. ChatAnywhere standard `gpt-4.1-mini`, `gpt-4o-mini`, or `gpt-5-mini`
     when Tuzi is unavailable or a second paid provider is needed.
  4. ChatAnywhere `-ca` variants only for explicitly labelled low-cost
     experiments, because the provider documentation describes them as cheaper
     but less stable than non-`-ca` routes.
  5. Larger models such as Claude Sonnet, Gemini Pro, or GPT full-size models
     only after the prompt/gate pipeline is validated.
- Pricing interpretation: ChatAnywhere publishes per-model token prices in its
  model table, including `gpt-4.1-mini` and `gpt-4.1-mini-ca`. Tuzi currently
  requires checking its account billing/routing page for exact per-run price,
  although the local API smoke confirms model availability. GWDG/SAIA remains
  the preferred cost-control path because it is the free academic provider.
- Every ChatAnywhere fallback run should record the trigger condition
  (for example GWDG rate limit, timeout, or HTTP 500), provider, base URL,
  model name, prompt id, and whether the selected model was a low-cost fallback.
- Every Tuzi fallback run should record the provider as `tuzi-openai`, the base
  URL, model name, prompt id, token usage, latency, finish reason, and the
  account billing/routing price source used for cost estimation.
- Avoid relying on ChatAnywhere `-ca` variants for reported thesis runs unless
  the run metadata records the variant and the provider caveat, because the
  docs describe them as cheaper third-party channels with potentially lower
  stability.

## Token-limit capability note, 2026-06-05

The provider model-list endpoints available to this project do not expose a
complete per-model context-window or max-output table. For Track B generation,
record token limits from three separate evidence classes:

1. Published provider documentation, when available.
2. Local observed generation metadata, including prompt/completion token counts.
3. Local provider error messages, when a request is rejected before generation.

Do not treat unknown limits as unlimited. The relevant generation constraint is
the combined context budget: input tokens, multimodal/image tokens, output
tokens, and provider-side overhead must fit the provider/model limit.

The current local capability table is:

- `data/track_b/model_capabilities/model_capability_table_2026-06-05.json`
- `data/track_b/model_capabilities/model_capability_smoke_gwdg_2026-06-05.json`
  records a 1-token GWDG smoke probe for `qwen3.6-35b-a3b` and
  `qwen3-omni-30b-a3b-instruct`.

The helper script for future low-cost checks is:

- `scripts/probe_model_capabilities.py`

The probe script defaults to low-cost behavior. Its chat smoke mode asks for
`OK` only, so even a high requested `--output-cap` tests request acceptance
without forcing long generation. That means it is appropriate for checking
whether a provider accepts `max_tokens=40000`, but it does not prove that the
model will produce a useful 40k-token HTML artifact.

Current practical interpretation:

- `gwdg-openai/qwen3-omni-30b-a3b-instruct` has a locally observed hard total
  context limit of 65,536 tokens from the F03 `TB-GEN-v15` rejection. It is
  usable for smaller multimodal items, but F03-style inputs must be compressed
  or moved to another model.
- `gwdg-openai/qwen3.6-35b-a3b` has locally accepted F03 prompts around 83k
  prompt tokens and a 40k requested output cap. Its exact hard limit is still
  unknown, but it is the strongest current GWDG candidate for larger Track B
  smoke runs.
- `openai/gpt-4o-mini`, `openai/gpt-4.1`, `openai/gpt-5-mini`,
  `chatanywhere-anthropic/claude-sonnet-4-5-20250929`,
  `openai/gemini-2.5-flash`, and `openai/gemini-2.5-pro` remain paid/proxy
  fallback candidates through ChatAnywhere or compatible gateways. Reported
  runs must record the configured provider and base URL because proxy behavior
  can differ from official provider limits.
- `tuzi-openai/gpt-4.1-mini` is locally confirmed as a working low-cost
  OpenAI-compatible fallback for compact Track B generation. The first F10
  smoke result is eligible for static/dynamic evaluation but has one static
  warning for a missing local image source and only partial dynamic content
  success.
