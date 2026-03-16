from __future__ import annotations

import json
import os
import re
from typing import Any, Awaitable, Callable

AUDIO_SUPPORT_ERROR_HINTS = (
    "please install vllm[audio]",
    "audio support",
    "input_audio",
    "audio_url",
)

import httpx

from backend.agent.providers.base import BaseLLMProvider, LLMContentBlock, LLMResponse, LLMUsage
from backend.config.gateway import (
    resolve_openai_compat_api_key,
    resolve_unified_gateway_base,
)


def _env_optional_float(name: str) -> float | None:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return None
    try:
        return float(raw)
    except Exception:
        return None


def _env_optional_int(name: str) -> int | None:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return None
    try:
        return int(raw)
    except Exception:
        return None


def _env_optional_bool(name: str) -> bool | None:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return None
    lowered = raw.strip().lower()
    if lowered in {"1", "true", "yes", "on"}:
        return True
    if lowered in {"0", "false", "no", "off"}:
        return False
    return None


def _env_optional_json_dict(name: str) -> dict[str, Any] | None:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return None
    try:
        value = json.loads(raw)
        if isinstance(value, dict):
            return value
    except Exception:
        return None
    return None


class OpenAICompatProvider(BaseLLMProvider):
    """Provider for OpenAI-compatible /v1/chat/completions APIs."""

    def __init__(
        self,
        *,
        base_url: str | None = None,
        api_key: str | None = None,
        model_name: str | None = None,
        profile: str | None = None,
        provider_name: str = "openai_compat",
        direct_openai: bool | None = None,
    ):
        _ = profile
        self._provider_name = provider_name

        primary_model = os.getenv("LITELLM_MODEL_NAME")

        self._base_url = resolve_unified_gateway_base(
            explicit=base_url or os.getenv("OPENAI_COMPAT_BASE_URL") or os.getenv("LITELLM_MODEL_BASE_URL"),
        ).rstrip("/")
        self._api_key = resolve_openai_compat_api_key(
            explicit=api_key,
        )
        if not self._api_key:
            raise ValueError("Missing OPENAI_COMPAT_API_KEY/OPENAI_API_KEY or LiteLLM API key")

        self._model_name = (
            model_name
            or os.getenv("AGENT_MODEL")
            or os.getenv("OPENAI_COMPAT_MODEL")
            or primary_model
            or "gpt-4o-mini"
        )
        self._direct_openai_override = direct_openai
        self._timeout = float(os.getenv("OPENAI_COMPAT_TIMEOUT_SECONDS", "420"))
        self._connect_timeout = float(os.getenv("OPENAI_COMPAT_CONNECT_TIMEOUT_SECONDS", "20"))
        self._read_timeout = float(os.getenv("OPENAI_COMPAT_READ_TIMEOUT_SECONDS", str(self._timeout)))
        self._write_timeout = float(os.getenv("OPENAI_COMPAT_WRITE_TIMEOUT_SECONDS", "30"))
        self._max_retries = max(0, int(os.getenv("OPENAI_COMPAT_MAX_RETRIES", "1")))
        self._stream_enabled = os.getenv("OPENAI_COMPAT_STREAM", "true").strip().lower() in {"1", "true", "yes", "on"}
        self._top_p = _env_optional_float("OPENAI_COMPAT_TOP_P")
        self._top_k = _env_optional_int("OPENAI_COMPAT_TOP_K")
        self._min_p = _env_optional_float("OPENAI_COMPAT_MIN_P")
        self._repetition_penalty = _env_optional_float("OPENAI_COMPAT_REPETITION_PENALTY")
        self._enable_thinking = _env_optional_bool("OPENAI_COMPAT_ENABLE_THINKING")
        self._presence_penalty = _env_optional_float("OPENAI_COMPAT_PRESENCE_PENALTY")
        self._frequency_penalty = _env_optional_float("OPENAI_COMPAT_FREQUENCY_PENALTY")
        self._extra_body = _env_optional_json_dict("OPENAI_COMPAT_EXTRA_BODY_JSON")
        self._allow_no_tool_fallback = os.getenv(
            "OPENAI_COMPAT_ALLOW_NO_TOOL_FALLBACK", "true"
        ).strip().lower() in {"1", "true", "yes", "on"}
        self._configured_context_window = (
            _env_optional_int("OPENAI_COMPAT_CONTEXT_WINDOW")
            or _env_optional_int("MODEL_CONTEXT_WINDOW")
        )
        self._learned_context_window: int | None = None

    @property
    def provider_name(self) -> str:
        return self._provider_name

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def supports_image_prompt_blocks(self) -> bool:
        return True

    def _to_openai_messages(self, system: str, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = [{"role": "system", "content": system}]

        for msg in messages:
            role = msg.get("role")
            content = msg.get("content")
            if role not in {"user", "assistant", "tool"}:
                continue

            if isinstance(content, str):
                out.append({"role": role, "content": content})
                continue

            if isinstance(content, list):
                text_parts: list[str] = []
                content_parts: list[dict[str, Any]] = []
                tool_calls: list[dict[str, Any]] = []

                for block in content:
                    if not isinstance(block, dict):
                        text_parts.append(str(block))
                        continue
                    block_type = block.get("type")
                    if block_type == "text":
                        text = str(block.get("text", ""))
                        text_parts.append(text)
                        content_parts.append({"type": "text", "text": text})
                    elif block_type == "input_audio":
                        input_audio = block.get("input_audio")
                        if isinstance(input_audio, dict) and input_audio.get("data"):
                            content_parts.append(
                                {
                                    "type": "input_audio",
                                    "input_audio": {
                                        "data": str(input_audio.get("data") or ""),
                                        "format": str(input_audio.get("format") or "wav"),
                                    },
                                }
                            )
                        else:
                            label = str(
                                block.get("filename")
                                or (input_audio.get("filename") if isinstance(input_audio, dict) else "")
                                or "voice input"
                            )
                            content_parts.append({"type": "text", "text": f"[Audio attachment: {label}]"})
                    elif block_type == "audio_url":
                        audio_url = block.get("audio_url")
                        if isinstance(audio_url, dict) and audio_url.get("url"):
                            content_parts.append(
                                {
                                    "type": "audio_url",
                                    "audio_url": {"url": str(audio_url.get("url") or "")},
                                }
                            )
                        else:
                            label = str(
                                block.get("filename")
                                or (audio_url.get("filename") if isinstance(audio_url, dict) else "")
                                or "voice input"
                            )
                            content_parts.append({"type": "text", "text": f"[Audio attachment: {label}]"})
                    elif block_type == "image_url":
                        image_url = block.get("image_url")
                        if isinstance(image_url, dict) and image_url.get("url"):
                            content_parts.append({
                                "type": "image_url",
                                "image_url": {"url": str(image_url["url"])},
                            })
                    elif block_type == "thinking":
                        thinking_text = f"[thinking]\n{str(block.get('thinking', ''))}"
                        text_parts.append(thinking_text)
                        if role != "assistant":
                            content_parts.append({"type": "text", "text": thinking_text})
                    elif block_type == "tool_use":
                        tool_calls.append(
                            {
                                "id": block.get("tool_id") or block.get("id") or "",
                                "type": "function",
                                "function": {
                                    "name": block.get("tool_name") or block.get("name") or "",
                                    "arguments": json.dumps(block.get("input") or {}),
                                },
                            }
                        )
                    elif block_type == "tool_result":
                        out.append(
                            {
                                "role": "tool",
                                "tool_call_id": block.get("tool_use_id") or block.get("tool_id") or "",
                                "content": str(block.get("content") or block.get("result") or ""),
                            }
                        )

                if role == "assistant":
                    message_content: Any = "\n".join(p for p in text_parts if p).strip() or None
                else:
                    message_content = content_parts or ("\n".join(p for p in text_parts if p).strip() or None)

                msg_payload: dict[str, Any] = {"role": role, "content": message_content}
                if role == "assistant" and tool_calls:
                    msg_payload["tool_calls"] = tool_calls
                out.append(msg_payload)

        # Strip messages with no meaningful payload.
        return [m for m in out if m.get("content") is not None or m.get("tool_calls")]

    def _parse_tool_args(self, raw_args: str) -> dict[str, Any]:
        try:
            parsed = json.loads(raw_args)
            return parsed if isinstance(parsed, dict) else {"_raw_arguments": raw_args}
        except Exception:
            return {"_raw_arguments": raw_args}

    def _uses_openai_max_completion_tokens(self) -> bool:
        base_url = (self._base_url or "").lower()
        model_name = (self._model_name or "").lower()
        return "api.openai.com" in base_url and model_name.startswith("gpt-5")

    def _is_direct_openai(self) -> bool:
        if self._direct_openai_override is not None:
            return self._direct_openai_override
        return "api.openai.com" in (self._base_url or "").lower()

    def _messages_contain_direct_audio(self, messages: list[dict[str, Any]]) -> bool:
        for msg in messages:
            content = msg.get("content")
            if not isinstance(content, list):
                continue
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") in {"input_audio", "audio_url"}:
                    return True
        return False

    def _extract_error_preview(self, body: str) -> str:
        body = (body or "").strip()
        if not body:
            return "empty upstream error body"
        try:
            parsed = json.loads(body)
            if isinstance(parsed, dict):
                detail = parsed.get("error") or parsed.get("detail") or parsed.get("message")
                if isinstance(detail, dict):
                    for key in ("message", "detail", "error"):
                        value = detail.get(key)
                        if isinstance(value, str) and value.strip():
                            return value.strip()[:400]
                if isinstance(detail, str) and detail.strip():
                    return detail.strip()[:400]
        except Exception:
            pass
        return body[:400]

    def _extract_think_tags(self, text: str) -> tuple[str, list[str]]:
        raw = str(text or "")
        if not raw:
            return "", []

        thoughts: list[str] = []

        def _collect(match: re.Match[str]) -> str:
            thought = (match.group(1) or "").strip()
            if thought:
                thoughts.append(thought)
            return ""

        cleaned = re.sub(r"(?is)<think>\s*(.*?)\s*</think>", _collect, raw)
        return cleaned.strip(), thoughts

    def _parse_recovered_tool_args(self, raw_args: Any) -> dict[str, Any]:
        if isinstance(raw_args, dict):
            return raw_args
        if isinstance(raw_args, str):
            try:
                parsed = json.loads(raw_args)
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                return {"_raw_arguments": raw_args}
        return {}

    def _recover_tool_calls_from_text(
        self,
        text: str,
        *,
        available_tool_names: set[str],
    ) -> tuple[str, list[dict[str, Any]]]:
        raw = str(text or "")
        if not raw or not available_tool_names:
            return raw.strip(), []

        candidates: list[tuple[tuple[int, int], str]] = []
        for match in re.finditer(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", raw, flags=re.IGNORECASE):
            candidates.append((match.span(), match.group(1)))
        for match in re.finditer(
            r"(?is)(\{\s*\"name\"\s*:\s*\"[^\"]+\"[\s\S]*?\"arguments\"\s*:\s*(?:\{[\s\S]*?\}|\"[\s\S]*?\")\s*\})",
            raw,
        ):
            candidates.append((match.span(), match.group(1)))

        recovered: list[dict[str, Any]] = []
        spans_to_remove: list[tuple[int, int]] = []
        seen_spans: set[tuple[int, int]] = set()
        seen_names: set[str] = set()

        for span, candidate in candidates:
            if span in seen_spans:
                continue
            seen_spans.add(span)
            try:
                parsed = json.loads(candidate)
            except Exception:
                continue
            if not isinstance(parsed, dict):
                continue
            tool_name = str(parsed.get("name") or parsed.get("tool") or "").strip()
            if not tool_name or tool_name not in available_tool_names or tool_name in seen_names:
                continue
            arguments = self._parse_recovered_tool_args(parsed.get("arguments"))
            recovered.append(
                {
                    "id": f"recovered_{tool_name}_{len(recovered)}",
                    "function": {
                        "name": tool_name,
                        "arguments": json.dumps(arguments),
                    },
                }
            )
            seen_names.add(tool_name)
            spans_to_remove.append(span)

        if not recovered:
            return raw.strip(), []

        cleaned_parts: list[str] = []
        last_end = 0
        for start, end in sorted(spans_to_remove):
            cleaned_parts.append(raw[last_end:start])
            last_end = end
        cleaned_parts.append(raw[last_end:])
        cleaned = "".join(cleaned_parts).strip()
        return cleaned, recovered

    def _looks_like_tool_planning_scaffold(self, text: str) -> bool:
        normalized = " ".join(str(text or "").split()).lower()
        if not normalized:
            return False
        signals = [
            "step 1:",
            "step 2:",
            "next actions",
            "i'll use",
            "i will use",
            "let's proceed with",
            "execute the web search",
            '"name": "web_search"',
            '"arguments":',
        ]
        hits = sum(1 for signal in signals if signal in normalized)
        return hits >= 2

    def _normalize_upstream_error(self, status_code: int, body: str, *, direct_audio: bool) -> RuntimeError:
        preview = self._extract_error_preview(body)
        lowered = preview.lower()
        if direct_audio and any(hint in lowered for hint in AUDIO_SUPPORT_ERROR_HINTS):
            return RuntimeError(
                "Direct audio failed upstream: the OpenAI-compatible router/model path does not support audio yet "
                "(LiteLLM/vLLM reported missing audio support, e.g. 'install vllm[audio]'). "
                "This is an upstream deployment issue, not an ASR fallback issue."
            )
        if self._is_context_window_error_text(preview):
            return RuntimeError(
                "OpenAI-compatible request exceeded the upstream model context window. "
                f"{preview}"
            )
        return RuntimeError(
            f"OpenAI-compatible request failed with {status_code}: {preview}"
        )

    def _is_context_window_error_text(self, body: str) -> bool:
        preview = self._extract_error_preview(body)
        lowered = preview.lower()
        return "maximum context length" in lowered and any(
            signal in lowered
            for signal in (
                "input tokens",
                "requested output tokens",
                "prompt contains",
            )
        )

    def _set_max_tokens_payload(self, payload: dict[str, Any], max_tokens: int) -> None:
        payload.pop("max_tokens", None)
        payload.pop("max_completion_tokens", None)
        if self._uses_openai_max_completion_tokens():
            payload["max_completion_tokens"] = max_tokens
        else:
            payload["max_tokens"] = max_tokens

    def _effective_context_window(self, requested_max_tokens: int) -> int | None:
        for value in (self._learned_context_window, self._configured_context_window):
            if isinstance(value, int) and value > 0:
                return value
        if self._is_direct_openai():
            return None
        return max(8192, requested_max_tokens * 2)

    def _is_qwen_reasoning_family(self) -> bool:
        model_name = (self._model_name or "").strip().lower()
        if not model_name:
            return False
        normalized = model_name.replace("_", "-")
        return normalized.startswith("qwen3") or "/qwen3" in normalized

    def _resolve_enable_thinking(self, enable_thinking: bool | None) -> bool | None:
        if self._is_direct_openai():
            return None
        if enable_thinking is not None:
            return enable_thinking
        if self._enable_thinking is not None:
            return self._enable_thinking
        if self._is_qwen_reasoning_family():
            return False
        return None

    def _estimate_payload_input_tokens(self, payload: dict[str, Any]) -> int:
        probe = {
            "model": payload.get("model"),
            "messages": payload.get("messages"),
            "tools": payload.get("tools"),
            "tool_choice": payload.get("tool_choice"),
            "extra_body": payload.get("extra_body"),
        }
        try:
            serialized = json.dumps(probe, ensure_ascii=False)
        except Exception:
            serialized = str(probe)
        return max(1, len(serialized) // 4)

    def _preflight_adjust_max_tokens(self, payload: dict[str, Any], requested_max_tokens: int) -> int:
        context_window = self._effective_context_window(requested_max_tokens)
        if not context_window:
            return requested_max_tokens

        estimated_input_tokens = self._estimate_payload_input_tokens(payload)
        if estimated_input_tokens >= context_window:
            return requested_max_tokens

        if estimated_input_tokens + requested_max_tokens + 16 <= context_window:
            return requested_max_tokens

        adjusted = context_window - estimated_input_tokens - 16
        if adjusted <= 0:
            return requested_max_tokens
        return max(64, min(requested_max_tokens, adjusted))

    def _context_retry_max_tokens(self, body: str, requested_max_tokens: int) -> int | None:
        preview = self._extract_error_preview(body)
        lowered = preview.lower()
        if "maximum context length" not in lowered and "requested" not in lowered:
            return None

        context_match = re.search(r"maximum context length is (\d+) tokens", preview, flags=re.IGNORECASE)
        if not context_match:
            return None

        context_window = int(context_match.group(1))
        self._learned_context_window = context_window
        input_tokens_match = re.search(r"prompt contains at least (\d+) input tokens", preview, flags=re.IGNORECASE)
        if input_tokens_match:
            input_tokens = int(input_tokens_match.group(1))
            safety_margin = 16
            if input_tokens >= context_window:
                return None
            adjusted = context_window - input_tokens - safety_margin
            if adjusted <= 0:
                adjusted = context_window - input_tokens - 1
            if adjusted <= 0:
                return None
            adjusted = min(requested_max_tokens, adjusted)
            return adjusted if adjusted < requested_max_tokens else None

        prompt_chars_match = re.search(r"prompt contains (\d+) characters", preview, flags=re.IGNORECASE)
        estimated_prompt_tokens = 0
        if prompt_chars_match:
            prompt_chars = int(prompt_chars_match.group(1))
            estimated_prompt_tokens = max(1, prompt_chars // 4)

        if estimated_prompt_tokens >= context_window:
            return None

        reserve_tokens = 128
        allowed_output = context_window - estimated_prompt_tokens - reserve_tokens
        if allowed_output <= 0:
            fallback_output = max(64, min(requested_max_tokens, context_window // 8))
            return fallback_output if fallback_output < requested_max_tokens else None

        adjusted = min(requested_max_tokens, allowed_output)
        if adjusted < requested_max_tokens:
            return max(64, adjusted)
        return None

    async def _post_with_retries(
        self,
        *,
        client: httpx.AsyncClient,
        headers: dict[str, str],
        payload: dict[str, Any],
        request_max_retries: int,
    ) -> httpx.Response:
        resp = None
        for attempt in range(request_max_retries + 1):
            try:
                resp = await client.post(
                    f"{self._base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                if resp.status_code >= 500 and attempt < request_max_retries:
                    continue
                break
            except httpx.HTTPStatusError:
                raise
            except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.RemoteProtocolError):
                if attempt >= request_max_retries:
                    raise

        if resp is None:
            raise RuntimeError("No response from provider after retry attempts")
        return resp

    def _build_blocks_from_message(
        self,
        message: dict[str, Any],
        *,
        available_tool_names: set[str] | None = None,
    ) -> list[LLMContentBlock]:
        blocks: list[LLMContentBlock] = []

        reasoning_text = (
            message.get("reasoning_content")
            or (message.get("provider_specific_fields") or {}).get("reasoning_content")
            or (message.get("provider_specific_fields") or {}).get("reasoning")
        )
        if not isinstance(reasoning_text, str):
            reasoning_text = ""

        content_text = message.get("content")
        recovered_tool_calls: list[dict[str, Any]] = []
        if isinstance(content_text, str) and content_text.strip():
            content_text, extracted_thoughts = self._extract_think_tags(content_text)
            if extracted_thoughts:
                thought_blob = "\n\n".join(part for part in extracted_thoughts if part.strip())
                if thought_blob:
                    reasoning_text = "\n\n".join(part for part in [reasoning_text, thought_blob] if part).strip()
            if available_tool_names:
                content_text, recovered_tool_calls = self._recover_tool_calls_from_text(
                    content_text,
                    available_tool_names=available_tool_names,
                )
            if recovered_tool_calls and self._looks_like_tool_planning_scaffold(content_text):
                content_text = ""

        if isinstance(reasoning_text, str) and reasoning_text.strip():
            blocks.append(LLMContentBlock(type="thinking", thinking=reasoning_text))

        if isinstance(content_text, str) and content_text.strip():
            blocks.append(LLMContentBlock(type="text", text=content_text))

        tool_calls = list(message.get("tool_calls") or [])
        if recovered_tool_calls:
            tool_calls.extend(recovered_tool_calls)

        for call in tool_calls:
            function = call.get("function") or {}
            raw_args = function.get("arguments") or "{}"
            blocks.append(
                LLMContentBlock(
                    type="tool_use",
                    id=str(call.get("id") or ""),
                    name=str(function.get("name") or ""),
                    input=self._parse_tool_args(raw_args),
                )
            )

        return blocks

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
        direct_audio = self._messages_contain_direct_audio(messages)
        request_max_retries = 0 if direct_audio else self._max_retries
        allow_no_tool_fallback = self._allow_no_tool_fallback and not direct_audio

        payload: dict[str, Any] = {
            "model": self._model_name,
            "messages": self._to_openai_messages(system, messages),
            "temperature": temperature,
        }
        if direct_audio and not self._is_direct_openai():
            payload["num_retries"] = 0
        self._set_max_tokens_payload(payload, max_tokens)
        if self._top_p is not None:
            payload["top_p"] = self._top_p
        if self._top_k is not None:
            payload["top_k"] = self._top_k
        if self._min_p is not None:
            payload["min_p"] = self._min_p
        if self._repetition_penalty is not None:
            payload["repetition_penalty"] = self._repetition_penalty
        if self._presence_penalty is not None:
            payload["presence_penalty"] = self._presence_penalty
        if self._frequency_penalty is not None:
            payload["frequency_penalty"] = self._frequency_penalty
        resolved_enable_thinking = self._resolve_enable_thinking(enable_thinking)
        if resolved_enable_thinking is not None and not self._is_direct_openai():
            extra_body = payload.setdefault("extra_body", {})
            if isinstance(extra_body, dict):
                chat_kwargs = extra_body.setdefault("chat_template_kwargs", {})
                if isinstance(chat_kwargs, dict):
                    chat_kwargs["enable_thinking"] = resolved_enable_thinking
        if self._extra_body and not self._is_direct_openai():
            payload.update(self._extra_body)
        if tools:
            payload["tools"] = [
                {
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "parameters": tool.get("input_schema", {"type": "object", "properties": {}}),
                    },
                }
                for tool in tools
            ]
            payload["tool_choice"] = "auto"

        if not direct_audio:
            adjusted_max_tokens = self._preflight_adjust_max_tokens(payload, max_tokens)
            if adjusted_max_tokens < max_tokens:
                max_tokens = adjusted_max_tokens
                self._set_max_tokens_payload(payload, max_tokens)

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        fallback_error = None
        timeout = httpx.Timeout(
            timeout=self._timeout,
            connect=self._connect_timeout,
            read=self._read_timeout,
            write=self._write_timeout,
        )
        async with httpx.AsyncClient(timeout=timeout) as client:
            if self._stream_enabled and on_stream_event is not None:
                stream_error_status: tuple[int, str] | None = None

                for attempt in range(request_max_retries + 1):
                    stream_payload = dict(payload)
                    stream_payload["stream"] = True
                    stream_payload.setdefault("stream_options", {"include_usage": True})

                    content_parts: list[str] = []
                    reasoning_parts: list[str] = []
                    tool_calls: dict[int, dict[str, str]] = {}
                    emitted_tool_ids: set[str] = set()
                    usage_data: dict[str, Any] = {}
                    finish_reason = "stop"
                    stream_error_status = None

                    try:
                        async with client.stream(
                            "POST",
                            f"{self._base_url}/chat/completions",
                            headers=headers,
                            json=stream_payload,
                        ) as resp:
                            if resp.status_code >= 400:
                                body_text = (await resp.aread()).decode("utf-8", errors="replace")
                                adjusted_max_tokens = self._context_retry_max_tokens(body_text, max_tokens)
                                if adjusted_max_tokens is not None:
                                    max_tokens = adjusted_max_tokens
                                    self._set_max_tokens_payload(payload, max_tokens)
                                    continue
                                if resp.status_code >= 500 and attempt < request_max_retries:
                                    continue
                                stream_error_status = (resp.status_code, body_text[:4000])
                                break

                            async for raw_line in resp.aiter_lines():
                                line = (raw_line or "").strip()
                                if not line or line.startswith(":"):
                                    continue
                                if not line.startswith("data:"):
                                    continue

                                data_str = line[5:].strip()
                                if data_str == "[DONE]":
                                    break

                                try:
                                    chunk = json.loads(data_str)
                                except Exception:
                                    continue

                                if isinstance(chunk.get("usage"), dict):
                                    usage_data = chunk["usage"]

                                choices = chunk.get("choices") or []
                                if not choices:
                                    continue

                                choice0 = choices[0] or {}
                                delta = choice0.get("delta") or {}
                                if choice0.get("finish_reason"):
                                    finish_reason = str(choice0.get("finish_reason") or finish_reason)

                                reasoning_delta = delta.get("reasoning_content") or delta.get("reasoning")
                                if isinstance(reasoning_delta, str) and reasoning_delta:
                                    reasoning_parts.append(reasoning_delta)
                                    await on_stream_event(LLMContentBlock(type="thinking", thinking=reasoning_delta))

                                content_delta = delta.get("content")
                                if isinstance(content_delta, str) and content_delta:
                                    content_parts.append(content_delta)

                                for tool_delta in delta.get("tool_calls") or []:
                                    if not isinstance(tool_delta, dict):
                                        continue
                                    idx = int(tool_delta.get("index") or 0)
                                    slot = tool_calls.setdefault(idx, {"id": "", "name": "", "arguments": ""})
                                    if tool_delta.get("id"):
                                        slot["id"] = str(tool_delta["id"])

                                    fn = tool_delta.get("function") or {}
                                    if isinstance(fn, dict):
                                        if fn.get("name"):
                                            slot["name"] = str(fn["name"])
                                        if fn.get("arguments"):
                                            slot["arguments"] += str(fn["arguments"])

                                    if slot["id"] and slot["name"] and slot["id"] not in emitted_tool_ids:
                                        emitted_tool_ids.add(slot["id"])
                                        await on_stream_event(
                                            LLMContentBlock(
                                                type="tool_use",
                                                id=slot["id"],
                                                name=slot["name"],
                                                input={},
                                            )
                                )

                            blocks = self._build_blocks_from_message(
                                {
                                    "content": "".join(content_parts),
                                    "reasoning_content": "".join(reasoning_parts),
                                    "tool_calls": [
                                        {
                                            "id": tool_calls[idx]["id"],
                                            "function": {
                                                "name": tool_calls[idx]["name"],
                                                "arguments": tool_calls[idx]["arguments"] or "{}",
                                            },
                                        }
                                        for idx in sorted(tool_calls)
                                    ],
                                },
                                available_tool_names={str(tool.get("name") or "").strip() for tool in tools},
                            )
                            recovered_tool_use = any(block.type == "tool_use" for block in blocks)

                            return LLMResponse(
                                stop_reason="tool_use" if (finish_reason in {"tool_calls", "function_call"} or recovered_tool_use) else "end_turn",
                                content=blocks,
                                usage=LLMUsage(
                                    input_tokens=int(usage_data.get("prompt_tokens") or 0),
                                    output_tokens=int(usage_data.get("completion_tokens") or 0),
                                ),
                                provider_name=self.provider_name,
                                model_name=self.model_name,
                            )
                    except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.RemoteProtocolError):
                        if attempt >= request_max_retries:
                            raise

                if (
                    stream_error_status
                    and tools
                    and allow_no_tool_fallback
                    and not self._is_context_window_error_text(stream_error_status[1])
                ):
                    status_code, body_preview = stream_error_status
                    fallback_error = f"{status_code}: {body_preview}"
                elif stream_error_status:
                    raise self._normalize_upstream_error(
                        stream_error_status[0],
                        stream_error_status[1],
                        direct_audio=direct_audio,
                    )
            # Non-stream path (or stream fallback)
            request_payload = dict(payload)
            if fallback_error and tools and allow_no_tool_fallback:
                request_payload.pop("tools", None)
                request_payload.pop("tool_choice", None)

            resp = await self._post_with_retries(
                client=client,
                headers=headers,
                payload=request_payload,
                request_max_retries=request_max_retries,
            )

            if (
                not direct_audio
                and resp.status_code == 400
                and not self._uses_openai_max_completion_tokens()
                and "max_tokens" in resp.text
            ):
                request_payload.pop("max_tokens", None)
                request_payload["max_completion_tokens"] = max_tokens
                resp = await self._post_with_retries(
                    client=client,
                    headers=headers,
                    payload=request_payload,
                    request_max_retries=request_max_retries,
                )

            if resp.status_code >= 400:
                adjusted_max_tokens = self._context_retry_max_tokens(resp.text, max_tokens)
                if adjusted_max_tokens is not None:
                    self._set_max_tokens_payload(request_payload, adjusted_max_tokens)
                    max_tokens = adjusted_max_tokens
                    resp = await self._post_with_retries(
                        client=client,
                        headers=headers,
                        payload=request_payload,
                        request_max_retries=request_max_retries,
                    )

            if (
                resp.status_code >= 400
                and tools
                and allow_no_tool_fallback
                and not fallback_error
                and not self._is_context_window_error_text(resp.text)
            ):
                fallback_error = f"{resp.status_code}: {resp.text[:400]}"
                payload_no_tools = dict(request_payload)
                payload_no_tools.pop("tools", None)
                payload_no_tools.pop("tool_choice", None)
                resp = await self._post_with_retries(
                    client=client,
                    headers=headers,
                    payload=payload_no_tools,
                    request_max_retries=request_max_retries,
                )

            if resp.status_code >= 400:
                raise self._normalize_upstream_error(resp.status_code, resp.text, direct_audio=direct_audio)
            data = resp.json()

        choice = (data.get("choices") or [{}])[0]
        message = choice.get("message") or {}
        finish_reason = choice.get("finish_reason") or "stop"
        usage_data = data.get("usage") or {}
        usage = LLMUsage(
            input_tokens=int(usage_data.get("prompt_tokens") or 0),
            output_tokens=int(usage_data.get("completion_tokens") or 0),
        )
        blocks = self._build_blocks_from_message(
            message,
            available_tool_names={str(tool.get("name") or "").strip() for tool in tools},
        )
        recovered_tool_use = any(block.type == "tool_use" for block in blocks)
        stop_reason = "tool_use" if (finish_reason in {"tool_calls", "function_call"} or recovered_tool_use) else "end_turn"
        if fallback_error and blocks:
            blocks.append(
                LLMContentBlock(
                    type="text",
                    text=(
                        f"[Provider notice] Tool-call payload fallback was used due upstream error: {fallback_error}"
                    ),
                )
            )
        return LLMResponse(
            stop_reason=stop_reason,
            content=blocks,
            usage=usage,
            provider_name=self.provider_name,
            model_name=self.model_name,
        )
