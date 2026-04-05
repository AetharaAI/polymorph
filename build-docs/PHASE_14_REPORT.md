# PHASE 14 REPORT

## Scope
PolyMorph voice-lane stabilization and visibility pass.

## Done
- Traced the current voice path end to end:
  - live ASR websocket capture remains separate and unchanged
  - second button finalizes ASR transcript into `/api/voice/turn`
  - `/api/voice/turn` uses a dedicated voice-model lane and then TTS playback
- Updated the voice lane default model resolution in `mini-agent/backend/api/voice.py`:
  - default voice model is now `minicpm-v`
  - voice config falls back through `AGENT_FALLBACK_MODEL`, then provider defaults
  - voice base/key can inherit fallback-provider settings when voice-specific settings are absent
- Added transparent voice-lane failover:
  - primary voice model is `minicpm-v`
  - fallback voice model resolves to `omnicoder` when the primary voice model fails
  - fallback use is exposed in the response and logs
- Added live model-catalog discovery to `/api/voice/config`:
  - probes the configured gateway models endpoint
  - returns live `available_models`
  - reports `model_catalog_source` and whether the configured voice model appears in the live catalog
- Expanded voice response metadata:
  - requested model
  - used model
  - provider
  - base URL
  - fallback status
  - provider notice
  - TTS transport/model metadata
- Updated frontend voice UI to show:
  - current voice model and source
  - fallback model
  - live model count
  - provider fallback notice on assistant messages
- Added explicit env/example defaults for the voice lane:
  - `VOICE_AGENT_MODEL=minicpm-v`
  - realtime TTS defaults for the second-button voice path
- Added explicit backend voice-route logging for:
  - request start
  - LLM success
  - realtime TTS bootstrap failure
  - HTTP synth fallback

## Verified
- `python3 -m py_compile` passed for edited backend files.
- `npm run build` passed in `mini-agent/frontend`.
- Rebuilt and restarted the live backend/frontend containers.
- Live `GET /api/voice/config` now reports:
  - `model=minicpm-v`
  - `fallback_model=omnicoder`
  - `model_catalog_source=https://api.aetherpro.tech/v1/models`
  - live `available_models` including `minicpm-v` and `omnicoder`
- Live `POST /api/voice/turn` now returns a final response instead of crashing.

## Blocked / Runtime Issues
- Direct `minicpm-v` calls through the unified gateway are currently failing upstream with:
  - `401 Unauthorized`
- Realtime TTS bootstrap against the voice gateway is currently failing upstream with:
  - `401 Invalid bearer token`
- Because of those upstream credential issues, the live smoke turn behaved as:
  - requested voice model: `minicpm-v`
  - served voice model: `omnicoder` via voice-lane failover
  - TTS transport: `http_synth_fallback`

## Next
- Fix gateway authorization for `minicpm-v` so the voice lane can stay on its intended primary model.
- Set a valid realtime voice-gateway token for `/api/v1/tts/stream/start` so voice playback uses realtime streaming instead of HTTP synth fallback.
- If desired later, add explicit voice-lane config controls into the Connections panel instead of relying on env and `/api/voice/config`.

## Acceptance Status
- Code-path objective: met
- Voice-lane observability objective: met
- Live `minicpm-v` primary objective: blocked by upstream auth
- Live realtime TTS objective: blocked by upstream auth
