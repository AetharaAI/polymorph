import { useCallback, useEffect, useRef, useState } from 'react';
import { startLiveAsrStream } from '@/lib/api';

type RecordingMode = 'asr' | 'voice';

const TARGET_SAMPLE_RATE = 16000;
const TARGET_CHANNELS = 1;
const FRAME_ENCODING = 'pcm_s16le';
const BUFFER_SIZE = 4096;
const LEVEL_BAR_COUNT = 18;
const DEFAULT_LEVELS = Array.from({ length: LEVEL_BAR_COUNT }, () => 0.1);

function downsampleMonoBuffer(input: Float32Array, inputSampleRate: number, outputSampleRate: number): Float32Array {
  if (inputSampleRate === outputSampleRate) {
    return input;
  }

  const ratio = inputSampleRate / outputSampleRate;
  const newLength = Math.max(1, Math.round(input.length / ratio));
  const result = new Float32Array(newLength);

  let offsetResult = 0;
  let offsetBuffer = 0;

  while (offsetResult < result.length) {
    const nextOffsetBuffer = Math.min(input.length, Math.round((offsetResult + 1) * ratio));
    let accum = 0;
    let count = 0;
    for (let i = offsetBuffer; i < nextOffsetBuffer; i += 1) {
      accum += input[i];
      count += 1;
    }
    result[offsetResult] = count > 0 ? accum / count : input[Math.min(offsetBuffer, input.length - 1)] || 0;
    offsetResult += 1;
    offsetBuffer = nextOffsetBuffer;
  }

  return result;
}

function interleaveToMono(inputBuffer: AudioBuffer): Float32Array {
  const channelCount = inputBuffer.numberOfChannels;
  if (channelCount <= 1) {
    return inputBuffer.getChannelData(0);
  }

  const frameCount = inputBuffer.length;
  const mono = new Float32Array(frameCount);
  for (let channel = 0; channel < channelCount; channel += 1) {
    const channelData = inputBuffer.getChannelData(channel);
    for (let i = 0; i < frameCount; i += 1) {
      mono[i] += channelData[i] || 0;
    }
  }
  for (let i = 0; i < frameCount; i += 1) {
    mono[i] /= channelCount;
  }
  return mono;
}

function float32ToInt16Bytes(input: Float32Array): Uint8Array {
  const bytes = new Uint8Array(input.length * 2);
  const view = new DataView(bytes.buffer);
  for (let i = 0; i < input.length; i += 1) {
    const sample = Math.max(-1, Math.min(1, input[i] || 0));
    view.setInt16(i * 2, sample < 0 ? sample * 0x8000 : sample * 0x7fff, true);
  }
  return bytes;
}

function bytesToBase64(bytes: Uint8Array): string {
  let binary = '';
  const chunkSize = 0x8000;
  for (let i = 0; i < bytes.length; i += chunkSize) {
    const chunk = bytes.subarray(i, i + chunkSize);
    binary += String.fromCharCode(...Array.from(chunk));
  }
  return btoa(binary);
}

interface UseLiveAsrStreamResult {
  isRecording: boolean;
  isFinalizing: boolean;
  mode: RecordingMode | null;
  partialTranscript: string;
  audioLevels: number[];
  error: string | null;
  start: (mode: RecordingMode) => Promise<void>;
  stop: () => Promise<string>;
}

