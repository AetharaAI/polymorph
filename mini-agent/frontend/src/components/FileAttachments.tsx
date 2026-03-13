'use client';

import { FileText, X, Upload } from 'lucide-react';
import { FileAttachment } from '@/lib/types';

interface FileAttachmentsProps {
  files: FileAttachment[];
  onRemove: (fileId: string) => void;
  onAddClick: () => void;
}

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function getFileIcon(filename: string) {
  return <FileText size={14} />;
}

export function FileAttachments({ files, onRemove, onAddClick }: FileAttachmentsProps) {
  if (files.length === 0) {
    return (
      <button
        onClick={onAddClick}
        className="flex items-center gap-2 text-muted-foreground hover:text-foreground text-sm px-3 py-1 rounded hover:bg-secondary transition-colors"
      >
        <Upload size={14} />
        Attach files
      </button>
    );
  }

  return (
    <div className="flex flex-wrap gap-2 p-2">
      {files.map(file => (
        <div
          key={file.file_id}
          className="flex items-center gap-2 bg-secondary px-2 py-1 rounded text-sm"
        >
          {getFileIcon(file.filename)}
          <span className="max-w-[120px] truncate">{file.filename}</span>
          <span className="text-muted-foreground text-xs">
            {formatSize(file.size)}
          </span>
          <button
            onClick={() => onRemove(file.file_id)}
            className="text-muted-foreground hover:text-destructive transition-colors"
          >
            <X size={14} />
          </button>
        </div>
      ))}
      <button
        onClick={onAddClick}
        className="flex items-center gap-1 text-muted-foreground hover:text-foreground text-sm px-2 py-1 rounded hover:bg-secondary transition-colors"
      >
        <Upload size={14} />
        Add more
      </button>
    </div>
  );
}
