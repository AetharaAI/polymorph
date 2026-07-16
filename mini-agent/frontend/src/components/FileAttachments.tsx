'use client';

import { FileImage, FileText, Loader2, Upload, X } from 'lucide-react';
import { useState } from 'react';
import { FileAttachment } from '@/lib/types';
import { getFilePreview, FilePreviewResponse } from '@/lib/api';

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
  if (/\.(png|jpe?g|webp|gif|bmp)$/i.test(filename)) {
    return <FileImage size={14} />;
  }
  return <FileText size={14} />;
}

export function FileAttachments({ files, onRemove, onAddClick }: FileAttachmentsProps) {
  const [preview, setPreview] = useState<FilePreviewResponse | null>(null);
  const [previewLoading, setPreviewLoading] = useState(false);
  const [previewError, setPreviewError] = useState<string | null>(null);

  const openPreview = async (fileId: string) => {
    setPreviewLoading(true);
    setPreviewError(null);
    try {
      const next = await getFilePreview(fileId);
      setPreview(next);
    } catch (error) {
      setPreviewError(error instanceof Error ? error.message : 'Failed to load preview.');
    } finally {
      setPreviewLoading(false);
    }
  };

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
    <>
      <div className="flex flex-wrap gap-2 p-2">
        {files.map(file => (
          <div
            key={file.file_id}
            className="flex items-center gap-2 bg-secondary px-2 py-1 rounded text-sm"
          >
            <button
              onClick={() => {
                if (/\.(png|jpe?g|webp|gif|bmp)$/i.test(file.filename)) {
                  void openPreview(file.file_id);
                }
              }}
              className={`flex items-center gap-2 ${/\.(png|jpe?g|webp|gif|bmp)$/i.test(file.filename) ? 'hover:text-foreground' : ''}`}
              title={/\.(png|jpe?g|webp|gif|bmp)$/i.test(file.filename) ? 'Preview image' : file.filename}
            >
              {getFileIcon(file.filename)}
              <span className="max-w-[120px] truncate">{file.filename}</span>
            </button>
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

      {(previewLoading || previewError || preview) && (
        <div className="mt-2 rounded-lg border border-border bg-secondary/60 p-3">
          <div className="mb-2 flex items-center justify-between text-sm">
            <span className="font-medium">Attachment Preview</span>
            <button
              onClick={() => {
                setPreview(null);
                setPreviewError(null);
                setPreviewLoading(false);
              }}
              className="text-muted-foreground hover:text-foreground"
            >
              <X size={14} />
            </button>
          </div>
          {previewLoading && (
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Loader2 size={14} className="animate-spin" />
              Loading preview...
            </div>
          )}
          {previewError && <div className="text-sm text-amber-300">{previewError}</div>}
          {!previewLoading && preview?.kind === 'image' && preview.data_url && (
            <img
              src={preview.data_url}
              alt={preview.filename}
              className="max-h-60 rounded border border-border object-contain"
            />
          )}
          {!previewLoading && preview && preview.kind !== 'image' && (
            <div className="text-sm text-muted-foreground">{preview.message || 'Preview unavailable.'}</div>
          )}
        </div>
      )}
    </>
  );
}
