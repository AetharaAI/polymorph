from __future__ import annotations

import os

from backend.agent.providers.openai_compat_provider import OpenAICompatProvider


class OpenAIProvider(OpenAICompatProvider):
    """Direct OpenAI adapter with OpenAI-specific defaults and contract handling."""

    def __init__(
        self,
        *,
        base_url: str | None = None,
        api_key: str | None = None,
        model_name: str | None = None,
        provider_name: str = "openai",
    ):
        super().__init__(
            base_url=base_url or os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1",
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            model_name=model_name or os.getenv("OPENAI_MODEL") or os.getenv("AGENT_MODEL"),
            provider_name=provider_name,
            direct_openai=True,
        )
