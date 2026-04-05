# Changelog

## 2026-04-05
- Scrubbed a leaked Twilio Account SID from `3-good-calls-still-need-polsh-but-good-03-16-2026-last-call-of -the-night.md` and republished `main` cleanly after GitHub push-protection blocked the previous commit.
- Added a run-level completion gate in `mini-agent/backend/agent/runner.py` so prompts that declare explicit required artifact filenames (for example `/workspace/...`) cannot end as `done` until those artifacts are actually written via tool calls.
- Added replay logging for missing-required-artifact gate events to make future benchmark miss cases directly diagnosable from session telemetry.
- Added first-class Firecrawl tools (`firecrawl_scrape`, `firecrawl_interact`) in the runtime tool registry and wired `scrape_page` to prefer Firecrawl automatically when `FIRECRAWL_API_KEY` is configured.
- Updated tool-manifest docs and verification skill metadata so Firecrawl appears in dynamic research-tool discovery via `read_tool_schema`.
- Hardened the `xml_mcp_reasoning` compatibility parser for MiroThinker-style mixed output: it now recovers tool intents from `<tool>...</tool_call>` wrappers and JSON payload blocks, defaults missing `server_name` to `harness`, and strips recovered scaffolding from the visible final answer path.

## 2026-04-02
- Added a narrow OpenAI-compatible model-compatibility adapter path for MiroThinker-style outputs via `xml_mcp_reasoning`.
- Implemented parsing channels for `<think>` reasoning, `<use_mcp_tool>` XML intent, and final answer text while preserving raw output in compatibility telemetry logs.
- Added policy-gated XML tool intent handling: validate server name, validate tool name against approved registry, validate JSON arguments, and block unknown or malformed tool intents safely.
- Added minimal parser tests for think-only, think+tool-call, malformed XML, malformed arguments JSON, and plain-answer outputs.

## 2026-04-01
- Hardened artifact retrieval compatibility across canonical and legacy storage roots to reduce post-restart `404` preview/download failures when older sessions reference files written under prior paths.
- Updated file listing and session zip download behavior to include files from both current and legacy artifact roots for the same session id.

## 2026-03-20
- Reframed the active roadmap around operational autonomy instead of generic feature growth.
- Marked the message adapter layer as the first current priority, with Syndicate as the first platform-specific autonomy target after adapters.
- Updated repo instructions and state docs so future runs inherit the operational-asset standard instead of defaulting to benchmark/demo-first behavior.
- Recorded the real state of the current channel slice more explicitly: Telegram webhook bridge exists, but queueing, WhatsApp, and canonical action receipts are still missing.

## 2026-03-17
- Completed the persistent browser voice loop in PolyMorph: the voice button now starts a live session, speech turns auto-dispatch into `/api/voice/turn`, Kokoro realtime TTS plays the reply, and the session resumes listening until toggled off.
- Removed the old practical dependence on Chatterbox/Moss/`Emily.wav` for the normal voice-button path, set Kokoro realtime as the intended TTS path, and made `af_heart` the default voice.
- Added browser-side and backend-side debugging around voice execution:
  - browser: `[LiveASR]`, `[VoiceSession]`, `[VoiceMode]`
  - backend: `[AudioStream]`, `[VoiceTurn]`
- Added an idle-commit fallback for voice mode so the live loop can continue when ASR partials are visible but upstream finalization is delayed.
- Verified that the current live voice model can be set independently from the main chat model through env alone.
- Updated the active validated voice configuration to:
  - primary `qwen3.5-122`
  - fallback `omnicoder`
  - gateway `https://api.aetherpro.tech/v1`
  - Kokoro realtime TTS with default voice `af_heart`
- Confirmed that the active voice lane currently uses the normal `run_agent(...)` harness prompt stack rather than a dedicated lightweight voice persona prompt.
- Added root recovery/handoff documents for the voice milestone:
  - `VOICE_REALTIME_IMPLEMENTATION_CONTEXT_2026-03-17.md`
  - `VOICE_REALTIME_PROJECT_STATE_2026-03-17.md`
  - `LLM_HANDOFF_CURRENT_STATE_2026-03-17.md`

## 2026-03-13
- Confirmed the current realtime ASR to PolyMorph Voice Mode to TTS stack is working in live operator use and recorded that verification in project-state.
- Added a root proprietary `LICENSE` and a repo-level `.gitignore` for initial private git versioning.
- Added the current Tailscale/node-access note to active project-state references and corrected stale absolute repo paths.
- Added the internal fleet-aware operator layer backed by `fleet-inventory/`, including inventory normalization, helper-script audit, SSH/Tailscale execution wrappers, and inventory-aware operator actions.
- Replaced the old fleet build plan with a new Polymorph-native channel control plane plan, scaffolded `mini-agent/backend/channels/`, added `/api/channels` routes, and wired Telegram/channel runtime settings into the existing Connections config surface.
- Added `HARNESS_TOOL_REFERENCE.md` as the exact benchmark-generation reference for the current tool registry and scaffolded the first Telegram webhook bridge path on top of the new channel control plane.

