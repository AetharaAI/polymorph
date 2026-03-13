from __future__ import annotations

import time
from typing import Any

import asyncpg
import httpx
import redis.asyncio as redis
from fastapi import APIRouter, HTTPException, Request
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from qdrant_client import AsyncQdrantClient

from backend.agent.providers import provider_metadata, reset_provider
from backend.config import (
    apply_runtime_overrides_to_env,
    build_service_auth_headers,
    clear_service_overrides,
    encryption_status,
    get_service_overrides,
    resolve_env,
    set_service_overrides,
)

router = APIRouter()


SERVICE_SPECS: dict[str, dict[str, Any]] = {
    "provider": {
        "name": "Model Provider",
        "description": "Primary model provider plus explicit failover routing.",
        "requires_restart": False,
        "fields": [
            {"env_key": "AGENT_PROVIDER", "label": "Provider (openai/openai_compat/anthropic)", "secret": False, "required": True},
            {"env_key": "AGENT_MODEL", "label": "Primary Model", "secret": False, "required": True},
            {"env_key": "OPENAI_BASE_URL", "label": "OpenAI Base URL", "secret": False, "required": False},
            {"env_key": "OPENAI_API_KEY", "label": "OpenAI API Key", "secret": True, "required": False},
            {"env_key": "OPENAI_COMPAT_BASE_URL", "label": "OpenAI-Compatible Base URL", "secret": False, "required": False},
            {"env_key": "OPENAI_COMPAT_API_KEY", "label": "OpenAI-Compatible API Key", "secret": True, "required": False},
            {"env_key": "OPENAI_COMPAT_MODEL", "label": "OpenAI-Compatible Model", "secret": False, "required": False},
            {"env_key": "AGENT_ENABLE_FALLBACK", "label": "Enable Fallback (true/false)", "secret": False, "required": False},
            {"env_key": "AGENT_FALLBACK_PROVIDER", "label": "Fallback Provider", "secret": False, "required": False},
            {"env_key": "AGENT_FALLBACK_BASE_URL", "label": "Fallback Base URL", "secret": False, "required": False},
            {"env_key": "AGENT_FALLBACK_API_KEY", "label": "Fallback API Key", "secret": True, "required": False},
            {"env_key": "AGENT_FALLBACK_MODEL", "label": "Fallback Model", "secret": False, "required": False},
        ],
    },
    "asr": {
        "name": "ASR (Speech-to-Text)",
        "description": "Voice transcription service used by mic input in composer.",
        "requires_restart": False,
        "fields": [
            {"env_key": "ASR_BASE_URL", "label": "Base URL", "secret": False, "required": False},
            {"env_key": "ASR_API_KEY", "label": "API Key", "secret": True, "required": False},
            {"env_key": "ASR_MODEL", "label": "Model Name", "secret": False, "required": False},
            {"env_key": "ASR_TIMEOUT_SECONDS", "label": "Timeout (s)", "secret": False, "required": False},
        ],
    },
    "tts": {
        "name": "TTS (Text-to-Speech)",
        "description": "Optional speech synthesis service for voice responses.",
        "requires_restart": False,
        "fields": [
            {"env_key": "TTS_BASE_URL", "label": "Base URL", "secret": False, "required": False},
            {"env_key": "TTS_API_KEY", "label": "API Key", "secret": True, "required": False},
            {"env_key": "TTS_MODEL", "label": "Model Name", "secret": False, "required": False},
            {"env_key": "TTS_TIMEOUT_SECONDS", "label": "Timeout (s)", "secret": False, "required": False},
        ],
    },
    "redis": {
        "name": "Redis Memory",
        "description": "Session state + short-term working memory backend.",
        "requires_restart": True,
        "fields": [
            {"env_key": "REDIS_URL", "label": "Redis URL", "secret": True, "required": False},
        ],
    },
    "mongo": {
        "name": "MongoDB Memory",
        "description": "Document memory backend for long-term traces.",
        "requires_restart": True,
        "fields": [
            {"env_key": "AETHER_MONGO_URI", "label": "Mongo URI", "secret": True, "required": False},
        ],
    },
    "postgres": {
        "name": "Postgres Memory",
        "description": "Structured memory/events backend.",
        "requires_restart": True,
        "fields": [
            {"env_key": "POSTGRES_DSN", "label": "Postgres DSN", "secret": True, "required": False},
        ],
    },
    "qdrant": {
        "name": "Qdrant Vector DB",
        "description": "Vector memory backend for semantic recall.",
        "requires_restart": True,
        "fields": [
            {"env_key": "QDRANT_HOST", "label": "Host", "secret": False, "required": False},
            {"env_key": "QDRANT_PORT", "label": "Port", "secret": False, "required": False},
            {"env_key": "QDRANT_API_KEY", "label": "API Key", "secret": True, "required": False},
        ],
    },
    "governance": {
        "name": "Project Governance",
        "description": "Plan-before-build controls and approval mode for autonomous project generation.",
        "requires_restart": False,
        "fields": [
            {"env_key": "AGENT_REQUIRE_PLAN_FOR_PROJECTS", "label": "Require Plan (true/false)", "secret": False, "required": False},
            {"env_key": "AGENT_PLAN_APPROVAL_MODE", "label": "Approval Mode (manual/auto)", "secret": False, "required": False},
            {"env_key": "AGENT_SHELL_PROFILE", "label": "Shell Profile (strict/project/project_full)", "secret": False, "required": False},
        ],
    },
}


