function resolveBackendUrl(): string {
  if (process.env.NEXT_PUBLIC_BACKEND_URL) {
    return process.env.NEXT_PUBLIC_BACKEND_URL;
  }

  if (typeof window !== 'undefined') {
    const { protocol, hostname, port } = window.location;
    if (port === '33333') {
      return `${protocol}//${hostname}:38333`;
    }
    if (port === '3000') {
      return `${protocol}//${hostname}:8000`;
    }
    return `${protocol}//${hostname}:38333`;
  }

  return 'http://localhost:38333';
}

const BACKEND_URL = resolveBackendUrl();

export interface ChatRequest {
  session_id: string;
  message: string;
  file_ids: string[];
  audio_input?: {
    data: string;
    format: string;
    filename?: string;
    mime_type?: string;
    duration_ms?: number;
  } | null;
  audio_url?: {
    url: string;
    filename?: string;
    mime_type?: string;
    duration_ms?: number;
  } | null;
}

export interface ChatEvent {
  type: 'thinking' | 'text' | 'tool_call' | 'tool_result' | 'done' | 'error' | 'artifact' | 'skill';
  [key: string]: unknown;
}

export async function sendMessage(
  sessionId: string,
  message: string,
  fileIds: string[],
  onEvent: (event: ChatEvent) => void,
  options?: {
    audio_input?: ChatRequest['audio_input'];
    audio_url?: ChatRequest['audio_url'];
  }
): Promise<void> {
  const response = await fetch(`${BACKEND_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      session_id: sessionId,
      message,
      file_ids: fileIds,
      audio_input: options?.audio_input ?? null,
      audio_url: options?.audio_url ?? null,
    }),
  });

  if (!response.ok) {
    let detail = `HTTP error: ${response.status}`;
    try {
      const body = await response.text();
      if (body) {
        detail = `${detail} ${body.slice(0, 300)}`;
      }
    } catch {
      // Ignore body parsing failures; status is still useful.
    }
    throw new Error(detail);
  }

  if (!response.body) {
    throw new Error('No response body');
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  let eventType = 'text';
  let dataLines: string[] = [];
  let sawTerminalEvent = false;

  const dispatchEvent = () => {
    if (dataLines.length === 0) {
      eventType = 'text';
      return;
    }

    const rawData = dataLines.join('\n');
    try {
      const parsed = JSON.parse(rawData);
      if (eventType === 'done' || eventType === 'error') {
        sawTerminalEvent = true;
      }
      onEvent({
        ...parsed,
        type: eventType as ChatEvent['type'],
      });
    } catch (e) {
      console.error('Failed to parse SSE event data:', rawData);
    }

    eventType = 'text';
    dataLines = [];
  };

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    const lines = buffer.split('\n');
    buffer = lines.pop() || '';

    for (const rawLine of lines) {
      const line = rawLine.replace(/\r$/, '');

      if (line === '') {
        dispatchEvent();
        continue;
      }

      if (line.startsWith('event:')) {
        eventType = line.slice(6).trim() || 'text';
        continue;
      }

      if (line.startsWith('data:')) {
        dataLines.push(line.slice(5).trimStart());
        continue;
      }
    }
  }

  // Flush a trailing event if the stream ends without a blank line.
  dispatchEvent();
  if (!sawTerminalEvent) {
    onEvent({
      type: 'error',
      message: 'Stream ended unexpectedly before completion.',
    });
  }
}

export interface UploadResponse {
  file_id: string;
  filename: string;
  size: number;
  content_type: string;
}

export interface SessionSummary {
  id: string;
  title: string;
  updated_at: number;
  message_count: number;
}

export interface SessionStateResponse {
  session_id: string;
  messages: Array<Record<string, unknown>>;
  artifacts: Array<Record<string, unknown>>;
  files: UploadResponse[];
  message_count: number;
}

export interface FilePreviewResponse {
  file_id: string;
  filename: string;
  kind: 'text' | 'image' | 'binary';
  mime_type: string;
  size: number;
  text?: string;
  data_url?: string;
  truncated?: boolean;
  message?: string;
}

export interface ToolHealthSummary {
  status: 'healthy' | 'degraded' | string;
  healthy_count: number;
  total: number;
  registered_tool_count?: number;
  checked_at: string;
}

export interface ProviderHealth {
  configured: boolean;
  provider: string;
  model: string;
  detail: string;
}

export interface HealthResponse {
  status: 'healthy' | 'degraded' | string;
  service: string;
  version: string;
  tools?: ToolHealthSummary;
  provider?: ProviderHealth;
}

export interface DiagnosticsResponse {
  status: string;
  service: string;
  timestamp: string;
  uptime_seconds: number;
  process: {
    pid: number;
    rss_bytes: number;
    cpu_percent: number;
    threads: number;
  };
  system: {
    hostname: string;
    memory_total_bytes: number;
    memory_used_bytes: number;
    memory_available_bytes: number;
    memory_percent: number;
    disk_total_bytes: number;
    disk_used_bytes: number;
    disk_free_bytes: number;
    load_average: [number, number, number] | null;
  };
  tools?: ToolHealthSummary | null;
  provider?: ProviderHealth | null;
  services?: {
    asr?: {
      enabled: boolean;
      configured: boolean;
      base_url: string;
      model: string;
      has_api_key: boolean;
      status: string;
      checked_at: string;
      http_status?: number;
      error?: string;
    };
  };
}

export async function uploadFile(
  sessionId: string,
  file: File
): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append('session_id', sessionId);
  formData.append('file', file);

  const response = await fetch(`${BACKEND_URL}/api/files/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Upload failed: ${response.status}`);
  }

  return response.json();
}

export async function listFiles(sessionId: string): Promise<UploadResponse[]> {
  const response = await fetch(`${BACKEND_URL}/api/files/${sessionId}`);
  if (!response.ok) {
    throw new Error(`Failed to list files: ${response.status}`);
  }
  const data = await response.json();
  return data.files;
}

export async function listSessions(limit = 50): Promise<SessionSummary[]> {
  const response = await fetch(`${BACKEND_URL}/api/sessions?limit=${limit}`);
  if (!response.ok) {
    throw new Error(`Failed to list sessions: ${response.status}`);
  }
  const data = await response.json();
  return Array.isArray(data.sessions) ? data.sessions : [];
}

export async function getSessionState(sessionId: string): Promise<SessionStateResponse> {
  const response = await fetch(`${BACKEND_URL}/api/sessions/${sessionId}/state`);
  if (!response.ok) {
    throw new Error(`Failed to load session state: ${response.status}`);
  }
  return response.json();
}

export async function getFilePreview(fileId: string): Promise<FilePreviewResponse> {
  const response = await fetch(`${BACKEND_URL}/api/files/view/${fileId}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch file preview: ${response.status}`);
  }
  return response.json();
}

export async function getHealth(): Promise<HealthResponse> {
  const response = await fetch(`${BACKEND_URL}/api/health`);
  if (!response.ok) {
    throw new Error(`Health check failed: ${response.status}`);
  }
  return response.json();
}

export async function getDiagnostics(): Promise<DiagnosticsResponse> {
  const response = await fetch(`${BACKEND_URL}/api/health/diagnostics`);
  if (!response.ok) {
    throw new Error(`Diagnostics check failed: ${response.status}`);
  }
  return response.json();
}

export interface TranscribeResponse {
  text: string;
  model: string;
  raw?: unknown;
}

export interface LiveAsrStartRequest {
  model?: string;
  language?: string;
  sample_rate?: number;
  encoding?: string;
  channels?: number;
  triage_enabled?: boolean;
  metadata?: Record<string, string>;
}

export interface LiveAsrStartResponse {
  session_id: string;
  ws_url: string;
  model_requested?: string | null;
  model_used?: string | null;
  fallback_used?: boolean | null;
  upstream_base_url: string;
}

export async function transcribeAudio(
  blob: Blob,
  options?: { filename?: string; language?: string; prompt?: string; model?: string }
): Promise<TranscribeResponse> {
  const formData = new FormData();
  const filename = options?.filename || (blob.type.includes('wav') ? 'recording.wav' : 'recording.webm');
  formData.append('file', new File([blob], filename, { type: blob.type || 'audio/webm' }));
  if (options?.language) formData.append('language', options.language);
  if (options?.prompt) formData.append('prompt', options.prompt);
  if (options?.model) formData.append('model', options.model);

  const response = await fetch(`${BACKEND_URL}/api/audio/transcribe`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const detail = await response.text().catch(() => '');
    throw new Error(`Transcription failed: ${response.status} ${detail}`);
  }

  return response.json();
}

export async function startLiveAsrStream(
  payload?: LiveAsrStartRequest
): Promise<LiveAsrStartResponse> {
  const response = await fetch(`${BACKEND_URL}/api/audio/stream/start`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: payload?.model ?? 'auto',
      language: payload?.language ?? 'auto',
      sample_rate: payload?.sample_rate ?? 16000,
      encoding: payload?.encoding ?? 'pcm_s16le',
      channels: payload?.channels ?? 1,
      triage_enabled: payload?.triage_enabled ?? false,
      metadata: payload?.metadata ?? { source: 'polymorph-mic' },
    }),
  });

  if (!response.ok) {
    const detail = await response.text().catch(() => '');
    throw new Error(`ASR live start failed: ${response.status} ${detail}`);
  }

  return response.json();
}

export interface VoiceConfigResponse {
  configured: boolean;
  model: string;
  provider: string;
  transport: string;
  tts_base_url: string;
  default_voice_id: string;
  available_voices: Array<{
    id: string;
    label: string;
  }>;
  notes: string[];
}

export async function getVoiceConfig(): Promise<VoiceConfigResponse> {
  const response = await fetch(`${BACKEND_URL}/api/voice/config`);
  if (!response.ok) {
    const detail = await response.text().catch(() => '');
    throw new Error(`Voice config failed: ${response.status} ${detail}`);
  }
  return response.json();
}

interface VoiceTurnHistoryItem {
  role: 'user' | 'assistant';
  content: string;
}

export interface VoiceTurnResponse {
  assistant_text: string;
  provider: string;
  model: string;
  voice_id: string;
  mime_type: string;
  audio_url: string;
}

export async function sendVoiceTurn(
  sessionId: string,
  message: string,
  history: VoiceTurnHistoryItem[],
  voiceId?: string
): Promise<VoiceTurnResponse> {
  const response = await fetch(`${BACKEND_URL}/api/voice/turn`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      session_id: sessionId,
      message,
      history,
      voice_id: voiceId ?? null,
    }),
  });

  if (!response.ok) {
    const detail = await response.text().catch(() => '');
    throw new Error(`Voice turn failed: ${response.status} ${detail}`);
  }

  const data = await response.json();
  return {
    ...data,
    audio_url: typeof data.audio_url === 'string' && data.audio_url.startsWith('http')
      ? data.audio_url
      : `${BACKEND_URL}${data.audio_url}`,
  };
}

export interface ReplayRun {
  filename: string;
  path: string;
  size: number;
  modified: number;
}

export async function listReplayRuns(sessionId: string): Promise<ReplayRun[]> {
  const response = await fetch(`${BACKEND_URL}/api/replay/${sessionId}`);
  if (!response.ok) {
    throw new Error(`Replay list failed: ${response.status}`);
  }
  const data = await response.json();
  return data.runs || [];
}

export interface ConnectionField {
  env_key: string;
  label: string;
  secret: boolean;
  required: boolean;
  value: string;
  display_value: string;
  has_value: boolean;
  source: string;
}

export interface ConnectionService {
  service_id: string;
  name: string;
  description: string;
  requires_restart: boolean;
  status: string;
  details: string;
  fields: ConnectionField[];
}

export interface ConnectionsResponse {
  services: ConnectionService[];
  secrets?: {
    enabled: boolean;
    source: string;
    key_path: string;
  };
}

export interface ConnectionTestResponse {
  service_id: string;
  status: string;
  details: string;
  latency_ms: number;
}

export interface ConnectionSaveResponse {
  status: string;
  service_id: string;
  requires_restart: boolean;
  saved_keys: string[];
}

export async function getConnections(): Promise<ConnectionsResponse> {
  const response = await fetch(`${BACKEND_URL}/api/connections`);
  if (!response.ok) {
    throw new Error(`Failed to load connections: ${response.status}`);
  }
  return response.json();
}

export async function testConnection(
  serviceId: string,
  values: Record<string, string> = {}
): Promise<ConnectionTestResponse> {
  const response = await fetch(`${BACKEND_URL}/api/connections/test`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ service_id: serviceId, values }),
  });
  if (!response.ok) {
    throw new Error(`Connection test failed: ${response.status}`);
  }
  return response.json();
}

export async function saveConnection(
  serviceId: string,
  values: Record<string, string>,
  clearMissing = false
): Promise<ConnectionSaveResponse> {
  const response = await fetch(`${BACKEND_URL}/api/connections/save`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ service_id: serviceId, values, clear_missing: clearMissing }),
  });
  if (!response.ok) {
    throw new Error(`Connection save failed: ${response.status}`);
  }
  return response.json();
}
