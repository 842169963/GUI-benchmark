# Track B Vision2Web Pilot Plan

## Decision

Track B will use a reduced Vision2Web Level 1 / Level 2 subset as the primary pilot source.

- Level 1 (`webpage` config): static webpage generation, visual/rubric scoring only.
- Level 2 (`frontend` config): interactive frontend generation, visual/rubric scoring plus dynamic task validation.
- Level 3 (`website` config): excluded from the thesis scope because it introduces backend state, deployment, authentication, and long-horizon full-stack workflow complexity.

Design2Code remains a static UI-to-code reference and reserve source, not the main Track B substrate.

## Dataset Facts

Source: `zai-org/Vision2Web` on Hugging Face.

Configs:

| Config | Level | Count | Use in thesis |
| --- | --- | ---: | --- |
| `webpage` | Level 1 | 100 | Static visual/rubric pilot cases |
| `frontend` | Level 2 | 66 | Main static + dynamic Track B pilot cases |
| `website` | Level 3 | 27 | Excluded |

Repository archives:

| Archive | Approx. size | Note |
| --- | ---: | --- |
| `archives/webpage.tar.gz` | 431 MB | Feasible to download if needed |
| `archives/frontend.tar.gz` | 2.63 GB | Large; download only after task selection is fixed |
| `archives/website.tar.gz` | not needed | Level 3 excluded |

License note: Vision2Web dataset README states `CC-BY-NC-SA-4.0`. This is acceptable for academic research, but public redistribution in the thesis repository or leaderboard should use attribution and avoid commercial use.

## Pilot Selection Criteria

Prioritize tasks that:

- are Level 2 interactive frontend tasks with 4-7 functional test cases;
- have clear `prompt_preview` requirements;
- do not obviously require backend accounts, authentication, payment, or live external services;
- have moderate resource counts, to reduce local setup and rendering friction;
- cover varied UI domains such as SaaS, public service, content, community, events, and services.

Avoid for the pilot:

- tasks with very high test counts (for example 12+);
- tasks with very large resource counts unless strategically useful;
- Level 3 full-stack tasks;
- tasks whose main value depends on backend state or real external data.

## Proposed Level 2 Pilot Tasks

These are the initial dynamic-capable Track B candidates.

| ID | Task | Tests | Resources | Prototypes | Rationale |
| --- | --- | ---: | ---: | ---: | --- |
| F01 | `1daycloud` | 6 | 35 | 6 | SaaS/cloud navigation; clear multi-page structure |
| F02 | `401trucksource` | 6 | 79 | 6 | Commerce/dealership workflow; realistic navigation |
| F03 | `about_gitlab` | 4 | 109 | 6 | Developer/SaaS site; strong recognizable structure |
| F04 | `academy_govloop` | 5 | 160 | 6 | Education/public-sector learning platform |
| F05 | `balancingbirthbaby` | 5 | 18 | 6 | Service business; low resource count and clear content |
| F06 | `community_dynamics` | 6 | 48 | 5 | Community/forum interface; useful interaction checks |
| F07 | `community_hpe` | 7 | 45 | 4 | Community/content interface with moderate complexity |
| F08 | `copenhagenmarathon` | 5 | 169 | 6 | Event site; date/countdown/register-style semantics |
| F09 | `elections_bc` | 5 | 37 | 6 | Public-service navigation; different domain |
| F10 | `gourmania` | 4 | 50 | 6 | Content/recipe site; compact test count |

Reserve Level 2 candidates:

| Task | Tests | Resources | Reason to reserve |
| --- | ---: | ---: | --- |
| `casefox` | 9 | 251 | Good SaaS/legal case, but heavier resources |
| `caplugs` | 8 | 70 | E-commerce/product categories, slightly more tests |
| `afl` | 5 | 167 | Sports/content site, useful if one selected task fails |
| `fsb` | 4 | 68 | Public/institutional content, low test count |
| `git_drupalcode` | 5 | 4 | Developer repository interface, very low resources |

## Proposed Level 1 Static Control Tasks

These are static-only controls for rubric scoring and rendering pipeline checks.

| ID | Task | Resources | Prototypes | Rationale |
| --- | --- | ---: | ---: | --- |
| W01 | `aihw` | 0 | 3 | Very light static case |
| W02 | `aws` | 1 | 3 | Familiar cloud landing page structure |
| W03 | `eventbrite` | 9 | 3 | Event/commerce-style layout |
| W04 | `ebay` | 3 | 3 | Familiar marketplace layout |

## Immediate Next Steps

