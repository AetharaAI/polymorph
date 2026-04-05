# Voice Realtime Implementation Context

Date: 2026-03-17
Status: implementation complete enough to freeze; further work is polish and next-phase architecture.

## What This Document Is For

This file is the detailed handoff context for any fresh model or new session entering the PolyMorph voice work after context compaction.

Use this document when the question is:

- what was built
- what is actually working now
- what is still not ideal
- what should happen next

## Final Result Of This Phase

PolyMorph now has a working persistent browser voice loop:

1. user taps the voice button
2. browser starts live ASR
3. transcript is captured continuously
4. a speech turn is committed via explicit final transcript or idle-commit fallback
5. the backend runs `/api/voice/turn`
6. the selected voice LLM runs through the full harness loop
7. Kokoro realtime TTS streams the assistant reply
8. playback completes
9. browser resumes listening until voice mode is toggled off

The mic button remains the old manual-finalize transcription path on purpose.

## Current Live Configuration

Verified live on 2026-03-17:

- main chat model: `omnicoder`
- main chat fallback: `qwen3.5-9b`
- voice model: `qwen3.5-122`
- voice fallback: `omnicoder`
- gateway base: `https://api.aetherpro.tech/v1`
- realtime TTS model: `kokoro_realtime`
- default voice: `af_heart`

The important design point is that the main chat model and the voice model are now independently configurable without code changes.

## Files That Matter Most

Core runtime:

- `mini-agent/backend/api/voice.py`
- `mini-agent/backend/api/audio.py`
- `mini-agent/backend/agent/runner.py`

Frontend voice loop:

- `mini-agent/frontend/src/hooks/useLiveAsrStream.ts`
- `mini-agent/frontend/src/hooks/useVoiceChat.ts`
- `mini-agent/frontend/src/components/InputBar.tsx`
- `mini-agent/frontend/src/components/VoicePanel.tsx`
- `mini-agent/frontend/src/components/ChatWindow.tsx`
- `mini-agent/frontend/src/app/page.tsx`

Phase records:

- `build-docs/PHASE_17_REPORT.md`
- `build-docs/PHASE_18_REPORT.md`

## Important Current Truths

### 1. Voice mode is working

The current issue is no longer “make voice work.”

The current issue space is:

- model quality
- voice-specific shaping/persona
- pacing/polish
- future streaming architecture between models

### 2. Voice mode is not raw text to model

The active voice route uses `run_agent(...)`.

That means the voice model currently gets the normal harness prompt stack, not just the raw user utterance.

It inherits:

- temporal context
- main system prompt
- AGENTS rules
- memory/identity context
- project governance
- tool prompt blocks
- harness metadata

### 3. Dedicated voice prompt exists but is not wired

There is a helper in `mini-agent/backend/api/voice.py`:

- `_voice_agent_system_prompt()`

But it is not currently injected into the actual `run_agent(...)` path.

So right now:

- `VOICE_AGENT_SYSTEM_PROMPT` is not the active shaping mechanism
- voice uses the normal harness prompt stack

This is a likely next improvement.

### 4. Smaller model proved the loop, bigger model improved quality

The smaller model was enough to validate:

- ASR
- turn commit
- backend voice route
- Kokoro TTS
- resume loop

But conversation quality was better when the voice loop used `qwen3.5-122`.

## Logging That Exists Now

Browser console:

- `[LiveASR]`
- `[VoiceSession]`
- `[VoiceMode]`

Backend logs:

- `[AudioStream]`
- `[VoiceTurn]`

These logs were added specifically because the working loop was previously hard to diagnose when ASR appeared active but no turn ever reached the LLM or Kokoro.

## ASR Edge Case That Was Fixed

One of the real problems was:

- ASR transcript text was clearly appearing in the UI
- but the persistent voice loop was waiting on `final_transcript`
- so `/api/voice/turn` never fired in some real runs

Fix:

- voice mode now has an idle-commit fallback
- if ASR partial text is present and finalization is delayed, the loop commits the latest transcript after a short idle window

This is only to keep the live voice loop moving. It does not change the manual mic flow.

## Kokoro / Auth Reality

The Kokoro logs that were provided were useful and matched the intended TTS path.

Current ASR optional-auth behavior may show:

1. invalid bearer token
2. invalid API key
3. success with no auth

This is expected for the current gateway deployment and should not be treated as a break by itself.

## What A Fresh Model Should Not Re-Debug

Do not restart from these stale assumptions:

- voice still needs the green check
- voice is still on `qwen3.5-4b`
- default voice is still `Sky`
- voice is still using Chatterbox or `Emily.wav`
- the UI dropdown is stale
- Kokoro is not reachable

Those were earlier states and are no longer the current truth.

## Best Next Work

If continuing from this point, the best next sequence is:

1. implement a lightweight dedicated voice persona/system prompt path
2. decide whether the voice lane should keep full harness context or use a reduced prompt budget
3. continue polish on interruption and response pacing
4. only after that, move into Redis streams / model-to-model orchestration

## Fast Re-Entry Command Checks

If a fresh session needs to verify current live truth quickly:

- `curl http://localhost:38333/api/voice/config`
- inspect `mini-agent/.env.polymorph`
- inspect `build-docs/PHASE_17_REPORT.md`
- inspect `build-docs/PHASE_18_REPORT.md`
- tail backend logs for `[AudioStream]` and `[VoiceTurn]`
