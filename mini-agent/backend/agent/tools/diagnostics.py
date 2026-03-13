from __future__ import annotations

import asyncio
import json
import os
import py_compile
import subprocess
from pathlib import Path
from typing import Any

from backend.agent.tools.project_runner import run_project_command
from backend.agent.tools.workspace import get_session_workspace


MAX_DIAGNOSTIC_ITEMS = int(os.getenv("WORKSPACE_DIAGNOSTIC_MAX_ITEMS", "300"))
MAX_TSC_OUTPUT_CHARS = int(os.getenv("WORKSPACE_TSC_OUTPUT_MAX_CHARS", "12000"))


def _safe_cwd(session_id: str, cwd: str | None) -> Path:
    workspace = get_session_workspace(session_id).resolve()
    if not cwd or cwd.strip() in {"", "."}:
        return workspace
    candidate = (workspace / cwd).resolve()
    if workspace not in candidate.parents and candidate != workspace:
        raise ValueError("cwd escapes session workspace")
    candidate.mkdir(parents=True, exist_ok=True)
    return candidate


def _skip_dir(path: Path) -> bool:
    skip = {
        ".git",
        ".venv",
        "venv",
        "node_modules",
        ".next",
        "__pycache__",
        ".runs",
        ".processes",
    }
    return path.name in skip


def _collect_python_diagnostics(base: Path) -> dict[str, Any]:
    diagnostics: list[dict[str, Any]] = []
    scanned = 0
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if not _skip_dir(Path(root) / d)]
        for name in files:
            if not name.endswith(".py"):
                continue
            file_path = Path(root) / name
            scanned += 1
            try:
                py_compile.compile(str(file_path), doraise=True)
            except py_compile.PyCompileError as exc:
                diagnostics.append(
                    {
                        "tool": "python_compile",
                        "severity": "error",
                        "file": str(file_path.relative_to(base)),
                        "message": str(exc.msg),
                    }
                )
            except Exception as exc:  # pragma: no cover
                diagnostics.append(
                    {
                        "tool": "python_compile",
                        "severity": "error",
                        "file": str(file_path.relative_to(base)),
                        "message": str(exc),
                    }
                )
            if len(diagnostics) >= MAX_DIAGNOSTIC_ITEMS:
                break
        if len(diagnostics) >= MAX_DIAGNOSTIC_ITEMS:
            break
    return {"scanned": scanned, "diagnostics": diagnostics}


async def _collect_tsc_diagnostics(base: Path, timeout: int) -> dict[str, Any]:
    tsconfig = base / "tsconfig.json"
    if not tsconfig.exists():
        return {"scanned": 0, "diagnostics": [], "skipped": "tsconfig.json not found"}

    try:
        result = await asyncio.to_thread(
            subprocess.run,
            ["/bin/sh", "-lc", "npx tsc --noEmit --pretty false"],
            capture_output=True,
            text=True,
            timeout=max(10, min(timeout, 1800)),
            cwd=str(base),
            env={**os.environ, "HOME": str(base)},
        )
        output = (result.stdout or "") + ("\n" + result.stderr if result.stderr else "")
        diagnostics: list[dict[str, Any]] = []
        lowered = output.lower()
        if result.returncode == 127 and ("npx: not found" in lowered or "npx not found" in lowered):
            return {
                "scanned": 0,
                "diagnostics": [],
                "skipped": "npx not available",
                "raw_output_preview": output[:MAX_TSC_OUTPUT_CHARS],
                "exit_code": result.returncode,
            }
        if result.returncode != 0:
            for line in output.splitlines():
                line = line.strip()
                if not line:
                    continue
                diagnostics.append(
                    {
                        "tool": "typescript_tsc",
                        "severity": "error",
                        "message": line,
                    }
                )
                if len(diagnostics) >= MAX_DIAGNOSTIC_ITEMS:
                    break
        return {
            "scanned": 1,
            "diagnostics": diagnostics,
            "raw_output_preview": output[:MAX_TSC_OUTPUT_CHARS],
            "exit_code": result.returncode,
        }
    except FileNotFoundError:
        return {"scanned": 0, "diagnostics": [], "skipped": "npx not available"}
    except subprocess.TimeoutExpired:
        return {"scanned": 1, "diagnostics": [{"tool": "typescript_tsc", "severity": "error", "message": "tsc timeout"}]}
    except Exception as exc:
        return {"scanned": 1, "diagnostics": [{"tool": "typescript_tsc", "severity": "error", "message": str(exc)}]}


async def run_workspace_diagnostics(
    *,
    session_id: str,
    cwd: str | None = None,
    include_python: bool = True,
    include_typescript: bool = True,
    timeout: int = 180,
) -> str:
    """Run workspace diagnostics for Python and TypeScript projects."""
    try:
        base = _safe_cwd(session_id, cwd)
    except ValueError as exc:
        return f"Error: {exc}"

    summary: dict[str, Any] = {
        "ok": True,
        "kind": "workspace_diagnostics",
        "cwd": str(base),
        "python": {"scanned": 0, "diagnostics": [], "skipped": "disabled"},
        "typescript": {"scanned": 0, "diagnostics": [], "skipped": "disabled"},
        "diagnostic_count": 0,
    }

    if include_python:
        py = _collect_python_diagnostics(base)
        summary["python"] = py
    if include_typescript:
        ts = await _collect_tsc_diagnostics(base, timeout)
        summary["typescript"] = ts

    total = len(summary["python"].get("diagnostics", [])) + len(summary["typescript"].get("diagnostics", []))
    summary["diagnostic_count"] = total
    summary["ok"] = total == 0
    return json.dumps(summary, ensure_ascii=False, indent=2)


async def run_playwright_test(
    *,
    session_id: str,
    command: str | None = None,
    cwd: str | None = None,
    timeout: int = 600,
) -> str:
    """Run Playwright tests in workspace (default command: npx playwright test)."""
    cmd = (command or "").strip() or "npx playwright test"
    raw = await run_project_command(
        session_id=session_id,
        command=cmd,
        cwd=cwd,
        timeout=timeout,
    )
    try:
        parsed = json.loads(raw)
    except Exception:
        return raw
    if isinstance(parsed, dict):
        parsed["kind"] = "playwright_test"
        parsed["playwright_command"] = cmd
    return json.dumps(parsed, ensure_ascii=False, indent=2)
