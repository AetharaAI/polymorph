from __future__ import annotations

import json
import os
import re
import uuid
from pathlib import Path
from typing import Literal

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from backend.agent.providers.failover_provider import FailoverProvider
from backend.agent.providers.factory import _build_single_provider
from backend.agent.runner import run_agent
from backend.config import (
    build_service_auth_headers,
    resolve_env,
    resolve_openai_compat_api_key,
    resolve_unified_gateway_base,
)
from backend.memory import get_memory_service

router = APIRouter()

VOICE_OUTPUT_ROOT = (Path(__file__).resolve().parent.parent / "uploads").resolve()
DEFAULT_VOICE_AGENT_MODEL = "omnicoder"
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
    if normalized_base.endswith("/v1") and normalized_path.startswith("/v1/"):
        normalized_path = normalized_path[len("/v1"):]
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


def _log_voice_event(event: str, payload: dict[str, object]) -> None:
    record = {"event": event, **payload}
    print(f"[VoiceTurn] {json.dumps(record, ensure_ascii=True, default=str)}", flush=True)


def _upsert_tool_event(tool_events: list[dict[str, object]], event: dict[str, object]) -> None:
    event_type = str(event.get("type") or "")
    tool_id = str(event.get("tool_id") or "")
    if not event_type or not tool_id:
        tool_events.append(event)
        return
    for index in range(len(tool_events) - 1, -1, -1):
        existing = tool_events[index]
        if str(existing.get("type") or "") != event_type:
            continue
        if str(existing.get("tool_id") or "") != tool_id:
            continue
        tool_events[index] = event
        return
    tool_events.append(event)


def _voice_agent_config() -> tuple[str, str, str, str, str]:
    provider_name = (
        _norm(resolve_env("VOICE_AGENT_PROVIDER", default=""))
        or _norm(resolve_env("AGENT_PROVIDER", default=""))
        or DEFAULT_VOICE_AGENT_PROVIDER
    )
    base_url = (
        _norm(resolve_env("VOICE_AGENT_BASE_URL", default=""))
        or _norm(resolve_env("OPENAI_COMPAT_BASE_URL", service_id="provider", default=""))
        or resolve_unified_gateway_base(service_id="provider")
        or _norm(resolve_env("OPENAI_BASE_URL", service_id="provider", default=""))
        or _norm(os.getenv("OPENAI_BASE_URL"))
    )
    api_key = (
        _norm(resolve_env("VOICE_AGENT_API_KEY", default=""))
        or resolve_openai_compat_api_key(service_id="provider")
        or _norm(resolve_env("OPENAI_COMPAT_API_KEY", service_id="provider", default=""))
        or _norm(resolve_env("OPENAI_API_KEY", service_id="provider", default=""))
        or _norm(os.getenv("OPENAI_API_KEY"))
    )
    model_candidates = [
        ("VOICE_AGENT_MODEL", _norm(resolve_env("VOICE_AGENT_MODEL", default=""))),
        ("AGENT_MODEL", _norm(resolve_env("AGENT_MODEL", default=""))),
        ("OPENAI_COMPAT_MODEL", _norm(resolve_env("OPENAI_COMPAT_MODEL", service_id="provider", default=""))),
        ("AGENT_FALLBACK_MODEL", _norm(resolve_env("AGENT_FALLBACK_MODEL", default=""))),
        ("default", DEFAULT_VOICE_AGENT_MODEL),
    ]
    model_name = DEFAULT_VOICE_AGENT_MODEL
    model_source = "default"
    for source, value in model_candidates:
        if value:
            model_name = value
            model_source = source
            break
    return provider_name, base_url, api_key, model_name, model_source


