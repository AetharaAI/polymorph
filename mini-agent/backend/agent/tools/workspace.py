from __future__ import annotations

import re
from pathlib import Path


WORKSPACE_ROOT = Path("./workspaces")


def _sanitize_session_id(session_id: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_.-]+", "-", (session_id or "").strip())
    return cleaned[:96] or "default"


def get_session_workspace(session_id: str) -> Path:
    WORKSPACE_ROOT.mkdir(parents=True, exist_ok=True)
    workspace = WORKSPACE_ROOT / _sanitize_session_id(session_id)
    workspace.mkdir(parents=True, exist_ok=True)
    return workspace.resolve()
