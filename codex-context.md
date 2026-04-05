The current voice implementation confirms the root mismatch: it still calls a dedicated provider directly with tools=[], so it can never behave like the main harness. I’m reading the agent runner and page wiring now to see the smallest clean change that lets the second-button path use the real tool/multi-turn loop while still keeping a separate voice model and TTS output.

Explored 3 files
I’m going one layer deeper now. To make the second-button path actually support tools and multi-turns, it has to stop doing a one-shot provider.generate(... tools=[]) call and instead reuse the real run_agent loop with a voice-specific provider override. I’m patching for that path, then I’ll make the voice pane show the captured tool events.

Explored 4 files, 1 search
I’ve confirmed the runner already emits the metadata the voice lane needs, including fallback_used and tool-call events. The remaining patch is to swap /api/voice/turn off the one-shot model call and onto run_agent(...provider_override=voice_provider), then surface those tool events in the voice pane.

Explored 1 file
I’m editing the backend now. This patch changes the second-button route from a direct one-shot model call into a voice-specific run_agent execution, which is the only way it can inherit multi-turn behavior and tool use from the real harness.

Edited file
runner.py
+3
-2

from backend.agent.providers.factory import get_multimodal_audio_provider
from backend.agent.providers.base import LLMContentBlock
from backend.agent.providers.base import BaseLLMProvider, LLMContentBlock
from backend.agent.skills import build_skills_prompt
    audio_url: dict[str, Any] | None = None,
    provider_override: BaseLLMProvider | None = None,
) -> None:
        return
    provider = multimodal_provider or get_provider()
    provider = provider_override or multimodal_provider or get_provider()
    replay = SessionReplayLogger(session_id=session_id, enabled=ENABLE_REPLAY_LOGS)
Edited file
voice.py
+89
-34


from backend.agent.providers.base import LLMContentBlock
from backend.agent.providers.failover_provider import FailoverProvider
from backend.agent.providers.factory import _build_single_provider
from backend.agent.runner import run_agent
from backend.config import (
)
from backend.memory import get_memory_service

VOICE_OUTPUT_ROOT = (Path(__file__).resolve().parent.parent / "uploads").resolve()
DEFAULT_VOICE_AGENT_MODEL = "minicpm-v"
DEFAULT_VOICE_AGENT_MODEL = "omnicoder"
DEFAULT_VOICE_AGENT_PROVIDER = "openai_compat"

def _extract_text(blocks: list[LLMContentBlock]) -> str:
    return "".join(block.text or "" for block in blocks if block.type == "text").strip()
