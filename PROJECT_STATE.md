# Project State

This is the fast entrypoint for the current operational state of this repository.

For full context, use the `project-state/` package.

## Current State

- Project: `AetherOps_PolyMorph_Internal`
- Mode: internal-only harness
- Primary app path: `mini-agent/`
- Primary provider mode: unified OpenAI-compatible gateway with explicit fallback support
- Primary model target: `omnicoder`
- Direct OpenAI base URL: `https://api.openai.com/v1` (available, not current primary path)
- Unified gateway base URL: `https://api.aetherpro.tech/v1`
- Local fallback model target: `qwen3.5-9b`
- Explicit fallback: enabled with a distinct same-gateway fallback target
- Voice lane model target: `qwen3.5-122`
- Voice lane fallback target: `omnicoder`
- Voice lane provider mode: `openai_compat` through the unified gateway
- Voice lane UI: separate `PolyMorph Voice Mode` pane in the frontend
- Internal operator mode: fleet-aware control plane enabled
- Channel control plane: internal Telegram-first slice enabled
- Telegram bridge: webhook + webhook-sync live slice enabled
- Operational autonomy priority: message adapter layer first, Syndicate second, action ledger / approval-safe execution third
- Voice services:
  - ASR: `https://asr.aetherpro.us`
  - TTS: `https://tts.aetherpro.us`
- Voice stack status: persistent live browser voice loop working and manually verified on `2026-03-17`
- Provider env stack: canonical ordered loading enabled

## Current Engineering Notes

- Direct OpenAI GPT-5 models require OpenAI-specific request handling.
- OpenAI-compatible routers and direct OpenAI must remain separate adapters.
- Mongo memory writes use the shared database `aether_memory`.
- Namespace separation belongs in documents and keys, not implicit database renaming.
- `write_file` now uses canonical upload paths, atomic writes, and post-write verification.
- Every run now injects a structured temporal context block with exact time/date and elapsed-session markers.
- Main mic flow opens a live ASR websocket session, shows partial transcript updates, and inserts the final transcript into the composer before send.
- Voice mode now runs as a persistent live voice session:
  - ASR stream starts from the browser
  - finalized or idle-committed speech turns auto-dispatch into `/api/voice/turn`
  - the backend runs the full harness loop with a voice-specific model override
  - assistant speech plays through Kokoro realtime TTS
  - the session resumes listening until the user toggles voice mode off
- The current live voice lane has been manually verified with `qwen3.5-122` as the active voice model and `omnicoder` as fallback.
- Voice mode currently uses the full `run_agent(...)` harness prompt stack. A dedicated lightweight voice persona helper exists in code, but it is not yet wired into the active voice path.
- Current default voice is `af_heart`.
- Browser-side voice debugging logs now exist under:
  - `[LiveASR]`
  - `[VoiceSession]`
  - `[VoiceMode]`
- Backend-side voice debugging logs now exist under:
  - `[AudioStream]`
  - `[VoiceTurn]`
