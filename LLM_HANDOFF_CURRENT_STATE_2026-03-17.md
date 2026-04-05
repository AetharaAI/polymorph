# LLM Handoff Current State

Date: 2026-03-17
Audience: a fresh Codex session or any other model dropped into this repo without prior context.

## Start Here

Read in this order:

1. `PROJECT_STATE.md`
2. `project-state/ai/current-state.yaml`
3. `project-state/ai/runtime-contracts.yaml`
4. `project-state/human/Runtime-Contracts.md`
5. `project-state/human/Changelog.md`
6. `VOICE_REALTIME_PROJECT_STATE_2026-03-17.md`
7. `VOICE_REALTIME_IMPLEMENTATION_CONTEXT_2026-03-17.md`
8. `build-docs/PHASE_17_REPORT.md`
9. `build-docs/PHASE_18_REPORT.md`

## Current Frozen Truth

- This is not a new project. It is deep into an existing internal harness.
- The unified gateway architecture is active.
- Canonical OpenAI-compatible base:
  - `https://api.aetherpro.tech/v1`
- Main chat model is currently:
  - `omnicoder`
- Main chat fallback is currently:
  - `qwen3.5-9b`
- Voice mode is currently:
  - primary `qwen3.5-122`
  - fallback `omnicoder`
- Voice TTS is currently:
  - `kokoro_realtime`
  - default voice `af_heart`

## Voice Milestone Status

The persistent live browser voice loop is working.

That means:

- voice button starts a live voice session
- speech turns auto-dispatch into the backend voice route
- backend runs the full harness loop
- Kokoro realtime TTS speaks back
- the browser resumes listening

The mic/manual-finalize path remains separate and unchanged.

## Important Gotchas

### Voice prompt reality

Voice mode currently uses the normal `run_agent(...)` harness prompt stack.

There is a dedicated voice prompt helper in `mini-agent/backend/api/voice.py`, but it is not wired yet.

So if voice quality feels odd, the likely causes are:

- model choice
- prompt weight
- missing lightweight voice persona

not “no prompt at all.”

### ASR auth logs

In the current optional-auth gateway contract, it is normal to see:

- invalid bearer token
- invalid API key
- then success with no auth

That sequence is expected and should not be mistaken for the actual break.

### Logging that exists now

Browser:

- `[LiveASR]`
- `[VoiceSession]`
- `[VoiceMode]`

Backend:

- `[AudioStream]`
- `[VoiceTurn]`

Use those first before guessing.

## Best Next Work

The current best next tasks are:

1. add a lightweight dedicated voice system prompt/persona
2. keep polishing pacing/interruption behavior
3. then move into Redis streams / model-to-model orchestration

Do not restart by trying to rebuild the already-working voice loop from scratch.