class ConnectionSaveRequest(BaseModel):
    service_id: str
    values: dict[str, str] = Field(default_factory=dict)
    clear_missing: bool = False


class ConnectionTestRequest(BaseModel):
    service_id: str
    values: dict[str, str] = Field(default_factory=dict)
    timeout_seconds: float | None = None


def _mask_secret(value: str) -> str:
    if not value:
        return ""
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}{'*' * (len(value) - 6)}{value[-2:]}"


def _service_effective_values(service_id: str, draft: dict[str, str] | None = None) -> dict[str, str]:
    spec = SERVICE_SPECS[service_id]
    overrides = get_service_overrides(service_id)
    draft = draft or {}
    out: dict[str, str] = {}
    for field in spec["fields"]:
        env_key = field["env_key"]
        if env_key in draft and isinstance(draft[env_key], str):
            out[env_key] = draft[env_key].strip()
            continue
        if env_key in overrides:
            out[env_key] = overrides[env_key]
            continue
        out[env_key] = resolve_env(env_key, default="").strip()

    if service_id == "provider":
        if not out.get("AGENT_PROVIDER"):
            out["AGENT_PROVIDER"] = resolve_env("AGENT_PROVIDER", default="openai_compat").strip() or "openai_compat"
        if not out.get("AGENT_MODEL"):
            out["AGENT_MODEL"] = resolve_env("AGENT_MODEL", default="").strip()
        if not out.get("OPENAI_BASE_URL"):
            out["OPENAI_BASE_URL"] = resolve_env("OPENAI_BASE_URL", default="https://api.openai.com/v1").strip()
        if not out.get("OPENAI_API_KEY"):
            out["OPENAI_API_KEY"] = resolve_env("OPENAI_API_KEY", default="").strip()
        if not out.get("OPENAI_COMPAT_BASE_URL"):
            out["OPENAI_COMPAT_BASE_URL"] = (
                resolve_env("LITELLM_MODEL_BASE_URL", default="").strip()
                or resolve_env("LITELLM_2_MODEL_BASE_URL", default="").strip()
                or "https://api.openai.com/v1"
            )
        if not out.get("OPENAI_COMPAT_API_KEY"):
            out["OPENAI_COMPAT_API_KEY"] = (
                resolve_env("LITELLM_API_KEY", default="").strip()
                or resolve_env("LITELLM_2_API_KEY", default="").strip()
                or resolve_env("OPENAI_API_KEY", default="").strip()
            )
        if not out.get("OPENAI_COMPAT_MODEL"):
            out["OPENAI_COMPAT_MODEL"] = (
                resolve_env("AGENT_MODEL", default="").strip()
                or resolve_env("LITELLM_MODEL_NAME", default="").strip()
                or resolve_env("LITELLM_2_MODEL_NAME", default="").strip()
            )
        if not out.get("AGENT_ENABLE_FALLBACK"):
            out["AGENT_ENABLE_FALLBACK"] = resolve_env("AGENT_ENABLE_FALLBACK", default="true").strip() or "true"
        for env_key in [
            "AGENT_FALLBACK_PROVIDER",
            "AGENT_FALLBACK_BASE_URL",
            "AGENT_FALLBACK_API_KEY",
            "AGENT_FALLBACK_MODEL",
        ]:
            if not out.get(env_key):
                out[env_key] = resolve_env(env_key, default="").strip()
    return out


async def _test_provider(values: dict[str, str], timeout_seconds: float) -> tuple[str, str]:
    provider_kind = values.get("AGENT_PROVIDER", "openai_compat").strip().lower() or "openai_compat"
    if provider_kind == "openai":
        base_url = values.get("OPENAI_BASE_URL", "").rstrip("/")
        api_key = values.get("OPENAI_API_KEY", "")
    else:
        base_url = values.get("OPENAI_COMPAT_BASE_URL", "").rstrip("/")
        api_key = values.get("OPENAI_COMPAT_API_KEY", "")
    if not base_url or not api_key:
        return "degraded", f"Missing provider base URL or API key for provider '{provider_kind}'."

    url = f"{base_url}/models"
    headers = {"Authorization": f"Bearer {api_key}"}
    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout_seconds)) as client:
        resp = await client.get(url, headers=headers)
        if resp.is_success:
            return "healthy", f"HTTP {resp.status_code} from {url}"
        return "error", f"HTTP {resp.status_code} from {url}: {resp.text[:200]}"


