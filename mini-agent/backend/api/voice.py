from __future__ import annotations

import os
import re
import uuid
from pathlib import Path
from typing import Literal

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from backend.agent.providers.base import LLMContentBlock
from backend.agent.providers.factory import _build_single_provider
from backend.config import (
    build_service_auth_headers,
    resolve_env,
    resolve_openai_compat_api_key,
    resolve_unified_gateway_base,
)

router = APIRouter()

VOICE_OUTPUT_ROOT = (Path(__file__).resolve().parent.parent / "uploads").resolve()
DEFAULT_VOICE_AGENT_MODEL = "qwen3.5-4b"
DEFAULT_VOICE_AGENT_PROVIDER = "openai_compat"
DEFAULT_TTS_VOICE = "Emily.wav"
DEFAULT_TTS_OUTPUT_FORMAT = "wav"
DEFAULT_REALTIME_TTS_MODEL = "kokoro_realtime"
DEFAULT_REALTIME_TTS_VOICE = "af_sky"
DEFAULT_REALTIME_TTS_CONTEXT_MODE = "conversation"
DEFAULT_REALTIME_TTS_SAMPLE_RATE = 24000
DEFAULT_REALTIME_TTS_FORMAT = "wav"

REALTIME_VOICE_PRESETS = [
    {"id": "af_sky", "label": "Sky"},
    {"id": "af_bella", "label": "Bella"},
    {"id": "af_heart", "label": "Heart"},
    {"id": "af_nicole", "label": "Nicole"},
    {"id": "af_sarah", "label": "Sarah"},
    {"id": "am_adam", "label": "Adam"},
    {"id": "am_michael", "label": "Michael"},
    {"id": "bf_emma", "label": "Emma"},
    {"id": "bf_isabella", "label": "Isabella"},
    {"id": "bm_george", "label": "George"},
    {"id": "bm_lewis", "label": "Lewis"},
]


def _norm(value: str | None) -> str:
    return (value or "").strip()


def _resolve_live_ws_url(base_url: str, ws_url: str) -> str:
    trimmed = ws_url.strip()
    if not trimmed:
        return ""
    if trimmed.startswith("ws://") or trimmed.startswith("wss://"):
        return trimmed
    if trimmed.startswith("/"):
        http_base = base_url.rstrip("/")
        if http_base.startswith("https://"):
            return f"wss://{http_base[len('https://'):]}{trimmed}"
        if http_base.startswith("http://"):
            return f"ws://{http_base[len('http://'):]}{trimmed}"
        return f"{http_base}{trimmed}"
    return trimmed


def _build_gateway_endpoint(base_url: str, path: str) -> str:
    normalized_base = base_url.rstrip("/")
    normalized_path = path if path.startswith("/") else f"/{path}"
    if normalized_base.endswith("/api") and normalized_path.startswith("/api/"):
        normalized_path = normalized_path[len("/api"):]
    return f"{normalized_base}{normalized_path}"


def _realtime_voice_options() -> list[dict[str, str]]:
    return [dict(item) for item in REALTIME_VOICE_PRESETS]


def _resolve_realtime_voice_id(voice_id: str | None) -> str:
    requested = _norm(voice_id)
    valid = {item["id"] for item in REALTIME_VOICE_PRESETS}
    if requested in valid:
        return requested
    configured = _norm(resolve_env("VOICE_REALTIME_TTS_VOICE", default=DEFAULT_REALTIME_TTS_VOICE))
    if configured in valid:
        return configured
    return DEFAULT_REALTIME_TTS_VOICE


