import { useCallback, useEffect, useRef, useState } from 'react';
import { getVoiceConfig, sendVoiceTurn, VoiceTurnResponse } from '@/lib/api';
import { VoiceConfig, VoiceMessage } from '@/lib/types';

const VOICE_STATE_STORAGE_KEY = 'polymorph_voice_state_v1';

interface PersistedVoiceState {
  messages: VoiceMessage[];
  selectedVoiceId: string | null;
  updatedAt: number;
}

function readPersistedState(sessionId: string): PersistedVoiceState | null {
  if (typeof window === 'undefined' || !sessionId) return null;
  try {
    const raw = localStorage.getItem(VOICE_STATE_STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as Record<string, PersistedVoiceState>;
    return parsed[sessionId] || null;
  } catch {
    return null;
  }
}

function writePersistedState(sessionId: string, state: PersistedVoiceState) {
  if (typeof window === 'undefined' || !sessionId) return;
  try {
    const raw = localStorage.getItem(VOICE_STATE_STORAGE_KEY);
    const parsed = raw ? (JSON.parse(raw) as Record<string, PersistedVoiceState>) : {};
    parsed[sessionId] = state;
    localStorage.setItem(VOICE_STATE_STORAGE_KEY, JSON.stringify(parsed));
  } catch {
    // Ignore storage failures; voice mode still works in-memory.
  }
}

function b64ToBytes(payload: string) {
  const binary = atob(payload);
  return Uint8Array.from(binary, char => char.charCodeAt(0));
}

function splitRealtimeText(text: string, maxChars = 180): string[] {
  const normalized = text.replace(/\s+/g, ' ').trim();
  if (!normalized) return [];

  const sentences =
    normalized.match(/[^.!?]+[.!?]?/g)?.map(entry => entry.trim()).filter(Boolean) ?? [normalized];

  const chunks: string[] = [];
  let current = '';

  const pushLongChunk = (value: string) => {
    let remaining = value.trim();
    while (remaining.length > maxChars) {
      const splitAt = remaining.lastIndexOf(' ', maxChars);
      const pivot = splitAt > 40 ? splitAt : maxChars;
      chunks.push(remaining.slice(0, pivot).trim());
      remaining = remaining.slice(pivot).trim();
    }
    if (remaining) {
      current = remaining;
    }
  };

  for (const sentence of sentences) {
    if (!sentence) continue;
    if (!current) {
      if (sentence.length <= maxChars) {
        current = sentence;
      } else {
        pushLongChunk(sentence);
      }
      continue;
    }
    const candidate = `${current} ${sentence}`.trim();
    if (candidate.length <= maxChars) {
      current = candidate;
      continue;
    }
    chunks.push(current);
    current = '';
    if (sentence.length <= maxChars) {
      current = sentence;
    } else {
      pushLongChunk(sentence);
    }
  }

  if (current) {
    chunks.push(current);
  }
  return chunks;
}

function resolveAbsoluteUrl(baseUrl: string | null | undefined, value: string | null | undefined): string | null {
  const raw = (value || '').trim();
  if (!raw) return null;
  if (raw.startsWith('http://') || raw.startsWith('https://')) return raw;
  const base = (baseUrl || '').trim();
  if (!base) return raw;
  return `${base.replace(/\/$/, '')}${raw.startsWith('/') ? raw : `/${raw}`}`;
}

export function useVoiceChat(sessionId: string) {
  const [messages, setMessages] = useState<VoiceMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [config, setConfig] = useState<VoiceConfig | null>(null);
  const [selectedVoiceId, setSelectedVoiceId] = useState<string | null>(null);

  const ttsSocketRef = useRef<WebSocket | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const nextPlaybackTimeRef = useRef(0);
  const finalBlobUrlRef = useRef<string | null>(null);

  const closeRealtimeTts = useCallback((force = false) => {
    const socket = ttsSocketRef.current;
    if (!socket) return;
    ttsSocketRef.current = null;
    socket.onopen = null;
    socket.onmessage = null;
    socket.onerror = null;
    socket.onclose = null;
    if (force && socket.readyState < WebSocket.CLOSING) {
      socket.close();
    }
  }, []);

  const revokeFinalBlobUrl = useCallback(() => {
    if (finalBlobUrlRef.current) {
      URL.revokeObjectURL(finalBlobUrlRef.current);
      finalBlobUrlRef.current = null;
    }
  }, []);

  const ensureAudioContext = useCallback(async (): Promise<AudioContext | null> => {
    if (typeof window === 'undefined') return null;
    const Context = window.AudioContext || (window as Window & { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
    if (!Context) return null;
    if (!audioContextRef.current) {
      audioContextRef.current = new Context();
    }
    if (audioContextRef.current.state === 'suspended') {
      await audioContextRef.current.resume();
    }
    return audioContextRef.current;
  }, []);

  const playChunkAudio = useCallback(async (payload: string) => {
    const context = await ensureAudioContext();
    if (!context) return;
    const bytes = b64ToBytes(payload);
    const chunkBuffer = bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
    const decoded = await context.decodeAudioData(chunkBuffer.slice(0));
    const source = context.createBufferSource();
    source.buffer = decoded;
    source.connect(context.destination);
    const now = context.currentTime + 0.02;
    const startAt = Math.max(now, nextPlaybackTimeRef.current);
    source.start(startAt);
    nextPlaybackTimeRef.current = startAt + decoded.duration;
  }, [ensureAudioContext]);

  const patchMessage = useCallback((messageId: string, patch: Partial<VoiceMessage>) => {
    setMessages(current =>
      current.map(message => (message.id === messageId ? { ...message, ...patch } : message))
    );
  }, []);

  useEffect(() => {
    setMessages([]);
    setIsLoading(false);
    setError(null);
    setSelectedVoiceId(null);
    closeRealtimeTts(true);
    revokeFinalBlobUrl();
    nextPlaybackTimeRef.current = 0;

    if (!sessionId) {
      return;
    }

    const persisted = readPersistedState(sessionId);
    if (persisted) {
      setMessages(Array.isArray(persisted.messages) ? persisted.messages : []);
      setSelectedVoiceId(persisted.selectedVoiceId || null);
    }
  }, [sessionId, closeRealtimeTts, revokeFinalBlobUrl]);

  useEffect(() => {
    let cancelled = false;
    const loadConfig = async () => {
      try {
        const nextConfig = await getVoiceConfig();
        if (cancelled) return;
        setConfig(nextConfig);
        setSelectedVoiceId(current => current || nextConfig.default_voice_id || null);
      } catch (err) {
        if (cancelled) return;
        setConfig(null);
        setError(err instanceof Error ? err.message : 'Failed to load voice mode config.');
      }
    };

    void loadConfig();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (!sessionId) return;
    writePersistedState(sessionId, {
      messages,
      selectedVoiceId,
      updatedAt: Date.now(),
    });
  }, [messages, selectedVoiceId, sessionId]);

  useEffect(() => () => {
    closeRealtimeTts(true);
    revokeFinalBlobUrl();
    if (audioContextRef.current) {
      void audioContextRef.current.close();
      audioContextRef.current = null;
    }
  }, [closeRealtimeTts, revokeFinalBlobUrl]);

  const streamAssistantAudio = useCallback(
    async (messageId: string, response: VoiceTurnResponse): Promise<void> => {
      if (response.tts_transport !== 'realtime_stream' || !response.tts_stream_ws_url) {
        if (response.audio_url) {
          patchMessage(messageId, {
            audio_url: response.audio_url,
            stream_state: 'completed',
          });
        }
        return;
      }

      await ensureAudioContext();
      nextPlaybackTimeRef.current = 0;
      patchMessage(messageId, { stream_state: 'starting' });

      await new Promise<void>((resolve, reject) => {
        let settled = false;
        let finalized = false;

        const finish = (cb: () => void) => {
          if (settled) return;
          settled = true;
          cb();
        };

        closeRealtimeTts(true);
        const socket = new WebSocket(response.tts_stream_ws_url as string);
        ttsSocketRef.current = socket;

        socket.onopen = () => {
          patchMessage(messageId, { stream_state: 'streaming' });
          const chunks = splitRealtimeText(response.assistant_text, 180);
          if (chunks.length === 0) {
            socket.send(JSON.stringify({ type: 'text_complete' }));
            socket.send(JSON.stringify({ type: 'end_stream' }));
            return;
          }
          for (const chunk of chunks) {
            socket.send(JSON.stringify({ type: 'text_chunk', text: chunk }));
          }
          socket.send(JSON.stringify({ type: 'text_complete' }));
          socket.send(JSON.stringify({ type: 'end_stream' }));
        };

        socket.onmessage = event => {
          try {
            const payload = JSON.parse(event.data) as {
              type: string;
              audio_b64?: string;
              format?: string;
              message?: string;
              metadata?: Record<string, unknown>;
            };

            if (payload.type === 'error') {
              finish(() => {
                patchMessage(messageId, { stream_state: 'error' });
                reject(new Error(payload.message || 'Realtime TTS stream failed.'));
              });
              socket.close();
              return;
            }

            if (payload.type === 'audio_chunk' && payload.audio_b64) {
              void playChunkAudio(payload.audio_b64);
              patchMessage(messageId, { stream_state: 'streaming' });
              return;
            }

            if (payload.type === 'final_audio' && payload.audio_b64) {
              finalized = true;
              const metadata = (payload.metadata || {}) as Record<string, unknown>;
              const gatewayAudioUrl =
                typeof metadata.audio_url === 'string'
                  ? resolveAbsoluteUrl(response.tts_stream_http_base_url, metadata.audio_url)
                  : null;
              let finalUrl = gatewayAudioUrl;
              if (!finalUrl) {
                revokeFinalBlobUrl();
                const bytes = b64ToBytes(payload.audio_b64);
                const mimeType = payload.format ? `audio/${payload.format}` : 'audio/wav';
                finalBlobUrlRef.current = URL.createObjectURL(new Blob([bytes], { type: mimeType }));
                finalUrl = finalBlobUrlRef.current;
              }
              patchMessage(messageId, {
                audio_url: finalUrl || undefined,
                stream_state: 'completed',
              });
              socket.close();
              finish(resolve);
            }
          } catch (err) {
            finish(() => {
              patchMessage(messageId, { stream_state: 'error' });
              reject(err instanceof Error ? err : new Error('Realtime TTS event parsing failed.'));
            });
            socket.close();
          }
        };

        socket.onerror = () => {
          finish(() => {
            patchMessage(messageId, { stream_state: 'error' });
            reject(new Error('Realtime TTS websocket failed.'));
          });
        };

        socket.onclose = () => {
          ttsSocketRef.current = null;
          if (settled) return;
          if (finalized) {
            finish(resolve);
            return;
          }
          finish(() => {
            patchMessage(messageId, { stream_state: 'error' });
            reject(new Error('Realtime TTS stream closed before final audio.'));
          });
        };
      });
    },
    [closeRealtimeTts, ensureAudioContext, patchMessage, playChunkAudio, revokeFinalBlobUrl]
  );

  const sendTurn = useCallback(async (transcript: string) => {
    const trimmed = transcript.trim();
    if (!trimmed || !sessionId) return;

    const userMessage: VoiceMessage = {
      id: `voice-user-${Date.now()}`,
      role: 'user',
      text: trimmed,
      timestamp: Date.now(),
    };
    const history = [...messages, userMessage].map(message => ({
      role: message.role,
      content: message.text,
    }));

    closeRealtimeTts(true);
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await sendVoiceTurn(sessionId, trimmed, history, selectedVoiceId || undefined);
      const assistantId = `voice-assistant-${Date.now()}`;
      const assistantMessage: VoiceMessage = {
        id: assistantId,
        role: 'assistant',
        text: response.assistant_text,
        timestamp: Date.now(),
        audio_url: response.audio_url || undefined,
        model: response.model,
        voice_id: response.voice_id,
        transport: response.tts_transport,
        stream_state: response.tts_transport === 'realtime_stream' ? 'starting' : 'completed',
      };
      setMessages(prev => [...prev, assistantMessage]);
      await streamAssistantAudio(assistantId, response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Voice mode failed.');
    } finally {
      setIsLoading(false);
    }
  }, [closeRealtimeTts, messages, selectedVoiceId, sessionId, streamAssistantAudio]);

  return {
    messages,
    isLoading,
    error,
    config,
    selectedVoiceId,
    setSelectedVoiceId,
    sendTurn,
  };
}