def _voice_agent_fallback_config(primary_model: str) -> tuple[str, str, str, str] | None:
    provider_name = (
        _norm(resolve_env("VOICE_AGENT_FALLBACK_PROVIDER", default=""))
        or _norm(resolve_env("VOICE_AGENT_PROVIDER", default=""))
        or _norm(resolve_env("AGENT_PROVIDER", default=""))
        or DEFAULT_VOICE_AGENT_PROVIDER
    )
    base_url = (
        _norm(resolve_env("VOICE_AGENT_FALLBACK_BASE_URL", default=""))
        or _norm(resolve_env("VOICE_AGENT_BASE_URL", default=""))
        or _norm(resolve_env("OPENAI_COMPAT_BASE_URL", service_id="provider", default=""))
        or resolve_unified_gateway_base(service_id="provider")
        or _norm(resolve_env("OPENAI_BASE_URL", service_id="provider", default=""))
        or _norm(os.getenv("OPENAI_BASE_URL"))
    )
    api_key = (
        _norm(resolve_env("VOICE_AGENT_FALLBACK_API_KEY", default=""))
        or resolve_openai_compat_api_key(service_id="provider")
        or _norm(resolve_env("OPENAI_COMPAT_API_KEY", service_id="provider", default=""))
        or _norm(resolve_env("OPENAI_API_KEY", service_id="provider", default=""))
        or _norm(os.getenv("OPENAI_API_KEY"))
    )
    model_candidates = [
        _norm(resolve_env("VOICE_AGENT_FALLBACK_MODEL", default="")),
        _norm(resolve_env("OPENAI_COMPAT_MODEL", service_id="provider", default="")),
        _norm(resolve_env("AGENT_FALLBACK_MODEL", default="")),
        _norm(resolve_env("AGENT_MODEL", default="")),
    ]
    model_name = ""
    for candidate in model_candidates:
        if candidate and candidate != primary_model:
            model_name = candidate
            break

    if not (provider_name and base_url and api_key and model_name):
        return None
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
        "Brand pronunciation guide: Aether and AetherPro are pronounced AY-ther, preferring the unvoiced TH. "
        "Keep replies concise, natural, and easy to listen to. "
        "When a tool is needed, use the harness tools directly instead of narrating the plan. "
        "Do not emit markdown, raw XML tool markup, or fake JSON tool payloads."
    )


def _voice_agent_provider(
    provider_name: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
    model_name: str | None = None,
    *,
    label: str = "voice_agent",
):
    if not (provider_name and base_url and api_key and model_name):
        provider_name, base_url, api_key, model_name, _ = _voice_agent_config()
    if not (base_url and api_key and model_name):
        raise HTTPException(
            status_code=503,
            detail=(
                "Voice mode is not configured. Set VOICE_AGENT_* or provider-compatible "
                "OPENAI_COMPAT_/LITELLM env vars for the dedicated voice route."
            ),
        )
    try:
        return _build_single_provider(
            provider_name,
            base_url=base_url,
            api_key=api_key,
            model_name=model_name,
            label=label,
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=f"Voice agent provider configuration failed: {exc}") from exc


def _voice_agent_provider_chain(
    provider_name: str,
    base_url: str,
    api_key: str,
    model_name: str,
):
    primary = _voice_agent_provider(
        provider_name=provider_name,
        base_url=base_url,
        api_key=api_key,
        model_name=model_name,
        label="voice_agent",
    )
    fallback_config = _voice_agent_fallback_config(model_name)
    if not fallback_config:
        return primary
    fallback_provider_name, fallback_base_url, fallback_api_key, fallback_model_name = fallback_config
    fallback = _voice_agent_provider(
        provider_name=fallback_provider_name,
        base_url=fallback_base_url,
        api_key=fallback_api_key,
        model_name=fallback_model_name,
        label="voice_agent_fallback",
    )
    return FailoverProvider([primary, fallback])


def _voice_audio_dir(session_id: str) -> Path:
    safe_session_id = "".join(ch for ch in session_id if ch.isalnum() or ch in {"-", "_"})
    if not safe_session_id:
        safe_session_id = "default"
    target = (VOICE_OUTPUT_ROOT / safe_session_id / "voice").resolve()
    target.mkdir(parents=True, exist_ok=True)
    return target


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


