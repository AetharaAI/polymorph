# PHASE 1 REPORT

## Done
- Added backend voice endpoints in `mini-agent/backend/api/voice.py`.
- Refactored the main composer so:
  - `Mic` uploads WAV audio for batch ASR transcription into the text box.
  - `Voice` sends the transcript into a separate `PolyMorph Voice Mode` pane.
- Added a dedicated qwen3.5-4b voice chat hook and UI pane.
- Updated ASR probing to prefer `/v1/asr/transcribe`, `/v1/health`, and `/v1/models`.
- Updated project-state docs to reflect the new active voice path.

## Verification
- `python3 -m py_compile mini-agent/backend/api/audio.py mini-agent/backend/api/connections.py mini-agent/backend/api/health.py mini-agent/backend/api/voice.py mini-agent/backend/main.py`
- `npm run build` in `mini-agent/frontend`
- Live smoke:
  - qwen3.5-4b responded successfully through `https://api.aetherpro.tech/v1`
  - TTS returned playable WAV bytes through `https://tts.aetherpro.us/tts`

## Known Gap
- The realtime ASR/TTS websocket frame contract is still not published in OpenAPI.
- This phase ships the stable HTTP path now and keeps the realtime gateway bootstrap as the next integration target.