def _sanitize_voice_reply_text(text: str) -> str:
    cleaned = str(text or "")
    cleaned = re.sub(r"(?is)<think>.*?</think>", "", cleaned)
    cleaned = re.sub(r"(?is)<tool_call>.*?</tool_call>", "", cleaned)
    cleaned = re.sub(r"(?is)<\|.*?\|>", "", cleaned)
    cleaned = re.sub(r"(?m)^\s*```(?:json|tool|xml)?\s*$", "", cleaned)
    cleaned = re.sub(r"(?m)^\s*```\s*$", "", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def _voice_agent_config() -> tuple[str, str, str, str]:
    provider_name = _norm(resolve_env("VOICE_AGENT_PROVIDER", default="")) or DEFAULT_VOICE_AGENT_PROVIDER
    base_url = (
        _norm(resolve_env("VOICE_AGENT_BASE_URL", default=""))
        or resolve_unified_gateway_base(service_id="provider")
        or _norm(resolve_env("OPENAI_BASE_URL", service_id="provider", default=""))
        or _norm(os.getenv("OPENAI_BASE_URL"))
    )
    api_key = (
        _norm(resolve_env("VOICE_AGENT_API_KEY", default=""))
        or resolve_openai_compat_api_key(service_id="provider")
        or _norm(resolve_env("OPENAI_API_KEY", service_id="provider", default=""))
        or _norm(os.getenv("OPENAI_API_KEY"))
    )
    model_name = _norm(resolve_env("VOICE_AGENT_MODEL", default=DEFAULT_VOICE_AGENT_MODEL)) or DEFAULT_VOICE_AGENT_MODEL
    return provider_name, base_url, api_key, model_name


def _realtime_tts_config() -> tuple[str, str, str]:
    base_url = (
        _norm(resolve_env("VOICE_REALTIME_TTS_BASE_URL", default=""))
        or _norm(resolve_env("ASR_BASE_URL", service_id="asr", default=""))
    )
    api_key = (
        _norm(resolve_env("VOICE_REALTIME_TTS_API_KEY", default=""))
        or _norm(resolve_env("ASR_API_KEY", service_id="asr", default=""))
        or _norm(resolve_env("TTS_API_KEY", service_id="tts", default=""))
    )
    model_name = _norm(resolve_env("VOICE_REALTIME_TTS_MODEL", default=DEFAULT_REALTIME_TTS_MODEL)) or DEFAULT_REALTIME_TTS_MODEL
    return base_url, api_key, model_name


def _voice_agent_system_prompt() -> str:
    configured = _norm(resolve_env("VOICE_AGENT_SYSTEM_PROMPT", default=""))
    if configured:
        return configured
    return (
        "You are PolyMorph Voice Mode, a fast spoken conversation assistant. "
        "Keep replies concise, natural, and easy to listen to. "
        "Do not emit markdown, lists, or tool chatter unless the user explicitly asks."
    )


def _voice_agent_provider():
    provider_name, base_url, api_key, model_name = _voice_agent_config()
    if not (base_url and api_key and model_name):
        raise HTTPException(
            status_code=503,
            detail=(
                "Voice mode is not configured. Set VOICE_AGENT_* or provider-compatible "
                "OPENAI_COMPAT_/LITELLM env vars for the qwen3.5-4b route."
            ),
        )
    try:
        return _build_single_provider(
            provider_name,
            base_url=base_url,
            api_key=api_key,
            model_name=model_name,
            label="voice_agent",
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=f"Voice agent provider configuration failed: {exc}") from exc


def _voice_audio_dir(session_id: str) -> Path:
    safe_session_id = "".join(ch for ch in session_id if ch.isalnum() or ch in {"-", "_"})
    if not safe_session_id:
        safe_session_id = "default"
    target = (VOICE_OUTPUT_ROOT / safe_session_id / "voice").resolve()
    target.mkdir(parents=True, exist_ok=True)
    return target


def _extract_text(blocks: list[LLMContentBlock]) -> str:
    return "".join(block.text or "" for block in blocks if block.type == "text").strip()


async def _fetch_predefined_voices(tts_base_url: str, timeout_seconds: float) -> list[dict[str, str]]:
    if not tts_base_url:
        return []
    url = f"{tts_base_url.rstrip('/')}/get_predefined_voices"
    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout_seconds)) as client:
        resp = await client.get(url)
        if not resp.is_success:
            return []
        data = resp.json()
    if not isinstance(data, list):
        return []
    voices: list[dict[str, str]] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        filename = _norm(str(item.get("filename") or ""))
        display_name = _norm(str(item.get("display_name") or filename))
        if not filename:
            continue
        voices.append({"id": filename, "label": display_name})
    return voices