1. [x] Download/extract only after confirming the pilot task list.
2. [x] Extract the Level 1/2 archives and copy only selected task directories into `data/track_b/vision2web_raw/`.
3. [x] Create normalized Track B item directories:
   - `requirement.md`
   - `prototypes/`
   - `resources/`
   - `workflow.json` if available
   - `source_meta.json`
4. [ ] Generate a first batch with two generator models.
   - [x] Smoke test: generated `F09_elections_bc` with `claude-sonnet-4-5-20250929` via ChatAnywhere Anthropic endpoint.
   - [x] Added `TB-GEN-v2` prompt constraints for complete HTML, same-file JavaScript handlers, workflow-required interactions, and responsive no-overflow layout.
   - [x] Iterated to `TB-GEN-v4`, which passes the static generation gate on `F09_elections_bc`.
   - [x] Added static generation gate script: `scripts/check_track_b_generation.py`.
   - [x] Revised the current generation prompt to `TB-GEN-v6`: desktop is the primary evaluation viewport; mobile/responsive behavior is recorded as future work, not a hard gate; workflow-required interactions remain hard requirements; secondary navigation and missing real PDF assets are treated as visible-content/quality issues rather than automatic generation failures.
   - [x] Added `gwdg-openai` support for the GWDG/SAIA OpenAI-compatible API.
   - [x] Ran a GWDG/SAIA smoke generation using `qwen3.5-397b-a17b` as the primary model; it timed out, so the valid artifact uses fallback `qwen3.6-35b-a3b` with `TB-GEN-v6` and a 40k output budget.
   - [ ] Run Claude with the same `TB-GEN-v6` prompt on `F09_elections_bc` to create a fair same-prompt comparison against the valid Qwen fallback artifact. Two ChatAnywhere attempts on 2026-05-25 (`claude_sonnet45_v6_smoke`, `claude_sonnet45_v6_smoke_retry`) failed with HTTP 524 before writing artifacts; retry later or use a more stable Anthropic-compatible provider.
   - [x] Created `TB-GEN-v7` as a compact prompt while keeping `max_tokens=20000`. Claude wrote an artifact, but the static gate failed because `Local Forms` was implemented as an inert `div`.
   - [x] Created `TB-GEN-v8` with exact workflow-label-to-route mappings and explicit `<a>` / `<button>` requirements. Both Claude and GWDG/SAIA Qwen fallback generated valid `F09_elections_bc` artifacts at `max_tokens=20000`, and both passed the static gate.
5. [ ] Render each generated UI with Playwright and save:
   - `generated.html`
   - `screenshot.png`
   - `dom.json`
   - `render_log.json`

## Extraction Status

Selected task directories have been extracted to `data/track_b/vision2web_raw/`.

- Level 2 `frontend`: 10/10 selected tasks extracted. Each has `prompt.txt`, `workflow.json`, `prototypes/`, and `resources/`.
- Level 1 `webpage`: 4/4 selected tasks extracted. Each has `workflow.json`, `prototypes/`, and `resources/`; these tasks do not include `prompt.txt` in the original dataset format.
- Extraction summary: `data/track_b/vision2web_extraction_summary.json`.

## Normalization Status

Selected tasks have been normalized into `data/track_b/items/`.

Each normalized item now contains:

- `requirement.md`
- `workflow.json`
- `prototypes/`
- `resources/`
- `source_meta.json`
- empty `generated/` and `renders/` directories for later stages

Level 2 requirements are copied from Vision2Web `prompt.txt`. Level 1 requirements are generated as static responsive webpage requirements from the prototype filenames and workflow viewports.

Normalization script: `scripts/normalize_track_b_vision2web_items.py`

Normalization summary: `data/track_b/normalization_summary.json`

## Generation Smoke Test

First smoke run:

- Item: `F09_elections_bc`
- Model/provider: `claude-sonnet-4-5-20250929` via `chatanywhere-anthropic`
- Prompt: `TB-GEN-v1`
- Output: `data/track_b/items/F09_elections_bc/generated/claude_sonnet45_smoke/`
- Render screenshots: `data/track_b/items/F09_elections_bc/renders/claude_sonnet45_smoke_chrome_desktop.png` and `data/track_b/items/F09_elections_bc/renders/claude_sonnet45_smoke_chrome_mobile.png`

Smoke-test result: the generation pipeline works end-to-end and the desktop render is non-empty. The mobile render shows horizontal overflow, so the formal generation prompt/render gate should be tightened before running the full Track B batch.

Static gate result on the first smoke run: failed. The generated HTML is missing closing `</body>` / `</html>` tags, uses `onclick="showPage(...)"` without defining `showPage`, and references route ids that are not present in the document. This confirms that the first smoke run should not be included as a valid Track B generation result.

Follow-up implemented locally: `TB-GEN-v2` through `TB-GEN-v5` and `scripts/check_track_b_generation.py`.