async def _test_asr(values: dict[str, str], timeout_seconds: float) -> tuple[str, str]:
    base_url = values.get("ASR_BASE_URL", "").rstrip("/")
    if not base_url:
        return "disabled", "ASR_BASE_URL is empty."
    api_key = values.get("ASR_API_KEY", "")
    headers = build_service_auth_headers(api_key, service_id="asr")
    probe_urls = [
        f"{base_url}/v1/health",
        f"{base_url}/v1/models",
        f"{base_url}/api/health",
    ]
    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout_seconds)) as client:
        last_error = ""
        for url in probe_urls:
            resp = await client.get(url, headers=headers)
            if resp.is_success:
                return "healthy", f"HTTP {resp.status_code} from {url}"
            last_error = f"HTTP {resp.status_code} from {url}: {resp.text[:200]}"
        return "error", last_error or "No ASR endpoint responded successfully."


async def _test_tts(values: dict[str, str], timeout_seconds: float) -> tuple[str, str]:
    base_url = values.get("TTS_BASE_URL", "").rstrip("/")
    if not base_url:
        return "disabled", "TTS_BASE_URL is empty."
    api_key = values.get("TTS_API_KEY", "")
    headers = build_service_auth_headers(api_key, service_id="tts")
    # Chatterbox deployments may not expose /api/health; probe known stable endpoints.
    probe_urls = [
        f"{base_url}/api/health",
        f"{base_url}/api/model-info",
        f"{base_url}/openapi.json",
    ]
    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout_seconds)) as client:
        last_error = ""
        for url in probe_urls:
            resp = await client.get(url, headers=headers)
            if resp.is_success:
                return "healthy", f"HTTP {resp.status_code} from {url}"
            last_error = f"HTTP {resp.status_code} from {url}: {resp.text[:200]}"
        return "error", last_error or "No TTS endpoint responded successfully."


async def _test_redis(values: dict[str, str], timeout_seconds: float) -> tuple[str, str]:
    redis_url = values.get("REDIS_URL", "")
    if not redis_url:
        return "disabled", "REDIS_URL is empty."
    client = redis.from_url(redis_url, decode_responses=True, socket_timeout=timeout_seconds)
    try:
        await client.ping()
        return "healthy", "PING ok"
    finally:
        await client.aclose()


async def _test_mongo(values: dict[str, str], timeout_seconds: float) -> tuple[str, str]:
    uri = values.get("AETHER_MONGO_URI", "")
    if not uri:
        return "disabled", "AETHER_MONGO_URI is empty."
    client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=max(1000, int(timeout_seconds * 1000)))
    try:
        await client.admin.command("ping")
        return "healthy", "ping ok"
    finally:
        client.close()


async def _test_postgres(values: dict[str, str], timeout_seconds: float) -> tuple[str, str]:
    dsn = values.get("POSTGRES_DSN", "")
    if not dsn:
        return "disabled", "POSTGRES_DSN is empty."
    conn = await asyncpg.connect(dsn, timeout=timeout_seconds)
    try:
        await conn.execute("SELECT 1")
        return "healthy", "SELECT 1 ok"
    finally:
        await conn.close()


async def _test_qdrant(values: dict[str, str], timeout_seconds: float) -> tuple[str, str]:
    host = values.get("QDRANT_HOST", "")
    if not host:
        return "disabled", "QDRANT_HOST is empty."
    raw_port = values.get("QDRANT_PORT", "6333").strip() or "6333"
    try:
        port = int(raw_port)
    except Exception:
        return "error", f"Invalid QDRANT_PORT: {raw_port}"
    api_key = values.get("QDRANT_API_KEY", "")
    client = AsyncQdrantClient(host=host, port=port, api_key=api_key or None, timeout=timeout_seconds)
    try:
        await client.get_collections()
        return "healthy", "collections query ok"
    finally:
        await client.close()


async def _test_governance(values: dict[str, str], timeout_seconds: float) -> tuple[str, str]:
    _ = timeout_seconds
    require_plan = values.get("AGENT_REQUIRE_PLAN_FOR_PROJECTS", "true").strip().lower()
    approval_mode = values.get("AGENT_PLAN_APPROVAL_MODE", "manual").strip().lower()
    shell_profile = values.get("AGENT_SHELL_PROFILE", "strict").strip().lower()
    return (
        "healthy",
        f"require_plan={require_plan or 'true'} approval_mode={approval_mode or 'manual'} shell_profile={shell_profile or 'strict'}",
    )