async def _start_realtime_tts_stream(
    *,
    session_id: str,
    voice_id: str | None,
    assistant_text: str,
) -> dict[str, object]:
    base_url, api_key, model_name = _realtime_tts_config()
    if not base_url:
        raise HTTPException(status_code=503, detail="Realtime voice gateway is not configured.")

    timeout_seconds = float(resolve_env("VOICE_REALTIME_TTS_TIMEOUT_SECONDS", default="20") or "20")
    resolved_voice = _resolve_realtime_voice_id(voice_id)
    payload = {
        "model": model_name,
        "voice": resolved_voice,
        "sample_rate": int(resolve_env("VOICE_REALTIME_TTS_SAMPLE_RATE", default=str(DEFAULT_REALTIME_TTS_SAMPLE_RATE)) or str(DEFAULT_REALTIME_TTS_SAMPLE_RATE)),
        "format": _norm(resolve_env("VOICE_REALTIME_TTS_FORMAT", default=DEFAULT_REALTIME_TTS_FORMAT)) or DEFAULT_REALTIME_TTS_FORMAT,
        "context_mode": _norm(resolve_env("VOICE_REALTIME_TTS_CONTEXT_MODE", default=DEFAULT_REALTIME_TTS_CONTEXT_MODE)) or DEFAULT_REALTIME_TTS_CONTEXT_MODE,
        "metadata": {
            "source": "polymorph_voice_mode",
            "extra": {
                "surface": "polymorph",
                "session_id": session_id,
                "assistant_chars": len(assistant_text),
            },
        },
    }
    headers = {"Content-Type": "application/json", **build_service_auth_headers(api_key, service_id="tts")}
    endpoint = _build_gateway_endpoint(base_url, "/api/v1/tts/stream/start")

    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout_seconds)) as client:
        resp = await client.post(endpoint, headers=headers, json=payload)
        if not resp.is_success:
            detail = resp.text[:300]
            raise HTTPException(status_code=502, detail=f"Realtime TTS bootstrap failed: {resp.status_code} {detail}")
        data = resp.json()

    if not isinstance(data, dict):
        raise HTTPException(status_code=502, detail="Realtime TTS bootstrap returned an invalid payload.")

    ws_url = _resolve_live_ws_url(base_url, str(data.get("ws_url") or ""))
    if not ws_url:
        raise HTTPException(status_code=502, detail="Realtime TTS bootstrap missing ws_url.")

    return {
        "transport": "realtime_stream",
        "stream_session_id": str(data.get("session_id") or "").strip(),
        "stream_ws_url": ws_url,
        "stream_http_base_url": base_url.rstrip("/"),
        "stream_model_requested": str(data.get("model_requested") or payload["model"]).strip() or payload["model"],
        "stream_model_used": str(data.get("model_used") or payload["model"]).strip() or payload["model"],
        "fallback_used": bool(data.get("fallback_used")) if "fallback_used" in data else False,
        "runtime": data.get("runtime") if isinstance(data.get("runtime"), dict) else {},
        "voice_id": resolved_voice,
    }


async def _synthesize_voice_audio(text: str, voice_id: str | None) -> tuple[bytes, str, str, str]:
    tts_base_url = _norm(resolve_env("TTS_BASE_URL", service_id="tts", default=""))
    if not tts_base_url:
        raise HTTPException(status_code=503, detail="TTS is not configured (missing TTS_BASE_URL).")

    tts_api_key = _norm(resolve_env("TTS_API_KEY", service_id="tts", default=""))
    timeout_seconds = float(resolve_env("TTS_TIMEOUT_SECONDS", service_id="tts", default="45") or "45")
    output_format = _norm(resolve_env("VOICE_TTS_OUTPUT_FORMAT", default=DEFAULT_TTS_OUTPUT_FORMAT)) or DEFAULT_TTS_OUTPUT_FORMAT
    requested_voice = _norm(voice_id)
    if requested_voice in {item["id"] for item in REALTIME_VOICE_PRESETS} and "." not in requested_voice:
        requested_voice = ""
    resolved_voice = requested_voice or _norm(resolve_env("VOICE_TTS_PREDEFINED_VOICE_ID", default=DEFAULT_TTS_VOICE)) or DEFAULT_TTS_VOICE

    headers = {"Content-Type": "application/json", **build_service_auth_headers(tts_api_key, service_id="tts")}

    payload = {
        "text": text,
        "voice_mode": "predefined",
        "predefined_voice_id": resolved_voice,
        "output_format": output_format,
        "split_text": True,
    }

    endpoint = f"{tts_base_url.rstrip('/')}/tts"
    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout_seconds)) as client:
        resp = await client.post(endpoint, headers=headers, json=payload)
        if not resp.is_success:
            detail = resp.text[:300]
            raise HTTPException(status_code=502, detail=f"TTS synthesis failed: {resp.status_code} {detail}")
        content_type = _norm(resp.headers.get("content-type")) or "audio/wav"
        ext = "wav"
        if "opus" in content_type:
            ext = "opus"
        elif "mpeg" in content_type or output_format == "mp3":
            ext = "mp3"
        return resp.content, content_type, ext, resolved_voice


