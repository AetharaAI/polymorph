from __future__ import annotations

import os

from backend.config.runtime import resolve_env


UNIFIED_OPENAI_COMPAT_BASE_URL = "https://api.aetherpro.tech/v1"


def _first_non_empty(*values: str | None) -> str:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def resolve_unified_gateway_base(
    *,
    explicit: str | None = None,
    service_id: str | None = None,
) -> str:
    return _first_non_empty(
        explicit,
        resolve_env("OPENAI_COMPAT_BASE_URL", service_id=service_id, default=""),
        os.getenv("OPENAI_COMPAT_BASE_URL"),
        os.getenv("LITELLM_MODEL_BASE_URL"),
        UNIFIED_OPENAI_COMPAT_BASE_URL,
    )


def resolve_openai_compat_api_key(
    *,
    explicit: str | None = None,
    service_id: str | None = None,
) -> str:
    return _first_non_empty(
        explicit,
        resolve_env("OPENAI_COMPAT_API_KEY", service_id=service_id, default=""),
        os.getenv("OPENAI_COMPAT_API_KEY"),
        os.getenv("LITELLM_API_KEY"),
        resolve_env("OPENAI_API_KEY", service_id=service_id, default=""),
        os.getenv("OPENAI_API_KEY"),
    )
