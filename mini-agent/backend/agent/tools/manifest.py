from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


TOOLS_MANIFEST_PATH = Path(__file__).resolve().parents[2] / "TOOLS.md"


def _split_front_matter(raw: str) -> tuple[dict[str, Any], str]:
    text = raw.strip()
    if not text.startswith("---\n"):
        return {}, raw
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}, raw
    try:
        parsed = yaml.safe_load(parts[0][4:]) or {}
    except Exception:
        parsed = {}
    return (parsed if isinstance(parsed, dict) else {}), parts[1]


def _compact_description(text: str, limit: int = 120) -> str:
    cleaned = " ".join(str(text or "").split())
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3].rstrip() + "..."


def load_tool_manifest() -> dict[str, Any]:
    try:
        raw = TOOLS_MANIFEST_PATH.read_text(encoding="utf-8")
    except Exception:
        return {
            "front_matter": {},
            "body": "",
        }
    front_matter, body = _split_front_matter(raw)
    return {
        "front_matter": front_matter,
        "body": body.strip(),
    }


def core_tool_names() -> list[str]:
    manifest = load_tool_manifest()
    raw = manifest.get("front_matter", {}).get("core_tools") or []
    return [str(name).strip() for name in raw if str(name).strip()]


def dynamic_tool_groups() -> dict[str, dict[str, Any]]:
    manifest = load_tool_manifest()
    groups = manifest.get("front_matter", {}).get("dynamic_groups") or {}
    return groups if isinstance(groups, dict) else {}


def dynamic_tool_names() -> list[str]:
    names: list[str] = []
    for payload in dynamic_tool_groups().values():
        tools = payload.get("tools") if isinstance(payload, dict) else []
        for tool_name in tools or []:
            name = str(tool_name).strip()
            if name:
                names.append(name)
    return names


def manifest_tool_names() -> list[str]:
    ordered: list[str] = []
    for name in [*core_tool_names(), *dynamic_tool_names()]:
        if name not in ordered:
            ordered.append(name)
    return ordered


def _defs_by_name(tool_definitions: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for tool in tool_definitions:
        name = str(tool.get("name") or "").strip()
        if name:
            out[name] = tool
    return out


def get_tool_definition(tool_definitions: list[dict[str, Any]], tool_name: str) -> dict[str, Any] | None:
    return _defs_by_name(tool_definitions).get(str(tool_name or "").strip())


def get_active_tool_definitions(
    tool_definitions: list[dict[str, Any]],
    loaded_tool_names: list[str] | None = None,
) -> list[dict[str, Any]]:
    loaded = {str(name).strip() for name in (loaded_tool_names or []) if str(name).strip()}
    allowed = set(core_tool_names()) | loaded
    selected = [tool for tool in tool_definitions if str(tool.get("name") or "").strip() in allowed]
    return selected or tool_definitions


def build_tools_prompt_block(
    tool_definitions: list[dict[str, Any]],
    loaded_tool_names: list[str] | None = None,
) -> str:
    by_name = _defs_by_name(tool_definitions)
    loaded = [name for name in (loaded_tool_names or []) if name in by_name]

    lines = ["## Tools Bootstrap"]
    core_names = core_tool_names()
    if core_names:
        lines.append(f"- Core tools callable now: {', '.join(f'`{name}`' for name in core_names if name in by_name)}")

    lines.append("- Dynamic tools are schema-gated. To use one, call `read_tool_schema` with the exact tool name first.")

    groups = dynamic_tool_groups()
    if groups:
        lines.append("- Dynamic tool catalog:")
        for group_name, payload in groups.items():
            if not isinstance(payload, dict):
                continue
            tools = [f"`{name}`" for name in payload.get("tools") or [] if name in by_name]
            if not tools:
                continue
            lines.append(f"  - {group_name}: {', '.join(tools)}")

    if loaded:
        lines.append(f"- Schemas already loaded this session: {', '.join(f'`{name}`' for name in loaded)}")

    return "\n".join(lines)


def build_tool_schema_payload(
    tool_definitions: list[dict[str, Any]],
    tool_name: str,
) -> str:
    tool = get_tool_definition(tool_definitions, tool_name)
    if not tool:
        available = manifest_tool_names()
        return json.dumps(
            {
                "status": "error",
                "message": f"Unknown tool '{tool_name}'.",
                "available_tools": available,
            },
            indent=2,
        )

    payload = {
        "status": "ok",
        "tool": tool["name"],
        "description": tool.get("description", ""),
        "input_schema": tool.get("input_schema", {}),
        "core_tool": tool["name"] in set(core_tool_names()),
        "loaded": True,
    }
    return json.dumps(payload, indent=2)
