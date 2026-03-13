import os

import httpx
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from backend.config import build_service_auth_headers, resolve_env

router = APIRouter()

MAX_AUDIO_FILE_SIZE = int(os.getenv("ASR_MAX_FILE_SIZE_BYTES", str(25 * 1024 * 1024)))
DEFAULT_ASR_MODEL = os.getenv("ASR_MODEL", "auto")
DEFAULT_ASR_TIMEOUT_SECONDS = float(os.getenv("ASR_TIMEOUT_SECONDS", "60"))
EMPTY_AUTH_SENTINELS = {"", "empty", "none", "null", "optional"}


def _resolve_asr_config() -> tuple[str, str, str, float]:
    base_url = resolve_env("ASR_BASE_URL", service_id="asr", default="").strip()
    api_key = resolve_env("ASR_API_KEY", service_id="asr", default="").strip()
    model = resolve_env("ASR_MODEL", service_id="asr", default=DEFAULT_ASR_MODEL).strip() or DEFAULT_ASR_MODEL
    timeout = float(resolve_env("ASR_TIMEOUT_SECONDS", service_id="asr", default=str(DEFAULT_ASR_TIMEOUT_SECONDS)))
    return base_url, api_key, model, timeout


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


def _build_asr_endpoint(base_url: str, path: str) -> str:
    normalized_base = base_url.rstrip("/")
    normalized_path = path if path.startswith("/") else f"/{path}"
    if normalized_base.endswith("/api") and normalized_path.startswith("/api/"):
        normalized_path = normalized_path[len("/api"):]
    return f"{normalized_base}{normalized_path}"


def _normalize_optional_api_key(api_key: str) -> str:
    token = (api_key or "").strip()
    if token.lower() in EMPTY_AUTH_SENTINELS:
        return ""
    return token


def _asr_auth_header_candidates(api_key: str) -> list[dict[str, str]]:
    token = _normalize_optional_api_key(api_key)
    if not token:
        return [{}]

    candidates: list[dict[str, str]] = []
    configured = build_service_auth_headers(token, service_id="asr")
    if configured:
        candidates.append(configured)
        header_name = next(iter(configured.keys())).strip().lower()
        if header_name == "authorization":
            candidates.append({"X-API-Key": token})
    else:
        candidates.append({"X-API-Key": token})
    candidates.append({})

    deduped: list[dict[str, str]] = []
    seen: set[tuple[tuple[str, str], ...]] = set()
    for candidate in candidates:
        key = tuple(sorted(candidate.items()))
        if key in seen:
            continue
        deduped.append(candidate)
        seen.add(key)
    return deduped


class AsrLiveStartRequest(BaseModel):
    model: str = DEFAULT_ASR_MODEL
    language: str = "auto"
    sample_rate: int = 16000
    encoding: str = "pcm_s16le"
    channels: int = 1
    triage_enabled: bool = False
    metadata: dict[str, object] = Field(default_factory=lambda: {"source": "polymorph-mic"})


class AsrLiveStartResponse(BaseModel):
    session_id: str
    ws_url: str
    model_requested: str | None = None
    model_used: str | None = None
    fallback_used: bool | None = None
    upstream_base_url: str


