'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { AudioLines, Check, Loader2, Mic, Send } from 'lucide-react';
import { FileAttachment } from '@/lib/types';
import { useLiveAsrStream } from '@/hooks/useLiveAsrStream';
import { FileAttachments } from './FileAttachments';

interface InputBarProps {
  onSend: (text: string, fileIds: string[]) => void;
  onVoiceTurn: (text: string) => Promise<void> | void;
  isLoading: boolean;
  isVoiceLoading: boolean;
  files: FileAttachment[];
  onAddFile: () => void;
  onRemoveFile: (fileId: string) => void;
}

function appendTranscript(previous: string, transcript: string): string {
  const next = transcript.trim();
  if (!next) return previous;
  const prefix = previous.trim();
  if (!prefix) return next;
  return `${prefix}${prefix.endsWith('\n') ? '' : '\n'}${next}`;
}

function logVoiceSession(event: string, payload: Record<string, unknown> = {}) {
  console.info('[VoiceSession]', {
    event,
    ...payload,
  });
}

export function InputBar({
  onSend,
  onVoiceTurn,
  isLoading,
  isVoiceLoading,
  files,
  onAddFile,
  onRemoveFile,
}: InputBarProps) {
  const [text, setText] = useState('');
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [isVoiceSessionActive, setIsVoiceSessionActive] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const voiceSessionActiveRef = useRef(false);
  const voiceTurnInFlightRef = useRef(false);
  const startVoiceCaptureRef = useRef<(() => Promise<void>) | null>(null);
  const {
    isRecording,
    isFinalizing,
    mode: recordingMode,
    partialTranscript,
    audioLevels,
    error: recordingError,
    start,
    stop,
    cancel,
  } = useLiveAsrStream();

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 150)}px`;
    }
  }, [text]);

  useEffect(() => {
    voiceSessionActiveRef.current = isVoiceSessionActive;
  }, [isVoiceSessionActive]);

  const stopVoiceSession = useCallback(() => {
    logVoiceSession('stop_requested');
    voiceSessionActiveRef.current = false;
    voiceTurnInFlightRef.current = false;
    setIsVoiceSessionActive(false);
    cancel({ preserveTranscript: false });
  }, [cancel]);

  const handleSend = () => {
    if (!text.trim() && files.length === 0) return;
    if (isLoading) return;

    const fileIds = files.map(file => file.file_id);
    onSend(text.trim(), fileIds);
    setText('');
    setSubmitError(null);
  };

  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  const handleStartRecording = async (mode: 'asr' | 'voice') => {
    if (mode === 'voice') return;
    if (isLoading || isVoiceLoading || isRecording || isFinalizing || isVoiceSessionActive) return;
    setSubmitError(null);
    try {
      await start(mode);
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : 'Unable to start live ASR.');
    }
  };

  const handleStopRecording = async () => {
    if (!recordingMode || recordingMode !== 'asr') return;
    setSubmitError(null);

    try {
      const transcript = await stop();
      const finalText = transcript.trim();
      if (!finalText) {
        throw new Error('Live ASR returned an empty final transcript.');
      }

      setText(previous => appendTranscript(previous, finalText));
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : 'Failed to finalize the live transcript.');
    }
  };

  const startVoiceCapture = useCallback(async () => {
    await start('voice', {
      onFinalTranscript: async transcript => {
        const finalText = transcript.trim();
        if (!voiceSessionActiveRef.current || !finalText || voiceTurnInFlightRef.current) {
          return;
        }

        logVoiceSession('turn_committed', {
          chars: finalText.length,
          preview: finalText.slice(0, 160),
        });
        voiceTurnInFlightRef.current = true;
        cancel({ preserveTranscript: true });

        try {
          logVoiceSession('turn_dispatch_start');
          await Promise.resolve(onVoiceTurn(finalText));
          logVoiceSession('turn_dispatch_success');
        } catch (error) {
          logVoiceSession('turn_dispatch_failed', {
            message: error instanceof Error ? error.message : 'Voice mode failed.',
          });
          setSubmitError(error instanceof Error ? error.message : 'Voice mode failed.');
          stopVoiceSession();
          return;
        } finally {
          voiceTurnInFlightRef.current = false;
        }

        if (!voiceSessionActiveRef.current) {
          return;
        }

        try {
          logVoiceSession('resume_listening');
          await startVoiceCaptureRef.current?.();
        } catch (error) {
          logVoiceSession('resume_failed', {
            message: error instanceof Error ? error.message : 'Unable to resume live voice mode.',
          });
          setSubmitError(error instanceof Error ? error.message : 'Unable to resume live voice mode.');
          stopVoiceSession();
        }
      },
    });
  }, [cancel, onVoiceTurn, start, stopVoiceSession]);

  useEffect(() => {
    startVoiceCaptureRef.current = startVoiceCapture;
  }, [startVoiceCapture]);

  const handleToggleVoiceSession = async () => {
    if (isVoiceSessionActive) {
      stopVoiceSession();
      return;
    }

    if (isLoading || isFinalizing || (isRecording && recordingMode === 'asr')) return;

    setSubmitError(null);
    setIsVoiceSessionActive(true);
    voiceSessionActiveRef.current = true;
    logVoiceSession('session_start_requested');

    try {
      await startVoiceCapture();
      logVoiceSession('session_started');
    } catch (error) {
      logVoiceSession('session_start_failed', {
        message: error instanceof Error ? error.message : 'Unable to start live voice mode.',
      });
      setSubmitError(error instanceof Error ? error.message : 'Unable to start live voice mode.');
      stopVoiceSession();
    }
  };

  const statusError = submitError || recordingError;
  const isMicCaptureActive = isRecording && recordingMode === 'asr';
  const isMicBusy = isMicCaptureActive || isFinalizing;
  const isBusy = isMicBusy || isVoiceSessionActive;

  return (
    <div className="shrink-0 border-t border-border bg-card p-4">
      <FileAttachments
        files={files}
        onRemove={onRemoveFile}
        onAddClick={onAddFile}
      />

      <div className="mt-2 flex items-end gap-2">
        <textarea
          ref={textareaRef}
          value={text}
          onChange={event => setText(event.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Message PolyMorph..."
          disabled={isLoading || isBusy}
          className="flex-1 resize-none rounded-lg bg-secondary px-4 py-3 text-foreground focus:outline-none focus:ring-2 focus:ring-primary disabled:opacity-50"
          rows={1}
        />

        {isRecording && (
          <div className="flex h-10 items-center gap-0.5 rounded-lg border border-border bg-secondary px-2">
            {audioLevels.map((level, index) => (
              <span
                // eslint-disable-next-line react/no-array-index-key
                key={index}
                className="w-1 rounded bg-emerald-400/90 transition-all duration-75"
                style={{ height: `${Math.round(8 + level * 24)}px` }}
              />
            ))}
          </div>
        )}

        {isMicCaptureActive ? (
          <button
            onClick={() => void handleStopRecording()}
            className="rounded-lg bg-emerald-500 px-3 py-3 text-black transition-colors hover:bg-emerald-400"
            title="Finish live capture"
          >
            <Check size={20} />
          </button>
        ) : (
          <button
            onClick={() => void handleStartRecording('asr')}
            disabled={isLoading || isVoiceLoading || isFinalizing || isVoiceSessionActive}
            className="rounded-lg border border-border bg-secondary px-3 py-3 text-foreground transition-colors hover:bg-secondary/80 disabled:cursor-not-allowed disabled:opacity-50"
            title="Start live ASR transcription"
          >
            {isFinalizing && recordingMode === 'asr' ? (
              <Loader2 size={20} className="animate-spin" />
            ) : (
              <Mic size={20} />
            )}
          </button>
        )}

        <button
          onClick={() => void handleToggleVoiceSession()}
          disabled={!isVoiceSessionActive && (isLoading || isFinalizing || isMicCaptureActive)}
          className={`rounded-lg border px-3 py-3 transition-colors disabled:cursor-not-allowed disabled:opacity-50 ${
            isVoiceSessionActive
              ? 'border-emerald-500 bg-emerald-500 text-black hover:bg-emerald-400'
              : 'border-border bg-secondary text-foreground hover:bg-secondary/80'
          }`}
          title={isVoiceSessionActive ? 'Stop live voice mode' : 'Start live voice mode'}
        >
          {isVoiceLoading && isVoiceSessionActive ? (
            <Loader2 size={20} className="animate-spin" />
          ) : (
            <AudioLines size={20} />
          )}
        </button>

        <button
          onClick={handleSend}
          disabled={isLoading || isBusy || (!text.trim() && files.length === 0)}
          className="rounded-lg bg-primary px-4 py-3 text-primary-foreground transition-colors hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {isLoading ? (
            <Loader2 size={20} className="animate-spin" />
          ) : (
            <Send size={20} />
          )}
        </button>
      </div>

      {isLoading && (
        <div className="mt-2 flex items-center gap-2 text-sm text-muted-foreground">
          <Loader2 size={14} className="animate-spin" />
          Agent is thinking...
        </div>
      )}

      {(isBusy || partialTranscript || statusError) && (
        <div className="mt-2 space-y-2 text-xs">
          {isVoiceSessionActive && (
            <span className="block text-emerald-400">
              {isVoiceLoading
                ? 'Voice mode is responding. It will resume listening when playback completes. Tap the voice button again to stop.'
                : 'Voice mode is live. Speak naturally and PolyMorph will keep the conversation going until you tap the voice button again.'}
            </span>
          )}
          {isMicCaptureActive && (
            <span className="block text-emerald-400">
              Listening live for transcription. Press ✓ when you want the finalized transcript inserted into the composer.
            </span>
          )}
          {isFinalizing && recordingMode === 'asr' && (
            <span className="flex items-center gap-1 text-muted-foreground">
              <Loader2 size={12} className="animate-spin" />
              Finalizing live transcript...
            </span>
          )}
          {partialTranscript && (
            <div className="max-h-32 overflow-y-auto rounded-lg border border-emerald-500/20 bg-emerald-500/5 px-3 py-2 text-sm text-foreground">
              {partialTranscript}
            </div>
          )}
          {statusError && <span className="block text-red-400">{statusError}</span>}
        </div>
      )}
    </div>
  );
}
