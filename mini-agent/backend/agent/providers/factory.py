from __future__ import annotations

import os
from typing import Any

from backend.agent.providers.anthropic_provider import AnthropicProvider
from backend.agent.providers.base import BaseLLMProvider
from backend.agent.providers.failover_provider import FailoverProvider
from backend.agent.providers.openai_compat_provider import OpenAICompatProvider
from backend.agent.providers.openai_provider import OpenAIProvider
from backend.config.runtime import get_service_overrides

_PROVIDER: BaseLLMProvider | None = None


def _norm(value: str | None) -> str:
    return (value or "").strip()


def _provider_target(provider: BaseLLMProvider) -> tuple[str, str]:
    if isinstance(provider, OpenAICompatProvider):
        return (_norm(getattr(provider, "_base_url", "")), provider.model_name)
    return (provider.provider_name, provider.model_name)


def _build_single_provider(
    provider_name: str,
    *,
    base_url: str | None = None,
    api_key: str | None = None,
    model_name: str | None = None,
    label: str | None = None,
) -> BaseLLMProvider:
    normalized = _norm(provider_name).lower()
    if normalized == "openai":
        return OpenAIProvider(
            base_url=base_url,
            api_key=api_key,
            model_name=model_name,
            provider_name=label or "openai",
        )
    if normalized in {"openai_compat", "openai-compatible"}:
        return OpenAICompatProvider(
            base_url=base_url,
            api_key=api_key,
            model_name=model_name,
            provider_name=label or "openai_compat",
        )
    if normalized == "anthropic":
        return AnthropicProvider(
            api_key=api_key or None,
            base_url=base_url or None,
            model_name=model_name or None,
            provider_name=label or "anthropic",
        )
    raise ValueError(f"Unsupported AGENT_PROVIDER '{provider_name}'")


def _explicit_fallback_provider() -> BaseLLMProvider | None:
    provider_name = _norm(os.getenv("AGENT_FALLBACK_PROVIDER"))
    base_url = _norm(os.getenv("AGENT_FALLBACK_BASE_URL"))
    api_key = _norm(os.getenv("AGENT_FALLBACK_API_KEY"))
    model_name = _norm(os.getenv("AGENT_FALLBACK_MODEL"))
    if not provider_name:
        return None
    if provider_name.lower() in {"openai", "openai_compat", "openai-compatible"} and not (api_key and model_name):
        return None
    try:
        return _build_single_provider(
            provider_name,
            base_url=base_url or None,
            api_key=api_key or None,
            model_name=model_name or None,
            label=f"{provider_name}_fallback",
        )
    except Exception:
        return None


def _litellm_fallback_providers() -> list[BaseLLMProvider]:
    fallbacks: list[BaseLLMProvider] = []
    pairs = [
        (
            _norm(os.getenv("LITELLM_MODEL_BASE_URL")),
            _norm(os.getenv("LITELLM_API_KEY")),
            _norm(os.getenv("LITELLM_MODEL_NAME")),
            "litellm_primary_fallback",
        ),
        (
            _norm(os.getenv("LITELLM_2_MODEL_BASE_URL")),
            _norm(os.getenv("LITELLM_2_API_KEY")),
            _norm(os.getenv("LITELLM_2_MODEL_NAME")),
            "litellm_secondary_fallback",
        ),
    ]
    for base_url, api_key, model_name, label in pairs:
        if not (base_url and api_key and model_name):
            continue
        try:
            fallbacks.append(
                OpenAICompatProvider(
                    base_url=base_url,
                    api_key=api_key,
                    model_name=model_name,
                    provider_name=label,
                )
            )
        except Exception:
            continue
    return fallbacks


def _build_provider_chain(primary: BaseLLMProvider) -> BaseLLMProvider:
    enable_fallback = _norm(os.getenv("AGENT_ENABLE_FALLBACK", "true")).lower() in {"1", "true", "yes", "on"}
    if not enable_fallback:
        return primary

    candidates: list[BaseLLMProvider] = []
    explicit = _explicit_fallback_provider()
    if explicit is not None:
        candidates.append(explicit)
    candidates.extend(_litellm_fallback_providers())

    deduped: list[BaseLLMProvider] = []
    seen = {_provider_target(primary)}
    for candidate in candidates:
        target = _provider_target(candidate)
        if target in seen:
            continue
        seen.add(target)
        deduped.append(candidate)

    if not deduped:
        return primary
    return FailoverProvider([primary, *deduped])


