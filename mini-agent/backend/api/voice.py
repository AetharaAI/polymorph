from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Literal

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from backend.agent.providers.base import LLMContentBlock
from backend.agent.providers.factory import _build_single_provider
from backend.config import build_service_auth_headers, resolve_env

router = APIRouter()

VOICE_OUTPUT_ROOT = (Path(__file__).resolve().parent.parent / "uploads").resolve()
DEFAULT_VOICE_AGENT_MODEL = "qwen3.5-4b"
DEFAULT_VOICE_AGENT_PROVIDER = "openai_compat"
DEFAULT_TTS_VOICE = "Emily.wav"
DEFAULT_TTS_OUTPUT_FORMAT = "wav"


def _norm(value: str | None) -> str:
    return (value or "").strip()


def _voice_agent_config() -> tuple[str, str, str, str]:
    provider_name = _norm(resolve_env("VOICE_AGENT_PROVIDER", default="")) or DEFAULT_VOICE_AGENT_PROVIDER
    base_url = (
        _norm(resolve_env("VOICE_AGENT_BASE_URL", default=""))
        or _norm(os.getenv("LITELLM_MODEL_BASE_URL"))
        or _norm(os.getenv("LITELLM_2_MODEL_BASE_URL"))
        or _norm(resolve_env("OPENAI_COMPAT_BASE_URL", service_id="provider", default=""))
        or _norm(resolve_env("OPENAI_BASE_URL", service_id="provider", default=""))
        or _norm(os.getenv("OPENAI_BASE_URL"))
    )
    api_key = (
        _norm(resolve_env("VOICE_AGENT_API_KEY", default=""))
        or _norm(os.getenv("LITELLM_API_KEY"))
        or _norm(os.getenv("LITELLM_2_API_KEY"))
        or _norm(resolve_env("OPENAI_COMPAT_API_KEY", service_id="provider", default=""))
        or _norm(resolve_env("OPENAI_API_KEY", service_id="provider", default=""))
        or _norm(os.getenv("OPENAI_API_KEY"))
    )
    model_name = _norm(resolve_env("VOICE_AGENT_MODEL", default=DEFAULT_VOICE_AGENT_MODEL)) or DEFAULT_VOICE_AGENT_MODEL
    return provider_name, base_url, api_key, model_name


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


async def _synthesize_voice_audio(text: str, voice_id: str | None) -> tuple[bytes, str, str, str]:
    tts_base_url = _norm(resolve_env("TTS_BASE_URL", service_id="tts", default=""))
    if not tts_base_url:
        raise HTTPException(status_code=503, detail="TTS is not configured (missing TTS_BASE_URL).")

    tts_api_key = _norm(resolve_env("TTS_API_KEY", service_id="tts", default=""))
    timeout_seconds = float(resolve_env("TTS_TIMEOUT_SECONDS", service_id="tts", default="45") or "45")
    output_format = _norm(resolve_env("VOICE_TTS_OUTPUT_FORMAT", default=DEFAULT_TTS_OUTPUT_FORMAT)) or DEFAULT_TTS_OUTPUT_FORMAT
    resolved_voice = _norm(voice_id) or _norm(resolve_env("VOICE_TTS_PREDEFINED_VOICE_ID", default=DEFAULT_TTS_VOICE)) or DEFAULT_TTS_VOICE

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


class VoiceConfigResponse(BaseModel):
    configured: bool
    model: str
    provider: str
    transport: str
    tts_base_url: str
    default_voice_id: str
    available_voices: list[dict[str, str]] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


@router.get("/voice/config", response_model=VoiceConfigResponse)
async def get_voice_config():
    provider_name, base_url, _, model_name = _voice_agent_config()
    tts_base_url = _norm(resolve_env("TTS_BASE_URL", service_id="tts", default=""))
    timeout_seconds = float(resolve_env("TTS_TIMEOUT_SECONDS", service_id="tts", default="20") or "20")
    voices = await _fetch_predefined_voices(tts_base_url, timeout_seconds)
    default_voice_id = _norm(resolve_env("VOICE_TTS_PREDEFINED_VOICE_ID", default=DEFAULT_TTS_VOICE)) or DEFAULT_TTS_VOICE
    return VoiceConfigResponse(
        configured=bool(base_url),
        model=model_name,
        provider=provider_name,
        transport="live_asr_final_to_qwen4b_plus_http_tts",
        tts_base_url=tts_base_url,
        default_voice_id=default_voice_id,
        available_voices=voices,
        notes=[
            "Mic opens a live ASR websocket session and writes the final transcript into the main composer.",
            "Voice mode uses the same live ASR final transcript, then routes the turn through the separate qwen3.5-4b PolyMorph Voice pane.",
            "Assistant speech still uses stable HTTP TTS synthesis after the voice-model text reply is finalized.",
        ],
    )


@router.post("/voice/turn")
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
        on_stream_event=None,
    )
    assistant_text = _extract_text(response.content)
    if not assistant_text:
        raise HTTPException(status_code=502, detail="Voice agent returned an empty response.")

    audio_bytes, mime_type, extension, resolved_voice = await _synthesize_voice_audio(assistant_text, request.voice_id)
    audio_dir = _voice_audio_dir(request.session_id)
    filename = f"voice-response-{uuid.uuid4().hex}.{extension}"
    file_path = (audio_dir / filename).resolve()
    file_path.write_bytes(audio_bytes)

    return {
        "assistant_text": assistant_text,
        "provider": response.provider_name or provider.provider_name,
        "model": response.model_name or provider.model_name,
        "voice_id": resolved_voice,
        "mime_type": mime_type,
        "audio_url": f"/api/voice/audio/{request.session_id}/{filename}",
    }


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