async def _latest_assistant_text(session_id: str) -> str:
    memory = await get_memory_service()
    messages = await memory.get_messages(session_id)
    for message in reversed(messages):
        if str(message.get("role") or "") != "assistant":
            continue
        content = message.get("content") or []
        if not isinstance(content, list):
            continue
        parts: list[str] = []
        for block in content:
            if not isinstance(block, dict):
                continue
            if str(block.get("type") or "") != "text":
                continue
            text = str(block.get("text") or "")
            if text:
                parts.append(text)
        combined = "".join(parts).strip()
        if combined:
            return combined
    return ""

    assistant_text: str
    tool_events: list[dict[str, object]] = Field(default_factory=list)
    provider: str
            "Mic opens a live ASR websocket session and writes the final transcript into the main composer.",
            "Voice mode uses the same live ASR final transcript, then routes the turn through the separate voice model pane.",
            "The voice lane is intentionally separate from the main tool-using agent loop; tools are disabled in this lane.",
            "Voice mode uses the same live ASR final transcript, then runs the full agent loop with a voice-specific model override.",
            "Tool calls and multi-turn execution stay enabled in the voice lane.",
            "Assistant speech now prefers realtime Kokoro TTS streaming for end-to-end voice playback.",
            "Model-to-model streams are deferred; this pass upgrades the TTS leg only.",
            "Model-to-model streams are still deferred; this route is turn-based voice over the full harness loop.",
        ],
    )
    messages: list[dict[str, object]] = []
    for item in request.history[-10:]:
        text = item.content.strip()
        if not text:
            continue
        messages.append(
            {
                "role": item.role,
                "content": [{"type": "text", "text": text}],
            }
        )
    messages.append({"role": "user", "content": [{"type": "text", "text": user_message}]})

    _log_voice_event(
            "reasoning_mode": request.reasoning_mode or "direct",
            "history_messages": len(messages) - 1,
            "history_messages": len(request.history[-10:]),
            "user_chars": len(user_message),

    response = await provider.generate(
        system=_voice_agent_system_prompt(),
        tools=[],
        messages=messages,
        max_tokens=int(resolve_env("VOICE_AGENT_MAX_TOKENS", default="512") or "512"),
        temperature=float(resolve_env("VOICE_AGENT_TEMPERATURE", default="0.6") or "0.6"),
        enable_thinking=request.reasoning_mode == "reasoning",
        on_stream_event=None,
    text_fragments: list[str] = []
    tool_events: list[dict[str, object]] = []
    terminal_error: str | None = None
    done_event: dict[str, object] = {}

    async def collect_voice_event(event: dict[str, object]) -> None:
        nonlocal terminal_error, done_event
        event_type = str(event.get("type") or "")
        if event_type == "text":
            text = str(event.get("text") or "")
            if text:
                text_fragments.append(text)
            return
        if event_type == "tool_call":
            tool_events.append(
                {
                    "type": "tool_call",
                    "tool_name": str(event.get("tool_name") or ""),
                    "tool_id": str(event.get("tool_id") or ""),
                    "input": event.get("input") if isinstance(event.get("input"), dict) else {},
                }
            )
            return
        if event_type == "tool_result":
            tool_events.append(
                {
                    "type": "tool_result",
                    "tool_id": str(event.get("tool_id") or ""),
                    "result": str(event.get("result") or ""),
                }
            )
            return
        if event_type == "error":
            terminal_error = str(event.get("message") or "Voice agent execution failed.")
            return
        if event_type == "done":
            done_event = dict(event)

    await run_agent(
        request.session_id,
        user_message,
        [],
        collect_voice_event,
        reasoning_mode=request.reasoning_mode,
        provider_override=provider,
    )
    assistant_text = _sanitize_voice_reply_text(_extract_text(response.content))

    if terminal_error:
        raise HTTPException(status_code=502, detail=terminal_error)

    assistant_text = _sanitize_voice_reply_text("".join(text_fragments))
    if not assistant_text:
        assistant_text = _sanitize_voice_reply_text(await _latest_assistant_text(request.session_id))
    if not assistant_text:
        raise HTTPException(status_code=502, detail="Voice agent returned an empty response.")
    llm_provider = response.provider_name or provider.provider_name
    llm_model_used = response.model_name or provider.model_name
    llm_notice = response.notice
    llm_fallback_used = bool(response.fallback_used)
    llm_provider = str(done_event.get("provider") or provider.provider_name)
    llm_model_used = str(done_event.get("model") or provider.model_name)
    llm_notice = str(done_event.get("provider_notice") or "").strip() or None
    llm_fallback_used = bool(done_event.get("fallback_used")) or llm_model_used != configured_model
    _log_voice_event(
            "assistant_chars": len(assistant_text),
            "tool_events": len(tool_events),
        },
            assistant_text=assistant_text,
            tool_events=tool_events,
            provider=llm_provider,
            assistant_text=assistant_text,
            tool_events=tool_events,
            provider=llm_provider,
Edited file
api.ts
+7
-0

  assistant_text: string;
  tool_events?: Array<{
    type: 'tool_call' | 'tool_result';
    tool_name?: string;
    tool_id?: string;
    input?: Record<string, unknown>;
    result?: string;
  }>;
  provider: string;
Edited file
types.ts
+7
-0

  fallback_used?: boolean;
  tool_events?: Array<{
    type: 'tool_call' | 'tool_result';
    tool_name?: string;
    tool_id?: string;
    input?: Record<string, unknown>;
    result?: string;
  }>;
  voice_id?: string;
Edited file
useVoiceChat.ts
+1
-0

        fallback_used: Boolean(response.llm_fallback_used),
        tool_events: Array.isArray(response.tool_events) ? response.tool_events : [],
        voice_id: response.voice_id,
Edited file
VoicePanel.tsx
+40
-1

import { Loader2 } from 'lucide-react';
import { VoiceConfig, VoiceMessage } from '@/lib/types';
import { ToolCall, VoiceConfig, VoiceMessage } from '@/lib/types';
import { ToolCallCard } from './ToolCallCard';


function buildVoiceToolCards(message: VoiceMessage): ToolCall[] {
  const events = Array.isArray(message.tool_events) ? message.tool_events : [];
  const calls = new Map<string, ToolCall>();

  for (const event of events) {
    const toolId = String(event.tool_id || '');
    if (event.type === 'tool_call') {
      calls.set(toolId || `voice-tool-${calls.size + 1}`, {
        tool_name: String(event.tool_name || 'tool'),
        tool_id: toolId || `voice-tool-${calls.size + 1}`,
        input: event.input || {},
        status: 'loading',
      });
      continue;
    }
    if (event.type === 'tool_result') {
      const existing = calls.get(toolId);
      if (existing) {
        existing.status = 'completed';
        existing.result = String(event.result || '');
        continue;
      }
      calls.set(toolId || `voice-tool-${calls.size + 1}`, {
        tool_name: 'tool',
        tool_id: toolId || `voice-tool-${calls.size + 1}`,
        input: {},
        status: 'completed',
        result: String(event.result || ''),
      });
    }
  }

  return Array.from(calls.values());
}

export function VoicePanel({
            )}
            {message.role === 'assistant' && buildVoiceToolCards(message).map(toolCall => (
              <ToolCallCard key={toolCall.tool_id} toolCall={toolCall} />
            ))}
            {message.audio_url && (
I’m switching the configured voice model over to Omnicoder now so the voice lane matches the model you actually trust for agentic behavior. The code stays configurable, but the defaults and live env will stop pointing at minicpm-v.

Edited file
BUILD_PLAN.md
+14
-10

- keep the second button as the dedicated voice lane
- align the voice lane to the intended model stack:
  - main tool/chat lane: `omnicoder`
  - voice conversation lane: `minicpm-v`
- make the voice lane aware of live model catalogs instead of relying on stale hardcoded assumptions
- move the voice lane onto a known-good Qwen-family instruction path, with `omnicoder` as the current default
- make the voice lane use the full harness tool/multi-turn loop instead of the old one-shot `tools=[]` route
- keep the voice lane aware of live model catalogs instead of relying on stale hardcoded assumptions
- preserve end-to-end voice playback through realtime TTS with clear runtime visibility
2. Refactor voice model/config resolution
   - move the voice lane default model from the old `qwen3.5-4b` assumption to `minicpm-v`
   - preserve separate voice-lane config so the main agent model remains independent
   - move the voice lane off the old `qwen3.5-4b` and `minicpm-v` assumptions onto `omnicoder` by default
   - preserve separate voice-lane config so the main agent model remains independently configurable
   - add live model-catalog fetching against the configured gateway/models endpoint where practical
3. Tighten voice-route runtime reporting
3. Replace the one-shot voice LLM path
   - stop calling the voice model with `tools=[]`
   - route the voice lane through the real agent loop with a voice-specific provider override
   - surface tool activity in the voice UI so multi-turn/tool behavior is visible
4. Tighten voice-route runtime reporting
   - expose authoritative voice-route config and available models to the frontend
   - keep realtime TTS preferred and HTTP synth as fallback
4. Verify the full path
5. Verify the full path
   - run targeted compile/build checks
- The second-button voice lane remains a separate turn-based voice surface, not the main tool-using chat lane.
- `minicpm-v` is the intended default conversation model for the current voice lane.
- `omnicoder` is the intended current default conversation model for the voice lane until the next known-good Qwen-family voice model is chosen.
- The unified gateway remains the canonical model base when a specific voice base URL is not set.
- `/api/voice/config` reports the intended voice model, transport, and available models/catalog details.
- Voice turns default to `minicpm-v` unless explicitly overridden by voice-specific config.
- Voice turns default to `omnicoder` unless explicitly overridden by voice-specific config.
- Voice turns use the real tool/multi-turn harness loop rather than the old one-shot direct generation path.
- The voice route returns authoritative requested/used model metadata and keeps realtime TTS bootstrap working.
Edited file
.env.polymorph.example
+1
-1

VOICE_AGENT_PROVIDER=openai_compat
VOICE_AGENT_MODEL=minicpm-v
VOICE_AGENT_MODEL=omnicoder
VOICE_AGENT_MAX_TOKENS=512
Edited file
.env.example
+1
-1

# VOICE_AGENT_PROVIDER=openai_compat
# VOICE_AGENT_MODEL=minicpm-v
# VOICE_AGENT_MODEL=omnicoder
# VOICE_AGENT_MAX_TOKENS=512
Edited file
.env
+1
-1

VOICE_AGENT_PROVIDER=openai_compat
VOICE_AGENT_MODEL=minicpm-v
VOICE_AGENT_MODEL=omnicoder
VOICE_AGENT_MAX_TOKENS=512
Edited file
.env.polymorph
+1
-1

VOICE_AGENT_PROVIDER=openai_compat
VOICE_AGENT_MODEL=minicpm-v
VOICE_AGENT_MODEL=omnicoder
VOICE_REALTIME_TTS_BASE_URL=https://asr.aetherpro.us
Edited file
VoicePanel.tsx
+1
-1

          <div className="rounded-xl border border-dashed border-border bg-card/60 p-3 text-sm text-muted-foreground">
            Voice turns land here instead of the main tool-using chat. The mic button now uses live ASR and the voice button sends the finalized transcript into this pane.
            Voice turns land here instead of the main text pane. The mic button still uses live ASR, and the voice button sends the finalized transcript through the full agent loop before audio playback lands here.
          </div>
Edited file
voice.py
+1
-1

        base_url=base_url,
        transport="live_asr_final_to_voice_model_plus_realtime_tts",
        transport="live_asr_final_to_voice_agent_loop_plus_tts",
        realtime_tts_configured=bool(realtime_base_url),
The voice route is now wired into the actual agent loop on disk. I’m running compile/build again and then I’ll rebuild the containers and do a live second-button-style probe to confirm three things together: Omnicoder is the voice model, tool calls come back in the voice response payload, and TTS still wraps the final answer.

Background terminal finished with python3 -m py_compile mini-agent/backend/api/voice.py mini-agent/backend/agent/runner.py mini-agent/backend/api/chat.py


Background terminal finished with npm run build


Background terminal finished with docker compose build backend frontend && docker compose up -d backend frontend


The rebuilt stack is live. I’m sending a tool-using voice turn now, not just a plain greeting, because the important verification is whether the second-button route now actually executes the harness loop and returns tool activity with the final answer.

Background terminal finished with curl -fsS http://localhost:38333/api/voice/config


Background terminal finished with curl -fsS http://localhost:38333/api/voice/turn -H 'Content-Type: application/json' -d '{"session_id":"voice-tool-smoke","message":"Use the calculator tool to add 12 and 30, then answer with the result.","history":[],"voice_id":"af_sky","reasoning_mode":"direct"}'


The live config is right: the voice lane now boots on omnicoder and advertises the full agent-loop transport. The tool-using voice smoke turn hit a 502 though, so I’m pulling the backend logs to see whether that is the agent loop itself, a tool execution issue, or the TTS leg after the tool run.

Background terminal finished with docker compose logs --tail=160 backend


This is the result I wanted from the probe: the voice lane is now definitely hitting the real tool loop. The turn reached stop_reason=tool_use on omnicoder; it only failed afterward because one of the fleet tools tries to read /fleet-inventory/model-inventory.yaml, which does not exist inside the backend container. I’m fixing that path issue next so the tool loop can complete instead of dying on the first tool call.

Explored 2 files, 2 lists
The failure is a packaging bug in the fleet tool layer, not the voice loop itself. The backend container only ships /app/backend, but the fleet inventory loader assumes a repo-root /fleet-inventory path and crashes at import time. I’m patching that loader to degrade cleanly when the external inventory bundle is absent, so unrelated tool calls do not take the whole voice turn down.

Explored 1 file, 1 search
I’m patching the fleet inventory loader now so the backend can boot and import fleet tools even when the external fleet-inventory/ bundle is not present inside the container image. That should stop unrelated tool calls from dying before they even reach the actual requested tool.

Edited file
inventory.py
+22
-1

from functools import lru_cache
import os
from pathlib import Path

FLEET_DIR = Path(__file__).resolve().parents[3] / "fleet-inventory"
def _resolve_fleet_dir() -> Path:
    override = os.getenv("FLEET_INVENTORY_DIR", "").strip()
    candidates = [
        Path(override) if override else None,
        Path(__file__).resolve().parents[3] / "fleet-inventory",
        Path(__file__).resolve().parents[2] / "fleet-inventory",
        Path("/app/fleet-inventory"),
        Path("/app/backend/fleet-inventory"),
        Path.cwd() / "fleet-inventory",
    ]
    for candidate in candidates:
        if candidate and candidate.exists():
            return candidate.resolve()
    return (Path(__file__).resolve().parents[2] / "fleet-inventory").resolve()


FLEET_DIR = _resolve_fleet_dir()
MODEL_TAGS = {
def _load_yaml(path: Path) -> Any:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")
The loader fix is in. I’m rebuilding just the backend now and rerunning the same tool-using voice turn; if this works, it means the second-button route is genuinely on the full harness loop and the earlier failure was just that fleet-inventory packaging bug.

Background terminal finished with python3 -m py_compile backend/fleet/inventory.py backend/api/voice.py backend/agent/runner.py && docker compose build backend && docker compose up -d backend


Background terminal finished with curl -fsS http://localhost:38333/api/voice/turn -H 'Content-Type: application/json' -d '{"session_id":"voice-tool-smoke-2","message":"Use the calculator tool to add 12 and 30, then answer with the result.","history":[],"voice_id":"af_sky","reasoning_mode":"direct"}'


One last voice-specific tweak: I’m adding your brand pronunciation note into the voice prompt so spoken references to Aether/AetherPro stay aligned with how you want it said. Then I’ll write the phase report and give you the live result summary.

Edited file
voice.py
+1
-0

        "You are PolyMorph Voice Mode, a fast spoken conversation assistant. "
        "Brand pronunciation guide: Aether and AetherPro are pronounced AY-ther, preferring the unvoiced TH. "
        "Keep replies concise, natural, and easy to listen to. "
Edited file
voice.py
+2
-2

        "Keep replies concise, natural, and easy to listen to. "
        "Tools are unavailable in this voice lane, so never emit tool calls, XML tool markup, or JSON tool payloads. "
        "Do not emit markdown, lists, or tool chatter unless the user explicitly asks."
        "When a tool is needed, use the harness tools directly instead of narrating the plan. "
        "Do not emit markdown, raw XML tool markup, or fake JSON tool payloads."
    )
Background terminal finished with python3 -m py_compile backend/api/voice.py && docker compose build backend && docker compose up -d backend


Created file
PHASE_15_REPORT.md
+48
-0

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
Background terminal finished with curl -fsS http://localhost:38333/api/voice/config


Background terminal finished with curl -fsS http://localhost:38333/api/voice/turn -H 'Content-Type: application/json' -d '{"session_id":"voice-tool-smoke-3","message":"Use the calculator tool to add 12 and 30, then answer with the result.","history":[],"voice_id":"af_sky","reasoning_mode":"direct"}'


The full voice loop is working now, including actual tool activity, but I see one cleanup item in the payload: streamed tool-call inputs are still arriving as {} before the final validated tool args are known. I’m patching the runner to emit the resolved tool input right before dispatch so the frontend shows the real tool parameters instead of empty shells.