@router.post("/audio/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str | None = Form(default=None),
    prompt: str | None = Form(default=None),
    model: str | None = Form(default=None),
):
    base_url, api_key, default_model, timeout_seconds = _resolve_asr_config()
    if not base_url:
        raise HTTPException(status_code=503, detail="ASR is not configured (missing ASR_BASE_URL).")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Audio file is empty.")
    if len(content) > MAX_AUDIO_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Audio file too large. Max size: {MAX_AUDIO_FILE_SIZE} bytes.",
        )

    resolved_model = (model or default_model).strip()
    auth_header_candidates = _asr_auth_header_candidates(api_key)

    # Compatibility: prefer the current voice gateway contract, then fall back to older
    # OpenAI-style or legacy native endpoints if an older deployment is still in use.
    override_path = resolve_env("ASR_TRANSCRIBE_PATH", service_id="asr", default="").strip()
    candidate_paths: list[str] = []
    if override_path:
        candidate_paths.append(override_path if override_path.startswith("/") else f"/{override_path}")
    candidate_paths.extend(["/v1/asr/transcribe", "/v1/audio/transcriptions", "/api/asr"])

    files = {
        "file": (
            file.filename or "recording.webm",
            content,
            file.content_type or "application/octet-stream",
        )
    }

    last_error = "ASR upstream request failed."
    response = None
    endpoint = ""
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(timeout_seconds)) as client:
            for path in candidate_paths:
                endpoint = _build_asr_endpoint(base_url, path)
                payload = {"model": resolved_model}
                if language:
                    payload["language"] = language
                if prompt and path == "/v1/audio/transcriptions":
                    payload["prompt"] = prompt

                for candidate_headers in auth_header_candidates:
                    resp = await client.post(endpoint, data=payload, files=files, headers=candidate_headers)
                    if resp.is_success:
                        response = resp
                        break

                    body = resp.text[:500]
                    last_error = f"{endpoint} returned {resp.status_code}: {body}"

                    if resp.status_code == 401:
                        continue

                    # Try fallback endpoint when path is not supported.
                    if resp.status_code in {404, 405}:
                        break

                    # For all other errors, stop and surface the real upstream response.
                    raise HTTPException(status_code=502, detail=last_error)

                if response is not None:
                    break

                if resp.status_code in {404, 405}:
                    continue
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"ASR upstream request failed: {exc}") from exc

    if response is None:
        raise HTTPException(status_code=502, detail=last_error)

    try:
        data = response.json()
    except ValueError as exc:
        raise HTTPException(status_code=502, detail="ASR upstream returned non-JSON response.") from exc

    text = data.get("text") if isinstance(data, dict) else None
    if not isinstance(text, str):
        text = ""

    return JSONResponse(
        content={
            "text": text,
            "model": resolved_model,
            "upstream": {
                "base_url": base_url,
                "status_code": response.status_code,
            },
            "raw": data,
        }
    )


@router.post("/audio/stream/start", response_model=AsrLiveStartResponse)
async def start_audio_stream(request: AsrLiveStartRequest):
    base_url, api_key, default_model, timeout_seconds = _resolve_asr_config()
    if not base_url:
        raise HTTPException(status_code=503, detail="ASR is not configured (missing ASR_BASE_URL).")

    endpoint = _build_asr_endpoint(base_url, "/api/v1/asr/stream/start")
    auth_header_candidates = _asr_auth_header_candidates(api_key)

    payload = request.model_dump()
    payload["model"] = (request.model or default_model).strip() or default_model
    if not payload["metadata"]:
        payload["metadata"] = {"source": "polymorph-mic"}

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(timeout_seconds)) as client:
            resp = None
            last_error = ""
            for auth_headers in auth_header_candidates:
                headers = {"Content-Type": "application/json", **auth_headers}
                resp = await client.post(endpoint, headers=headers, json=payload)
                if resp.is_success:
                    break
                detail = resp.text[:500]
                last_error = f"ASR live start failed: {resp.status_code} {detail}"
                if resp.status_code == 401:
                    continue
                break
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"ASR live start failed: {exc}") from exc

    if resp is None or not resp.is_success:
        raise HTTPException(status_code=502, detail=last_error or "ASR live start failed.")

    try:
        data = resp.json()
    except ValueError as exc:
        raise HTTPException(status_code=502, detail="ASR live start returned non-JSON response.") from exc

    if not isinstance(data, dict):
        raise HTTPException(status_code=502, detail="ASR live start returned an invalid payload.")

    session_id = str(data.get("session_id") or "").strip()
    ws_url = _resolve_live_ws_url(base_url, str(data.get("ws_url") or ""))
    if not session_id or not ws_url:
        raise HTTPException(status_code=502, detail="ASR live start response missing session_id or ws_url.")

    return AsrLiveStartResponse(
        session_id=session_id,
        ws_url=ws_url,
        model_requested=str(data.get("model_requested") or payload["model"]).strip() or None,
        model_used=str(data.get("model_used") or "").strip() or None,
        fallback_used=bool(data.get("fallback_used")) if "fallback_used" in data else None,
        upstream_base_url=base_url.rstrip("/"),
    )
