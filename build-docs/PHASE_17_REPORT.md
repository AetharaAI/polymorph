# PHASE 17 REPORT

## Scope
Upgrade PolyMorph voice mode from manual-confirm turn capture to a persistent live voice-session controller, and align the TTS path with Kokoro realtime instead of the legacy fallback voice path.

## Done
- Added two recovery/reference documents in the repo root before implementation:
  - `VOICE_REALTIME_IMPLEMENTATION_CONTEXT_2026-03-17.md`
  - `VOICE_REALTIME_PROJECT_STATE_2026-03-17.md`
- Fixed realtime TTS bootstrap auth in `backend/api/voice.py` by trying compatible TTS auth header variants, including raw `Authorization` without `Bearer`.
- Switched the default realtime Kokoro voice to `af_heart`.
- Added explicit realtime TTS API key env support in the live env files and examples.
- Disabled legacy HTTP synth fallback for the normal voice-button path by default via `VOICE_ALLOW_LEGACY_TTS_FALLBACK=false`.
- Removed explicit Chatterbox/Emily defaults from the voice stack:
  - voice fallback default no longer points at `chatterbox`
  - fallback default voice no longer uses `Emily.wav`
  - `.env` now sets `TTS_MODEL=kokoro_realtime`
- Updated the frontend ASR hook to support live final-transcript callbacks and cancellation.
- Converted the voice button in `InputBar.tsx` into a persistent session toggle:
  - mic path remains manual-confirm
  - voice path no longer requires the green check
  - finalized speech turns auto-send into the voice agent loop
  - after the assistant finishes, the voice session automatically resumes listening until toggled off
- Tightened layout sizing so the lower transcript/status region remains visible:
  - `page.tsx` main column now uses `min-h-0`
  - `ChatWindow.tsx` uses `min-h-0`
  - `VoicePanel.tsx` is marked `shrink-0`
  - transcript box in `InputBar.tsx` now has bounded height and its own scroll

## Verified
- `python3 -m py_compile` passed for:
  - `mini-agent/backend/api/voice.py`
  - `mini-agent/backend/api/health.py`
  - `mini-agent/backend/fleet/inventory.py`
  - `mini-agent/backend/agent/runner.py`
- `npm run build` passed in `mini-agent/frontend`.
- Rebuilt and restarted both backend and frontend containers successfully.
- Live `GET /api/voice/config` now reports:
  - `default_voice_id=af_heart`
  - `realtime_tts_model=kokoro_realtime`
  - `realtime_tts_base_url=https://asr.aetherpro.us`
  - `model=omnicoder`
  - `fallback_model=qwen3.5-9b`
- Live `POST /api/voice/turn` now returns realtime Kokoro stream metadata instead of HTTP synth fallback:
  - `assistant_text="READY"`
  - `voice_id="af_heart"`
  - `tts_transport="realtime_stream"`
  - `tts_stream_model_used="kokoro_realtime"`
  - `tts_stream_ws_url` present
- Backend logs confirm:
  - `tts_realtime_start`
  - `requested_model="kokoro_realtime"`
  - `used_model="kokoro_realtime"`
  - `fallback_used=false`
- Playwright browser verification after the final frontend rebuild confirms:
  - the voice dropdown now defaults to `Heart`
  - the voice panel copy reflects persistent live voice mode
  - the voice button is labeled as a live voice-mode toggle instead of a manual finalize action

## Not Fully Automated
- I did not run an end-to-end browser microphone automation test for the new persistent voice-session controller.
- The persistent frontend voice-mode logic compiles and is wired, but the final behavioral check still needs manual browser testing with a real mic:
  - tap voice once to start
  - speak without pressing the green check
  - confirm PolyMorph responds
  - confirm it resumes listening automatically
  - tap voice again to stop

## Remaining Deferred Work
- True model-to-model streaming between two LLMs remains out of scope for this pass.
- This pass keeps the live voice loop browser-side as:
  - repeated ASR capture sessions
  - one voice turn per finalized utterance
  - assistant playback
  - automatic resume

## Recommended Manual Test
1. Open PolyMorph.
2. Verify the voice dropdown defaults to `Heart`.
3. Tap the voice button once.
4. Speak naturally without pressing the green check.
5. Wait for the assistant reply and audio playback.
6. Confirm the app returns to listening automatically.
7. Tap the voice button again to stop.
