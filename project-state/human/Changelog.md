# Changelog

## 2026-03-13
- Confirmed the current realtime ASR to PolyMorph Voice Mode to TTS stack is working in live operator use and recorded that verification in project-state.
- Added a root proprietary `LICENSE` and a repo-level `.gitignore` for initial private git versioning.
- Added the current Tailscale/node-access note to active project-state references and corrected stale absolute repo paths.
- Added the internal fleet-aware operator layer backed by `fleet-inventory/`, including inventory normalization, helper-script audit, SSH/Tailscale execution wrappers, and inventory-aware operator actions.

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
