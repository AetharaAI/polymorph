from __future__ import annotations

import asyncio
import json
import os
import signal
import subprocess
import time
import uuid
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx

from backend.agent.tools.workspace import get_session_workspace


DEFAULT_COMMAND_TIMEOUT = int(os.getenv("PROJECT_COMMAND_TIMEOUT_SECONDS", "300"))
DEFAULT_HTTP_TIMEOUT = float(os.getenv("PROJECT_HTTP_TIMEOUT_SECONDS", "20"))
MAX_OUTPUT_CHARS = int(os.getenv("PROJECT_RUNNER_MAX_OUTPUT_CHARS", "8000"))
MAX_LOG_LINES = int(os.getenv("PROJECT_RUNNER_MAX_LOG_LINES", "2000"))


def _trim(text: str, max_chars: int = MAX_OUTPUT_CHARS) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + f"\n...[truncated {len(text) - max_chars} chars]"


def _safe_cwd(session_id: str, cwd: str | None) -> Path:
    workspace = get_session_workspace(session_id)
    if not cwd or cwd.strip() in {".", ""}:
        return workspace

    candidate = (workspace / cwd).resolve()
    workspace_resolved = workspace.resolve()
    if workspace_resolved not in candidate.parents and candidate != workspace_resolved:
        raise ValueError("cwd escapes session workspace")
    candidate.mkdir(parents=True, exist_ok=True)
    return candidate


@dataclass
class ProcessHandle:
    process_id: str
    session_id: str
    command: str
    cwd: str
    pid: int
    started_at: float
    log_path: Path


_PROCESS_REGISTRY: dict[str, ProcessHandle] = {}
_PROCESS_LOCK = asyncio.Lock()


async def run_project_command(
    *,
    session_id: str,
    command: str,
    cwd: str | None = None,
    timeout: int = DEFAULT_COMMAND_TIMEOUT,
) -> str:
    """Run a project command synchronously in session workspace and return structured result JSON."""
    command = (command or "").strip()
    if not command:
        return "Error: run_project_command requires 'command'"

    try:
        safe_cwd = _safe_cwd(session_id, cwd)
    except ValueError as exc:
        return f"Error: {exc}"

    timeout = max(1, min(int(timeout), 1800))
    started = time.time()
    try:
        result = await asyncio.to_thread(
            subprocess.run,
            ["/bin/sh", "-lc", command],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(safe_cwd),
            env={**os.environ, "HOME": str(safe_cwd), "SESSION_WORKSPACE": str(get_session_workspace(session_id))},
        )
        payload = {
            "ok": result.returncode == 0,
            "kind": "project_command",
            "command": command,
            "cwd": str(safe_cwd),
            "exit_code": result.returncode,
            "duration_ms": int((time.time() - started) * 1000),
            "stdout": _trim(result.stdout or ""),
            "stderr": _trim(result.stderr or ""),
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)
    except subprocess.TimeoutExpired as exc:
        payload = {
            "ok": False,
            "kind": "project_command",
            "command": command,
            "cwd": str(safe_cwd),
            "exit_code": None,
            "duration_ms": int((time.time() - started) * 1000),
            "timeout_seconds": timeout,
            "stdout": _trim((exc.stdout or "") if isinstance(exc.stdout, str) else ""),
            "stderr": _trim((exc.stderr or "") if isinstance(exc.stderr, str) else ""),
            "error": f"Command timed out after {timeout} seconds",
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)
    except Exception as exc:
        return f"Error: run_project_command failed: {exc}"


def _auto_test_command(workspace: Path) -> str:
    if (workspace / "pytest.ini").exists() or (workspace / "pyproject.toml").exists():
        return "pytest -q"
    if (workspace / "requirements.txt").exists() and (workspace / "tests").exists():
        return "pytest -q"
    if (workspace / "package.json").exists():
        return "npm test -- --runInBand"
    return "ls -la"


