'use client';

import { useEffect, useMemo, useRef } from 'react';
import { Loader2 } from 'lucide-react';
import { VoiceConfig, VoiceMessage } from '@/lib/types';

interface VoicePanelProps {
  messages: VoiceMessage[];
  isLoading: boolean;
  error: string | null;
  config: VoiceConfig | null;
  selectedVoiceId: string | null;
  onVoiceIdChange: (voiceId: string) => void;
}

export function VoicePanel({
  messages,
  isLoading,
  error,
  config,
  selectedVoiceId,
  onVoiceIdChange,
}: VoicePanelProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const lastAssistantAudio = useMemo(
    () => [...messages].reverse().find(message => message.role === 'assistant' && message.audio_url)?.audio_url || null,
    [messages]
  );

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  useEffect(() => {
    if (!lastAssistantAudio) return;
    const audio = new Audio(lastAssistantAudio);
    void audio.play().catch(() => undefined);
    return () => {
      audio.pause();
    };
  }, [lastAssistantAudio]);

  return (
    <section className="mx-4 mt-4 rounded-2xl border border-emerald-500/20 bg-gradient-to-br from-emerald-500/8 via-card to-card">
      <div className="flex flex-wrap items-center gap-3 border-b border-border/70 px-4 py-3">
        <div className="flex items-center gap-2 text-sm font-medium">
          <img
            src="/branding/voice-mic-mark.png"
            alt="Voice mode mark"
            className="h-5 w-5 object-contain"
          />
          <span>PolyMorph Voice Mode</span>
        </div>
        <div className="text-xs text-muted-foreground">
          {config ? `${config.model} via ${config.provider}` : 'Loading voice config...'}
        </div>
        <div className="ml-auto flex items-center gap-2">
          <label htmlFor="voice-select" className="text-xs text-muted-foreground">
            Voice
          </label>
          <select
            id="voice-select"
            value={selectedVoiceId || ''}
            onChange={e => onVoiceIdChange(e.target.value)}
            className="rounded-lg border border-border bg-secondary px-2 py-1 text-xs text-foreground"
            disabled={!config || config.available_voices.length === 0}
          >
            {(config?.available_voices || []).map(voice => (
              <option key={voice.id} value={voice.id}>
                {voice.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div ref={containerRef} className="max-h-64 space-y-3 overflow-y-auto px-4 py-4">
        {messages.length === 0 && (
          <div className="rounded-xl border border-dashed border-border bg-card/60 p-3 text-sm text-muted-foreground">
            Voice turns land here instead of the main tool-using chat. The mic button now uses live ASR and the voice button sends the finalized transcript into this pane.
          </div>
        )}

        {messages.map(message => (
          <div
            key={message.id}
            className={`rounded-xl px-3 py-2 text-sm ${
              message.role === 'user'
                ? 'ml-auto max-w-[85%] bg-secondary text-foreground'
                : 'mr-auto max-w-[90%] border border-border bg-card text-foreground'
            }`}
          >
            <div className="mb-1 text-[11px] uppercase tracking-[0.12em] text-muted-foreground">
              {message.role === 'user' ? 'You' : `Voice Agent${message.model ? ` • ${message.model}` : ''}`}
            </div>
            <div className="whitespace-pre-wrap break-words">{message.text}</div>
            {message.audio_url && (
              <audio className="mt-2 w-full" controls preload="none" src={message.audio_url} />
            )}
          </div>
        ))}

        {isLoading && (
          <div className="flex items-center gap-2 rounded-xl border border-border bg-card px-3 py-2 text-sm text-muted-foreground">
            <Loader2 size={14} className="animate-spin" />
            PolyMorph Voice Mode is responding...
          </div>
        )}

        {error && (
          <div className="rounded-xl border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-300">
            {error}
          </div>
        )}
      </div>
    </section>
  );
}