TESTERS = {
    "provider": _test_provider,
    "asr": _test_asr,
    "tts": _test_tts,
    "redis": _test_redis,
    "mongo": _test_mongo,
    "postgres": _test_postgres,
    "qdrant": _test_qdrant,
    "governance": _test_governance,
}


@router.get("/connections")
async def get_connections(request: Request):
    service_payloads: list[dict[str, Any]] = []
    provider = getattr(request.app.state, "provider", provider_metadata())

    for service_id, spec in SERVICE_SPECS.items():
        overrides = get_service_overrides(service_id)
        effective = _service_effective_values(service_id)
        fields: list[dict[str, Any]] = []

        for field in spec["fields"]:
            env_key = field["env_key"]
            secret = bool(field.get("secret"))
            value = effective.get(env_key, "")
            source = "override" if env_key in overrides else ("env" if value else "default")
            fields.append(
                {
                    "env_key": env_key,
                    "label": field["label"],
                    "secret": secret,
                    "required": bool(field.get("required")),
                    "value": "" if secret else value,
                    "display_value": _mask_secret(value) if secret else value,
                    "has_value": bool(value),
                    "source": source,
                }
            )

        status = "unknown"
        details = ""
        if service_id == "provider":
            status = "healthy" if provider.get("configured") else "degraded"
            details = provider.get("detail", "")
        elif service_id == "asr":
            status = "configured" if effective.get("ASR_BASE_URL") else "disabled"
            details = effective.get("ASR_BASE_URL", "")
        elif service_id == "tts":
            status = "configured" if effective.get("TTS_BASE_URL") else "disabled"
            details = effective.get("TTS_BASE_URL", "")
        else:
            status = "configured" if any(v for v in effective.values()) else "disabled"

        service_payloads.append(
            {
                "service_id": service_id,
                "name": spec["name"],
                "description": spec["description"],
                "requires_restart": bool(spec.get("requires_restart")),
                "status": status,
                "details": details,
                "fields": fields,
            }
        )

    return {"services": service_payloads, "secrets": encryption_status()}


@router.post("/connections/test")
async def test_connection(payload: ConnectionTestRequest):
    service_id = payload.service_id
    if service_id not in SERVICE_SPECS:
        raise HTTPException(status_code=400, detail=f"Unknown service_id '{service_id}'")

    timeout_seconds = payload.timeout_seconds or 8.0
    if timeout_seconds <= 0:
        timeout_seconds = 8.0
    values = _service_effective_values(service_id, payload.values)
    tester = TESTERS.get(service_id)
    if not tester:
        raise HTTPException(status_code=400, detail=f"No tester for service '{service_id}'")

    start = time.perf_counter()
    try:
        status, details = await tester(values, timeout_seconds)
        latency_ms = int((time.perf_counter() - start) * 1000)
        return {"service_id": service_id, "status": status, "details": details, "latency_ms": latency_ms}
    except Exception as exc:  # noqa: BLE001
        latency_ms = int((time.perf_counter() - start) * 1000)
        return {"service_id": service_id, "status": "error", "details": str(exc), "latency_ms": latency_ms}


@router.post("/connections/save")
async def save_connection(payload: ConnectionSaveRequest, request: Request):
    service_id = payload.service_id
    if service_id not in SERVICE_SPECS:
        raise HTTPException(status_code=400, detail=f"Unknown service_id '{service_id}'")

    spec = SERVICE_SPECS[service_id]
    allowed_keys = {field["env_key"] for field in spec["fields"]}
    current = get_service_overrides(service_id)
    next_values = {} if payload.clear_missing else dict(current)

    for key, value in payload.values.items():
        if key not in allowed_keys:
            continue
        if value is None:
            continue
        if not isinstance(value, str):
            value = str(value)
        trimmed = value.strip()
        if trimmed:
            next_values[key] = trimmed
        elif key in next_values:
            next_values.pop(key, None)

    if next_values:
        set_service_overrides(service_id, next_values)
    else:
        clear_service_overrides(service_id)

    apply_runtime_overrides_to_env()

    provider_update: dict[str, Any] | None = None
    if service_id == "provider":
        try:
            reset_provider()
            provider_update = provider_metadata()
            request.app.state.provider = provider_update
        except Exception as exc:  # noqa: BLE001
            provider_update = {"configured": False, "detail": str(exc)}

    return {
        "status": "ok",
        "service_id": service_id,
        "requires_restart": bool(spec.get("requires_restart")),
        "saved_keys": sorted(next_values.keys()),
        "provider": provider_update,
    }
