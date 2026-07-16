import asyncio
import json
import os
import re
import shlex
import subprocess
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

SHELL_META_PATTERN = re.compile(r"[;&|><`\n]")


def _profile() -> str:
    return os.getenv("AGENT_SHELL_PROFILE", "strict").strip().lower()


def _env_flag(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _policy(workspace: Path) -> dict[str, object]:
    profile = _profile()
    outside_workspace = _env_flag("AGENT_ALLOW_OUTSIDE_WORKSPACE_ACCESS", profile == "project_full")
    http_egress = _env_flag("AGENT_ALLOW_HTTP_EGRESS", True)
    if profile == "strict":
        allowed_commands = sorted(STRICT_ALLOWED_COMMANDS)
    elif profile == "project":
        allowed_commands = sorted(PROJECT_ALLOWED_COMMANDS)
    else:
        allowed_commands = ["<full shell in backend container>"]
    return {
        "shell_profile": profile,
        "workspace_root": str(workspace),
        "single_command_only": profile != "project_full",
        "outside_workspace_access": outside_workspace,
        "http_egress": http_egress,
        "allowed_commands": allowed_commands,
        "container_scope_note": (
            "Access beyond the session workspace is still limited to the backend container filesystem "
            "and mounted volumes; this does not grant arbitrary host access."
        ),
    }


def execution_policy_for_session(session_id: str | None = None) -> dict[str, object]:
    return _policy(get_session_workspace(session_id or "default"))


def _json_error(message: str, *, command: str, policy: dict[str, object]) -> str:
    return json.dumps(
        {
            "ok": False,
            "kind": "shell_policy_error",
            "message": message,
            "command": command,
            "policy": policy,
        },
        ensure_ascii=False,
        indent=2,
    )


def _extract_absolute_paths(parts: list[str]) -> list[Path]:
    paths: list[Path] = []
    for part in parts[1:]:
        value = part.strip()
        if not value or value.startswith(("http://", "https://")):
            continue
        if value.startswith("file://"):
            value = value[len("file://"):]
        if value.startswith("/"):
            paths.append(Path(value))
    return paths


async def run_shell(command: str, session_id: str | None = None) -> str:
    """Run a restricted shell command or project-profile command in session workspace."""
    try:
        profile = _profile()
        timeout = int(os.getenv("SHELL_TIMEOUT_SECONDS", "60"))
        if profile == "project_full":
            timeout = int(os.getenv("SHELL_TIMEOUT_SECONDS", "300"))

        workspace = get_session_workspace(session_id or "default")
        policy = _policy(workspace)
        raw_command = (command or "").strip()
        if not raw_command:
            return _json_error("Empty command.", command=command or "", policy=policy)

        if profile != "project_full" and SHELL_META_PATTERN.search(raw_command):
            return _json_error(
                "run_shell accepts exactly one command in strict/project profiles. "
                "Chaining, pipes, redirection, and inline cd are disabled. "
                "Use a single allowed command, or use run_project_command for multi-step workspace execution.",
                command=raw_command,
                policy=policy,
            )

        parts = shlex.split(raw_command)
        if not parts:
            return _json_error("Empty command.", command=raw_command, policy=policy)

        base_cmd = parts[0]

        if profile == "strict":
            allowed = STRICT_ALLOWED_COMMANDS
        elif profile == "project":
            allowed = PROJECT_ALLOWED_COMMANDS
        else:
            allowed = None

        if allowed is not None and base_cmd not in allowed:
            return _json_error(
                f"Command '{base_cmd}' is not allowed for profile '{profile}'. "
                "If you need workspace builds/tests, use run_project_command or widen the execution policy.",
                command=raw_command,
                policy=policy,
            )

        if base_cmd == "curl" and not policy["http_egress"]:
            return _json_error(
                "HTTP/network egress is disabled by execution policy. Ask the operator to enable it in the UI before using curl.",
                command=raw_command,
                policy=policy,
            )

        if base_cmd == "curl":
            if "-X" in parts or "--request" in parts:
                return _json_error("Only GET requests are allowed with curl.", command=raw_command, policy=policy)
            if "-s" not in parts and "--silent" not in parts:
                parts.insert(1, "-s")

        if not policy["outside_workspace_access"]:
            workspace_resolved = workspace.resolve()
            for path in _extract_absolute_paths(parts):
                resolved = path.resolve() if path.exists() else path
                if workspace_resolved not in resolved.parents and resolved != workspace_resolved:
                    return _json_error(
                        "Access to absolute paths outside the session workspace is disabled by execution policy.",
                        command=raw_command,
                        policy=policy,
                    )

        if profile == "project_full":
            result = await asyncio.to_thread(
                subprocess.run,
                ["/bin/sh", "-lc", raw_command],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(workspace),
                env={**os.environ, "HOME": str(workspace), "SESSION_WORKSPACE": str(workspace)},
            )
        else:
            result = await asyncio.to_thread(
                subprocess.run,
                parts,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(workspace),
                env={**os.environ, "HOME": str(workspace), "SESSION_WORKSPACE": str(workspace)},
            )

        return json.dumps(
            {
                "ok": result.returncode == 0,
                "kind": "shell_command",
                "command": raw_command,
                "exit_code": result.returncode,
                "workspace": str(workspace),
                "policy": policy,
                "stdout": result.stdout or "(No output)",
                "stderr": result.stderr or "",
            },
            ensure_ascii=False,
            indent=2,
        )

    except subprocess.TimeoutExpired:
        workspace = get_session_workspace(session_id or "default")
        return _json_error(
            f"Command timed out after {timeout} seconds.",
            command=(command or "").strip(),
            policy=_policy(workspace),
        )
    except Exception as e:
        workspace = get_session_workspace(session_id or "default")
        return _json_error(
            str(e),
            command=(command or "").strip(),
            policy=_policy(workspace),
        )
