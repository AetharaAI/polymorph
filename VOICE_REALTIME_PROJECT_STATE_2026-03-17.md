# Voice Realtime Project State

Date: 2026-03-17
Purpose: frozen current-state snapshot for PolyMorph voice mode after the persistent live voice loop was made to work.

## Current Live Voice Configuration

- unified gateway base: `https://api.aetherpro.tech/v1`
- voice provider: `openai_compat`
- current voice model: `qwen3.5-122`
- current voice fallback model: `omnicoder`
- main chat model remains: `omnicoder`
- realtime TTS model: `kokoro_realtime`
- default voice: `af_heart`

Verified live from `GET /api/voice/config` on 2026-03-17:

- `model=qwen3.5-122`
- `fallback_model=omnicoder`
- `provider=openai_compat`
- `default_voice_id=af_heart`
- `realtime_tts_model=kokoro_realtime`

## What Is Working

- The mic button still behaves as the original manual-finalize ASR path.
- The voice button now runs as a persistent live voice session.
- Browser ASR starts successfully through `/api/audio/stream/start`.
- Voice turns dispatch into `/api/voice/turn`.
- The backend runs the full harness loop for the voice lane.
- Tool calls remain enabled in voice mode.
- Kokoro realtime TTS is the intended speech path for the voice button.
- The session resumes listening after the assistant finishes speaking.

## Important Behavioral Notes

- Voice mode is no longer waiting only on explicit ASR `final_transcript` events.
- There is now an idle-commit fallback for voice mode so the loop can continue when ASR partials are visible but finalization is delayed.
- Current ASR optional-auth behavior may show:
  - invalid bearer attempt
  - invalid API-key attempt
  - successful no-auth attempt
  This is expected for the present gateway contract.

## Prompt / Persona Reality

- Voice mode is not raw user text straight to the model.
- The active voice lane currently uses the normal `run_agent(...)` harness prompt stack.
- That means voice currently inherits:
  - temporal context
  - system prompt
  - AGENTS rules
  - memory/identity context
  - skills/tool prompt blocks
  - harness metadata blocks used by the main loop
- There is a helper for a dedicated voice prompt in `mini-agent/backend/api/voice.py`, but it is not wired into the active route yet.

## Quality Observation From Live Testing

- The smaller voice-loop model worked enough to prove the loop and audio path.
- Conversation quality was better after switching the live voice model to `qwen3.5-122`.
- Current recommendation for this internal setup:
  - keep main chat on `omnicoder`
  - keep voice on `qwen3.5-122`
  - keep `omnicoder` as voice fallback

## Current Debugging Surface

Browser console:

- `[LiveASR]`
- `[VoiceSession]`
- `[VoiceMode]`

Backend logs:

- `[AudioStream]`
- `[VoiceTurn]`

These are the first places a fresh session should inspect if voice breaks again.

## Files A Fresh Model Should Read First

1. `PROJECT_STATE.md`
2. `project-state/ai/current-state.yaml`
3. `project-state/ai/runtime-contracts.yaml`
4. `project-state/human/Runtime-Contracts.md`
5. `build-docs/PHASE_17_REPORT.md`
6. `build-docs/PHASE_18_REPORT.md`
7. `VOICE_REALTIME_IMPLEMENTATION_CONTEXT_2026-03-17.md`

## Next Likely Work

- wire a lightweight dedicated voice system prompt/persona into the active voice route
- polish pacing/interruption behavior
- reduce unnecessary prompt weight for voice specifically
- later phase: Redis streams / model-to-model stream orchestration
