from __future__ import annotations

import os
from pathlib import Path

from backend.agent.tools.workspace import get_session_workspace


STRICT_ALLOWED_COMMANDS = {
    "ls", "pwd", "cat", "head", "tail", "grep", "wc", "echo", "date", "curl",
    "which", "find", "sed", "awk", "cut", "sort", "uniq", "tr", "xargs", "jq",
    "rg", "uname", "whoami", "env", "df", "du", "stat", "file"
}

PROJECT_ALLOWED_COMMANDS = STRICT_ALLOWED_COMMANDS | {
    "mkdir", "touch", "cp", "mv", "rm", "python", "python3", "pip", "pip3",
    "node", "npm", "pnpm", "yarn", "pytest", "uvicorn", "git"
}


def env_flag(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def shell_profile() -> str:
    return os.getenv("AGENT_SHELL_PROFILE", "strict").strip().lower()


def _mode(profile: str, outside_workspace: bool, host_elevated: bool) -> str:
    if host_elevated:
        return "host_elevated"
    if outside_workspace or profile == "project_full":
        return "brokered"
    return "contained"


def _allowed_commands(profile: str) -> list[str]:
    if profile == "strict":
        return sorted(STRICT_ALLOWED_COMMANDS)
    if profile == "project":
        return sorted(PROJECT_ALLOWED_COMMANDS)
    return ["<full shell in backend container>"]


def _allowed_roots(workspace: Path, outside_workspace: bool, host_elevated: bool) -> list[str]:
    if host_elevated:
        return ["/"]
    if outside_workspace:
        return ["<backend-container-visible filesystem>", str(workspace.resolve())]
    return [str(workspace.resolve())]


def execution_boundary_for_workspace(workspace: Path, session_id: str | None = None) -> dict[str, object]:
    profile = shell_profile()
    outside_workspace = env_flag("AGENT_ALLOW_OUTSIDE_WORKSPACE_ACCESS", profile == "project_full")
    http_egress_enabled = env_flag("AGENT_ALLOW_HTTP_EGRESS", True)
    host_elevated = env_flag("AGENT_HOST_ELEVATED_ACCESS", False)
    mode = _mode(profile, outside_workspace, host_elevated)
    shell_supports_single_command = profile != "project_full"
    shell_http_egress = http_egress_enabled and (
        profile == "project_full" or "curl" in _allowed_commands(profile)
    )

    if mode == "contained":
        scope_summary = (
            "Commands are contained to the current session workspace. Shell and project inspection do not describe "
            "files outside that workspace."
        )
        model_guidance = (
            "Inspection results are workspace-scoped only. Do not infer that files, repos, services, or paths are "
            "globally missing outside the session workspace."
        )
    elif mode == "brokered":
        scope_summary = (
            "Commands can inspect beyond the session workspace, but only through the backend container's visible "
            "filesystem and approved tool/runtime paths."
        )
        model_guidance = (
            "Broader inspection is allowed inside the backend container boundary, but this is still not arbitrary "
            "host access. Missing host paths may still exist outside container-visible mounts."
        )
    else:
        scope_summary = (
            "Commands are running with elevated host-visible scope. Treat filesystem actions as potentially affecting "
            "the broader machine, not just the session workspace."
        )
        model_guidance = (
            "Host-elevated scope is active. Be explicit about touched paths and avoid destructive commands unless "
            "they are clearly intended and allowed."
        )

    return {
        "session_id": session_id or "default",
        "workspace_id": Path(workspace).name,
        "workspace_root": str(workspace),
        "shell_profile": profile,
        "scope_mode": mode,
        "scope_summary": scope_summary,
        "model_guidance": model_guidance,
        "single_command_only": shell_supports_single_command,
        "outside_workspace_access": outside_workspace,
        "allowed_roots": _allowed_roots(workspace, outside_workspace, host_elevated),
        "container_scope_note": (
            "Backend shell access is bounded by the backend container filesystem and mounted volumes unless an "
            "explicit host-elevated mode is enabled."
        ),
        "http_egress": {
            "tools": http_egress_enabled,
            "shell": shell_http_egress,
            "connectors": True,
            "raw_sockets": False,
        },
        "http_egress_note": (
            "HTTP egress is enabled for tool/runtime lanes according to the current execution policy."
            if http_egress_enabled
            else "HTTP egress is disabled for operator-exposed tool lanes by execution policy."
        ),
        "allowed_commands": _allowed_commands(profile),
    }


def execution_boundary_for_session(session_id: str | None = None) -> dict[str, object]:
    effective_session_id = session_id or "default"
    workspace = get_session_workspace(effective_session_id)
    return execution_boundary_for_workspace(workspace, effective_session_id)
