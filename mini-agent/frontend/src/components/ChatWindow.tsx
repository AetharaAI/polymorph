'use client';

import { useEffect, useRef } from 'react';
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

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

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
      className="flex-1 overflow-y-auto p-4"
    >
      {messages.map(message => (
        <MessageBubble
          key={message.id}
          message={message}
          toolCalls={toolCalls}
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
