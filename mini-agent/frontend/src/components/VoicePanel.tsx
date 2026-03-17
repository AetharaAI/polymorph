'use client';

import { useEffect, useMemo, useRef } from 'react';
import { Loader2 } from 'lucide-react';
import { ToolCall, VoiceConfig, VoiceMessage } from '@/lib/types';
import { ToolCallCard } from './ToolCallCard';

interface VoicePanelProps {
  messages: VoiceMessage[];
  isLoading: boolean;
  error: string | null;
  config: VoiceConfig | null;
  selectedVoiceId: string | null;
  onVoiceIdChange: (voiceId: string) => void;
}

function buildVoiceToolCards(message: VoiceMessage): ToolCall[] {
  const events = Array.isArray(message.tool_events) ? message.tool_events : [];
  const calls = new Map<string, ToolCall>();

  for (const event of events) {
    const toolId = String(event.tool_id || '');
    if (event.type === 'tool_call') {
      calls.set(toolId || `voice-tool-${calls.size + 1}`, {
        tool_name: String(event.tool_name || 'tool'),
        tool_id: toolId || `voice-tool-${calls.size + 1}`,
        input: event.input || {},
        status: 'loading',
      });
      continue;
    }
    if (event.type === 'tool_result') {
      const existing = calls.get(toolId);
      if (existing) {
        existing.status = 'completed';
        existing.result = String(event.result || '');
        continue;
      }
      calls.set(toolId || `voice-tool-${calls.size + 1}`, {
        tool_name: 'tool',
        tool_id: toolId || `voice-tool-${calls.size + 1}`,
        input: {},
        status: 'completed',
        result: String(event.result || ''),
      });
    }
  }

  return Array.from(calls.values());
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
          {config
            ? `${config.model} via ${config.provider} • ${config.model_source}${config.fallback_model ? ` • fallback ${config.fallback_model}` : ''}${config.available_models.length ? ` • ${config.available_models.length} live models` : ''}`
            : 'Loading voice config...'}
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
            Voice turns land here instead of the main text pane. The mic button still uses live ASR, and the voice button sends the finalized transcript through the full agent loop before audio playback lands here.
          </div>
        )}

        {config?.model_available_in_catalog === false && (
          <div className="rounded-xl border border-amber-500/30 bg-amber-500/10 p-3 text-sm text-amber-200">
            The configured voice model `{config.model}` was not found in the live gateway model catalog.
          </div>
        )}

        {config?.model_catalog_error && (
          <div className="rounded-xl border border-border bg-card/60 p-3 text-xs text-muted-foreground">
            Live model catalog probe: {config.model_catalog_error}
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
            {message.role === 'assistant' && (message.requested_model || message.provider || message.fallback_used) && (
              <div className="mt-2 text-[11px] text-muted-foreground">
                {message.provider ? `${message.provider}` : 'voice-agent'}
                {message.requested_model && message.requested_model !== message.model ? ` • requested ${message.requested_model}` : ''}
                {message.fallback_used ? ' • fallback used' : ''}
              </div>
            )}
            {message.role === 'assistant' && message.stream_state && (
              <div className="mt-2 text-[11px] uppercase tracking-[0.12em] text-muted-foreground">
                {message.transport === 'realtime_stream'
                  ? `Realtime TTS • ${message.stream_state}`
                  : `Audio • ${message.stream_state}`}
              </div>
            )}
            {message.provider_notice && (
              <div className="mt-2 rounded-lg border border-amber-500/30 bg-amber-500/10 px-2 py-1 text-xs text-amber-200">
                {message.provider_notice}
              </div>
            )}
            {message.role === 'assistant' && buildVoiceToolCards(message).map(toolCall => (
              <ToolCallCard key={toolCall.tool_id} toolCall={toolCall} />
            ))}
            {message.audio_url && (
              <audio className="mt-2 w-full" controls preload="none" src={message.audio_url} />
            )}
          </div>
        ))}

        {isLoading && (
          <div className="flex items-center gap-2 rounded-xl border border-border bg-card px-3 py-2 text-sm text-muted-foreground">
            <Loader2 size={14} className="animate-spin" />
            PolyMorph Voice Mode is responding and preparing audio...
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