def _normalize_model_catalog(payload: object) -> list[dict[str, str]]:
    items: list[object] = []
    if isinstance(payload, dict):
        if isinstance(payload.get("data"), list):
            items = list(payload.get("data") or [])
        elif isinstance(payload.get("models"), list):
            items = list(payload.get("models") or [])
    elif isinstance(payload, list):
        items = list(payload)

    models: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in items:
        if isinstance(item, str):
            model_id = _norm(item)
            extra: dict[str, str] = {}
        elif isinstance(item, dict):
            model_id = _norm(str(item.get("id") or item.get("name") or ""))
            extra = {}
            kind = _norm(str(item.get("kind") or ""))
            status = _norm(str(item.get("status") or ""))
            if kind:
                extra["kind"] = kind
            if status:
                extra["status"] = status
        else:
            continue

        if not model_id or model_id in seen:
            continue
        seen.add(model_id)
        models.append({"id": model_id, "label": model_id, **extra})
    return models


async def _fetch_live_model_catalog(
    *,
    base_url: str,
    api_key: str,
    timeout_seconds: float,
) -> tuple[list[dict[str, str]], str | None, str | None]:
    if not base_url:
        return [], None, "Voice model base URL is empty."

    headers = build_service_auth_headers(api_key, default_header="Authorization")
    probe_paths = ["/models", "/v1/models"]
    last_error = ""
    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout_seconds)) as client:
        for path in probe_paths:
            endpoint = _build_gateway_endpoint(base_url, path)
            try:
                resp = await client.get(endpoint, headers=headers)
            except Exception as exc:  # noqa: BLE001
                last_error = f"{endpoint} request failed: {exc}"
                continue

            if not resp.is_success:
                last_error = f"{endpoint} returned {resp.status_code}: {resp.text[:200]}"
                continue

            try:
                data = resp.json()
            except ValueError:
                last_error = f"{endpoint} returned non-JSON payload."
                continue

            models = _normalize_model_catalog(data)
            if models:
                return models, endpoint, None
            last_error = f"{endpoint} returned an empty or unrecognized model catalog."

    return [], None, last_error or "No model catalog endpoint responded successfully."


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


async def _synthesize_voice_audio(text: str, voice_id: str | None) -> tuple[bytes, str, str, str, str, str]:
    tts_base_url = _norm(resolve_env("TTS_BASE_URL", service_id="tts", default=""))
    if not tts_base_url:
        raise HTTPException(status_code=503, detail="TTS is not configured (missing TTS_BASE_URL).")

    tts_api_key = _norm(resolve_env("TTS_API_KEY", service_id="tts", default=""))
    timeout_seconds = float(resolve_env("TTS_TIMEOUT_SECONDS", service_id="tts", default="45") or "45")
    tts_model = _norm(resolve_env("TTS_MODEL", service_id="tts", default="chatterbox")) or "chatterbox"
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
        return resp.content, content_type, ext, resolved_voice, tts_model, tts_base_url.rstrip("/")


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
    fallback_model: str | None = None
    model_source: str
    provider: str
    base_url: str
    transport: str
    realtime_tts_configured: bool
    realtime_tts_model: str
    realtime_tts_base_url: str
    tts_base_url: str
    default_voice_id: str
    available_voices: list[dict[str, str]] = Field(default_factory=list)
    available_models: list[dict[str, str]] = Field(default_factory=list)
    model_catalog_source: str | None = None
    model_catalog_error: str | None = None
    model_available_in_catalog: bool | None = None
    notes: list[str] = Field(default_factory=list)


