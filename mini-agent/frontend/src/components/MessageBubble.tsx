'use client';

import { Copy, Check } from 'lucide-react';
import { useState } from 'react';
import { Message } from '@/lib/types';
import { ThinkingBlock } from './ThinkingBlock';
import { ToolCallCard } from './ToolCallCard';
import { ToolCall } from '@/lib/types';

interface MessageBubbleProps {
  message: Message;
  toolCalls: ToolCall[];
}

export function MessageBubble({ message, toolCalls }: MessageBubbleProps) {
  const [copied, setCopied] = useState(false);

  const isUser = message.role === 'user';

  const handleCopy = () => {
    const text = message.content
      .filter(c => c.type === 'text')
      .map(c => c.text)
      .join('');
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Get thinking content
  const thinkingContent = message.content.find(c => c.type === 'thinking');
  // Get text content
  const textContents = message.content.filter(c => c.type === 'text');
  // Get tool use content
  const toolUseContents = message.content.filter(c => c.type === 'tool_use');
  // Get tool result content
  const toolResultContents = message.content.filter(c => c.type === 'tool_result');
  // Get selected skills
  const skillContents = message.content.filter(c => c.type === 'skill');
  const audioContents = message.content.filter(c => c.type === 'input_audio' || c.type === 'audio_url');

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`min-w-0 w-full ${isUser ? 'max-w-[82%]' : 'max-w-[74%]'} rounded-lg p-4 overflow-hidden [overflow-wrap:anywhere] [word-break:break-word] ${
          isUser
            ? 'bg-primary text-primary-foreground'
            : 'bg-card border border-border'
        }`}
      >
        {!isUser && skillContents.length > 0 && (
          <div className="mb-2 flex flex-wrap gap-2">
            {skillContents.map((skill, i) => (
              <div
                key={`${skill.skill_name}-${skill.skill_file}-${i}`}
                className="text-[11px] px-2 py-1 rounded border border-emerald-500/30 bg-emerald-500/10 text-emerald-300 max-w-full truncate"
                title={`${skill.skill_name} • ${skill.skill_file}\n${skill.skill_reason || ''}`}
              >
                Skill: {skill.skill_name || 'unknown'}
              </div>
            ))}
          </div>
        )}

        {/* Thinking block */}
        {thinkingContent && !isUser && (
          <ThinkingBlock text={thinkingContent.thinking || ''} />
        )}

        {/* Text content */}
        {textContents.map((content, i) => (
          <div key={i} className="text-sm whitespace-pre-wrap break-words [overflow-wrap:anywhere]">
            {content.text}
          </div>
        ))}

        {audioContents.length > 0 && (
          <div className={`mt-2 text-xs rounded border px-2 py-1 ${
            isUser
              ? 'border-primary-foreground/20 bg-primary-foreground/10 text-primary-foreground/80'
              : 'border-border bg-secondary text-muted-foreground'
          }`}>
            Voice input attached
          </div>
        )}

        {/* Tool calls */}
        {!isUser && toolUseContents.map((toolUse, i) => {
          const toolCall = toolCalls.find(tc => tc.tool_id === toolUse.tool_id);
          return (
            <ToolCallCard
              key={toolUse.tool_id || i}
              toolCall={toolCall || {
                tool_name: toolUse.tool_name || '',
                tool_id: toolUse.tool_id || '',
                input: toolUse.input || {},
                status: 'completed',
                result: toolResultContents.find(tr => tr.tool_id === toolUse.tool_id)?.result
              }}
            />
          );
        })}

        {/* Tool results in message */}
        {!isUser && toolResultContents.map((tr, i) => {
          const alreadyShown = toolCalls.some(tc => tc.tool_id === tr.tool_id);
          if (alreadyShown) return null;
          return (
            <ToolCallCard
              key={tr.tool_id || i}
              toolCall={{
                tool_name: 'result',
                tool_id: tr.tool_id || '',
                input: {},
                status: 'completed',
                result: tr.result
              }}
            />
          );
        })}

        {/* Timestamp and copy button */}
        <div className={`flex items-center gap-2 mt-2 text-xs ${
          isUser ? 'text-primary-foreground/70' : 'text-muted-foreground'
        }`}>
          <span>{new Date(message.timestamp).toLocaleTimeString()}</span>
          {!isUser && (
            <button
              onClick={handleCopy}
              className="hover:text-foreground transition-colors"
              title="Copy"
            >
              {copied ? <Check size={12} /> : <Copy size={12} />}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
