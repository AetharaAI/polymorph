'use client';

import { useState } from 'react';
import { Search, FileCode, FileText, Terminal, Calculator, Loader2, ChevronDown, ChevronUp } from 'lucide-react';
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
  const [isExpanded, setIsExpanded] = useState(true);

  return (
    <div className="border border-accent/30 bg-accent/5 rounded-lg my-2 overflow-hidden animate-slide-in max-w-full min-w-0">
      <div className="flex items-center gap-2 px-3 py-2 bg-accent/10 border-b border-accent/20">
        <span className="text-accent">{toolIcons[toolCall.tool_name]}</span>
        <span className="text-accent font-medium text-sm min-w-0 truncate">
          {toolLabels[toolCall.tool_name] || toolCall.tool_name}
        </span>
        {toolCall.status === 'loading' && (
          <Loader2 size={14} className="animate-spin text-accent ml-auto" />
        )}
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="ml-auto text-muted-foreground hover:text-foreground transition-colors"
        >
          {isExpanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
        </button>
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
    </div>
  );
}
