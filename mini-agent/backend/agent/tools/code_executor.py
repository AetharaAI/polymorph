import asyncio
import subprocess
import os
import time
import sys
import shutil
from pathlib import Path

from backend.agent.tools.workspace import get_session_workspace


async def execute_python(code: str, timeout: int = 30, session_id: str | None = None) -> str:
    """Execute Python code in a sandboxed environment."""
    timeout = min(timeout, int(os.getenv("PYTHON_TOOL_MAX_TIMEOUT_SECONDS", "180")))
    python_bin = shutil.which("python3") or shutil.which("python") or sys.executable

    session = session_id or "default"
    workspace = get_session_workspace(session)
    scripts_dir = workspace / ".runs"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    script_path = (scripts_dir / f"script_{int(time.time() * 1000)}.py").resolve()

    # Write code to file
    script_path.write_text(code, encoding="utf-8")

    start_time = time.time()

    try:
        result = await asyncio.to_thread(
            subprocess.run,
            [python_bin, str(script_path)],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(workspace),
            env={
                "PATH": "/usr/local/bin:/usr/bin:/bin",
                "PYTHONPATH": "",
                "HOME": str(workspace),
                "SESSION_WORKSPACE": str(workspace),
            }
        )

        execution_time = time.time() - start_time

        output_parts = []
        output_parts.append(f"Execution time: {execution_time:.2f}s")
        output_parts.append(f"Workspace: {workspace}")

        if result.stdout:
            output_parts.append(f"\n--- stdout ---\n{result.stdout}")
        if result.stderr:
            output_parts.append(f"\n--- stderr ---\n{result.stderr}")
        if result.returncode != 0:
            output_parts.append(f"\n--- exit code: {result.returncode} ---")
            return "Error: Python execution failed\n" + "\n".join(output_parts)

        if not result.stdout and not result.stderr and result.returncode == 0:
            output_parts.append("\n(No output)")

        return "\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return f"Error: Execution timed out after {timeout} seconds"
    except Exception as e:
        return f"Error executing code: {str(e)}"
