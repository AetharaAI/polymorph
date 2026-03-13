from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException

router = APIRouter()

REPLAY_ROOT = Path("backend/replays")


@router.get("/replay/{session_id}")
async def list_replays(session_id: str):
    session_dir = REPLAY_ROOT / session_id
    if not session_dir.exists() or not session_dir.is_dir():
        return {"session_id": session_id, "runs": []}

    runs = []
    for path in sorted(session_dir.glob("*.jsonl"), reverse=True):
        runs.append(
            {
                "filename": path.name,
                "path": str(path),
                "size": path.stat().st_size,
                "modified": int(path.stat().st_mtime * 1000),
            }
        )

    return {"session_id": session_id, "runs": runs}


@router.get("/replay/{session_id}/{filename}")
async def read_replay(session_id: str, filename: str):
    if "/" in filename or ".." in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    path = REPLAY_ROOT / session_id / filename
    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail="Replay file not found")

    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return {
        "session_id": session_id,
        "filename": filename,
        "line_count": len(lines),
        "events": lines,
    }
