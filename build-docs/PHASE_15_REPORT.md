# PHASE 15 REPORT

## Scope
PolyMorph voice-lane upgrade from one-shot voice chat to full harness agent-loop execution.

## Done
- Switched the voice lane default model from `minicpm-v` to `omnicoder`.
- Added a voice-specific provider override path into `run_agent(...)` so the second-button route can use the full harness loop without changing the main chat provider.
- Replaced `/api/voice/turn` direct `provider.generate(... tools=[])` execution with a call into the real agent loop.
- Captured tool-call and tool-result events during voice turns and returned them in the voice response payload.
- Updated the voice UI to render those tool events in the voice pane.
- Updated voice config messaging so it accurately reports that the second-button lane now uses the full agent loop.
- Added brand pronunciation guidance for `Aether` / `AetherPro` to the voice prompt.
- Fixed fleet-inventory loader behavior so missing external inventory files do not crash unrelated tool imports inside the backend container.

## Verified
- `python3 -m py_compile` passed for:
  - `backend/api/voice.py`
  - `backend/agent/runner.py`
  - `backend/fleet/inventory.py`
- `npm run build` passed in `mini-agent/frontend`.
- Rebuilt and restarted the live backend/frontend containers.
- Live `GET /api/voice/config` now reports:
  - `model=omnicoder`
  - `transport=live_asr_final_to_voice_agent_loop_plus_tts`
  - live gateway model catalog populated from `https://api.aetherpro.tech/v1/models`
- Live `POST /api/voice/turn` with a tool-using prompt now returns successfully.

## Live Smoke Result
- Request:
  - `Use the calculator tool to add 12 and 30, then answer with the result.`
- Live response:
  - `assistant_text="42"`
  - `provider="voice_agent"`
  - `model="omnicoder"`
  - `llm_fallback_used=false`
  - `tool_events` present in payload
- The earlier 502 was traced to fleet inventory import-time failure, not the voice loop itself.

## Remaining Runtime Issue
- Realtime TTS bootstrap is still failing upstream and falling back to HTTP synth:
  - `Realtime TTS bootstrap failed: 401 {"detail":"Invalid bearer token"}`
- Because of that, live voice turns currently return valid audio through `http_synth_fallback` rather than realtime streaming.

## Next
- Set a valid bearer token for the realtime voice gateway if you want live streamed TTS instead of HTTP synth fallback.
- If you want the voice lane on another Qwen-family model later, set `VOICE_AGENT_MODEL` to that model and keep `enable_thinking=false` behavior via the existing provider logic.
- If you want live tool-call streaming in the voice pane, add a dedicated voice SSE route instead of the current turn-based collection model.