async def run_tests(
    *,
    session_id: str,
    command: str | None = None,
    cwd: str | None = None,
    timeout: int = DEFAULT_COMMAND_TIMEOUT,
) -> str:
    """Run test command in workspace. Auto-selects a default command when omitted."""
    try:
        safe_cwd = _safe_cwd(session_id, cwd)
    except ValueError as exc:
        return f"Error: {exc}"

    test_cmd = (command or "").strip() or _auto_test_command(safe_cwd)
    raw = await run_project_command(
        session_id=session_id,
        command=test_cmd,
        cwd=str(safe_cwd.relative_to(get_session_workspace(session_id))),
        timeout=timeout,
    )
    parsed: Any
    try:
        parsed = json.loads(raw)
    except Exception:
        return raw

    if isinstance(parsed, dict):
        parsed["kind"] = "test_run"
        parsed["test_command"] = test_cmd
    return json.dumps(parsed, ensure_ascii=False, indent=2)


async def http_check(
    *,
    url: str,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    body: str | None = None,
    timeout_seconds: float = DEFAULT_HTTP_TIMEOUT,
    expect_status: int | None = None,
) -> str:
    """Issue HTTP request and return structured response preview."""
    method_upper = (method or "GET").upper()
    if method_upper not in {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}:
        return f"Error: Unsupported method '{method_upper}'"
    if not (url or "").strip().startswith(("http://", "https://")):
        return "Error: http_check requires absolute http(s) URL"

    started = time.time()
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(timeout_seconds)) as client:
            resp = await client.request(
                method_upper,
                url.strip(),
                headers=headers or None,
                content=body.encode("utf-8") if isinstance(body, str) else None,
            )
        elapsed = int((time.time() - started) * 1000)
        payload = {
            "ok": (expect_status is None and 200 <= resp.status_code < 400)
            or (expect_status is not None and resp.status_code == expect_status),
            "kind": "http_check",
            "url": url.strip(),
            "method": method_upper,
            "status_code": resp.status_code,
            "elapsed_ms": elapsed,
            "expect_status": expect_status,
            "headers": dict(resp.headers),
            "body_preview": _trim(resp.text or ""),
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)
    except Exception as exc:
        payload = {
            "ok": False,
            "kind": "http_check",
            "url": url.strip(),
            "method": method_upper,
            "elapsed_ms": int((time.time() - started) * 1000),
            "error": str(exc),
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)