class VoiceHistoryItem(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(default="")


class VoiceTurnRequest(BaseModel):
    session_id: str
    message: str
    history: list[VoiceHistoryItem] = Field(default_factory=list)
    voice_id: str | None = None
    reasoning_mode: Literal["direct", "reasoning"] | None = None


class VoiceConfigResponse(BaseModel):
    configured: bool
    model: str
    provider: str
    transport: str
    realtime_tts_configured: bool
    realtime_tts_model: str
    realtime_tts_base_url: str
    tts_base_url: str
    default_voice_id: str
    available_voices: list[dict[str, str]] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class VoiceTurnResponse(BaseModel):
    assistant_text: str
    provider: str
    model: str
    voice_id: str
    tts_transport: str
    audio_url: str | None = None
    mime_type: str | None = None
    tts_stream_session_id: str | None = None
    tts_stream_ws_url: str | None = None
    tts_stream_http_base_url: str | None = None
    tts_stream_model_requested: str | None = None
    tts_stream_model_used: str | None = None
    tts_stream_fallback_used: bool | None = None
    tts_stream_runtime: dict[str, object] = Field(default_factory=dict)


@router.get("/voice/config", response_model=VoiceConfigResponse)
async def get_voice_config():
    provider_name, base_url, _, model_name = _voice_agent_config()
    realtime_base_url, _, realtime_model = _realtime_tts_config()
    tts_base_url = _norm(resolve_env("TTS_BASE_URL", service_id="tts", default=""))
    default_voice_id = _resolve_realtime_voice_id(None)
    return VoiceConfigResponse(
        configured=bool(base_url),
        model=model_name,
        provider=provider_name,
        transport="live_asr_final_to_voice_model_plus_realtime_tts",
        realtime_tts_configured=bool(realtime_base_url),
        realtime_tts_model=realtime_model,
        realtime_tts_base_url=realtime_base_url,
        tts_base_url=tts_base_url,
        default_voice_id=default_voice_id,
        available_voices=_realtime_voice_options(),
        notes=[
            "Mic opens a live ASR websocket session and writes the final transcript into the main composer.",
            "Voice mode uses the same live ASR final transcript, then routes the turn through the separate voice model pane.",
            "Assistant speech now prefers realtime Kokoro TTS streaming for end-to-end voice playback.",
            "Model-to-model streams are deferred; this pass upgrades the TTS leg only.",
        ],
    )


@router.post("/voice/turn", response_model=VoiceTurnResponse)
async def voice_turn(request: VoiceTurnRequest):
    user_message = request.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Voice turn message is empty.")

    provider = _voice_agent_provider()
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

    response = await provider.generate(
        system=_voice_agent_system_prompt(),
        tools=[],
        messages=messages,
        max_tokens=int(resolve_env("VOICE_AGENT_MAX_TOKENS", default="512") or "512"),
        temperature=float(resolve_env("VOICE_AGENT_TEMPERATURE", default="0.6") or "0.6"),
        enable_thinking=request.reasoning_mode == "reasoning",
        on_stream_event=None,
    )
    assistant_text = _sanitize_voice_reply_text(_extract_text(response.content))
    if not assistant_text:
        raise HTTPException(status_code=502, detail="Voice agent returned an empty response.")
    try:
        realtime = await _start_realtime_tts_stream(
            session_id=request.session_id,
            voice_id=request.voice_id,
            assistant_text=assistant_text,
        )
        return VoiceTurnResponse(
            assistant_text=assistant_text,
            provider=response.provider_name or provider.provider_name,
            model=response.model_name or provider.model_name,
            voice_id=str(realtime.get("voice_id") or _resolve_realtime_voice_id(request.voice_id)),
            tts_transport="realtime_stream",
            tts_stream_session_id=str(realtime.get("stream_session_id") or "") or None,
            tts_stream_ws_url=str(realtime.get("stream_ws_url") or "") or None,
            tts_stream_http_base_url=str(realtime.get("stream_http_base_url") or "") or None,
            tts_stream_model_requested=str(realtime.get("stream_model_requested") or "") or None,
            tts_stream_model_used=str(realtime.get("stream_model_used") or "") or None,
            tts_stream_fallback_used=bool(realtime.get("fallback_used")) if "fallback_used" in realtime else None,
            tts_stream_runtime=realtime.get("runtime") if isinstance(realtime.get("runtime"), dict) else {},
        )
    except HTTPException:
        audio_bytes, mime_type, extension, resolved_voice = await _synthesize_voice_audio(assistant_text, request.voice_id)
        audio_dir = _voice_audio_dir(request.session_id)
        filename = f"voice-response-{uuid.uuid4().hex}.{extension}"
        file_path = (audio_dir / filename).resolve()
        file_path.write_bytes(audio_bytes)
        return VoiceTurnResponse(
            assistant_text=assistant_text,
            provider=response.provider_name or provider.provider_name,
            model=response.model_name or provider.model_name,
            voice_id=resolved_voice,
            tts_transport="http_synth_fallback",
            mime_type=mime_type,
            audio_url=f"/api/voice/audio/{request.session_id}/{filename}",
        )


@router.get("/voice/audio/{session_id}/{filename}")
async def get_voice_audio(session_id: str, filename: str):
    audio_dir = _voice_audio_dir(session_id)
    target = (audio_dir / filename).resolve()
    if audio_dir not in target.parents:
        raise HTTPException(status_code=400, detail="Invalid voice audio path.")
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="Voice audio not found.")
    media_type = "audio/wav"
    if target.suffix.lower() == ".mp3":
        media_type = "audio/mpeg"
    elif target.suffix.lower() == ".opus":
        media_type = "audio/opus"
    return FileResponse(path=target, media_type=media_type, filename=target.name)
