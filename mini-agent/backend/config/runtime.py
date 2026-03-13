from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet, InvalidToken

RUNTIME_CONFIG_PATH = Path(
    os.getenv("RUNTIME_CONFIG_PATH", "./replays/runtime_config.json")
).resolve()
RUNTIME_CONFIG_KEY_PATH = Path(
    os.getenv("RUNTIME_CONFIG_KEY_PATH", "./replays/runtime_config.key")
).resolve()
RUNTIME_CONFIG_KEY_ENV = os.getenv("RUNTIME_CONFIG_ENCRYPTION_KEY", "").strip()
_ENC_PREFIX = "enc::"

_LOCK = threading.Lock()
_FERNET: Fernet | None = None
_FERNET_SOURCE: str = "none"
_APPLIED_KEYS: set[str] = set()
_BASE_ENV: dict[str, str | None] = {}
_EMPTY_AUTH_SENTINELS = {"empty", "none", "null", "optional"}


def _default_config() -> dict[str, Any]:
    return {
        "services": {},
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


def _get_fernet() -> Fernet | None:
    global _FERNET, _FERNET_SOURCE
    if _FERNET is not None:
        return _FERNET

    key: bytes | None = None
    if RUNTIME_CONFIG_KEY_ENV:
        key = RUNTIME_CONFIG_KEY_ENV.encode("utf-8")
        _FERNET_SOURCE = "env"
    else:
        if RUNTIME_CONFIG_KEY_PATH.exists():
            key = RUNTIME_CONFIG_KEY_PATH.read_text(encoding="utf-8").strip().encode("utf-8")
            _FERNET_SOURCE = "file"
        else:
            RUNTIME_CONFIG_KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
            generated = Fernet.generate_key()
            RUNTIME_CONFIG_KEY_PATH.write_text(generated.decode("utf-8"), encoding="utf-8")
            try:
                os.chmod(RUNTIME_CONFIG_KEY_PATH, 0o600)
            except Exception:
                pass
            key = generated
            _FERNET_SOURCE = "generated_file"

    if not key:
        _FERNET_SOURCE = "none"
        return None

    try:
        _FERNET = Fernet(key)
    except Exception:
        _FERNET = None
        _FERNET_SOURCE = "invalid"
    return _FERNET


def encryption_status() -> dict[str, Any]:
    fernet = _get_fernet()
    return {
        "enabled": bool(fernet),
        "source": _FERNET_SOURCE,
        "key_path": str(RUNTIME_CONFIG_KEY_PATH),
    }


def _encrypt_value(raw: str) -> str:
    fernet = _get_fernet()
    if not fernet:
        return raw
    token = fernet.encrypt(raw.encode("utf-8")).decode("utf-8")
    return f"{_ENC_PREFIX}{token}"


def _decrypt_value(raw: str) -> str:
    if not isinstance(raw, str):
        return ""
    if not raw.startswith(_ENC_PREFIX):
        return raw

    token = raw[len(_ENC_PREFIX):]
    fernet = _get_fernet()
    if not fernet:
        return ""
    try:
        return fernet.decrypt(token.encode("utf-8")).decode("utf-8")
    except (InvalidToken, ValueError):
        return ""
    except Exception:
        return ""


def load_runtime_config() -> dict[str, Any]:
    with _LOCK:
        if not RUNTIME_CONFIG_PATH.exists():
            return _default_config()
        try:
            payload = json.loads(RUNTIME_CONFIG_PATH.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                payload.setdefault("services", {})
                return payload
        except Exception:
            pass
        return _default_config()


def save_runtime_config(config: dict[str, Any]) -> None:
    with _LOCK:
        RUNTIME_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        config["updated_at"] = datetime.now(timezone.utc).isoformat()
        tmp_path = RUNTIME_CONFIG_PATH.with_suffix(".tmp")
        tmp_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp_path.replace(RUNTIME_CONFIG_PATH)


def get_service_overrides(service_id: str) -> dict[str, str]:
    config = load_runtime_config()
    services = config.get("services", {})
    service = services.get(service_id, {})
    if not isinstance(service, dict):
        return {}
    out: dict[str, str] = {}
    for key, value in service.items():
        if isinstance(key, str) and isinstance(value, str):
            out[key] = _decrypt_value(value)
    return out


def set_service_overrides(service_id: str, values: dict[str, str]) -> dict[str, Any]:
    config = load_runtime_config()
    services = config.setdefault("services", {})
    sanitized: dict[str, str] = {}
    for key, value in values.items():
        if not isinstance(key, str):
            continue
        if value is None:
            continue
        if not isinstance(value, str):
            value = str(value)
        stripped = value.strip()
        if not stripped:
            continue
        sanitized[key] = _encrypt_value(stripped)
    services[service_id] = sanitized
    save_runtime_config(config)
    return config


def clear_service_overrides(service_id: str) -> dict[str, Any]:
    config = load_runtime_config()
    services = config.setdefault("services", {})
    services.pop(service_id, None)
    save_runtime_config(config)
    return config


def resolve_env(env_key: str, service_id: str | None = None, default: str = "") -> str:
    if service_id:
        overrides = get_service_overrides(service_id)
        if env_key in overrides:
            return overrides[env_key]
    return os.getenv(env_key, default)


def build_service_auth_headers(
    api_key: str,
    *,
    service_id: str | None = None,
    default_header: str = "Authorization",
) -> dict[str, str]:
    token = (api_key or "").strip()
    if not token or token.lower() in _EMPTY_AUTH_SENTINELS:
        return {}

    prefix = service_id.upper() if service_id else ""
    service_header_key = f"{prefix}_API_KEY_HEADER" if prefix else ""
    service_prefix_key = f"{prefix}_API_KEY_PREFIX" if prefix else ""

    header_name = (
        resolve_env(service_header_key, service_id=service_id, default="").strip()
        if service_header_key
        else ""
    )
    if not header_name:
        header_name = resolve_env("API_KEY_HEADER", service_id=service_id, default=default_header).strip() or default_header

    token_prefix = (
        resolve_env(service_prefix_key, service_id=service_id, default="").strip()
        if service_prefix_key
        else ""
    )
    if not token_prefix:
        token_prefix = resolve_env("API_KEY_PREFIX", service_id=service_id, default="").strip()
    if not token_prefix and header_name.lower() == "authorization":
        token_prefix = "Bearer"

    header_value = f"{token_prefix} {token}".strip() if token_prefix else token
    return {header_name: header_value}


def apply_runtime_overrides_to_env() -> None:
    global _APPLIED_KEYS
    config = load_runtime_config()
    services = config.get("services", {})
    if not isinstance(services, dict):
        return

    resolved_values: dict[str, str] = {}
    for _, values in services.items():
        if not isinstance(values, dict):
            continue
        for key, value in values.items():
            if not (isinstance(key, str) and isinstance(value, str)):
                continue
            plain = _decrypt_value(value).strip()
            if plain:
                resolved_values[key] = plain

    # Restore keys that were previously overridden but are no longer present.
    for key in list(_APPLIED_KEYS):
        if key in resolved_values:
            continue
        if key in _BASE_ENV and _BASE_ENV[key] is not None:
            os.environ[key] = _BASE_ENV[key] or ""
        else:
            os.environ.pop(key, None)

    # Apply fresh runtime overrides.
    for key, value in resolved_values.items():
        if key not in _BASE_ENV:
            _BASE_ENV[key] = os.environ.get(key)
        os.environ[key] = value

    _APPLIED_KEYS = set(resolved_values.keys())
