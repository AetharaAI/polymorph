# PHASE 13 REPORT

## Scope

This phase upgraded PolyMorph Voice Mode from a blocking HTTP-TTS leg to a realtime TTS stream leg, while keeping the main chat/tool lane separate from the voice lane.

## What Was Changed

- Replaced the active build plan with the end-to-end voice plan in:
  - `BUILD_PLAN.md`
- Extended the voice backend in:
  - `mini-agent/backend/api/voice.py`
- Extended the frontend voice contract in:
  - `mini-agent/frontend/src/lib/api.ts`
  - `mini-agent/frontend/src/lib/types.ts`
- Replaced the frontend voice orchestration hook in:
  - `mini-agent/frontend/src/hooks/useVoiceChat.ts`
- Updated the voice UI state display in:
  - `mini-agent/frontend/src/components/VoicePanel.tsx`

## Architecture

The live voice lane is now:

`live ASR final transcript -> separate voice model text reply -> realtime TTS stream bootstrap -> websocket text_chunk/text_complete/end_stream -> browser chunk playback`

Key points:

- the main chat/tool model lane is unchanged
- the separate voice model lane is unchanged
- only the TTS leg was upgraded in this phase
- model-to-model streams are still deferred follow-on work

## Backend Contract Changes

`POST /api/voice/turn` now:

- sanitizes assistant text before speech output
- prefers realtime TTS stream bootstrap against the gateway-backed contract
- returns realtime stream metadata:
  - `tts_transport`
  - `tts_stream_session_id`
  - `tts_stream_ws_url`
  - `tts_stream_http_base_url`
  - `tts_stream_model_requested`
  - `tts_stream_model_used`
  - `tts_stream_runtime`
- falls back to the older HTTP synth path if realtime bootstrap fails

`GET /api/voice/config` now exposes:

- realtime TTS configuration status
- realtime model/base URL
- Kokoro preset voices for the voice UI

## Frontend Behavior Changes

The voice hook now:

- sends the voice turn as before
- if the backend returns realtime TTS bootstrap data:
  - opens the websocket
  - splits the assistant text into small chunks
  - sends `text_chunk` frames
  - seals with `text_complete`
  - flushes with `end_stream`
  - plays `audio_chunk` events immediately through `AudioContext`
  - stores the final artifact URL when `final_audio` arrives
- if the backend returns HTTP synth fallback:
  - uses the returned `audio_url` as before

## Verification

Passed:

- `python3 -m compileall mini-agent/backend/api/voice.py`
- `pnpm -C mini-agent/frontend exec tsc --noEmit`

## Notes

- The current realtime voice lane still works turn-by-turn, not as a full duplex always-open conversation socket.
- The next architecture step is not more TTS work; it is the deferred model-to-model stream/orchestration layer the user described.
