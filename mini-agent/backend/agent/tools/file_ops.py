import os
import io
import json
import asyncio
import base64
import hashlib
import secrets
import aiofiles
from pathlib import Path
from datetime import datetime
from typing import Any

from backend.agent.tools.artifact_validator import validate_artifact
from backend.agent.tools.workspace import get_session_workspace

# Canonical artifact root anchored to the repo package, not process cwd.
UPLOAD_DIR = (Path(__file__).resolve().parents[3] / "uploads").resolve()
TEXT_EXTENSIONS = {".txt", ".md", ".py", ".js", ".ts", ".json", ".csv", ".yaml", ".yml", ".html", ".xml", ".sh"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}
IMAGE_MIME_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".bmp": "image/bmp",
}
MCP_ARTIFACT_MAX_BYTES = int(os.getenv("MCP_ARTIFACT_MAX_BYTES", str(50 * 1024 * 1024)))
MCP_ARTIFACT_ALLOWED_ROOTS_RAW = os.getenv(
    "MCP_ARTIFACT_ALLOWED_ROOTS",
    "/aether-data,uploads,backend/uploads",
)


def _get_session_dir(session_id: str) -> Path:
    """Get or create the session directory."""
    session_dir = UPLOAD_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir


def _generate_file_id(filename: str, session_id: str) -> str:
    """Generate a unique file ID."""
    raw = f"{session_id}:{filename}:{os.urandom(8).hex()}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def _find_file_path(file_id: str) -> Path | None:
    """Find a stored file path by file_id across all session directories."""
    if not UPLOAD_DIR.exists():
        return None

    for session_dir in UPLOAD_DIR.iterdir():
        if not session_dir.is_dir():
            continue
        for file_path in session_dir.iterdir():
            if file_path.is_file() and file_path.name.startswith(file_id):
                return file_path
    return None


def _path_is_under(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except Exception:
        return False


def _artifact_allowed_roots() -> list[Path]:
    roots: list[Path] = []
    for raw in MCP_ARTIFACT_ALLOWED_ROOTS_RAW.split(","):
        candidate = raw.strip()
        if not candidate:
            continue
        root = Path(candidate)
        if not root.is_absolute():
            root = Path.cwd() / root
        roots.append(root.resolve(strict=False))
    return roots


async def save_uploaded_file(session_id: str, filename: str, content: bytes) -> dict:
    """Save an uploaded file and return its metadata."""
    file_id = _generate_file_id(filename, session_id)
    session_dir = _get_session_dir(session_id)

    # Determine file extension for text extraction
    ext = Path(filename).suffix.lower()

    # For text files, save directly
    is_text = ext in TEXT_EXTENSIONS

    if is_text:
        file_path = session_dir / f"{file_id}_{filename}"
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)
    else:
        # For binary files, just save as-is
        file_path = session_dir / f"{file_id}_{filename}"
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)

    # Extract text content for supported file types
    text_content = None
    if ext == ".pdf":
        try:
            import fitz
            doc = fitz.open(stream=content, filetype="pdf")
            text_content = ""
            for page in doc:
                text_content += page.get_text()
            doc.close()
        except Exception:
            pass
    elif ext == ".docx":
        try:
            from docx import Document
            doc = Document(io.BytesIO(content))
            text_content = "\n".join([p.text for p in doc.paragraphs])
        except Exception:
            pass
    elif is_text:
        try:
            text_content = content.decode("utf-8")
        except Exception:
            pass

    return {
        "file_id": file_id,
        "filename": filename,
        "size": len(content),
        "content_type": ext[1:] if ext else "binary",
        "text_content": text_content,
        "timestamp": int(datetime.now().timestamp() * 1000)
    }


