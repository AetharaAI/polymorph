'use client';

import { Copy, Check } from 'lucide-react';
import { Ref, useMemo, useState } from 'react';
import { Message } from '@/lib/types';
import { ThinkingBlock } from './ThinkingBlock';
import { ToolCallCard } from './ToolCallCard';
import { ToolCall } from '@/lib/types';
import { MarkdownMessage } from './MarkdownMessage';

interface MessageBubbleProps {
  message: Message;
  toolCalls: ToolCall[];
  finalResponseAnchorRef?: Ref<HTMLDivElement>;
}

export function MessageBubble({ message, toolCalls, finalResponseAnchorRef }: MessageBubbleProps) {
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

  const textContents = message.content.filter(c => c.type === 'text');
  const skillContents = message.content.filter(c => c.type === 'skill');
  const toolUseIds = useMemo(
    () => new Set(message.content.filter(c => c.type === 'tool_use' && c.tool_id).map(c => c.tool_id as string)),
    [message.content]
  );
  const firstTextIndex = message.content.findIndex(
    c => c.type === 'text' && typeof c.text === 'string' && c.text.trim().length > 0
  );

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

        {message.content.map((content, i) => {
          if (content.type === 'skill') {
            return null;
          }

          if (content.type === 'thinking' && !isUser) {
            return <ThinkingBlock key={`thinking-${i}`} text={content.thinking || ''} />;
          }

          if (content.type === 'text') {
            const text = content.text || '';
            if (!text) return null;
            const anchorRef = !isUser && i === firstTextIndex ? finalResponseAnchorRef : undefined;
            return (
              <div
                key={`text-${i}`}
                ref={anchorRef}
                className={isUser ? 'text-sm whitespace-pre-wrap break-words [overflow-wrap:anywhere]' : 'text-sm break-words [overflow-wrap:anywhere]'}
              >
                {isUser ? text : <MarkdownMessage content={text} />}
              </div>
            );
          }

          if (content.type === 'input_audio' || content.type === 'audio_url') {
            return (
              <div
                key={`${content.type}-${i}`}
                className={`mt-2 text-xs rounded border px-2 py-1 ${
                  isUser
                    ? 'border-primary-foreground/20 bg-primary-foreground/10 text-primary-foreground/80'
                    : 'border-border bg-secondary text-muted-foreground'
                }`}
              >
                Voice input attached
              </div>
            );
          }

          if (content.type === 'tool_use' && !isUser) {
            const toolCall = toolCalls.find(tc => tc.tool_id === content.tool_id);
            const fallbackResult = message.content.find(
              block => block.type === 'tool_result' && block.tool_id === content.tool_id
            )?.result;

            return (
              <ToolCallCard
                key={content.tool_id || `tool-use-${i}`}
                toolCall={toolCall || {
                  tool_name: content.tool_name || '',
                  tool_id: content.tool_id || '',
                  input: content.input || {},
                  status: 'completed',
                  result: fallbackResult
                }}
              />
            );
          }

          if (content.type === 'tool_result' && !isUser) {
            if (content.tool_id && toolUseIds.has(content.tool_id)) {
              return null;
            }
            return (
              <ToolCallCard
                key={content.tool_id || `tool-result-${i}`}
                toolCall={{
                  tool_name: 'result',
                  tool_id: content.tool_id || '',
                  input: {},
                  status: 'completed',
                  result: content.result
                }}
              />
            );
          }

          return null;
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
