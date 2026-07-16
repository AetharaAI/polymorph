'use client';

import { useCallback, useEffect, useMemo, useRef } from 'react';
import { Message, ToolCall } from '@/lib/types';
import { MessageBubble } from './MessageBubble';
import { Loader2, Search, FileCode, FileText, Calculator } from 'lucide-react';

interface ChatWindowProps {
  messages: Message[];
  toolCalls: ToolCall[];
  isLoading: boolean;
}

const suggestedPrompts = [
  { icon: <Search size={16} />, text: "Search the web for latest AI news" },
  { icon: <FileCode size={16} />, text: "Write and run Python code to calculate factorial" },
  { icon: <FileText size={16} />, text: "Analyze this file and summarize it" },
  { icon: <Calculator size={16} />, text: "Calculate the square root of 12345" }
];

export function ChatWindow({ messages, toolCalls, isLoading }: ChatWindowProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const finalResponseRef = useRef<HTMLDivElement>(null);
  const autoFollowModeRef = useRef<'bottom' | 'final' | 'off'>('bottom');
  const suppressScrollHandlerRef = useRef(false);
  const previousAssistantMessageIdRef = useRef<string | null>(null);
  const previousAssistantHadTextRef = useRef(false);

  const activeAssistantMessage = useMemo(() => {
    const lastMessage = messages[messages.length - 1];
    return lastMessage?.role === 'assistant' ? lastMessage : null;
  }, [messages]);

  const finalResponseStarted = Boolean(
    activeAssistantMessage?.content.some(
      content => content.type === 'text' && typeof content.text === 'string' && content.text.trim().length > 0
    )
  );

  const isNearBottom = useCallback((container: HTMLDivElement) => {
    return container.scrollHeight - (container.scrollTop + container.clientHeight) <= 80;
  }, []);

  const isNearFinalRegion = useCallback((container: HTMLDivElement, anchor: HTMLDivElement | null) => {
    if (!anchor) return false;
    const containerRect = container.getBoundingClientRect();
    const anchorRect = anchor.getBoundingClientRect();
    return (
      anchorRect.top <= containerRect.top + 120 &&
      anchorRect.bottom >= containerRect.top - 120
    );
  }, []);

  const scrollToTopPosition = useCallback((top: number) => {
    const container = containerRef.current;
    if (!container) return;
    suppressScrollHandlerRef.current = true;
    container.scrollTo({ top: Math.max(0, top), behavior: 'auto' });
    window.requestAnimationFrame(() => {
      suppressScrollHandlerRef.current = false;
    });
  }, []);

  const scrollToBottom = useCallback(() => {
    const container = containerRef.current;
    if (!container) return;
    scrollToTopPosition(container.scrollHeight);
  }, [scrollToTopPosition]);

  const scrollToFinalResponse = useCallback(() => {
    const container = containerRef.current;
    const anchor = finalResponseRef.current;
    if (!container || !anchor) return;
    const containerRect = container.getBoundingClientRect();
    const anchorRect = anchor.getBoundingClientRect();
    const nextTop = container.scrollTop + (anchorRect.top - containerRect.top) - 12;
    scrollToTopPosition(nextTop);
  }, [scrollToTopPosition]);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const onScroll = () => {
      if (suppressScrollHandlerRef.current) {
        return;
      }

      const nearBottom = isNearBottom(container);
      const nearFinal = isNearFinalRegion(container, finalResponseRef.current);

      if (nearBottom || nearFinal) {
        autoFollowModeRef.current = finalResponseStarted ? 'final' : 'bottom';
        return;
      }

      autoFollowModeRef.current = 'off';
    };

    container.addEventListener('scroll', onScroll, { passive: true });
    return () => {
      container.removeEventListener('scroll', onScroll);
    };
  }, [finalResponseStarted, isNearBottom, isNearFinalRegion]);

  useEffect(() => {
    const currentAssistantId = activeAssistantMessage?.id || null;
    const isNewAssistantMessage = currentAssistantId !== previousAssistantMessageIdRef.current;

    if (isNewAssistantMessage) {
      previousAssistantMessageIdRef.current = currentAssistantId;
      previousAssistantHadTextRef.current = false;
      autoFollowModeRef.current = 'bottom';
    }

    if (finalResponseStarted && !previousAssistantHadTextRef.current) {
      autoFollowModeRef.current = 'final';
      previousAssistantHadTextRef.current = true;
      window.requestAnimationFrame(scrollToFinalResponse);
      return;
    }

    if (finalResponseStarted) {
      previousAssistantHadTextRef.current = true;
      if (autoFollowModeRef.current === 'final') {
        window.requestAnimationFrame(scrollToFinalResponse);
      }
      return;
    }

    previousAssistantHadTextRef.current = false;
    if (autoFollowModeRef.current === 'bottom') {
      window.requestAnimationFrame(scrollToBottom);
    }
  }, [activeAssistantMessage?.id, finalResponseStarted, messages, isLoading, scrollToBottom, scrollToFinalResponse]);

  if (messages.length === 0 && !isLoading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-8">
        <img
          src="/branding/ember-orb-mark.png"
          alt="PolyMorph ambient mark"
          className="mb-5 h-24 w-24 object-contain drop-shadow-[0_0_34px_rgba(249,115,22,0.32)]"
        />
        <h2 className="text-3xl font-bold tracking-tight mb-2">PolyMorph</h2>
        <p className="text-muted-foreground mb-8">
          Agentic harness for autonomous persistent digital intelligence
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl w-full">
          {suggestedPrompts.map((prompt, i) => (
            <button
              key={i}
              className="flex items-center gap-3 p-4 bg-card border border-border rounded-lg hover:border-primary transition-colors text-left"
            >
              <span className="text-primary">{prompt.icon}</span>
              <span className="text-sm">{prompt.text}</span>
            </button>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      className="min-h-0 flex-1 overflow-y-auto p-4"
    >
      {messages.map(message => (
        <MessageBubble
          key={message.id}
          message={message}
          toolCalls={toolCalls}
          finalResponseAnchorRef={message.id === activeAssistantMessage?.id && finalResponseStarted ? finalResponseRef : undefined}
        />
      ))}

      {isLoading && messages.length > 0 && (
        <div className="flex items-center gap-2 text-muted-foreground p-4">
          <Loader2 size={16} className="animate-spin" />
          <span className="text-sm">Agent is thinking...</span>
        </div>
      )}
    </div>
  );
}