def _normalize_workspace_target(
    session_id: str,
    filename: str,
    workspace_path: str | None,
) -> tuple[str, Path | None]:
    normalized_filename = (filename or "").strip()
    inferred_workspace_path = workspace_path

    if not inferred_workspace_path and any(sep in normalized_filename for sep in ("/", "\\")):
        inferred_workspace_path = normalized_filename
        normalized_filename = Path(normalized_filename.replace("\\", "/")).name

    normalized_filename = normalized_filename or "artifact.txt"

    if not inferred_workspace_path or not str(inferred_workspace_path).strip():
        return normalized_filename, None

    raw_target = str(inferred_workspace_path).replace("\\", "/").strip()
    if raw_target.startswith("file://"):
        raw_target = raw_target[7:]

    workspace_root = get_session_workspace(session_id).resolve()
    target_candidate = Path(raw_target)
    if target_candidate.is_absolute():
        try:
            target_candidate = target_candidate.resolve().relative_to(workspace_root)
        except Exception:
            target_candidate = Path(target_candidate.name)

    target_path = (workspace_root / target_candidate).resolve()
    if workspace_root not in target_path.parents and target_path != workspace_root:
        raise ValueError("workspace_path escapes session workspace")

    return normalized_filename, target_path


async def _atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.parent / f".{path.name}.{secrets.token_hex(6)}.tmp"
    try:
        async with aiofiles.open(tmp_path, "w", encoding="utf-8") as handle:
            await handle.write(content)
        await asyncio.to_thread(os.replace, tmp_path, path)
    finally:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except FileNotFoundError:
                pass


async def _verify_text_file(path: Path, expected_content: str) -> dict[str, Any]:
    if not path.exists() or not path.is_file():
        return {
            "exists": False,
            "matches_expected": False,
            "size": 0,
            "sha256": None,
        }

    observed = await asyncio.to_thread(path.read_text, encoding="utf-8")
    digest = hashlib.sha256(observed.encode("utf-8")).hexdigest()
    return {
        "exists": True,
        "matches_expected": observed == expected_content,
        "size": len(observed),
        "sha256": digest,
    }


async def read_file(file_id: str, max_chars: int = 50000) -> str:
    """Read file content by file_id."""
    file_path = _find_file_path(file_id)
    if not file_path:
        return "Error: File not found"

    try:
        content = file_path.read_text(encoding="utf-8")
        if len(content) > max_chars:
            return content[:max_chars] + f"\n\n[Truncated - showing first {max_chars} characters]"
        return content
    except UnicodeDecodeError:
        return f"Binary file: {file_path.name}\nSize: {file_path.stat().st_size} bytes\n\n(Use execute_python to process this binary file)"
    except Exception as e:
        return f"Error reading file: {str(e)}"


async def list_files(session_id: str) -> str:
    """List all files for a session."""
    session_dir = _get_session_dir(session_id)

    files = []
    for file_path in session_dir.iterdir():
        if file_path.is_file():
            # Extract original filename from stored name
            parts = file_path.name.split("_", 1)
            original_name = parts[1] if len(parts) > 1 else file_path.name
            files.append({
                "file_id": parts[0] if len(parts) > 1 else file_path.stem,
                "filename": original_name,
                "size": file_path.stat().st_size
            })

    if not files:
        return json.dumps([], indent=2)

    return json.dumps(files, indent=2)


async def write_file(
    filename: str,
    content: str,
    session_id: str,
    workspace_path: str | None = None,
) -> str:
    """Write content to artifact storage and optionally mirror to session workspace.

    Contract:
    - One logical write creates one artifact entry under UPLOAD_DIR/session_id.
    - Optional workspace mirroring is written atomically into the session workspace.
    - Success is only reported after post-write verification of every requested target.
    """
    try:
        normalized_filename, workspace_target_path = _normalize_workspace_target(
            session_id=session_id,
            filename=filename,
            workspace_path=workspace_path,
        )
    except ValueError as exc:
        return f"Error: {exc}"

    file_id = _generate_file_id(normalized_filename, session_id)
    session_dir = _get_session_dir(session_id)
    file_path = session_dir / f"{file_id}_{normalized_filename}"

    await _atomic_write_text(file_path, content)
    if workspace_target_path is not None:
        await _atomic_write_text(workspace_target_path, content)

    validation = validate_artifact(filename=normalized_filename, content=content)
    artifact_verification = await _verify_text_file(file_path, content)
    workspace_verification = None
    if workspace_target_path is not None:
        workspace_verification = await _verify_text_file(workspace_target_path, content)

    verified = artifact_verification["matches_expected"] and (
        workspace_verification is None or workspace_verification["matches_expected"]
    )
    status = "ok" if verified else "error"
    warnings: list[str] = []
    if not artifact_verification["matches_expected"]:
        warnings.append("artifact verification failed")
    if workspace_verification is not None and not workspace_verification["matches_expected"]:
        warnings.append("workspace verification failed")

    return json.dumps({
        "status": status,
        "file_id": file_id,
        "filename": normalized_filename,
        "size": len(content),
        "path": str(file_path.resolve()),
        "workspace_written": workspace_target_path is not None,
        "workspace_path": str(workspace_target_path) if workspace_target_path is not None else None,
        "verified": verified,
        "verification": {
            "artifact": artifact_verification,
            "workspace": workspace_verification,
        },
        "warnings": warnings,
        "timestamp": int(datetime.now().timestamp() * 1000),
        "validation": validation,
    }, indent=2)


