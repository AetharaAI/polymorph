import json
import os
from datetime import datetime, timezone
from typing import Any

import httpx


def _base_url() -> str:
    raw = (os.getenv("FIRECRAWL_BASE_URL", "https://api.firecrawl.dev") or "").strip()
    return raw.rstrip("/")


def _api_key() -> str:
    return (os.getenv("FIRECRAWL_API_KEY", "") or "").strip()


def _origin() -> str | None:
    value = (os.getenv("FIRECRAWL_ORIGIN", "") or "").strip()
    return value or None


def _timeout_seconds() -> float:
    raw = (os.getenv("FIRECRAWL_TIMEOUT_SECONDS", "60") or "").strip()
    try:
        return max(5.0, min(float(raw), 300.0))
    except Exception:
        return 60.0


def is_configured() -> bool:
    return bool(_api_key())


def _headers() -> dict[str, str]:
    key = _api_key()
    headers = {
        "Content-Type": "application/json",
    }
    if key:
        headers["Authorization"] = f"Bearer {key}"
    return headers


def _truncate_text(value: Any, max_chars: int) -> str:
    text = str(value or "")
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + f"\n...[truncated {len(text) - max_chars} chars]"


def _extract_scrape_id(data: dict[str, Any]) -> str:
    if not isinstance(data, dict):
        return ""
    for key in ("scrapeId", "scrape_id", "id"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    metadata = data.get("metadata")
    if isinstance(metadata, dict):
        for key in ("scrapeId", "scrape_id", "id"):
            value = metadata.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return ""


async def firecrawl_scrape(
    *,
    url: str,
    max_chars: int = 120000,
    formats: list[str] | None = None,
    only_main_content: bool | None = None,
    mobile: bool | None = None,
    wait_for: int | None = None,
    timeout_seconds: int | None = None,
) -> str:
    target = (url or "").strip()
    if not target:
        return "Error: firecrawl_scrape requires a non-empty url."
    if not is_configured():
        return "Error: FIRECRAWL_API_KEY is not configured."

    max_chars = max(2000, min(int(max_chars), 500000))
    request_timeout = float(timeout_seconds) if timeout_seconds is not None else _timeout_seconds()
    request_timeout = max(5.0, min(request_timeout, 300.0))

    payload: dict[str, Any] = {
        "url": target,
    }
    if formats:
        payload["formats"] = formats
    if only_main_content is not None:
        payload["onlyMainContent"] = bool(only_main_content)
    if mobile is not None:
        payload["mobile"] = bool(mobile)
    if wait_for is not None:
        payload["waitFor"] = int(wait_for)
    origin = _origin()
    if origin:
        payload["origin"] = origin

    endpoint = f"{_base_url()}/v2/scrape"
    timeout = httpx.Timeout(timeout=request_timeout, connect=15.0, read=request_timeout)
    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            resp = await client.post(endpoint, headers=_headers(), json=payload)
            resp.raise_for_status()
            raw = resp.json()
    except Exception as exc:
        return f"Error: firecrawl_scrape failed: {exc}"

    data = raw.get("data") if isinstance(raw, dict) else None
    if not isinstance(data, dict):
        data = {}

    markdown = data.get("markdown")
    if not isinstance(markdown, str):
        markdown = ""
    html = data.get("html")
    if not isinstance(html, str):
        html = ""

    text_blob = markdown or html or json.dumps(data, ensure_ascii=False)
    result = {
        "provider": "firecrawl",
        "url": target,
        "endpoint": endpoint,
        "success": bool(raw.get("success", True)) if isinstance(raw, dict) else True,
        "scrape_id": _extract_scrape_id(data),
        "data": data,
        "text_excerpt": _truncate_text(text_blob, max_chars),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    return json.dumps(result, indent=2)


async def firecrawl_interact(
    *,
    scrape_id: str,
    prompt: str | None = None,
    code: str | None = None,
    language: str | None = None,
    timeout: int | None = None,
) -> str:
    sid = (scrape_id or "").strip()
    if not sid:
        return "Error: firecrawl_interact requires 'scrape_id'."
    if not is_configured():
        return "Error: FIRECRAWL_API_KEY is not configured."

    prompt_text = (prompt or "").strip()
    code_text = (code or "").strip()
    if not prompt_text and not code_text:
        return "Error: firecrawl_interact requires at least one of 'prompt' or 'code'."

    payload: dict[str, Any] = {}
    if prompt_text:
        payload["prompt"] = prompt_text
    if code_text:
        payload["code"] = code_text
    if language:
        payload["language"] = str(language).strip()
    if timeout is not None:
        payload["timeout"] = int(timeout)
    origin = _origin()
    if origin:
        payload["origin"] = origin

    endpoint = f"{_base_url()}/v2/scrape/{sid}/interact"
    request_timeout = _timeout_seconds()
    timeout_cfg = httpx.Timeout(timeout=request_timeout, connect=15.0, read=request_timeout)
    try:
        async with httpx.AsyncClient(timeout=timeout_cfg, follow_redirects=True) as client:
            resp = await client.post(endpoint, headers=_headers(), json=payload)
            resp.raise_for_status()
            raw = resp.json()
    except Exception as exc:
        return f"Error: firecrawl_interact failed: {exc}"

    result = {
        "provider": "firecrawl",
        "endpoint": endpoint,
        "scrape_id": sid,
        "success": bool(raw.get("success", True)) if isinstance(raw, dict) else True,
        "output": raw.get("output") if isinstance(raw, dict) else None,
        "result": raw.get("result") if isinstance(raw, dict) else None,
        "stdout": raw.get("stdout") if isinstance(raw, dict) else None,
        "stderr": raw.get("stderr") if isinstance(raw, dict) else None,
        "live_view_url": raw.get("liveViewUrl") if isinstance(raw, dict) else None,
        "interactive_live_view_url": raw.get("interactiveLiveViewUrl") if isinstance(raw, dict) else None,
        "exit_code": raw.get("exitCode") if isinstance(raw, dict) else None,
        "raw": raw,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    return json.dumps(result, indent=2)

