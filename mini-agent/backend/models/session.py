"""
DEPRECATED: Session management is now handled by the MemoryService using Redis.
This module is kept for backwards compatibility but should not be used.
"""
import uuid
import warnings

warnings.warn(
    "backend.models.session is deprecated. Use backend.memory.get_memory_service() instead.",
    DeprecationWarning,
    stacklevel=2
)

# In-memory session storage (DEPRECATED - only used as fallback)
sessions: dict[str, list] = {}


def get_history(session_id: str) -> list:
    """Get conversation history for a session. DEPRECATED - use MemoryService."""
    return sessions.get(session_id, [])


def add_message(session_id: str, message: dict) -> None:
    """Add a message to the session history. DEPRECATED - use MemoryService."""
    if session_id not in sessions:
        sessions[session_id] = []
    sessions[session_id].append(message)


def clear_session(session_id: str) -> None:
    """Clear a session's history. DEPRECATED - use MemoryService."""
    if session_id in sessions:
        sessions[session_id] = []


def create_session() -> str:
    """Create a new session and return its ID. DEPRECATED - use MemoryService."""
    session_id = str(uuid.uuid4())
    sessions[session_id] = []
    return session_id


def get_or_create_session(session_id: str | None = None) -> str:
    """Get existing session or create new one. DEPRECATED - use MemoryService."""
    if session_id and session_id in sessions:
        return session_id
    return create_session()
