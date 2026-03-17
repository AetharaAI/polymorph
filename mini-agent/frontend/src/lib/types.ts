export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: MessageContent[];
  timestamp: number;
}

export interface MessageContent {
  type: 'text' | 'thinking' | 'tool_use' | 'tool_result' | 'skill' | 'input_audio' | 'audio_url';
  text?: string;
  thinking?: string;
  tool_name?: string;
  tool_id?: string;
  input?: Record<string, unknown>;
  result?: string;
  skill_name?: string;
  skill_file?: string;
  skill_reason?: string;
  skill_score?: number;
  filename?: string;
  mime_type?: string;
  duration_ms?: number;
  input_audio?: {
    data?: string;
    format?: string;
    filename?: string;
    mime_type?: string;
  };
  audio_url?: {
    url?: string;
    filename?: string;
    mime_type?: string;
  };
}

export interface ThinkingBlock {
  block_index: number;
  text: string;
}

export interface ToolCall {
  tool_name: string;
  tool_id: string;
  input: Record<string, unknown>;
  status: 'loading' | 'completed' | 'error';
  result?: string;
}

export interface FileAttachment {
  file_id: string;
  filename: string;
  size: number;
  content_type?: string;
}

export interface Session {
  id: string;
  title: string;
  updated_at?: number;
  message_count?: number;
}

export interface UsageStats {
  input_tokens: number;
  output_tokens: number;
  iterations: number;
  max_iterations: number;
  context_input_tokens: number;
  context_window: number;
  provider?: string;
  model?: string;
  tool_calls?: number;
  replay_path?: string | null;
}

export interface Artifact {
  file_id: string;
  filename: string;
  size: number;
  path: string;
  timestamp: number;
  source?: string;
  source_path?: string;
  validation?: {
    status: string;
    kind: string;
    valid: boolean;
    warnings: string[];
  };
}

export interface ToolHealthSummary {
  status: string;
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

export interface AsrServiceHealth {
  enabled: boolean;
  configured: boolean;
  base_url: string;
  model: string;
  has_api_key: boolean;
  status: string;
  checked_at: string;
  http_status?: number;
  error?: string;
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
    asr?: AsrServiceHealth;
  };
}

export interface ConnectionField {
  env_key: string;
  label: string;
  secret: boolean;
  required: boolean;
  value: string;
  display_value: string;
  has_value: boolean;
  source: 'override' | 'env' | 'default' | string;
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
}

export interface VoiceMessage {
  id: string;
  role: 'user' | 'assistant';
  text: string;
  timestamp: number;
  audio_url?: string;
  model?: string;
  requested_model?: string;
  provider?: string;
  provider_notice?: string;
  fallback_used?: boolean;
  tool_events?: Array<{
    type: 'tool_call' | 'tool_result';
    tool_name?: string;
    tool_id?: string;
    input?: Record<string, unknown>;
    result?: string;
  }>;
  voice_id?: string;
  transport?: string;
  stream_state?: 'starting' | 'streaming' | 'completed' | 'error';
}

export interface VoiceConfig {
  configured: boolean;
  model: string;
  fallback_model?: string | null;
  model_source: string;
  provider: string;
  base_url: string;
  transport: string;
  realtime_tts_configured: boolean;
  realtime_tts_model: string;
  realtime_tts_base_url: string;
  tts_base_url: string;
  default_voice_id: string;
  available_voices: Array<{
    id: string;
    label: string;
  }>;
  available_models: Array<{
    id: string;
    label: string;
    kind?: string;
    status?: string;
  }>;
  model_catalog_source?: string | null;
  model_catalog_error?: string | null;
  model_available_in_catalog?: boolean | null;
  notes: string[];
}
