from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

_THINK_TAG_RE = re.compile(r"(?is)<think>\s*(.*?)\s*</think>")
_MCP_TOOL_BLOCK_RE = re.compile(r"(?is)<use_mcp_tool>\s*(.*?)\s*</use_mcp_tool>")
_GENERIC_TOOL_BLOCK_RE = re.compile(r"(?is)<tool(?:_call)?>\s*(.*?)\s*</tool(?:_call)?>")
_SERVER_RE = re.compile(r"(?is)<server_name>\s*(.*?)\s*</server_name>")
_TOOL_RE = re.compile(r"(?is)<tool_name>\s*(.*?)\s*</tool_name>")
_ARGS_RE = re.compile(r"(?is)<arguments>\s*(.*?)\s*</arguments>")
_JSON_TOOL_RE = re.compile(
    r'(?is)\{\s*"name"\s*:\s*"([^"]+)"\s*,\s*"arguments"\s*:\s*(\{[\s\S]*\}|"(?:\\.|[^"])*")\s*\}'
)


@dataclass(slots=True)
class XMLMCPToolCall:
    server_name: str
    tool_name: str
    arguments_raw: str
    arguments: dict[str, Any] | None
    parse_error: str | None
    allowed: bool
    blocked_reason: str | None


@dataclass(slots=True)
class XMLMCPParseResult:
    raw_output: str
    reasoning_channel: str
    final_answer_channel: str
    tool_call_channel: list[XMLMCPToolCall] = field(default_factory=list)
    parse_errors: list[str] = field(default_factory=list)


def _extract_first(tag_re: re.Pattern[str], text: str) -> str:
    match = tag_re.search(text)
    if not match:
        return ""
    return (match.group(1) or "").strip()


def _parse_tool_payload(payload: str) -> tuple[str, str, str]:
    server_name = _extract_first(_SERVER_RE, payload)
    tool_name = _extract_first(_TOOL_RE, payload)
    arguments_raw = _extract_first(_ARGS_RE, payload)

    if tool_name and arguments_raw:
        return server_name, tool_name, arguments_raw

    candidate = (payload or "").strip()
    if not candidate:
        return server_name, tool_name, arguments_raw

    try:
        parsed = json.loads(candidate)
        if isinstance(parsed, dict):
            recovered_name = str(parsed.get("name") or parsed.get("tool") or "").strip()
            if recovered_name:
                recovered_args = parsed.get("arguments")
                if isinstance(recovered_args, str):
                    return server_name, recovered_name, recovered_args
                if recovered_args is not None:
                    return server_name, recovered_name, json.dumps(recovered_args)
    except Exception:
        pass

    inline = _JSON_TOOL_RE.search(candidate)
    if inline:
        recovered_name = (inline.group(1) or "").strip()
        recovered_args = (inline.group(2) or "").strip()
        if recovered_name and recovered_args:
            return server_name, recovered_name, recovered_args

    return server_name, tool_name, arguments_raw


def parse_xml_mcp_reasoning_output(
    text: str,
    *,
    available_tool_names: set[str],
    allowed_server_names: set[str] | None,
) -> XMLMCPParseResult:
    raw = str(text or "")

    thought_parts: list[str] = []

    def _collect_think(match: re.Match[str]) -> str:
        thought = (match.group(1) or "").strip()
        if thought:
            thought_parts.append(thought)
        return ""

    without_think = _THINK_TAG_RE.sub(_collect_think, raw)

    tool_calls: list[XMLMCPToolCall] = []
    parse_errors: list[str] = []
    seen_keys: set[tuple[str, str]] = set()

    def _collect_tool(match: re.Match[str]) -> str:
        payload = (match.group(1) or "").strip()
        server_name, tool_name, arguments_raw = _parse_tool_payload(payload)

        parse_error: str | None = None
        arguments: dict[str, Any] | None = None
        blocked_reason: str | None = None

        if not tool_name:
            parse_error = "missing tool_name"
        elif not arguments_raw:
            parse_error = "missing arguments"
        else:
            try:
                parsed = json.loads(arguments_raw)
                if isinstance(parsed, dict):
                    arguments = parsed
                else:
                    parse_error = "arguments must decode to a JSON object"
            except Exception as exc:
                parse_error = f"invalid arguments JSON: {exc}"

        if not server_name and tool_name:
            # Some OpenAI-compat outputs emit tool blocks without server_name.
            # Use harness as the default local server alias for tool-gate checks.
            server_name = "harness"

        dedupe_key = (
            str(tool_name or "").strip().lower(),
            json.dumps(arguments, sort_keys=True) if isinstance(arguments, dict) else str(arguments_raw or ""),
        )
        if tool_name and dedupe_key in seen_keys:
            return ""
        if tool_name:
            seen_keys.add(dedupe_key)

        allowed = parse_error is None
        if allowed:
            if allowed_server_names is not None and server_name.lower() not in allowed_server_names:
                allowed = False
                blocked_reason = f"server '{server_name}' is not approved"
            elif tool_name not in available_tool_names:
                allowed = False
                blocked_reason = f"tool '{tool_name}' is not in approved registry"

        if parse_error:
            parse_errors.append(parse_error)

        tool_calls.append(
            XMLMCPToolCall(
                server_name=server_name,
                tool_name=tool_name,
                arguments_raw=arguments_raw,
                arguments=arguments,
                parse_error=parse_error,
                allowed=allowed,
                blocked_reason=blocked_reason,
            )
        )
        return ""

    without_mcp_tools = _MCP_TOOL_BLOCK_RE.sub(_collect_tool, without_think)
    without_tools = _GENERIC_TOOL_BLOCK_RE.sub(_collect_tool, without_mcp_tools)

    final_answer = without_tools.strip()
    reasoning_channel = "\n\n".join(part for part in thought_parts if part.strip()).strip()

    return XMLMCPParseResult(
        raw_output=raw,
        reasoning_channel=reasoning_channel,
        final_answer_channel=final_answer,
        tool_call_channel=tool_calls,
        parse_errors=parse_errors,
    )