Current valid smoke run:

- Run: `claude_sonnet45_v4_smoke`
- Prompt: `TB-GEN-v4`
- Gate report: `data/track_b/items/F09_elections_bc/generated/claude_sonnet45_v4_smoke/gate_report.json`
- Result: passed all static gate checks. The generated HTML closes properly, defines `showPage`, includes `window.__TRACK_B_ROUTES`, and exposes workflow-required controls as clickable anchors/buttons.

Important comparison note: this Claude artifact uses `TB-GEN-v4`, while the valid Qwen artifact uses `TB-GEN-v6`. It is valid as a pipeline smoke result, but it should not be used as the primary Claude-vs-Qwen comparison because prompt-version differences would confound generator quality.

`TB-GEN-v5` adds a route-handler no-scroll refinement and stricter mobile CSS wording, but the first v5 generation attempt failed with ChatAnywhere HTTP 524 before an artifact was written.

Current next smoke run:

- Provider/key: GWDG/SAIA via local `GWDG_API_KEY` and `https://chat-ai.academiccloud.de/v1`.
- Primary model: `qwen3.5-397b-a17b`.
- Fallback model: `qwen3.6-35b-a3b` if the primary model times out, rejects multimodal data URLs, or returns unusable HTML.
- Prompt: `TB-GEN-v6`.
- Rationale: the listed GWDG/SAIA model set includes multiple multimodal-capable options; `qwen3.5-397b-a17b` is selected first because it is the largest Qwen-family model available in the account and is expected to be strong at structured HTML/CSS/JavaScript generation from visual and textual requirements. The fallback keeps the same provider while reducing likely latency and gateway risk.

GWDG/SAIA smoke result on `F09_elections_bc`:

- `qwen3.5-397b-a17b` did not return within the 360 second read timeout. No artifact was written. This makes it a poor current choice for batch generation despite being the strongest-looking model on paper.
- `qwen3.6-35b-a3b` with the default 20k output budget wrote an artifact, but the provider returned `finish_reason = length`; the HTML was truncated before `</body></html>` and before the route handler was complete.
- `qwen3.6-35b-a3b` with `--max-tokens 40000` wrote `data/track_b/items/F09_elections_bc/generated/gwdg_qwen36_35b_v6_smoke_40k/`. The generation finished normally with `finish_reason = stop`, 24,638 prompt tokens, 19,192 completion tokens, 43,830 total tokens, and about 135 seconds elapsed.
- Static gate: passed after updating the gate to recognize delegated route links using `data-route-target` plus a shared `addEventListener` handler.
- Route checks: direct hash loads for `#voter_registration` and `#local_election_forms` expose the expected sections and active route state.
- Visual caveat: the desktop screenshot is non-empty, but the initial viewport scrolls past the utility/header/navigation area to the homepage section. Treat this as a prompt/rendering issue caused by hash/anchor route handling, not as a hard gate failure. The next prompt should add a delayed no-scroll safeguard or use a non-anchor route token.

Generation-gate boundary for `TB-GEN-v6`:

- Hard checks: complete HTML, non-truncated script/style, defined click handlers, implemented route ids, and clickable workflow labels.
- Not hard checks in the current phase: mobile overflow, fully functional secondary navigation items that are not in the workflow, and real downloadable PDF files when the dataset does not provide PDF assets.
- Interpretation: missing secondary pages or real PDF downloads should be reported as generated-UI quality limitations, but they should not block the smoke pipeline unless the workflow explicitly requires that interaction.

Recommended immediate next step:

- Treat `TB-GEN-v8` as the current same-prompt comparison candidate because it avoids the Claude 524 timeout seen with `TB-GEN-v6`, fixes the inert-control failure seen with `TB-GEN-v7`, and works for both Claude and Qwen fallback at `max_tokens=20000`.
- Use the free GWDG/SAIA API key first for future prompt smoke tests to reduce cost. Use paid/proxy providers only after the prompt and gate are validated or when the experiment specifically requires that provider.
- Treat the generator leaderboard unit as the generated HTML submission, aggregated by generator model and requirement set. The benchmark item supplies the fixed screenshots, requirement, workflow checks, and assets; submitters provide the executable UI artifact and generator metadata.
- Run `qwen3.6-35b-a3b` and Claude with `TB-GEN-v8` on 2-3 diverse Track B items before expanding to the full pilot.

## Thesis Framing

Track B is not a full Vision2Web reproduction. It is a reduced, thesis-specific subset inspired by Vision2Web, selected to support a generator leaderboard for LLM-generated executable web interfaces and the thesis question:

> How do static GUI-quality signals relate to dynamic task-validation outcomes for LLM-generated executable web interfaces?