async def import_external_artifact(
    session_id: str,
    source_path: str,
    filename: str | None = None,
) -> dict[str, Any] | None:
    """Import an externally-written file into the session uploads namespace.

    This is used for MCP filesystem writes so the UI can render/download them
    through the existing `/api/files/download/{file_id}` route.
    """
    if not source_path:
        return None

    raw_path = source_path.strip()
    if raw_path.startswith("file://"):
        raw_path = raw_path[7:]
    source = Path(raw_path)
    if not source.is_absolute():
        source = Path.cwd() / source

    try:
        resolved = source.resolve(strict=True)
    except Exception:
        return None

    if not resolved.is_file():
        return None

    allowed_roots = _artifact_allowed_roots()
    if allowed_roots and not any(_path_is_under(resolved, root) for root in allowed_roots):
        return None

    size = resolved.stat().st_size
    if size > MCP_ARTIFACT_MAX_BYTES:
        return None

    blob = await asyncio.to_thread(resolved.read_bytes)
    target_name = (filename or resolved.name).strip() or resolved.name
    file_info = await save_uploaded_file(session_id=session_id, filename=target_name, content=blob)
    stored_path = _get_session_dir(session_id) / f"{file_info['file_id']}_{target_name}"

    validation = None
    text_content = file_info.get("text_content")
    if isinstance(text_content, str):
        validation = validate_artifact(filename=target_name, content=text_content)

    return {
        "file_id": file_info.get("file_id"),
        "filename": target_name,
        "size": file_info.get("size", size),
        "path": str(stored_path),
        "timestamp": file_info.get("timestamp", int(datetime.now().timestamp() * 1000)),
        "validation": validation,
        "source": "mcp",
        "source_path": str(resolved),
    }


async def get_file_text(file_id: str) -> str | None:
    """Get text content of a file for context."""
    return await read_file(file_id, max_chars=50000)


async def get_file_prompt_blocks(file_id: str, include_images: bool = True, max_chars: int = 50000) -> list[dict[str, Any]]:
    """Build model-ready message blocks for a given uploaded file."""
    file_path = _find_file_path(file_id)
    if not file_path:
        return []

    stored_name = file_path.name
    parts = stored_name.split("_", 1)
    original_name = parts[1] if len(parts) > 1 else stored_name
    ext = Path(original_name).suffix.lower()

    if include_images and ext in IMAGE_EXTENSIONS:
        try:
            raw = file_path.read_bytes()
            max_inline = int(os.getenv("MAX_INLINE_IMAGE_BYTES", "5242880"))
            if len(raw) > max_inline:
                return [{
                    "type": "text",
                    "text": (
                        f"[Image {original_name} too large to inline "
                        f"({len(raw)} bytes > {max_inline} bytes)]"
                    ),
                }]

            mime = IMAGE_MIME_TYPES.get(ext, "image/png")
            data_uri = f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"
            return [
                {"type": "text", "text": f"[Image attachment: {original_name}]"},
                {"type": "image_url", "image_url": {"url": data_uri}},
            ]
        except Exception as exc:
            return [{"type": "text", "text": f"[Failed to load image {original_name}: {exc}]"}]

    text = await read_file(file_id=file_id, max_chars=max_chars)
    if text and not text.startswith("Error:"):
        return [{"type": "text", "text": f"[File content from {original_name}]:\n{text}"}]
    return [{"type": "text", "text": f"[Unable to read file {original_name}]"}]