def get_provider() -> BaseLLMProvider:
    global _PROVIDER
    if _PROVIDER is not None:
        return _PROVIDER

    provider_name = _norm(os.getenv("AGENT_PROVIDER", "openai_compat")).lower()
    primary = _build_single_provider(provider_name)
    _PROVIDER = _build_provider_chain(primary)
    return _PROVIDER


def get_multimodal_audio_provider() -> BaseLLMProvider | None:
    provider_name = _norm(os.getenv("DIRECT_AUDIO_PROVIDER")) or "openai_compat"
    base_url = (
        _norm(os.getenv("DIRECT_AUDIO_BASE_URL"))
        or _norm(os.getenv("PHI_4_INSTRUCT_MODEL_BASE_URL"))
        or _norm(os.getenv("OPENAI_COMPAT_BASE_URL"))
    )
    api_key = (
        _norm(os.getenv("DIRECT_AUDIO_API_KEY"))
        or _norm(os.getenv("PHI_4_INSTRUCT_API_KEY"))
        or _norm(os.getenv("OPENAI_COMPAT_API_KEY"))
        or _norm(os.getenv("LITELLM_API_KEY"))
    )
    model_name = (
        _norm(os.getenv("DIRECT_AUDIO_MODEL"))
        or _norm(os.getenv("PHI_4_INSTRUCT_MODEL_NAME"))
        or "phi-4-instruct"
    )
    if not (base_url and api_key and model_name):
        return None
    return _build_single_provider(
        provider_name,
        base_url=base_url,
        api_key=api_key,
        model_name=model_name,
        label="multimodal_audio",
    )


def reset_provider() -> None:
    global _PROVIDER
    _PROVIDER = None


def validate_provider_config() -> tuple[bool, str]:
    provider_name = _norm(os.getenv("AGENT_PROVIDER", "openai_compat")).lower()

    try:
        provider = get_provider()
        return True, f"provider={provider.provider_name} model={provider.model_name}"
    except Exception as exc:
        if provider_name == "anthropic":
            return False, "Missing Anthropic-compatible credentials (PROVIDER_ANTHROPIC_API_KEY)"
        if provider_name == "openai":
            return False, "Missing OpenAI credentials or invalid OpenAI configuration (OPENAI_API_KEY / OPENAI_MODEL)"
        if provider_name in {"openai_compat", "openai-compatible"}:
            return False, "Missing OpenAI-compatible credentials or router config (OPENAI_COMPAT_API_KEY / OPENAI_COMPAT_BASE_URL / OPENAI_COMPAT_MODEL)"
        return False, f"Invalid provider configuration: {exc}"


def provider_metadata() -> dict[str, Any]:
    requested_provider = _norm(os.getenv("AGENT_PROVIDER", "openai_compat")).lower()
    requested_model = _norm(os.getenv("AGENT_MODEL", "agent-default"))
    runtime_overrides = get_service_overrides("provider")
    ok, detail = validate_provider_config()
    actual_provider = requested_provider
    actual_model = requested_model
    fallbacks: list[dict[str, str]] = []
    if ok:
        try:
            provider = get_provider()
            actual_provider = provider.provider_name
            actual_model = provider.model_name
            detail = f"provider={provider.provider_name} model={provider.model_name}"
            if isinstance(provider, FailoverProvider):
                fallbacks = provider.fallbacks
        except Exception:
            pass
    return {
        "configured": ok,
        "provider": actual_provider,
        "model": actual_model,
        "requested": {
            "provider": requested_provider,
            "model": requested_model,
        },
        "actual": {
            "provider": actual_provider,
            "model": actual_model,
        },
        "runtime_overrides": {
            "present": bool(runtime_overrides),
            "keys": sorted(runtime_overrides.keys()),
        },
        "detail": detail,
        "fallbacks": fallbacks,
    }