def _registry_snapshot_for_session(session_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for handle in _PROCESS_REGISTRY.values():
        if handle.session_id != session_id:
            continue
        alive = _is_process_alive(handle)
        rows.append(
            {
                "process_id": handle.process_id,
                "command": handle.command,
                "cwd": handle.cwd,
                "pid": handle.pid,
                "started_at": int(handle.started_at * 1000),
                "alive": alive,
                "log_path": str(handle.log_path),
            }
        )
    rows.sort(key=lambda r: r["started_at"], reverse=True)
    return rows


def _is_process_alive(handle: ProcessHandle) -> bool:
    try:
        os.kill(handle.pid, 0)
        return True
    except OSError:
        return False


async def start_process(
    *,
    session_id: str,
    command: str,
    cwd: str | None = None,
    name: str | None = None,
) -> str:
    """Start a background process in session workspace and capture logs to a file."""
    command = (command or "").strip()
    if not command:
        return "Error: start_process requires 'command'"

    try:
        safe_cwd = _safe_cwd(session_id, cwd)
    except ValueError as exc:
        return f"Error: {exc}"

    processes_dir = get_session_workspace(session_id) / ".processes"
    processes_dir.mkdir(parents=True, exist_ok=True)

    process_id = (name or "").strip() or f"proc_{uuid.uuid4().hex[:12]}"
    process_id = process_id.replace(" ", "_")
    async with _PROCESS_LOCK:
        existing = _PROCESS_REGISTRY.get(process_id)
    if existing and _is_process_alive(existing):
        return f"Error: process_id '{process_id}' already exists and is running"

    log_path = processes_dir / f"{process_id}.log"

    try:
        log_file = open(log_path, "a", encoding="utf-8")
        proc = subprocess.Popen(
            ["/bin/sh", "-lc", command],
            cwd=str(safe_cwd),
            stdout=log_file,
            stderr=log_file,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
            env={**os.environ, "HOME": str(safe_cwd), "SESSION_WORKSPACE": str(get_session_workspace(session_id))},
            text=True,
        )
        log_file.close()
        handle = ProcessHandle(
            process_id=process_id,
            session_id=session_id,
            command=command,
            cwd=str(safe_cwd),
            pid=proc.pid,
            started_at=time.time(),
            log_path=log_path,
        )
        async with _PROCESS_LOCK:
            _PROCESS_REGISTRY[process_id] = handle
        payload = {
            "ok": True,
            "kind": "process_start",
            "process_id": process_id,
            "pid": proc.pid,
            "command": command,
            "cwd": str(safe_cwd),
            "log_path": str(log_path),
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)
    except Exception as exc:
        return f"Error: start_process failed: {exc}"


async def list_processes(*, session_id: str) -> str:
    """List tracked processes for a session."""
    async with _PROCESS_LOCK:
        rows = _registry_snapshot_for_session(session_id)
    payload = {"ok": True, "kind": "process_list", "session_id": session_id, "processes": rows}
    return json.dumps(payload, ensure_ascii=False, indent=2)


async def stop_process(*, session_id: str, process_id: str, force: bool = False) -> str:
    """Stop tracked process by id."""
    process_id = (process_id or "").strip()
    if not process_id:
        return "Error: stop_process requires 'process_id'"

    async with _PROCESS_LOCK:
        handle = _PROCESS_REGISTRY.get(process_id)
    if not handle or handle.session_id != session_id:
        return f"Error: process '{process_id}' not found for session"

    if not _is_process_alive(handle):
        async with _PROCESS_LOCK:
            _PROCESS_REGISTRY.pop(process_id, None)
        payload = {"ok": True, "kind": "process_stop", "process_id": process_id, "already_stopped": True}
        return json.dumps(payload, ensure_ascii=False, indent=2)

    try:
        sig = signal.SIGKILL if force else signal.SIGTERM
        os.killpg(handle.pid, sig)
        if not force:
            await asyncio.sleep(0.4)
            if _is_process_alive(handle):
                os.killpg(handle.pid, signal.SIGKILL)
        async with _PROCESS_LOCK:
            _PROCESS_REGISTRY.pop(process_id, None)
        payload = {"ok": True, "kind": "process_stop", "process_id": process_id, "forced": force}
        return json.dumps(payload, ensure_ascii=False, indent=2)
    except Exception as exc:
        return f"Error: stop_process failed: {exc}"


async def read_process_logs(
    *,
    session_id: str,
    process_id: str,
    tail_lines: int = 200,
) -> str:
    """Read tail log lines for a tracked process."""
    process_id = (process_id or "").strip()
    if not process_id:
        return "Error: read_process_logs requires 'process_id'"

    async with _PROCESS_LOCK:
        handle = _PROCESS_REGISTRY.get(process_id)

    if not handle or handle.session_id != session_id:
        return f"Error: process '{process_id}' not found for session"
    if not handle.log_path.exists():
        return f"Error: log file missing for process '{process_id}'"

    try:
        tail_lines = max(10, min(int(tail_lines), MAX_LOG_LINES))
        text = handle.log_path.read_text(encoding="utf-8", errors="ignore")
        dq = deque(text.splitlines(), maxlen=tail_lines)
        payload = {
            "ok": True,
            "kind": "process_logs",
            "process_id": process_id,
            "alive": _is_process_alive(handle),
            "tail_lines": tail_lines,
            "logs": "\n".join(dq),
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)
    except Exception as exc:
        return f"Error: read_process_logs failed: {exc}"
