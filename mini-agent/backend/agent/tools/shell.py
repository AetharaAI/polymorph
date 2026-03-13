import subprocess
import shlex
import asyncio
import os

from backend.agent.tools.workspace import get_session_workspace


# Whitelist of allowed commands
STRICT_ALLOWED_COMMANDS = {
    "ls", "pwd", "cat", "head", "tail", "grep", "wc", "echo", "date", "curl",
    "which", "find", "sed", "awk", "cut", "sort", "uniq", "tr", "xargs", "jq",
    "rg", "uname", "whoami", "env", "df", "du", "stat", "file"
}

PROJECT_ALLOWED_COMMANDS = STRICT_ALLOWED_COMMANDS | {
    "mkdir", "touch", "cp", "mv", "rm", "python", "python3", "pip", "pip3",
    "node", "npm", "pnpm", "yarn", "pytest", "uvicorn", "git"
}

def _profile() -> str:
    return os.getenv("AGENT_SHELL_PROFILE", "strict").strip().lower()


async def run_shell(command: str, session_id: str | None = None) -> str:
    """Run a restricted shell command or project-profile command in session workspace."""
    try:
        profile = _profile()
        timeout = int(os.getenv("SHELL_TIMEOUT_SECONDS", "60"))
        if profile == "project_full":
            timeout = int(os.getenv("SHELL_TIMEOUT_SECONDS", "300"))

        workspace = get_session_workspace(session_id or "default")

        # Parse the command
        parts = shlex.split(command)
        if not parts:
            return "Error: Empty command"

        base_cmd = parts[0]

        if profile == "strict":
            allowed = STRICT_ALLOWED_COMMANDS
        elif profile == "project":
            allowed = PROJECT_ALLOWED_COMMANDS
        else:
            allowed = None

        # Check if command is whitelisted (strict/project)
        if allowed is not None and base_cmd not in allowed:
            return (
                f"Error: Command '{base_cmd}' is not allowed for profile '{profile}'. "
                f"Allowed commands: {', '.join(sorted(allowed))}"
            )

        # Additional restrictions for curl (GET only)
        if base_cmd == "curl":
            if "-X" in parts or "--request" in parts:
                return "Error: Only GET requests are allowed with curl"
            # Add -s flag if not present
            if "-s" not in parts and "--silent" not in parts:
                parts.insert(1, "-s")

        if profile == "project_full":
            # Full command execution in sandboxed backend container workspace.
            result = await asyncio.to_thread(
                subprocess.run,
                ["/bin/sh", "-lc", command],
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

        output = []
        output.append(f"profile={profile} workspace={workspace}")
        if result.stdout:
            output.append(result.stdout)
        if result.stderr:
            output.append(f"stderr: {result.stderr}")
        if not result.stdout and not result.stderr:
            output.append("(No output)")

        return "\n".join(output)

    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after {timeout} seconds"
    except Exception as e:
        return f"Error: {str(e)}"
