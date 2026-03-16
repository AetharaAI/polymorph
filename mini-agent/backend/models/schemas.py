from pydantic import BaseModel, Field
from typing import Optional


class ChatAudioInputPayload(BaseModel):
    data: Optional[str] = None
    format: str = "wav"
    filename: Optional[str] = None
    mime_type: Optional[str] = None
    duration_ms: Optional[int] = None


class ChatAudioUrlPayload(BaseModel):
    url: str
    filename: Optional[str] = None
    mime_type: Optional[str] = None
    duration_ms: Optional[int] = None


class ChatRequest(BaseModel):
    session_id: str
    message: str
    file_ids: list[str] = Field(default_factory=list)
    reasoning_mode: Optional[str] = None
    audio_input: Optional[ChatAudioInputPayload] = None
    audio_url: Optional[ChatAudioUrlPayload] = None


class ChatResponse(BaseModel):
    session_id: str
    message: str


class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    size: int
    content_type: str


class FileInfo(BaseModel):
    file_id: str
    filename: str
    size: int


class SessionListResponse(BaseModel):
    sessions: list[str]
