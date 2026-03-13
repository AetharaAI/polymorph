import { useCallback, useEffect, useState } from 'react';
import { getVoiceConfig, sendVoiceTurn } from '@/lib/api';
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

export function useVoiceChat(sessionId: string) {
  const [messages, setMessages] = useState<VoiceMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [config, setConfig] = useState<VoiceConfig | null>(null);
  const [selectedVoiceId, setSelectedVoiceId] = useState<string | null>(null);

  useEffect(() => {
    setMessages([]);
    setIsLoading(false);
    setError(null);
    setSelectedVoiceId(null);

    if (!sessionId) {
      return;
    }

    const persisted = readPersistedState(sessionId);
    if (persisted) {
      setMessages(Array.isArray(persisted.messages) ? persisted.messages : []);
      setSelectedVoiceId(persisted.selectedVoiceId || null);
    }
  }, [sessionId]);

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

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await sendVoiceTurn(sessionId, trimmed, history, selectedVoiceId || undefined);
      const assistantMessage: VoiceMessage = {
        id: `voice-assistant-${Date.now()}`,
        role: 'assistant',
        text: response.assistant_text,
        timestamp: Date.now(),
        audio_url: response.audio_url,
        model: response.model,
        voice_id: response.voice_id,
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Voice mode failed.');
    } finally {
      setIsLoading(false);
    }
  }, [messages, selectedVoiceId, sessionId]);

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
