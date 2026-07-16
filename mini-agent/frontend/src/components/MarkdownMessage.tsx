'use client';

import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface MarkdownMessageProps {
  content: string;
}

export function MarkdownMessage({ content }: MarkdownMessageProps) {
  return (
    <div className="space-y-3 text-sm break-words [overflow-wrap:anywhere]">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({ node: _node, ...props }) => <h1 className="mt-5 text-xl font-semibold tracking-tight first:mt-0" {...props} />,
          h2: ({ node: _node, ...props }) => <h2 className="mt-4 text-lg font-semibold tracking-tight first:mt-0" {...props} />,
          h3: ({ node: _node, ...props }) => <h3 className="mt-4 text-base font-semibold tracking-tight first:mt-0" {...props} />,
          p: ({ node: _node, ...props }) => <p className="leading-7" {...props} />,
          ul: ({ node: _node, ...props }) => <ul className="list-disc pl-5 space-y-1" {...props} />,
          ol: ({ node: _node, ...props }) => <ol className="list-decimal pl-5 space-y-1" {...props} />,
          li: ({ node: _node, ...props }) => <li className="leading-7" {...props} />,
          a: ({ node: _node, ...props }) => (
            <a
              className="text-sky-300 underline underline-offset-2 hover:text-sky-200"
              target="_blank"
              rel="noreferrer noopener"
              {...props}
            />
          ),
          table: ({ node: _node, ...props }) => (
            <div className="my-3 overflow-x-auto">
              <table className="min-w-full border-collapse text-left text-xs sm:text-sm" {...props} />
            </div>
          ),
          thead: ({ node: _node, ...props }) => <thead className="bg-secondary/70" {...props} />,
          th: ({ node: _node, ...props }) => <th className="border border-border px-3 py-2 font-medium" {...props} />,
          td: ({ node: _node, ...props }) => <td className="border border-border px-3 py-2 align-top" {...props} />,
          blockquote: ({ node: _node, ...props }) => (
            <blockquote className="border-l-2 border-primary/40 pl-3 italic text-muted-foreground" {...props} />
          ),
          code({ node: _node, className, children, ...props }) {
            const isBlock = Boolean(className);
            if (isBlock) {
              return (
                <code className={`${className} block whitespace-pre-wrap break-words`} {...props}>
                  {children}
                </code>
              );
            }

            return (
              <code className="rounded bg-secondary px-1.5 py-0.5 text-[0.9em]" {...props}>
                {children}
              </code>
            );
          },
          pre: ({ node: _node, ...props }) => (
            <pre className="my-3 overflow-x-auto rounded-lg bg-background px-3 py-3 text-xs sm:text-sm" {...props} />
          ),
          hr: ({ node: _node, ...props }) => <hr className="border-border/80" {...props} />,
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
