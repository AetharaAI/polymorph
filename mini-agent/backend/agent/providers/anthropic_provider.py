from __future__ import annotations

import os
import asyncio
from typing import Any, Awaitable, Callable

import anthropic

from backend.agent.providers.base import BaseLLMProvider, LLMContentBlock, LLMResponse, LLMUsage


class AnthropicProvider(BaseLLMProvider):
    """Anthropic SDK provider (supports Anthropic and compatible gateways)."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        model_name: str | None = None,
        provider_name: str = "anthropic",
    ):
        api_key = api_key or os.getenv("PROVIDER_ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Missing PROVIDER_ANTHROPIC_API_KEY")

        self._provider_name = provider_name
        self._model_name = (
            model_name
            or os.getenv("PROVIDER_ANTHROPIC_MODEL")
            or os.getenv("AGENT_MODEL", "claude-3-5-sonnet-latest")
        )
        self._client = anthropic.Anthropic(
            api_key=api_key,
            base_url=base_url or os.getenv("PROVIDER_ANTHROPIC_BASE_URL", "https://api.anthropic.com"),
        )

    @property
    def provider_name(self) -> str:
        return self._provider_name

    @property
    def model_name(self) -> str:
        return self._model_name

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
        response = await asyncio.to_thread(
            self._client.messages.create,
            model=self._model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            tools=tools,
            messages=messages,
        )

        usage = LLMUsage(
            input_tokens=int(getattr(response.usage, "input_tokens", 0) or 0),
            output_tokens=int(getattr(response.usage, "output_tokens", 0) or 0),
        )

        content: list[LLMContentBlock] = []
        for block in response.content:
            block_type = getattr(block, "type", "text")
            if block_type == "thinking":
                content.append(
                    LLMContentBlock(type="thinking", thinking=getattr(block, "thinking", "") or "")
                )
            elif block_type == "text":
                content.append(LLMContentBlock(type="text", text=getattr(block, "text", "") or ""))
            elif block_type == "tool_use":
                content.append(
                    LLMContentBlock(
                        type="tool_use",
                        id=getattr(block, "id", "") or "",
                        name=getattr(block, "name", "") or "",
                        input=getattr(block, "input", {}) or {},
                    )
                )
            else:
                # Preserve unknown blocks as text for visibility.
                content.append(LLMContentBlock(type="text", text=str(block)))

        stop_reason = getattr(response, "stop_reason", "end_turn") or "end_turn"
        return LLMResponse(
            stop_reason=stop_reason,
            content=content,
            usage=usage,
            provider_name=self.provider_name,
            model_name=self.model_name,
        )
