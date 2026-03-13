import { useState, useCallback, useRef, useEffect } from 'react';
import { sendMessage, ChatEvent, getSessionState } from '@/lib/api';
import { Message, ToolCall, UsageStats, Artifact } from '@/lib/types';

const CHAT_STATE_STORAGE_KEY = 'aetherops_chat_state_v1';

function isWriteLikeToolName(name: string | undefined): boolean {
  const normalized = (name || '').toLowerCase();
  if (!normalized) return false;
  return (
    normalized === 'write_file' ||
    normalized.endsWith('.write_file') ||
    normalized.endsWith('/write_file') ||
    normalized.endsWith(':write_file') ||
    normalized.includes('__write_file') ||
    normalized.includes('write_file')
  );
}

function parseArtifactFromToolResult(result: string): Artifact | null {
  const trimmed = result.trim();
  const withoutFence = trimmed
    .replace(/^```(?:json)?\s*/i, '')
    .replace(/\s*```$/, '')
    .trim();

  try {
    const parsed = JSON.parse(withoutFence) as Record<string, unknown>;
    if (!parsed.file_id || !parsed.filename) {
      return null;
    }

    return {
      file_id: String(parsed.file_id),
      filename: String(parsed.filename),
      size: Number(parsed.size ?? 0),
      path: String(parsed.path ?? ''),
      timestamp: Number(parsed.timestamp ?? Date.now()),
      source: typeof parsed.source === 'string' ? parsed.source : undefined,
      source_path: typeof parsed.source_path === 'string' ? parsed.source_path : undefined,
      validation: parsed.validation as Artifact['validation'],
    };
  } catch {
    return null;
  }
}

function upsertArtifact(existing: Artifact[], next: Artifact): Artifact[] {
  const idx = existing.findIndex(a => a.file_id === next.file_id);
  if (idx === -1) {
    return [...existing, next];
  }

  const updated = [...existing];
  updated[idx] = { ...updated[idx], ...next };
  return updated;
}

interface PersistedSessionState {
  messages: Message[];
  artifacts: Artifact[];
  usage: UsageStats | null;
  updated_at: number;
}

