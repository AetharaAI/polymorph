from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable


@dataclass(slots=True)
class LLMUsage:
    input_tokens: int = 0
    output_tokens: int = 0


@dataclass(slots=True)
class LLMContentBlock:
    type: str
    text: str | None = None
    thinking: str | None = None
    name: str | None = None
    id: str | None = None
    input: dict[str, Any] | None = None


@dataclass(slots=True)
class LLMResponse:
    stop_reason: str
    content: list[LLMContentBlock] = field(default_factory=list)
    usage: LLMUsage = field(default_factory=LLMUsage)
    provider_name: str | None = None
    model_name: str | None = None
    fallback_used: bool = False
    notice: str | None = None


class BaseLLMProvider(ABC):
    """Normalized provider interface for the harness."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def model_name(self) -> str:
        raise NotImplementedError

    @property
    def supports_image_prompt_blocks(self) -> bool:
        return False

    @abstractmethod
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
        raise NotImplementedError
