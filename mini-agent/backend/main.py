import os
import sys
import time
from pathlib import Path
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.agent.providers import provider_metadata, validate_provider_config
from backend.agent.tools.health_check import run_tool_health_checks
from backend.api import audio, chat, connections, files, health, replay, sessions, voice
from backend.config import apply_runtime_overrides_to_env
from backend.memory import get_memory_service

# Load environment variables
load_dotenv()
apply_runtime_overrides_to_env()

provider_ok, provider_detail = validate_provider_config()
if not provider_ok:
    raise ValueError(provider_detail)


def _parse_cors_origins() -> list[str]:
    """Parse comma-separated CORS origins from env."""
    raw = os.getenv("CORS_ALLOWED_ORIGINS", "")
    if not raw.strip():
        return []
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


# Global memory service reference
memory = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    global memory

    # Startup: Initialize memory service
    print("[Startup] Initializing memory service...")
    memory = await get_memory_service()
    print("[Startup] Memory service ready")

    print("[Startup] Running tool health checks...")
    app.state.started_at = time.time()
    tool_health = await run_tool_health_checks()
    app.state.tool_health = tool_health
    print(f"[Startup] Tool health: {tool_health['status']} ({tool_health['healthy_count']}/{tool_health['total']})")

    app.state.provider = provider_metadata()
    requested = app.state.provider.get("requested", {})
    actual = app.state.provider.get("actual", {})
    overrides = app.state.provider.get("runtime_overrides", {})
    print(
        "[Startup] Provider requested="
        f"{requested.get('provider')}:{requested.get('model')} "
        "actual="
        f"{actual.get('provider')}:{actual.get('model')} "
        f"runtime_overrides={overrides.get('keys', [])}"
    )

    yield

    # Shutdown: Close memory service
    print("[Shutdown] Closing memory service...")
    if memory:
        await memory.close()
    print("[Shutdown] Done")


app = FastAPI(title="AetherOps Agentic Harness API", version="1.0.0", lifespan=lifespan)

# CORS middleware
cors_origins = _parse_cors_origins()
cors_origin_regex = os.getenv("CORS_ALLOWED_ORIGIN_REGEX")

# Default: allow localhost/127.0.0.1 from any port (docker/dev friendly).
if not cors_origins and not cors_origin_regex:
    cors_origin_regex = r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$"

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_origin_regex=cors_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(files.router, prefix="/api", tags=["files"])
app.include_router(replay.router, prefix="/api", tags=["replay"])
app.include_router(sessions.router, prefix="/api", tags=["sessions"])
app.include_router(audio.router, prefix="/api", tags=["audio"])
app.include_router(connections.router, prefix="/api", tags=["connections"])
app.include_router(voice.router, prefix="/api", tags=["voice"])


@app.get("/")
async def root():
    return {"message": "AetherOps Agentic Harness API", "version": "1.0.0"}
