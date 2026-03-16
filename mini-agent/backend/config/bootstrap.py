from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv

_LOADED = False


def load_harness_env() -> None:
    """Load the canonical env stack in a deterministic order.

    Later files intentionally override earlier ones:
    1. `mini-agent/.env`
    2. `mini-agent/backend/.env`
    3. `mini-agent/.env.polymorph`

    `.env.legacy` is reference-only and is not loaded automatically.
    """

    global _LOADED
    if _LOADED:
        return

    root = Path(__file__).resolve().parents[2]
    env_paths = [
        root / ".env",
        root / "backend" / ".env",
        root / ".env.polymorph",
    ]

    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(env_path, override=True)

    _LOADED = True