## 2026-03-14
- Simplified the provider control plane around the unified gateway at `https://api.aetherpro.tech/v1`, removed active code assumptions about multiple client-facing LiteLLM gateways, and kept routing model-name-based behind the gateway.
- Added per-request Qwen reasoning-mode control and defaulted production/direct-answer flows to `enable_thinking=false` so short Qwen3/Qwen3.5 turns no longer disappear into `reasoning_content` by default.
- Fixed provider bootstrap/env loading so the backend now loads `mini-agent/.env`, `mini-agent/backend/.env`, and `mini-agent/.env.polymorph` in a deterministic order instead of depending on current working directory.
- Changed provider failover behavior so an explicit fallback no longer silently accumulates extra implicit LiteLLM fallbacks unless explicitly opted in.
- Verified the current provider chain resolves as intended for the active model test case: primary `minicpm-v` on `api.aetherpro.tech`, explicit fallback `vulnllm-r-7b` on the same router.
- Fixed the OpenAI-compatible streaming context-window retry path so retryable `400 maximum context length` responses now resend the same provider request with a reduced output-token budget.
- Added proactive OpenAI-compatible output-budget clamping and iteration-scoped history compaction so small-context router targets no longer start every turn from the same `4097 + 4096 > 8192` shape.
- Clarified that context-window failures are request-budget errors and must not silently hop across providers.
- Stopped context-window failures from degrading into the provider's no-tool fallback notice path, so request-budget bugs surface cleanly instead of being hidden by tool stripping.
- Verified the exact LiteLLM-style `8192 / 4097 / 4096` error now reduces the retry budget to `4079`.
- Verified the current live env stack resolves `minicpm-v` as primary and no distinct fallback target because the configured fallback currently dedupes to the same router/model as primary.
- Reduced prompt overhead by enabling per-turn tool selection instead of sending the full 40-tool schema on every request.
- Stopped injecting harness self-description metadata into every prompt by default and compacted the temporal context block.
- Compared the current harness against the known-good `Minimax-M2.5` copy and confirmed the main prompt-budget regression came from tool/schema growth and extra prompt blocks rather than the older repo having “better routing.”
- Added the first real tool manifest/bootstrap layer: `mini-agent/backend/TOOLS.md`, `read_tool_schema`, and session-cached dynamic schema loading.
- Added a product handoff doc for porting the same manifest/bootstrap tool architecture into the product repo.
- Normalized OpenAI-compatible model output so visible `<think>` leakage is stripped, pseudo tool-call JSON can be recovered into real tool calls, and raw compat text is buffered until final normalization instead of being streamed straight into the chat UI.
- Upgraded PolyMorph Voice Mode so the TTS leg now prefers gateway-backed realtime Kokoro streaming with browser chunk playback, while keeping the older HTTP synth path as fallback.

## 2026-03-12
- Hardened PolyMorph ASR live-start auth handling to follow the optional-auth gateway contract and avoid sending invalid bearer tokens by default.
- Updated visible frontend branding from AetherOps-facing labels to a cleaner PolyMorph presentation.
- Removed redundant hero-logo clutter and relabeled the status bar tool check indicator as core health checks.
- Added selective placement of the new March 11 logo set: ambient orb in the hero, waveform accent in the sidebar, and a dedicated voice-mode mark in the Voice pane.

## 2026-03-11
- Replaced the main composer mic flow with live ASR websocket capture and partial transcript UI.
- Added backend live ASR session bootstrap at `POST /api/audio/stream/start` so browser streaming can reuse server-side ASR credentials.
- Rewired the `Voice` button to use the same finalized live ASR transcript before sending the turn into PolyMorph Voice Mode.

## 2026-03-09
- Replaced the failed direct Phi-4 voice path with a split PolyMorph voice lane.
- Added a dedicated frontend `PolyMorph Voice Mode` pane backed by `qwen3.5-4b`.
- Kept the mic button on batch WAV ASR transcription into the main composer.
- Added backend voice routes for qwen4b text responses and TTS audio file playback.
- Updated ASR health/transcription probing to prefer the current `/v1/asr/*` gateway contract.

## 2026-03-06
- Added Project State package for explicit human-readable and machine-readable repo state.
- Added reusable bootstrap rule templates for AGENTS/Memory/provider-specific assistant docs.
- Documented current direct OpenAI GPT-5 compatibility constraints.

## 2026-03-05
- Hardened direct OpenAI GPT-5 request compatibility in the harness provider layer.
- Added recent search/profit/campaign tooling and documentation updates.
