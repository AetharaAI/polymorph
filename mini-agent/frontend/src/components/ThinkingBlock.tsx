'use client';

import { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';

interface ThinkingBlockProps {
  text: string;
}

export function ThinkingBlock({ text }: ThinkingBlockProps) {
  const [isExpanded, setIsExpanded] = useState(true);

  return (
    <div className="border-l-2 border-thinking pl-3 my-2">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex items-center gap-2 text-thinking text-sm hover:text-thinking/80 transition-colors"
      >
        <span className="animate-thinking">Thinking...</span>
        {isExpanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
      </button>

      {isExpanded && (
        <div className="mt-2 text-thinking/90 text-sm whitespace-pre-wrap break-words [overflow-wrap:anywhere] [word-break:break-word] bg-thinking/10 p-2 rounded min-w-0 max-w-full">
          {text}
        </div>
      )}
    </div>
  );
}
