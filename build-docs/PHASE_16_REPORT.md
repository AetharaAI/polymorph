# PHASE 16 REPORT

## Scope
Finish the remaining PolyMorph voice-lane cleanup after the full agent-loop migration:
- remove fallback-model contamination from voice primary-model resolution
- make the intended Omnicoder-to-Qwen9 voice path explicit
- ensure voice tool events return finalized tool inputs instead of placeholder `{}` payloads

## Done
- Updated `backend/api/voice.py` so the voice primary model no longer implicitly inherits `AGENT_FALLBACK_MODEL` before `AGENT_MODEL` / `OPENAI_COMPAT_MODEL`.
- Kept explicit voice-lane fallback support and aligned the fallback search order with unified-gateway OpenAI-compatible routing.
- Added voice-event upsert logic so duplicate placeholder tool-call entries are replaced by the finalized tool-call payload for the same `tool_id`.
- Updated `backend/agent/runner.py` to emit a finalized `tool_call` event immediately before real dispatch, ensuring downstream consumers can capture the resolved tool arguments.
- Set the live voice env path to the intended pair:
  - primary `omnicoder`
  - fallback `qwen3.5-9b`
- Updated env examples to reflect the same voice pairing.

## Verified
- `python3 -m py_compile` passed for:
  - `backend/api/voice.py`
  - `backend/agent/runner.py`
  - `backend/fleet/inventory.py`
- Rebuilt and restarted the backend container successfully.
- Live `GET /api/voice/config` now reports:
  - `model=omnicoder`
  - `fallback_model=qwen3.5-9b`
  - `model_source=VOICE_AGENT_MODEL`
  - `provider=openai_compat`
- Live `POST /api/voice/turn` with a tool-using prompt returned:
  - `assistant_text="12 + 30 = 42"`
  - `model="omnicoder"`
  - `requested_model="omnicoder"`
  - `llm_fallback_used=false`
  - `tool_events` containing one finalized `tool_call` with `input.code="12 + 30"` plus the matching `tool_result`

## Remaining Runtime Issue
- Realtime TTS bootstrap still falls back to HTTP synthesis because the upstream bearer token is invalid:
  - `Realtime TTS bootstrap failed: 401 {"detail":"Invalid bearer token"}`

## Next
- Rebuild the frontend only if you want to pick up any unbuilt UI changes from earlier voice-pane work; this pass itself required only a backend rebuild.
- If you want the voice lane to prefer `qwen3.5-9b` directly instead of `omnicoder`, set `VOICE_AGENT_MODEL=qwen3.5-9b` and keep `enable_thinking=false`.
- If you want true live streaming of intermediate tool cards in the voice pane, the next step is a dedicated SSE/websocket voice event channel rather than turn-end collection.