export function useLiveAsrStream(): UseLiveAsrStreamResult {
  const [isRecording, setIsRecording] = useState(false);
  const [isFinalizing, setIsFinalizing] = useState(false);
  const [mode, setMode] = useState<RecordingMode | null>(null);
  const [partialTranscript, setPartialTranscript] = useState('');
  const [audioLevels, setAudioLevels] = useState<number[]>(DEFAULT_LEVELS);
  const [error, setError] = useState<string | null>(null);

  const streamRef = useRef<MediaStream | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const sourceRef = useRef<MediaStreamAudioSourceNode | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const processorRef = useRef<ScriptProcessorNode | null>(null);
  const monitorGainRef = useRef<GainNode | null>(null);
  const rafIdRef = useRef<number | null>(null);
  const sequenceRef = useRef(0);
  const startedAtRef = useRef(0);
  const stoppedRef = useRef(false);
  const finalTranscriptRef = useRef('');
  const finalizeTimerRef = useRef<number | null>(null);
  const finalPromiseRef = useRef<{
    resolve: (value: string) => void;
    reject: (reason?: unknown) => void;
  } | null>(null);

  const resetLevels = () => {
    setAudioLevels(Array.from({ length: LEVEL_BAR_COUNT }, () => 0.1));
  };

  const clearFinalizeTimer = () => {
    if (finalizeTimerRef.current != null) {
      window.clearTimeout(finalizeTimerRef.current);
      finalizeTimerRef.current = null;
    }
  };

  const resolvePendingFinal = useCallback((value: string) => {
    clearFinalizeTimer();
    const pending = finalPromiseRef.current;
    finalPromiseRef.current = null;
    if (pending) {
      pending.resolve(value);
    }
  }, []);

  const rejectPendingFinal = useCallback((reason: unknown) => {
    clearFinalizeTimer();
    const pending = finalPromiseRef.current;
    finalPromiseRef.current = null;
    if (pending) {
      pending.reject(reason);
    }
  }, []);

  const cleanup = useCallback((options?: { closeSocket?: boolean; preserveTranscript?: boolean; preserveError?: boolean }) => {
    if (rafIdRef.current != null) {
      cancelAnimationFrame(rafIdRef.current);
      rafIdRef.current = null;
    }

    processorRef.current?.disconnect();
    processorRef.current = null;
    sourceRef.current?.disconnect();
    sourceRef.current = null;
    analyserRef.current?.disconnect();
    analyserRef.current = null;
    monitorGainRef.current?.disconnect();
    monitorGainRef.current = null;

    if (audioContextRef.current) {
      void audioContextRef.current.close().catch(() => undefined);
      audioContextRef.current = null;
    }

    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }

    if (options?.closeSocket !== false && wsRef.current) {
      wsRef.current.onopen = null;
      wsRef.current.onmessage = null;
      wsRef.current.onerror = null;
      wsRef.current.onclose = null;
      if (wsRef.current.readyState === WebSocket.OPEN || wsRef.current.readyState === WebSocket.CONNECTING) {
        wsRef.current.close();
      }
      wsRef.current = null;
    }

    setIsRecording(false);
    setIsFinalizing(false);
    setMode(null);
    if (!options?.preserveError) {
      setError(null);
    }
    resetLevels();
    if (!options?.preserveTranscript) {
      setPartialTranscript('');
      finalTranscriptRef.current = '';
    }
  }, []);

  useEffect(() => () => {
    cleanup();
    rejectPendingFinal(new Error('Live ASR session was cancelled.'));
  }, [cleanup, rejectPendingFinal]);

  const startAudioMonitor = useCallback((analyser: AnalyserNode) => {
    const samples = new Uint8Array(analyser.frequencyBinCount);
    const tick = () => {
      const activeAnalyser = analyserRef.current;
      if (!activeAnalyser) {
        return;
      }
      activeAnalyser.getByteFrequencyData(samples);
      const bucket = Math.max(1, Math.floor(samples.length / LEVEL_BAR_COUNT));
      const next = Array.from({ length: LEVEL_BAR_COUNT }, (_, index) => {
        const start = index * bucket;
        const end = Math.min(samples.length, start + bucket);
        let sum = 0;
        for (let i = start; i < end; i += 1) {
          sum += samples[i];
        }
        const average = sum / Math.max(1, end - start);
        return Math.min(1, Math.max(0.08, average / 255));
      });
      setAudioLevels(next);
      rafIdRef.current = requestAnimationFrame(tick);
    };
    tick();
  }, []);

  const start = useCallback(async (nextMode: RecordingMode) => {
    if (isRecording || isFinalizing) {
      return;
    }

    cleanup();
    setError(null);
    setMode(nextMode);
    setPartialTranscript('');
    finalTranscriptRef.current = '';
    sequenceRef.current = 0;
    startedAtRef.current = Date.now();
    stoppedRef.current = false;

    try {
      const liveSession = await startLiveAsrStream({
        model: 'auto',
        language: 'auto',
        sample_rate: TARGET_SAMPLE_RATE,
        encoding: FRAME_ENCODING,
        channels: TARGET_CHANNELS,
        triage_enabled: false,
        metadata: { source: nextMode === 'voice' ? 'polymorph-voice' : 'polymorph-mic' },
      });

      const ws = await new Promise<WebSocket>((resolve, reject) => {
        const socket = new WebSocket(liveSession.ws_url);
        const handleError = () => {
          socket.onopen = null;
          socket.onerror = null;
          reject(new Error('Unable to connect to the live ASR websocket.'));
        };
        socket.onopen = () => {
          socket.onopen = null;
          socket.onerror = null;
          resolve(socket);
        };
        socket.onerror = handleError;
      });

      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          channelCount: TARGET_CHANNELS,
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      });

      const AudioContextCtor = window.AudioContext || (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
      if (!AudioContextCtor) {
        ws.close();
        stream.getTracks().forEach(track => track.stop());
        throw new Error('This browser does not support AudioContext for live ASR.');
      }

      const audioContext = new AudioContextCtor();
      await audioContext.resume();
      const source = audioContext.createMediaStreamSource(stream);
      const analyser = audioContext.createAnalyser();
      analyser.fftSize = 512;
      const processor = audioContext.createScriptProcessor(BUFFER_SIZE, TARGET_CHANNELS, TARGET_CHANNELS);
      const silentGain = audioContext.createGain();
      silentGain.gain.value = 0;

      wsRef.current = ws;
      streamRef.current = stream;
      audioContextRef.current = audioContext;
      sourceRef.current = source;
      analyserRef.current = analyser;
      processorRef.current = processor;
      monitorGainRef.current = silentGain;

      ws.onmessage = event => {
        try {
          const message = JSON.parse(String(event.data)) as { type?: string; text?: string };
          if (message.type === 'partial_transcript') {
            setPartialTranscript((message.text || '').trim());
            return;
          }
          if (message.type === 'final_transcript') {
            const finalText = (message.text || '').trim();
            finalTranscriptRef.current = finalText;
            setPartialTranscript(finalText);
            if (stoppedRef.current) {
              resolvePendingFinal(finalText);
              cleanup({ preserveTranscript: false });
            }
          }
        } catch {
          // Ignore malformed websocket messages from upstream.
        }
      };

      ws.onerror = () => {
        const nextError = new Error('Live ASR stream error.');
        setError(nextError.message);
        rejectPendingFinal(nextError);
        cleanup({ preserveTranscript: false, preserveError: true });
      };

      ws.onclose = () => {
        wsRef.current = null;
        if (!stoppedRef.current) {
          const nextError = new Error('Live ASR stream closed unexpectedly.');
          setError(nextError.message);
          rejectPendingFinal(nextError);
          cleanup({ closeSocket: false, preserveTranscript: false, preserveError: true });
          return;
        }
        if (finalPromiseRef.current) {
          if (finalTranscriptRef.current.trim()) {
            resolvePendingFinal(finalTranscriptRef.current.trim());
          } else {
            rejectPendingFinal(new Error('Live ASR ended without a final transcript.'));
          }
        }
        cleanup({ closeSocket: false, preserveTranscript: false });
      };

      processor.onaudioprocess = event => {
        const activeWs = wsRef.current;
        if (!activeWs || activeWs.readyState !== WebSocket.OPEN || stoppedRef.current) {
          return;
        }
        const monoSamples = interleaveToMono(event.inputBuffer);
        const downsampled = downsampleMonoBuffer(monoSamples, audioContext.sampleRate, TARGET_SAMPLE_RATE);
        if (downsampled.length === 0) {
          return;
        }
        const bytes = float32ToInt16Bytes(downsampled);
        sequenceRef.current += 1;
        activeWs.send(JSON.stringify({
          type: 'audio_frame',
          seq: sequenceRef.current,
          timestamp_ms: Date.now() - startedAtRef.current,
          sample_rate: TARGET_SAMPLE_RATE,
          encoding: FRAME_ENCODING,
          channels: TARGET_CHANNELS,
          payload_b64: bytesToBase64(bytes),
        }));
      };

      source.connect(analyser);
      source.connect(processor);
      processor.connect(silentGain);
      silentGain.connect(audioContext.destination);
      startAudioMonitor(analyser);
      setIsRecording(true);
    } catch (error) {
      const nextError = error instanceof Error ? error : new Error('Unable to start live ASR.');
      setError(nextError.message);
      cleanup({ preserveError: true });
      throw nextError;
    }
  }, [cleanup, isFinalizing, isRecording, rejectPendingFinal, resolvePendingFinal, startAudioMonitor]);

  const stop = useCallback(async () => {
    if (!isRecording && !isFinalizing) {
      return '';
    }

    if (finalTranscriptRef.current.trim()) {
      const finalText = finalTranscriptRef.current.trim();
      cleanup({ preserveTranscript: false });
      return finalText;
    }

    const ws = wsRef.current;
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      cleanup({ preserveTranscript: false });
      throw new Error('Live ASR websocket is not open.');
    }

    stoppedRef.current = true;
    setIsRecording(false);
    setIsFinalizing(true);
    setError(null);

    const finalTranscript = await new Promise<string>((resolve, reject) => {
      finalPromiseRef.current = { resolve, reject };
      clearFinalizeTimer();
      finalizeTimerRef.current = window.setTimeout(() => {
        rejectPendingFinal(new Error('Timed out waiting for the final ASR transcript.'));
        cleanup({ preserveTranscript: false });
      }, 15000);
      ws.send(JSON.stringify({ type: 'end_stream' }));
    });

    cleanup({ preserveTranscript: false });
    return finalTranscript;
  }, [cleanup, isFinalizing, isRecording, rejectPendingFinal]);

  return {
    isRecording,
    isFinalizing,
    mode,
    partialTranscript,
    audioLevels,
    error,
    start,
    stop,
  };
}
