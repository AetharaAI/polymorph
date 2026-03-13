# Project State

This is the fast entrypoint for the current operational state of this repository.

For full context, use the `project-state/` package.

## Current State

- Project: `AetherOps_PolyMorph_Internal`
- Mode: internal-only harness
- Primary app path: `mini-agent/`
- Primary provider mode: direct OpenAI with explicit router failover
- Primary model target: `gpt-5.4`
- Direct OpenAI base URL: `https://api.openai.com/v1`
- Local router fallback base URL: `https://api.aetherpro.tech/v1`
- Local fallback model target: `qwen3.5-35b`
- Explicit fallback: enabled
- Voice lane model target: `qwen3.5-4b`
- Voice lane provider mode: `openai_compat` via LiteLLM/router-first resolution
- Voice lane UI: separate `PolyMorph Voice Mode` pane in the frontend
- Internal operator mode: fleet-aware control plane enabled
- Voice services:
  - ASR: `https://asr.aetherpro.us`
  - TTS: `https://tts.aetherpro.us`
- Voice stack status: live-tested in active operator use on `2026-03-13`

## Current Engineering Notes

- Direct OpenAI GPT-5 models require OpenAI-specific request handling.
- OpenAI-compatible routers and direct OpenAI must remain separate adapters.
- Mongo memory writes use the shared database `aether_memory`.
- Namespace separation belongs in documents and keys, not implicit database renaming.
- `write_file` now uses canonical upload paths, atomic writes, and post-write verification.
- Every run now injects a structured temporal context block with exact time/date and elapsed-session markers.
- Main mic flow opens a live ASR websocket session, shows partial transcript updates, and inserts the final transcript into the composer before send.
- Voice mode now uses the same live ASR final transcript, sends it to `qwen3.5-4b`, and synthesizes assistant playback through the TTS service.
- The current realtime voice stack has been verified in live operator use and is the active path.
- Internal fleet/operator actions now load canonical topology from `fleet-inventory/`, preserve cross-file path mismatches, and execute approved helper scripts over SSH/Tailscale.
- Fleet execution must respect `operator-manifest.yaml` approved paths and require explicit confirmation for destructive stack actions.
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
