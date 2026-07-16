'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import { Search, FileCode, FileText, Terminal, Calculator, Loader2, ChevronDown, ChevronUp, Copy, Check } from 'lucide-react';
import { ToolCall } from '@/lib/types';

const toolIcons: Record<string, React.ReactNode> = {
  web_search: <Search size={16} />,
  tavily_search: <Search size={16} />,
  execute_python: <FileCode size={16} />,
  read_file: <FileText size={16} />,
  list_files: <FileText size={16} />,
  write_file: <FileText size={16} />,
  run_shell: <Terminal size={16} />,
  calculate: <Calculator size={16} />,
  summarize_document: <FileText size={16} />
};

const toolLabels: Record<string, string> = {
  web_search: 'Web Search',
  tavily_search: 'Tavily Search',
  execute_python: 'Python',
  read_file: 'Read File',
  list_files: 'List Files',
  write_file: 'Write File',
  run_shell: 'Shell',
  calculate: 'Calculator',
  summarize_document: 'Summarize'
};

interface ToolCallCardProps {
  toolCall: ToolCall;
}

export function ToolCallCard({ toolCall }: ToolCallCardProps) {
  const [isExpanded, setIsExpanded] = useState(toolCall.status === 'loading');
  const [copied, setCopied] = useState(false);
  const previousStatusRef = useRef(toolCall.status);

  useEffect(() => {
    const previousStatus = previousStatusRef.current;
    if (toolCall.status === 'loading') {
      setIsExpanded(true);
    } else if (previousStatus === 'loading') {
      setIsExpanded(false);
    }
    previousStatusRef.current = toolCall.status;
  }, [toolCall.status]);

  const resultPreview = useMemo(() => {
    const preview = (toolCall.result || '').replace(/\s+/g, ' ').trim();
    return preview.length > 140 ? `${preview.slice(0, 140)}...` : preview;
  }, [toolCall.result]);

  const handleCopy = async () => {
    const payload = {
      tool_name: toolCall.tool_name,
      tool_id: toolCall.tool_id,
      status: toolCall.status,
      input: toolCall.input,
      result: toolCall.result,
    };
    await navigator.clipboard.writeText(JSON.stringify(payload, null, 2));
    setCopied(true);
    window.setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="border border-accent/30 bg-accent/5 rounded-lg my-2 overflow-hidden animate-slide-in max-w-full min-w-0">
      <div className="flex items-center gap-2 px-3 py-2 bg-accent/10 border-b border-accent/20">
        <span className="text-accent">{toolIcons[toolCall.tool_name]}</span>
        <span className="text-accent font-medium text-sm min-w-0 truncate">
          {toolLabels[toolCall.tool_name] || toolCall.tool_name}
        </span>
        <div className="ml-auto flex items-center gap-2">
          {toolCall.status === 'loading' && (
            <Loader2 size={14} className="animate-spin text-accent" />
          )}
          {toolCall.status !== 'loading' && (
            <span className="text-[11px] uppercase tracking-wide text-muted-foreground">
              {toolCall.status}
            </span>
          )}
          <button
            onClick={() => void handleCopy()}
            className="text-muted-foreground hover:text-foreground transition-colors"
            title="Copy tool call"
          >
            {copied ? <Check size={14} /> : <Copy size={14} />}
          </button>
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-muted-foreground hover:text-foreground transition-colors"
            title={isExpanded ? 'Collapse tool call' : 'Expand tool call'}
          >
            {isExpanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
          </button>
        </div>
      </div>

      {isExpanded && (
        <>
          <div className="p-3 min-w-0">
            <div className="text-xs text-muted-foreground mb-1">Input:</div>
            <pre className="text-xs bg-secondary p-2 rounded overflow-x-auto max-w-full whitespace-pre-wrap break-words [overflow-wrap:anywhere] [word-break:break-word] min-w-0">
              {JSON.stringify(toolCall.input, null, 2)}
            </pre>
          </div>

          {toolCall.result && (
            <div className="border-t border-accent/20 p-3 min-w-0">
              <div className="text-xs text-muted-foreground mb-1">Result:</div>
              <pre className="text-xs bg-background p-2 rounded overflow-x-auto max-h-40 max-w-full whitespace-pre-wrap break-words [overflow-wrap:anywhere] [word-break:break-word] min-w-0">
                {toolCall.result}
              </pre>
            </div>
          )}
        </>
      )}

      {!isExpanded && (
        <div className="px-3 py-2 text-xs text-muted-foreground">
          {resultPreview || 'Completed without visible result payload.'}
        </div>
      )}
    </div>
  );
}
