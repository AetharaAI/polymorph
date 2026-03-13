'use client';

import { useEffect, useRef, useState } from 'react';
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
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const {
    isRecording,
    isFinalizing,
    mode: recordingMode,
    partialTranscript,
    audioLevels,
    error: recordingError,
    start,
    stop,
  } = useLiveAsrStream();

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 150)}px`;
    }
  }, [text]);

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
    if (isLoading || isVoiceLoading || isRecording || isFinalizing) return;
    setSubmitError(null);
    try {
      await start(mode);
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : 'Unable to start live ASR.');
    }
  };

  const handleStopRecording = async () => {
    if (!recordingMode) return;
    setSubmitError(null);

    try {
      const transcript = await stop();
      const finalText = transcript.trim();
      if (!finalText) {
        throw new Error('Live ASR returned an empty final transcript.');
      }

      if (recordingMode === 'voice') {
        await Promise.resolve(onVoiceTurn(finalText));
      } else {
        setText(previous => appendTranscript(previous, finalText));
      }
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : 'Failed to finalize the live transcript.');
    }
  };

  const statusError = submitError || recordingError;
  const isBusy = isRecording || isFinalizing;

  return (
    <div className="border-t border-border bg-card p-4">
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

        {!isRecording ? (
          <>
            <button
              onClick={() => void handleStartRecording('asr')}
              disabled={isLoading || isVoiceLoading || isFinalizing}
              className="rounded-lg border border-border bg-secondary px-3 py-3 text-foreground transition-colors hover:bg-secondary/80 disabled:cursor-not-allowed disabled:opacity-50"
              title="Start live ASR transcription"
            >
              {isFinalizing && recordingMode === 'asr' ? (
                <Loader2 size={20} className="animate-spin" />
              ) : (
                <Mic size={20} />
              )}
            </button>

            <button
              onClick={() => void handleStartRecording('voice')}
              disabled={isLoading || isVoiceLoading || isFinalizing}
              className="rounded-lg border border-border bg-secondary px-3 py-3 text-foreground transition-colors hover:bg-secondary/80 disabled:cursor-not-allowed disabled:opacity-50"
              title="Start live voice turn"
            >
              {isFinalizing && recordingMode === 'voice' ? (
                <Loader2 size={20} className="animate-spin" />
              ) : (
                <AudioLines size={20} />
              )}
            </button>
          </>
        ) : (
          <button
            onClick={() => void handleStopRecording()}
            className="rounded-lg bg-emerald-500 px-3 py-3 text-black transition-colors hover:bg-emerald-400"
            title="Finish live capture"
          >
            <Check size={20} />
          </button>
        )}

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
          {isRecording && recordingMode === 'voice' && (
            <span className="block text-emerald-400">
              Listening live for a voice turn. Press ✓ when you want the final transcript sent into PolyMorph Voice Mode.
            </span>
          )}
          {isRecording && recordingMode === 'asr' && (
            <span className="block text-emerald-400">
              Listening live for transcription. Press ✓ when you want the finalized transcript inserted into the composer.
            </span>
          )}
          {isFinalizing && (
            <span className="flex items-center gap-1 text-muted-foreground">
              <Loader2 size={12} className="animate-spin" />
              {recordingMode === 'voice'
                ? 'Finalizing live transcript and sending it into PolyMorph Voice Mode...'
                : 'Finalizing live transcript...'}
            </span>
          )}
          {partialTranscript && (
            <div className="rounded-lg border border-emerald-500/20 bg-emerald-500/5 px-3 py-2 text-sm text-foreground">
              {partialTranscript}
            </div>
          )}
          {statusError && <span className="block text-red-400">{statusError}</span>}
        </div>
      )}
    </div>
  );
}