class VoiceTurnResponse(BaseModel):
    assistant_text: str
    tool_events: list[dict[str, object]] = Field(default_factory=list)
    provider: str
    model: str
    requested_model: str | None = None
    llm_provider: str | None = None
    llm_model_requested: str | None = None
    llm_model_used: str | None = None
    llm_base_url: str | None = None
    llm_fallback_used: bool = False
    llm_notice: str | None = None
    voice_id: str
    tts_transport: str
    tts_model_requested: str | None = None
    tts_model_used: str | None = None
    tts_base_url: str | None = None
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
    provider_name, base_url, api_key, model_name, model_source = _voice_agent_config()
    fallback_config = _voice_agent_fallback_config(model_name)
    realtime_base_url, _, realtime_model = _realtime_tts_config()
    tts_base_url = _norm(resolve_env("TTS_BASE_URL", service_id="tts", default=""))
    default_voice_id = _resolve_realtime_voice_id(None)
    catalog_timeout_seconds = float(resolve_env("VOICE_AGENT_CATALOG_TIMEOUT_SECONDS", default="4") or "4")
    available_models, model_catalog_source, model_catalog_error = await _fetch_live_model_catalog(
        base_url=base_url,
        api_key=api_key,
        timeout_seconds=catalog_timeout_seconds,
    )
    available_model_ids = {entry.get("id", "") for entry in available_models}
    model_available_in_catalog = None if not available_models else model_name in available_model_ids
    return VoiceConfigResponse(
        configured=bool(base_url and api_key and model_name),
        model=model_name,
        fallback_model=fallback_config[3] if fallback_config else None,
        model_source=model_source,
        provider=provider_name,
        base_url=base_url,
        transport="live_asr_final_to_voice_agent_loop_plus_tts",
        realtime_tts_configured=bool(realtime_base_url),
        realtime_tts_model=realtime_model,
        realtime_tts_base_url=realtime_base_url,
        tts_base_url=tts_base_url,
        default_voice_id=default_voice_id,
        available_voices=_realtime_voice_options(),
        available_models=available_models,
        model_catalog_source=model_catalog_source,
        model_catalog_error=model_catalog_error,
        model_available_in_catalog=model_available_in_catalog,
        notes=[
            "Mic opens a live ASR websocket session and writes the final transcript into the main composer.",
            "Voice mode uses the same live ASR final transcript, then runs the full agent loop with a voice-specific model override.",
            "Tool calls and multi-turn execution stay enabled in the voice lane.",
            "Assistant speech now prefers realtime Kokoro TTS streaming for end-to-end voice playback.",
            "Model-to-model streams are still deferred; this route is turn-based voice over the full harness loop.",
        ],
    )


