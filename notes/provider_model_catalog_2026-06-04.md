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

## Sources

- GWDG Chat AI available-models page: https://docs.hpc.gwdg.de/services/ai-services/chat-ai/models/index.html
- GWDG SAIA API documentation: https://docs.hpc.gwdg.de/services/ai-services/saia/index.html
- ChatAnywhere GitHub repository README: https://github.com/chatanywhere/GPT_API_free
- ChatAnywhere API documentation, model list/pricing page: https://docs.chatanywhere.tech/doc-2694962
- ChatAnywhere API documentation, `GET /v1/models`: https://docs.chatanywhere.tech/api-92222074

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

## Practical defaults for this thesis project

- Cheapest/free smoke-test path: use GWDG/SAIA first when the task fits an
  available GWDG-hosted model, per the project cost-control rule.
- Current GWDG model already used in Track B smoke runs: `qwen3.6-35b-a3b`.
- Conservative GWDG fallback for fast text smoke tests: `meta-llama-3.1-8b-instruct`.
- Fallback rule for tests: when GWDG/SAIA is rate-limited, quota-limited,
  timing out, or otherwise unavailable, switch to ChatAnywhere only with a
  low-cost model first. For Track B-style HTML generation, start with
  `gpt-4o-mini`, `gpt-4.1-mini`, or `gpt-5-mini`; use larger models only after
  prompt/gate validation.
- Every ChatAnywhere fallback run should record the trigger condition
  (for example GWDG rate limit, timeout, or HTTP 500), provider, base URL,
  model name, prompt id, and whether the selected model was a low-cost fallback.
- Avoid relying on ChatAnywhere `-ca` variants for reported thesis runs unless
  the run metadata records the variant and the provider caveat, because the
  docs describe them as cheaper third-party channels with potentially lower
  stability.