function readPersistedState(sessionId: string): PersistedSessionState | null {
  if (typeof window === 'undefined' || !sessionId) return null;
  try {
    const raw = localStorage.getItem(CHAT_STATE_STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as Record<string, PersistedSessionState>;
    return parsed[sessionId] || null;
  } catch {
    return null;
  }
}

function writePersistedState(sessionId: string, state: PersistedSessionState) {
  if (typeof window === 'undefined' || !sessionId) return;
  try {
    const raw = localStorage.getItem(CHAT_STATE_STORAGE_KEY);
    const parsed = raw ? (JSON.parse(raw) as Record<string, PersistedSessionState>) : {};
    parsed[sessionId] = state;
    localStorage.setItem(CHAT_STATE_STORAGE_KEY, JSON.stringify(parsed));
  } catch {
    // Ignore storage failures; session still works in-memory.
  }
}

function coerceMessage(input: Record<string, unknown>, fallbackIndex: number): Message {
  const role = input.role === 'assistant' ? 'assistant' : 'user';
  const rawContent = Array.isArray(input.content) ? input.content : [];
  const content = rawContent
    .filter((c): c is Record<string, unknown> => typeof c === 'object' && c !== null)
    .map(c => ({
      type: String(c.type || 'text') as Message['content'][number]['type'],
      text: typeof c.text === 'string' ? c.text : undefined,
      thinking: typeof c.thinking === 'string' ? c.thinking : undefined,
      tool_name: typeof c.tool_name === 'string' ? c.tool_name : undefined,
      tool_id: typeof c.tool_id === 'string' ? c.tool_id : undefined,
      input: typeof c.input === 'object' && c.input !== null ? (c.input as Record<string, unknown>) : undefined,
      result: typeof c.result === 'string' ? c.result : undefined,
      skill_name: typeof c.skill_name === 'string' ? c.skill_name : undefined,
      skill_file: typeof c.skill_file === 'string' ? c.skill_file : undefined,
      skill_reason: typeof c.skill_reason === 'string' ? c.skill_reason : undefined,
      skill_score: typeof c.skill_score === 'number' ? c.skill_score : undefined,
      filename: typeof c.filename === 'string' ? c.filename : undefined,
      mime_type: typeof c.mime_type === 'string' ? c.mime_type : undefined,
      duration_ms: typeof c.duration_ms === 'number' ? c.duration_ms : undefined,
      input_audio: typeof c.input_audio === 'object' && c.input_audio !== null ? (c.input_audio as Message['content'][number]['input_audio']) : undefined,
      audio_url: typeof c.audio_url === 'object' && c.audio_url !== null ? (c.audio_url as Message['content'][number]['audio_url']) : undefined,
    }));

  return {
    id: typeof input.id === 'string' ? input.id : `${role}-${fallbackIndex}`,
    role,
    content,
    timestamp: typeof input.timestamp === 'number' ? input.timestamp : Date.now() + fallbackIndex,
  };
}

function coerceArtifact(input: Record<string, unknown>): Artifact | null {
  if (!input.file_id || !input.filename) return null;
  return {
    file_id: String(input.file_id),
    filename: String(input.filename),
    size: Number(input.size ?? 0),
    path: String(input.path ?? ''),
    timestamp: Number(input.timestamp ?? Date.now()),
    source: typeof input.source === 'string' ? input.source : undefined,
    source_path: typeof input.source_path === 'string' ? input.source_path : undefined,
    validation: input.validation as Artifact['validation'],
  };
}

export function useChat(sessionId: string) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentThinking, setCurrentThinking] = useState<{ text: string } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [toolCalls, setToolCalls] = useState<ToolCall[]>([]);
  const [usage, setUsage] = useState<UsageStats | null>(null);
  const [artifacts, setArtifacts] = useState<Artifact[]>([]);

  const currentMessageRef = useRef<Message | null>(null);
  const toolNameByIdRef = useRef<Record<string, string>>({});
  const ensureAssistantMessageExists = useCallback(() => {
    if (currentMessageRef.current) {
      return;
    }

    const newMsg: Message = {
      id: Date.now().toString(),
      role: 'assistant',
      content: [],
      timestamp: Date.now()
    };
    currentMessageRef.current = newMsg;
    setMessages(prev => [...prev, newMsg]);
  }, []);

  useEffect(() => {
    setMessages([]);
    setIsLoading(false);
    setCurrentThinking(null);
    setError(null);
    setToolCalls([]);
    setUsage(null);
    setArtifacts([]);
    currentMessageRef.current = null;
    toolNameByIdRef.current = {};

    if (!sessionId) {
      return;
    }

    const persisted = readPersistedState(sessionId);
    if (persisted) {
      setMessages(persisted.messages || []);
      setArtifacts(persisted.artifacts || []);
      setUsage(persisted.usage || null);
    }

    let canceled = false;
    const loadFromBackend = async () => {
      try {
        const state = await getSessionState(sessionId);
        if (canceled) return;

        const hydratedMessages = (state.messages || [])
          .filter((m): m is Record<string, unknown> => typeof m === 'object' && m !== null)
          .map((m, idx) => coerceMessage(m, idx));

        const hydratedArtifacts = (state.artifacts || [])
          .filter((a): a is Record<string, unknown> => typeof a === 'object' && a !== null)
          .map(coerceArtifact)
          .filter((a): a is Artifact => Boolean(a));

        if (hydratedMessages.length > 0) {
          setMessages(hydratedMessages);
        }
        if (hydratedArtifacts.length > 0) {
          setArtifacts(hydratedArtifacts);
        }
      } catch {
        // Session may not exist in backend yet; local snapshot remains source of truth.
      }
    };

    void loadFromBackend();
    return () => {
      canceled = true;
    };
  }, [sessionId]);

  useEffect(() => {
    if (!sessionId) return;
    writePersistedState(sessionId, {
      messages,
      artifacts,
      usage,
      updated_at: Date.now(),
    });
  }, [sessionId, messages, artifacts, usage]);

  const handleEvent = useCallback((event: ChatEvent) => {
    switch (event.type) {
      case 'thinking': {
        const text = (event.text as string) || '';
        ensureAssistantMessageExists();
        setCurrentThinking(prev => ({
          text: (prev?.text || '') + text
        }));
        setMessages(prev => {
          const newMessages = [...prev];
          const lastMsg = newMessages[newMessages.length - 1];
          if (lastMsg && lastMsg.role === 'assistant') {
            const existingThinking = lastMsg.content.find(c => c.type === 'thinking');
            if (existingThinking) {
              existingThinking.thinking = (existingThinking.thinking || '') + text;
            } else {
              lastMsg.content.push({ type: 'thinking', thinking: text });
            }
          }
          return newMessages;
        });
        break;
      }

      case 'text': {
        const text = (event.text as string) || '';
        ensureAssistantMessageExists();
        setMessages(prev => {
          const newMessages = [...prev];
          const lastMsg = newMessages[newMessages.length - 1];
          if (lastMsg && lastMsg.role === 'assistant') {
            const lastContent = lastMsg.content[lastMsg.content.length - 1];
            if (lastContent?.type === 'text') {
              lastContent.text = (lastContent.text || '') + text;
            } else {
              lastMsg.content.push({ type: 'text', text });
            }
          }
          return newMessages;
        });
        break;
      }

      case 'tool_call': {
        const toolId = event.tool_id as string;
        const toolCall: ToolCall = {
          tool_name: event.tool_name as string,
          tool_id: toolId,
          input: event.input as Record<string, unknown>,
          status: 'loading'
        };
        ensureAssistantMessageExists();
        toolNameByIdRef.current[toolCall.tool_id] = toolCall.tool_name;
        setToolCalls(prev => {
          const existing = prev.find(tc => tc.tool_id === toolId);
          if (existing) {
            return prev.map(tc => tc.tool_id === toolId ? { ...tc, input: toolCall.input, tool_name: toolCall.tool_name } : tc);
          }
          return [...prev, toolCall];
        });

        // Add tool call to current message
        setMessages(prev => {
          const newMessages = [...prev];
          const lastMsg = newMessages[newMessages.length - 1];
          if (lastMsg && lastMsg.role === 'assistant') {
            const exists = lastMsg.content.some(c => c.type === 'tool_use' && c.tool_id === toolId);
            if (!exists) {
              lastMsg.content.push({
                type: 'tool_use',
                tool_name: event.tool_name as string,
                tool_id: toolId,
                input: event.input as Record<string, unknown>
              });
            }
          }
          return newMessages;
        });
        break;
      }

      case 'tool_result': {
        const toolId = event.tool_id as string;
        const result = event.result as string;
        const toolName = toolNameByIdRef.current[toolId];
        ensureAssistantMessageExists();

        setToolCalls(prev => prev.map(tc =>
          tc.tool_id === toolId ? { ...tc, status: 'completed', result } : tc
        ));

        if (isWriteLikeToolName(toolName)) {
          const parsedArtifact = parseArtifactFromToolResult(result);
          if (parsedArtifact) {
            setArtifacts(prev => upsertArtifact(prev, parsedArtifact));
          }
        }

        // Add tool result to current message
        setMessages(prev => {
          const newMessages = [...prev];
          const lastMsg = newMessages[newMessages.length - 1];
          if (lastMsg && lastMsg.role === 'assistant') {
            lastMsg.content.push({
              type: 'tool_result',
              tool_id: toolId,
              result
            });
          }
          return newMessages;
        });
        break;
      }

      case 'done': {
        setUsage({
          input_tokens: (event.total_input_tokens as number) || 0,
          output_tokens: (event.total_output_tokens as number) || 0,
          iterations: (event.iterations as number) || 0,
          max_iterations: (event.max_iterations as number) || 0,
          context_input_tokens: (event.context_input_tokens as number) || 0,
          context_window: (event.context_window as number) || 204800,
          provider: (event.provider as string) || undefined,
          model: (event.model as string) || undefined,
          tool_calls: (event.tool_calls as number) || 0,
          replay_path: (event.replay_path as string) || null,
        });
        setIsLoading(false);
        setCurrentThinking(null);
        currentMessageRef.current = null;
        break;
      }

      case 'artifact': {
        const artifact: Artifact = {
          file_id: event.file_id as string,
          filename: event.filename as string,
          size: event.size as number,
          path: event.path as string,
          timestamp: (event.timestamp as number) || Date.now(),
          source: event.source as string | undefined,
          source_path: event.source_path as string | undefined,
          validation: event.validation as Artifact['validation'],
        };
        setArtifacts(prev => upsertArtifact(prev, artifact));
        break;
      }

      case 'skill': {
        ensureAssistantMessageExists();
        setMessages(prev => {
          const newMessages = [...prev];
          const lastMsg = newMessages[newMessages.length - 1];
          if (!lastMsg || lastMsg.role !== 'assistant') {
            return newMessages;
          }
          const skillName = (event.skill_name as string) || '';
          const skillFile = (event.skill_file as string) || '';
          const already = lastMsg.content.some(
            c => c.type === 'skill' && c.skill_name === skillName && c.skill_file === skillFile
          );
          if (!already) {
            lastMsg.content.push({
              type: 'skill',
              skill_name: skillName,
              skill_file: skillFile,
              skill_reason: (event.skill_reason as string) || '',
              skill_score: Number(event.skill_score || 0),
            });
          }
          return newMessages;
        });
        break;
      }

      case 'error': {
        setError((event.message as string) || 'Unknown error');
        setIsLoading(false);
        setCurrentThinking(null);
        currentMessageRef.current = null;
        break;
      }
    }
  }, [ensureAssistantMessageExists]);

  const send = useCallback(async (
    text: string,
    fileIds: string[] = [],
    options?: {
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
  ) => {
    // Add user message
    const userContent: Message['content'] = [{ type: 'text', text }];
    if (options?.audio_input) {
      userContent.unshift({
        type: 'input_audio',
        filename: options.audio_input.filename,
        mime_type: options.audio_input.mime_type,
        duration_ms: options.audio_input.duration_ms,
        input_audio: {
          format: options.audio_input.format,
          filename: options.audio_input.filename,
          mime_type: options.audio_input.mime_type,
        },
      });
    } else if (options?.audio_url) {
      userContent.unshift({
        type: 'audio_url',
        filename: options.audio_url.filename,
        mime_type: options.audio_url.mime_type,
        duration_ms: options.audio_url.duration_ms,
        audio_url: {
          filename: options.audio_url.filename,
          mime_type: options.audio_url.mime_type,
        },
      });
    }
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: userContent,
      timestamp: Date.now()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);
    setToolCalls([]);
    setUsage(null);
    setCurrentThinking(null);

    try {
      await sendMessage(sessionId, text, fileIds, handleEvent, options);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message');
      setIsLoading(false);
    }
  }, [sessionId, handleEvent]);

  return {
    messages,
    isLoading,
    currentThinking,
    error,
    toolCalls,
    usage,
    artifacts,
    send
  };
}
