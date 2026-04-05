# PHASE 18 REPORT

## Scope
Diagnose the live voice-mode disconnect where browser ASR stayed active and filled the transcript box, but `/api/voice/turn` and Kokoro TTS were not being hit during actual UI use.

## Root Cause
- The frontend persistent voice controller only advanced on websocket `final_transcript` events.
- In real browser use, the ASR stream was clearly producing transcript text, but the voice loop was not receiving the event it needed to dispatch the turn.
- Result:
  - the transcript box kept filling
  - the voice session stayed recording
  - backend `VoiceTurn` logs never appeared
  - Kokoro logs stayed idle except for unrelated prior smoke tests

## Done
- Added an idle-commit fallback in [`useLiveAsrStream.ts`](../mini-agent/frontend/src/hooks/useLiveAsrStream.ts):
  - voice mode now auto-commits the latest non-empty transcript after `1500ms` of ASR inactivity
  - this path is only used for the live voice session controller
  - explicit `final_transcript` events still take precedence when they arrive
- Added browser console logging in:
  - [`useLiveAsrStream.ts`](../mini-agent/frontend/src/hooks/useLiveAsrStream.ts) with `[LiveASR]`
  - [`InputBar.tsx`](../mini-agent/frontend/src/components/InputBar.tsx) with `[VoiceSession]`
  - [`useVoiceChat.ts`](../mini-agent/frontend/src/hooks/useVoiceChat.ts) with `[VoiceMode]`
- Added backend stdout logging in [`audio.py`](../mini-agent/backend/api/audio.py) with `[AudioStream]` for:
  - ASR live start requested
  - upstream auth/path success
  - upstream failure
  - returned session id / websocket URL

## Expected Observable Logs Now
- Backend `docker compose logs -f`:
  - `[AudioStream] start_requested ...`
  - `[AudioStream] start_success ...`
  - `[VoiceTurn] request_start ...`
  - `[VoiceTurn] llm_success ...`
  - `[VoiceTurn] tts_realtime_start ...`
- Browser devtools console:
  - `[VoiceSession] session_started`
  - `[LiveASR] partial_transcript`
  - `[LiveASR] idle_commit` or `[LiveASR] final_transcript`
  - `[VoiceSession] turn_dispatch_start`
  - `[VoiceMode] send_turn_start`
  - `[VoiceMode] send_turn_response`
  - `[VoiceMode] tts_stream_open`
  - `[VoiceSession] resume_listening`

## Verification
- `python3 -m py_compile mini-agent/backend/api/audio.py mini-agent/backend/api/voice.py` passed.
- `npm run build` passed.
- Backend/frontend containers rebuilt and restarted successfully.

## Still Not Fully Automated
- I did not automate a real browser microphone session.
- The auto-commit fix is targeted at the failure mode shown in the user screenshots, but the final confirmation still requires a manual voice-button test in the browser with the new logs visible.
