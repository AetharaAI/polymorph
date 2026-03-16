# Project State

This is the fast entrypoint for the current operational state of this repository.

For full context, use the `project-state/` package.

## Current State

- Project: `AetherOps_PolyMorph_Internal`
- Mode: internal-only harness
- Primary app path: `mini-agent/`
- Primary provider mode: unified OpenAI-compatible gateway with explicit fallback support
- Primary model target: `minicpm-v`
- Direct OpenAI base URL: `https://api.openai.com/v1` (available, not current primary path)
- Unified gateway base URL: `https://api.aetherpro.tech/v1`
- Local fallback model target: currently non-distinct in live env stack
- Explicit fallback: enabled, but current env resolves no distinct fallback target
- Voice lane model target: `qwen3.5-4b`
- Voice lane provider mode: `openai_compat` via LiteLLM/router-first resolution
- Voice lane UI: separate `PolyMorph Voice Mode` pane in the frontend
- Internal operator mode: fleet-aware control plane enabled
- Channel control plane: internal scaffold enabled
- Telegram bridge: webhook + webhook-sync scaffolding enabled
- Voice services:
  - ASR: `https://asr.aetherpro.us`
  - TTS: `https://tts.aetherpro.us`
- Voice stack status: live-tested in active operator use on `2026-03-13`
- Provider env stack: canonical ordered loading enabled

## Current Engineering Notes

- Direct OpenAI GPT-5 models require OpenAI-specific request handling.
- OpenAI-compatible routers and direct OpenAI must remain separate adapters.
- Mongo memory writes use the shared database `aether_memory`.
- Namespace separation belongs in documents and keys, not implicit database renaming.
- `write_file` now uses canonical upload paths, atomic writes, and post-write verification.
- Every run now injects a structured temporal context block with exact time/date and elapsed-session markers.
- Main mic flow opens a live ASR websocket session, shows partial transcript updates, and inserts the final transcript into the composer before send.
- Voice mode now uses the same live ASR final transcript, sends it to `qwen3.5-4b`, and prefers gateway-backed realtime TTS streaming with browser chunk playback and HTTP synth fallback.
- The current realtime voice stack has been verified in live operator use and is the active path.
- Internal fleet/operator actions now load canonical topology from `fleet-inventory/`, preserve cross-file path mismatches, and execute approved helper scripts over SSH/Tailscale.
- Fleet execution must respect `operator-manifest.yaml` approved paths and require explicit confirmation for destructive stack actions.
- Multi-channel work is being absorbed from `mcas/` as a Polymorph-native control plane; `mcas/` itself is reference material, not active runtime.
- The existing connections panel now serves as the configuration surface for channel runtime and Telegram adapter settings.
- Telegram now has a first internal bridge path: normalize inbound updates, map them into Polymorph session IDs, run the existing agent loop, and send replies back through the Telegram Bot API.
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
- The live env stack currently resolves `minicpm-v` as primary and no distinct fallback because the explicit fallback target dedupes to the same router/model as primary.
- Per-turn dynamic tool selection is now enabled to stop sending the full 40-tool schema on every request.
- Harness self-description metadata is now opt-in for the prompt path instead of being injected on every turn.
- Tool bootstrap now uses `mini-agent/backend/TOOLS.md` plus `read_tool_schema` lazy loading instead of exposing the full execution registry schema by default.
- Loaded dynamic tool schemas are cached in session state so the next iteration can expose them without rebroadcasting the full registry.
- OpenAI-compatible output normalization now strips visible `<think>` leakage, suppresses user-visible tool-planning scaffolds, and recovers pseudo tool-call JSON into real tool calls when possible.
- Qwen3/Qwen3.5 direct-answer flows now default to `enable_thinking=false` unless a request explicitly opts into reasoning mode.
- Voice Mode now prefers realtime Kokoro TTS streaming via the gateway contract and keeps model-to-model stream orchestration deferred to a later phase.
- ASR gateway auth must omit fake/stale bearer tokens; optional-auth mode should allow no-auth startup unless a valid API key or JWT is explicitly configured.
- Legacy direct multimodal Phi-4 audio wiring is no longer the active voice path.
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
