from __future__ import annotations

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

    async def generate(
        self,
        *,
        system: str,
        tools: list[dict[str, Any]],
        messages: list[dict[str, Any]],
        max_tokens: int,
        temperature: float,
        on_stream_event: Callable[[LLMContentBlock], Awaitable[None]] | None = None,
    ) -> LLMResponse:
        failures: list[str] = []
        primary = self._providers[0]

        for idx, provider in enumerate(self._providers):
            try:
                response = await provider.generate(
                    system=system,
                    tools=tools,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    on_stream_event=on_stream_event,
                )
                if not self._has_payload(response):
                    raise RuntimeError("provider returned empty response payload")

                response.provider_name = response.provider_name or provider.provider_name
                response.model_name = response.model_name or provider.model_name

                if idx > 0:
                    response.fallback_used = True
                    failure_note = failures[-1] if failures else "primary provider failed"
                    response.notice = (
                        f"[Provider notice] Primary provider {primary.provider_name}:{primary.model_name} failed. "
                        f"Fallback response served by {provider.provider_name}:{provider.model_name}. "
                        f"Last primary error: {failure_note}"
                    )
                return response
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{provider.provider_name}:{provider.model_name} -> {type(exc).__name__}: {exc}")
                continue

        joined = " | ".join(failures[:6]) if failures else "unknown provider failure"
        raise RuntimeError(f"All configured providers failed. {joined}")
