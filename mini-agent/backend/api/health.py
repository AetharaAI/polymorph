import os
import shutil
import socket
import time
from datetime import datetime, timezone

import httpx
import psutil
from fastapi import APIRouter, Request

from backend.agent.providers import provider_metadata, reset_provider
from backend.agent.tools.health_check import run_tool_health_checks
from backend.config import build_service_auth_headers, resolve_env

router = APIRouter()


@router.get("/health")
async def health_check(request: Request):
    tool_health = getattr(request.app.state, "tool_health", None)
    provider = getattr(request.app.state, "provider", None)
    status = "healthy"
    if tool_health and tool_health.get("status") != "healthy":
        status = "degraded"
    if provider and not provider.get("configured", False):
        status = "degraded"

    return {
        "status": status,
        "service": "AetherOps Agentic Harness API",
        "version": "1.0.0",
        "tools": tool_health,
        "provider": provider,
    }


@router.get("/health/diagnostics")
async def diagnostics(request: Request):
    process = psutil.Process(os.getpid())
    vm = psutil.virtual_memory()
    du = shutil.disk_usage("/")
    now = time.time()
    started_at = float(getattr(request.app.state, "started_at", now))

    asr_base_url = resolve_env("ASR_BASE_URL", service_id="asr", default="").strip()
    asr_api_key = resolve_env("ASR_API_KEY", service_id="asr", default="").strip()
    asr_model = resolve_env("ASR_MODEL", service_id="asr", default="auto").strip() or "auto"
    asr_timeout = float(
        resolve_env(
            "ASR_HEALTH_TIMEOUT_SECONDS",
            service_id="asr",
            default=resolve_env("ASR_TIMEOUT_SECONDS", service_id="asr", default="20"),
        )
    )
    asr_enabled = bool(asr_base_url)
    asr_health = {
        "enabled": asr_enabled,
        "configured": asr_enabled,
        "base_url": asr_base_url,
        "model": asr_model,
        "has_api_key": bool(asr_api_key),
        "status": "disabled",
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }

    if asr_enabled:
        probe_urls = [
            f"{asr_base_url.rstrip('/')}/v1/health",
            f"{asr_base_url.rstrip('/')}/v1/models",
            f"{asr_base_url.rstrip('/')}/api/health",
        ]
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(asr_timeout)) as client:
                headers = build_service_auth_headers(asr_api_key, service_id="asr")
                last_status = None
                for probe in probe_urls:
                    resp = await client.get(probe, headers=headers)
                    if resp.is_success:
                        asr_health["status"] = "healthy"
                        asr_health["http_status"] = resp.status_code
                        asr_health["checked_url"] = probe
                        break
                    last_status = (resp.status_code, probe, resp.text[:200])
                else:
                    if last_status:
                        asr_health["status"] = "degraded"
                        asr_health["http_status"] = last_status[0]
                        asr_health["checked_url"] = last_status[1]
                        asr_health["error"] = last_status[2]
        except Exception as exc:  # noqa: BLE001
            asr_health["status"] = "unreachable"
            asr_health["error"] = str(exc)

    tts_base_url = resolve_env("TTS_BASE_URL", service_id="tts", default="").strip()
    tts_api_key = resolve_env("TTS_API_KEY", service_id="tts", default="").strip()
    tts_model = resolve_env("TTS_MODEL", service_id="tts", default="chatterbox").strip() or "chatterbox"
    tts_timeout = float(resolve_env("TTS_TIMEOUT_SECONDS", service_id="tts", default="20"))
    tts_enabled = bool(tts_base_url)
    tts_health = {
        "enabled": tts_enabled,
        "configured": tts_enabled,
        "base_url": tts_base_url,
        "model": tts_model,
        "has_api_key": bool(tts_api_key),
        "status": "disabled",
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }

    if tts_enabled:
        probe_urls = [
            f"{tts_base_url.rstrip('/')}/api/health",
            f"{tts_base_url.rstrip('/')}/api/model-info",
            f"{tts_base_url.rstrip('/')}/openapi.json",
        ]
        headers = build_service_auth_headers(tts_api_key, service_id="tts")
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(tts_timeout)) as client:
                last_status = None
                for probe in probe_urls:
                    resp = await client.get(probe, headers=headers)
                    if resp.is_success:
                        tts_health["status"] = "healthy"
                        tts_health["http_status"] = resp.status_code
                        tts_health["checked_url"] = probe
                        break
                    last_status = (resp.status_code, probe, resp.text[:200])
                else:
                    if last_status:
                        tts_health["status"] = "degraded"
                        tts_health["http_status"] = last_status[0]
                        tts_health["checked_url"] = last_status[1]
                        tts_health["error"] = last_status[2]
        except Exception as exc:  # noqa: BLE001
            tts_health["status"] = "unreachable"
            tts_health["error"] = str(exc)

    return {
        "status": "healthy",
        "service": "AetherOps Agentic Harness API",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime_seconds": max(0, int(now - started_at)),
        "process": {
            "pid": process.pid,
            "rss_bytes": process.memory_info().rss,
            "cpu_percent": process.cpu_percent(interval=0.0),
            "threads": process.num_threads(),
        },
        "system": {
            "hostname": socket.gethostname(),
            "memory_total_bytes": vm.total,
            "memory_used_bytes": vm.used,
            "memory_available_bytes": vm.available,
            "memory_percent": vm.percent,
            "disk_total_bytes": du.total,
            "disk_used_bytes": du.used,
            "disk_free_bytes": du.free,
            "load_average": os.getloadavg() if hasattr(os, "getloadavg") else None,
        },
        "tools": getattr(request.app.state, "tool_health", None),
        "provider": getattr(request.app.state, "provider", None),
        "services": {
            "asr": asr_health,
            "tts": tts_health,
        },
    }


@router.post("/health/tools/refresh")
async def refresh_tool_health(request: Request):
    reset_provider()
    tool_health = await run_tool_health_checks()
    request.app.state.tool_health = tool_health
    request.app.state.provider = provider_metadata()
    return {"status": "ok", "tools": tool_health, "provider": request.app.state.provider}
