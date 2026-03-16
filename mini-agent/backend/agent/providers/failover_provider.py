from __future__ import annotations

import json
from typing import Any, Awaitable, Callable

from backend.agent.providers.base import BaseLLMProvider, LLMContentBlock, LLMResponse


class FailoverProvider(BaseLLMProvider):
    """Try providers in order and degrade gracefully before returning no response."""

    def __init__(self, providers: list[BaseLLMProvider]):
        if not providers:
            raise ValueError("FailoverProvider requires at least one provider")
        self._providers = providers

    @property
    def provider_name(self) -> str:
        return f"{self._providers[0].provider_name}+failover"

    @property
    def model_name(self) -> str:
        return self._providers[0].model_name

    @property
    def supports_image_prompt_blocks(self) -> bool:
        return any(getattr(provider, "supports_image_prompt_blocks", False) for provider in self._providers)

    @property
    def fallbacks(self) -> list[dict[str, str]]:
        return [
            {"provider": provider.provider_name, "model": provider.model_name}
            for provider in self._providers[1:]
        ]

    def _has_payload(self, response: LLMResponse) -> bool:
        if response.content:
            return True
        return False

    def _is_context_window_error(self, exc: Exception) -> bool:
        message = str(exc or "").lower()
        if not message:
            return False
        return (
            "contextwindowexceeded" in message
            or "maximum context length" in message
            or "input tokens" in message
            or "requested output tokens" in message
        )

    async def generate(
        self,
        *,
        system: str,
        tools: list[dict[str, Any]],
        messages: list[dict[str, Any]],
        max_tokens: int,
        temperature: float,
        enable_thinking: bool | None = None,
        on_stream_event: Callable[[LLMContentBlock], Awaitable[None]] | None = None,
    ) -> LLMResponse:
        failures: list[str] = []
        primary = self._providers[0]

        for idx, provider in enumerate(self._providers):
            print(
                "[ProviderFailover] "
                + json.dumps(
                    {
                        "event": "attempt_start",
                        "attempt": idx + 1,
                        "provider": provider.provider_name,
                        "model": provider.model_name,
                        "lane": "primary" if idx == 0 else "fallback",
                    },
                    ensure_ascii=False,
                )
            )
            try:
                response = await provider.generate(
                    system=system,
                    tools=tools,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    enable_thinking=enable_thinking,
                    on_stream_event=on_stream_event,
                )
                if not self._has_payload(response):
                    raise RuntimeError("provider returned empty response payload")

                response.provider_name = response.provider_name or provider.provider_name
                response.model_name = response.model_name or provider.model_name

                if idx > 0:
                    print(
                        "[ProviderFailover] "
                        + json.dumps(
                            {
                                "event": "fallback_served",
                                "attempt": idx + 1,
                                "primary_provider": primary.provider_name,
                                "primary_model": primary.model_name,
                                "fallback_provider": provider.provider_name,
                                "fallback_model": provider.model_name,
                            },
                            ensure_ascii=False,
                        )
                    )
                    response.fallback_used = True
                    failure_note = failures[-1] if failures else "primary provider failed"
                    response.notice = (
                        f"[Provider notice] Primary provider {primary.provider_name}:{primary.model_name} failed. "
                        f"Fallback response served by {provider.provider_name}:{provider.model_name}. "
                        f"Last primary error: {failure_note}"
                    )
                return response
            except Exception as exc:  # noqa: BLE001
                if self._is_context_window_error(exc):
                    provider_lane = "Primary provider" if idx == 0 else f"Fallback provider #{idx}"
                    raise RuntimeError(
                        f"{provider_lane} {provider.provider_name}:{provider.model_name} rejected the request due to context-window limits. {exc}"
                    ) from exc
                print(
                    "[ProviderFailover] "
                    + json.dumps(
                        {
                            "event": "attempt_failed",
                            "attempt": idx + 1,
                            "provider": provider.provider_name,
                            "model": provider.model_name,
                            "error_type": type(exc).__name__,
                            "error": str(exc)[:600],
                        },
                        ensure_ascii=False,
                    )
                )
                failures.append(f"{provider.provider_name}:{provider.model_name} -> {type(exc).__name__}: {exc}")
                continue

        joined = " | ".join(failures[:6]) if failures else "unknown provider failure"
        raise RuntimeError(f"All configured providers failed. {joined}")