@router.post("/voice/turn", response_model=VoiceTurnResponse)
async def voice_turn(request: VoiceTurnRequest):
    user_message = request.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Voice turn message is empty.")

    provider_name, base_url, api_key, configured_model, _ = _voice_agent_config()
    voice_fallback = _voice_agent_fallback_config(configured_model)
    provider = _voice_agent_provider_chain(
        provider_name=provider_name,
        base_url=base_url,
        api_key=api_key,
        model_name=configured_model,
    )
    _log_voice_event(
        "request_start",
        {
            "session_id": request.session_id,
            "provider": provider.provider_name,
            "base_url": base_url,
            "requested_model": configured_model,
            "fallback_model": voice_fallback[3] if voice_fallback else None,
            "reasoning_mode": request.reasoning_mode or "direct",
            "history_messages": len(request.history[-10:]),
            "user_chars": len(user_message),
            "voice_id": _resolve_realtime_voice_id(request.voice_id),
        },
    )

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
            _upsert_tool_event(
                tool_events,
                {
                    "type": "tool_call",
                    "tool_name": str(event.get("tool_name") or ""),
                    "tool_id": str(event.get("tool_id") or ""),
                    "input": event.get("input") if isinstance(event.get("input"), dict) else {},
                },
            )
            return
        if event_type == "tool_result":
            _upsert_tool_event(
                tool_events,
                {
                    "type": "tool_result",
                    "tool_id": str(event.get("tool_id") or ""),
                    "result": str(event.get("result") or ""),
                },
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

    if terminal_error:
        raise HTTPException(status_code=502, detail=terminal_error)

    assistant_text = _sanitize_voice_reply_text("".join(text_fragments))
    if not assistant_text:
        assistant_text = _sanitize_voice_reply_text(await _latest_assistant_text(request.session_id))
    if not assistant_text:
        raise HTTPException(status_code=502, detail="Voice agent returned an empty response.")
    llm_provider = str(done_event.get("provider") or provider.provider_name)
    llm_model_used = str(done_event.get("model") or provider.model_name)
    llm_notice = str(done_event.get("provider_notice") or "").strip() or None
    llm_fallback_used = bool(done_event.get("fallback_used")) or llm_model_used != configured_model
    _log_voice_event(
        "llm_success",
        {
            "session_id": request.session_id,
            "provider": llm_provider,
            "requested_model": configured_model,
            "used_model": llm_model_used,
            "fallback_used": llm_fallback_used,
            "assistant_chars": len(assistant_text),
            "tool_events": len(tool_events),
        },
    )
    try:
        realtime = await _start_realtime_tts_stream(
            session_id=request.session_id,
            voice_id=request.voice_id,
            assistant_text=assistant_text,
        )
        _log_voice_event(
            "tts_realtime_start",
            {
                "session_id": request.session_id,
                "requested_model": str(realtime.get("stream_model_requested") or "") or None,
                "used_model": str(realtime.get("stream_model_used") or "") or None,
                "fallback_used": bool(realtime.get("fallback_used")) if "fallback_used" in realtime else False,
                "voice_id": str(realtime.get("voice_id") or _resolve_realtime_voice_id(request.voice_id)),
            },
        )
        return VoiceTurnResponse(
            assistant_text=assistant_text,
            tool_events=tool_events,
            provider=llm_provider,
            model=llm_model_used,
            requested_model=configured_model,
            llm_provider=llm_provider,
            llm_model_requested=configured_model,
            llm_model_used=llm_model_used,
            llm_base_url=base_url,
            llm_fallback_used=llm_fallback_used,
            llm_notice=llm_notice,
            voice_id=str(realtime.get("voice_id") or _resolve_realtime_voice_id(request.voice_id)),
            tts_transport="realtime_stream",
            tts_model_requested=str(realtime.get("stream_model_requested") or "") or None,
            tts_model_used=str(realtime.get("stream_model_used") or "") or None,
            tts_base_url=str(realtime.get("stream_http_base_url") or "") or None,
            tts_stream_session_id=str(realtime.get("stream_session_id") or "") or None,
            tts_stream_ws_url=str(realtime.get("stream_ws_url") or "") or None,
            tts_stream_http_base_url=str(realtime.get("stream_http_base_url") or "") or None,
            tts_stream_model_requested=str(realtime.get("stream_model_requested") or "") or None,
            tts_stream_model_used=str(realtime.get("stream_model_used") or "") or None,
            tts_stream_fallback_used=bool(realtime.get("fallback_used")) if "fallback_used" in realtime else None,
            tts_stream_runtime=realtime.get("runtime") if isinstance(realtime.get("runtime"), dict) else {},
        )
    except HTTPException as exc:
        _log_voice_event(
            "tts_realtime_failed",
            {
                "session_id": request.session_id,
                "status_code": exc.status_code,
                "detail": str(exc.detail),
            },
        )
        audio_bytes, mime_type, extension, resolved_voice, tts_model, tts_base_url = await _synthesize_voice_audio(
            assistant_text,
            request.voice_id,
        )
        audio_dir = _voice_audio_dir(request.session_id)
        filename = f"voice-response-{uuid.uuid4().hex}.{extension}"
        file_path = (audio_dir / filename).resolve()
        file_path.write_bytes(audio_bytes)
        _log_voice_event(
            "tts_http_fallback",
            {
                "session_id": request.session_id,
                "tts_model": tts_model,
                "voice_id": resolved_voice,
                "mime_type": mime_type,
                "filename": filename,
            },
        )
        return VoiceTurnResponse(
            assistant_text=assistant_text,
            tool_events=tool_events,
            provider=llm_provider,
            model=llm_model_used,
            requested_model=configured_model,
            llm_provider=llm_provider,
            llm_model_requested=configured_model,
            llm_model_used=llm_model_used,
            llm_base_url=base_url,
            llm_fallback_used=llm_fallback_used,
            llm_notice=llm_notice,
            voice_id=resolved_voice,
            tts_transport="http_synth_fallback",
            tts_model_requested=tts_model,
            tts_model_used=tts_model,
            tts_base_url=tts_base_url,
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