- In optional-auth ASR mode, startup may probe invalid auth headers first and then succeed with no auth. That `401 -> 401 -> 200` sequence is expected for the current gateway contract.
- Internal fleet/operator actions now load canonical topology from `fleet-inventory/`, preserve cross-file path mismatches, and execute approved helper scripts over SSH/Tailscale.
- Fleet execution must respect `operator-manifest.yaml` approved paths and require explicit confirmation for destructive stack actions.
- Multi-channel work is being absorbed from `mcas/` as a Polymorph-native control plane; `mcas/` itself is reference material, not active runtime.
- The existing connections panel now serves as the configuration surface for channel runtime and Telegram adapter settings.
- Telegram now has a first internal bridge path: normalize inbound updates, map them into Polymorph session IDs, run the existing agent loop, and send replies back through the Telegram Bot API.
- The message adapter layer is the first operational-autonomy priority and should be treated as the reference ingress contract before more channel sprawl is added.
- Syndicate is the first platform-specific autonomy target after the adapter layer; future autonomy work should bias toward a Polymorph-native Syndicate adapter/tool surface instead of generic benchmark polish.
- Model/provider env rationalization and internal profile switching are deferred follow-on work and should not be mixed into the first channel pass.
- Provider envs now load in canonical order (`.env` -> `backend/.env` -> `.env.polymorph`) instead of depending on current working directory.
- OpenAI-compatible internal traffic now targets one unified gateway: `https://api.aetherpro.tech/v1`.
- Multiple client-facing LiteLLM gateway assumptions are being removed; remote nodes are worker backends behind the unified gateway.
- Explicit fallback now suppresses implicit LiteLLM fallback injection unless `AGENT_ENABLE_IMPLICIT_LITELLM_FALLBACKS=true` is set.
- The current provider chain should be interpreted as: one primary target plus one explicit fallback target by default.
- OpenAI-compatible context-window failures now retry on the same provider with a reduced output budget when the upstream error exposes the token counts.
- OpenAI-compatible requests now also preflight-clamp output budgets against the effective context window and compact message history per iteration instead of using a flat large-history cap.
- Context-window failures must not silently fall across providers; they are request-budget errors first, not model-selection errors.
- Context-window failures must not silently degrade into no-tool fallback responses.
- Per-turn dynamic tool selection is now enabled to stop sending the full 40-tool schema on every request.
- Harness self-description metadata is now opt-in for the prompt path instead of being injected on every turn.
- Tool bootstrap now uses `mini-agent/backend/TOOLS.md` plus `read_tool_schema` lazy loading instead of exposing the full execution registry schema by default.
- Loaded dynamic tool schemas are cached in session state so the next iteration can expose them without rebroadcasting the full registry.
- Firecrawl tools are now available as first-class dynamic tools (`firecrawl_scrape`, `firecrawl_interact`), and `scrape_page` now prefers Firecrawl automatically when `FIRECRAWL_API_KEY` is configured.
- OpenAI-compatible output normalization now strips visible `<think>` leakage, suppresses user-visible tool-planning scaffolds, and recovers pseudo tool-call JSON into real tool calls when possible.
- OpenAI-compatible model compatibility mode now supports a model-selectable `xml_mcp_reasoning` parser path for MiroThinker-style outputs (`<think>` + `<use_mcp_tool>` blocks) with gated tool routing through the approved tool registry.
- Qwen3/Qwen3.5 direct-answer flows now default to `enable_thinking=false` unless a request explicitly opts into reasoning mode.
- Voice Mode now prefers realtime Kokoro TTS streaming via the gateway contract and keeps model-to-model stream orchestration deferred to a later phase.
- ASR gateway auth must omit fake/stale bearer tokens; optional-auth mode should allow no-auth startup unless a valid API key or JWT is explicitly configured.
- Legacy direct multimodal Phi-4 audio wiring is no longer the active voice path.
- Voice model selection is now independently configurable from the main chat model through:
  - `VOICE_AGENT_MODEL`
  - `VOICE_AGENT_FALLBACK_MODEL`
- Main chat and voice lane can now run different models against the same unified gateway without code changes.
- Next likely voice work is:
  - lightweight dedicated voice persona/system prompt
  - polish on turn pacing and interruption behavior
  - Redis-stream-backed model-to-model orchestration as a later phase
- Provider state should always distinguish:
  - requested provider/model
  - actual provider/model
  - fallback usage
  - runtime override presence

## Read Order

1. [project-state/ai/manifest.yaml](/home/cory/Documents/OPERATIONS/POLYMORPH/project-state/ai/manifest.yaml)
2. [project-state/ai/current-state.yaml](/home/cory/Documents/OPERATIONS/POLYMORPH/project-state/ai/current-state.yaml)
3. [project-state/ai/runtime-contracts.yaml](/home/cory/Documents/OPERATIONS/POLYMORPH/project-state/ai/runtime-contracts.yaml)
4. [project-state/ai/repo-map.yaml](/home/cory/Documents/OPERATIONS/POLYMORPH/project-state/ai/repo-map.yaml)

## Human Context

- [Architecture Overview](/home/cory/Documents/OPERATIONS/POLYMORPH/project-state/human/Architecture-Overview.md)
- [Runtime Contracts](/home/cory/Documents/OPERATIONS/POLYMORPH/project-state/human/Runtime-Contracts.md)
- [Changelog](/home/cory/Documents/OPERATIONS/POLYMORPH/project-state/human/Changelog.md)
- [Autonomous Control-Plane Roadmap](/home/cory/Documents/OPERATIONS/POLYMORPH/mini-agent/docs/Autonomous-Control-Plane-Roadmap.md)

## Repo-Specific Rules

- Root rules shim: [AGENTS.md](/home/cory/Documents/OPERATIONS/POLYMORPH/AGENTS.md)
- Harness implementation rules: [mini-agent/backend/AGENTS.md](/home/cory/Documents/OPERATIONS/POLYMORPH/mini-agent/backend/AGENTS.md)

## Topology / External Context

- [AETHERPRO_INFRA_TOPOLOGY.md](/home/cory/Documents/OPERATIONS/POLYMORPH/AETHERPRO_INFRA_TOPOLOGY.md)
- [Tailscale-&-Node-Access-Convo-Poly.md](/home/cory/Documents/OPERATIONS/POLYMORPH/Tailscale-&-Node-Access-Convo-Poly.md)
- [fleet-inventory/](/home/cory/Documents/OPERATIONS/POLYMORPH/fleet-inventory)

## Update Rule

When the operational truth changes:

1. Update `project-state/ai/current-state.yaml`
2. Update this file with the short current summary
3. Update human docs only if architecture, contracts, or migration history changed
