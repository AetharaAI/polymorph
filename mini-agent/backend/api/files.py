import os
import json
import base64
import mimetypes
import tempfile
import zipfile
import sys
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.agent.tools import file_ops
from backend.models.schemas import FileUploadResponse

router = APIRouter()

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Supported extensions
SUPPORTED_EXTENSIONS = {
    ".txt", ".md", ".py", ".js", ".ts", ".json", ".csv", ".yaml", ".yml",
    ".html", ".xml", ".sh", ".pdf", ".docx",
    ".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"
}
TEXT_PREVIEW_EXTENSIONS = {
    ".txt", ".md", ".py", ".js", ".ts", ".json", ".csv", ".yaml", ".yml",
    ".html", ".xml", ".sh", ".log"
}
IMAGE_PREVIEW_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}
MAX_TEXT_PREVIEW_CHARS = int(os.getenv("MAX_TEXT_PREVIEW_CHARS", "200000"))
MAX_IMAGE_PREVIEW_BYTES = int(os.getenv("MAX_IMAGE_PREVIEW_BYTES", str(8 * 1024 * 1024)))


@router.post("/files/upload")
async def upload_file(
    session_id: str = Form(...),
    file: UploadFile = File(...)
):
    """Upload a file."""
    # Validate file size
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)

    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail=f"File too large. Max size: 50MB")

    # Validate extension
    ext = Path(file.filename).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Supported: {', '.join(SUPPORTED_EXTENSIONS)}"
        )

    # Read file content
    content = await file.read()

    # Save file
    try:
        file_info = await file_ops.save_uploaded_file(session_id, file.filename, content)
        return JSONResponse(content=file_info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/files/{session_id}")
async def list_files(session_id: str):
    """List all files for a session."""
    try:
        files = await file_ops.list_files(session_id)
        try:
            parsed = json.loads(files)
            if not isinstance(parsed, list):
                parsed = []
        except json.JSONDecodeError:
            parsed = []
        return JSONResponse(content={"files": parsed})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/files/{file_id}")
async def delete_file(file_id: str, session_id: str):
    """Delete a file."""
    # This is a placeholder - we would need to implement file deletion
    raise HTTPException(status_code=501, detail="Delete not implemented")


@router.get("/files/download/{file_id}")
async def download_file(file_id: str):
    """Download a file by file_id."""
    # Find the file in any session directory
    uploads_dir = file_ops.UPLOAD_DIR
    if not uploads_dir.exists():
        raise HTTPException(status_code=404, detail="File not found")

    for session_dir in uploads_dir.iterdir():
        if not session_dir.is_dir():
            continue
        for file_path in session_dir.iterdir():
            if file_path.is_file() and file_path.name.startswith(file_id):
                return FileResponse(
                    path=str(file_path),
                    filename=file_path.name.split("_", 1)[1] if "_" in file_path.name else file_path.name,
                    media_type="application/octet-stream"
                )

    raise HTTPException(status_code=404, detail="File not found")


@router.get("/files/download-session/{session_id}")
async def download_session_files(session_id: str, background_tasks: BackgroundTasks):
    """Download all files for a session as a zip archive."""
    uploads_dir = file_ops.UPLOAD_DIR
    session_dir = uploads_dir / session_id
    if not session_dir.exists() or not session_dir.is_dir():
        raise HTTPException(status_code=404, detail="Session has no files")

    files = [p for p in session_dir.iterdir() if p.is_file()]
    if not files:
        raise HTTPException(status_code=404, detail="Session has no files")

    tmp = tempfile.NamedTemporaryFile(prefix=f"{session_id}_", suffix=".zip", delete=False)
    tmp_path = Path(tmp.name)
    tmp.close()

    with zipfile.ZipFile(tmp_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        used_names: set[str] = set()
        for file_path in sorted(files):
            parts = file_path.name.split("_", 1)
            file_id = parts[0] if len(parts) > 1 else file_path.stem
            original_name = parts[1] if len(parts) > 1 else file_path.name
            arcname = original_name
            if arcname in used_names:
                arcname = f"{file_id}_{original_name}"
            used_names.add(arcname)
            zf.write(file_path, arcname=arcname)

    background_tasks.add_task(tmp_path.unlink, missing_ok=True)
    return FileResponse(
        path=str(tmp_path),
        filename=f"{session_id}_files.zip",
        media_type="application/zip",
    )


@router.get("/files/view/{file_id}")
async def view_file(file_id: str, max_chars: int = Query(default=MAX_TEXT_PREVIEW_CHARS, ge=1000, le=500000)):
    """Return an inline preview payload for text/image files."""
    file_path = file_ops._find_file_path(file_id)  # noqa: SLF001 - internal helper reuse
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found")

    parts = file_path.name.split("_", 1)
    filename = parts[1] if len(parts) > 1 else file_path.name
    ext = Path(filename).suffix.lower()
    size = file_path.stat().st_size
    mime_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

    if ext in IMAGE_PREVIEW_EXTENSIONS:
        if size > MAX_IMAGE_PREVIEW_BYTES:
            return JSONResponse(
                content={
                    "file_id": file_id,
                    "filename": filename,
                    "kind": "image",
                    "mime_type": mime_type,
                    "size": size,
                    "truncated": True,
                    "message": f"Image too large for inline preview ({size} bytes).",
                }
            )
        raw = file_path.read_bytes()
        data_url = f"data:{mime_type};base64,{base64.b64encode(raw).decode('ascii')}"
        return JSONResponse(
            content={
                "file_id": file_id,
                "filename": filename,
                "kind": "image",
                "mime_type": mime_type,
                "size": size,
                "data_url": data_url,
            }
        )

    if ext in TEXT_PREVIEW_EXTENSIONS:
        content = file_path.read_text(encoding="utf-8", errors="replace")
        truncated = False
        if len(content) > max_chars:
            content = content[:max_chars]
            truncated = True
        return JSONResponse(
            content={
                "file_id": file_id,
                "filename": filename,
                "kind": "text",
                "mime_type": mime_type,
                "size": size,
                "text": content,
                "truncated": truncated,
            }
        )

    return JSONResponse(
        content={
            "file_id": file_id,
            "filename": filename,
            "kind": "binary",
            "mime_type": mime_type,
            "size": size,
            "message": "No inline preview available for this file type.",
        }
    )
