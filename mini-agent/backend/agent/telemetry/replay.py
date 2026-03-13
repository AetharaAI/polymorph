from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class SessionReplayLogger:
    """Append-only JSONL event logger for per-session replay/debugging."""

    def __init__(self, session_id: str, enabled: bool = True, base_dir: str | Path = "backend/replays"):
        self.enabled = enabled
        self.session_id = session_id
        self.base_dir = Path(base_dir)
        self.file_path: Path | None = None

        if self.enabled:
            ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            session_dir = self.base_dir / session_id
            session_dir.mkdir(parents=True, exist_ok=True)
            self.file_path = session_dir / f"run-{ts}.jsonl"

    async def log(self, event_type: str, payload: dict[str, Any]) -> None:
        if not self.enabled or not self.file_path:
            return

        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "event": event_type,
            "payload": payload,
        }

        line = json.dumps(entry, ensure_ascii=True) + "\n"

        def _write() -> None:
            with self.file_path.open("a", encoding="utf-8") as f:
                f.write(line)

        await asyncio.to_thread(_write)

    def metadata(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "path": str(self.file_path) if self.file_path else None,
        }
