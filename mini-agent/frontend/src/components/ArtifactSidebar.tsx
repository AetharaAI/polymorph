'use client';

import { useMemo, useState } from 'react';
import { FileText, Download, Eye, X, Loader2, Image as ImageIcon, Upload, PanelRightClose, PanelRightOpen } from 'lucide-react';
import { Artifact, FileAttachment } from '@/lib/types';
import { getFilePreview, FilePreviewResponse } from '@/lib/api';

function resolveBackendUrl(): string {
  if (process.env.NEXT_PUBLIC_BACKEND_URL) {
    return process.env.NEXT_PUBLIC_BACKEND_URL;
  }

  if (typeof window !== 'undefined') {
    const { protocol, hostname, port } = window.location;
    if (port === '33333') {
      return `${protocol}//${hostname}:38333`;
    }
    if (port === '3000') {
      return `${protocol}//${hostname}:8000`;
    }
    return `${protocol}//${hostname}:38333`;
  }

  return 'http://localhost:38333';
}

const BACKEND_URL = resolveBackendUrl();

interface ArtifactSidebarProps {
  sessionId: string;
  artifacts: Artifact[];
  uploads: FileAttachment[];
  isOpen: boolean;
  onToggle: () => void;
}

interface PreviewSelection {
  fileId: string;
  filename: string;
}

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function formatDate(timestamp: number): string {
  return new Date(timestamp).toLocaleString();
}

export function ArtifactSidebar({ sessionId, artifacts, uploads, isOpen, onToggle }: ArtifactSidebarProps) {
  const [selected, setSelected] = useState<PreviewSelection | null>(null);
  const [preview, setPreview] = useState<FilePreviewResponse | null>(null);
  const [previewLoading, setPreviewLoading] = useState(false);
  const [previewError, setPreviewError] = useState<string | null>(null);
  const [expanded, setExpanded] = useState(false);

  const sortedArtifacts = useMemo(
    () => [...artifacts].sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0)),
    [artifacts]
  );

  const sortedUploads = useMemo(
    () => [...uploads].sort((a, b) => a.filename.localeCompare(b.filename)),
    [uploads]
  );

  const hasInlinePreview = Boolean(selected);
  const sidebarWidth = hasInlinePreview ? (expanded ? 'w-[72rem] max-w-[88vw]' : 'w-[52rem] max-w-[84vw]') : 'w-80';

  const openPreview = async (fileId: string, filename: string) => {
    setSelected({ fileId, filename });
    setPreview(null);
    setPreviewError(null);
    setPreviewLoading(true);
    try {
      const data = await getFilePreview(fileId);
      setPreview(data);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load preview';
      setPreviewError(message);
    } finally {
      setPreviewLoading(false);
    }
  };

  const closePreview = () => {
    setSelected(null);
    setPreview(null);
    setPreviewError(null);
    setPreviewLoading(false);
    setExpanded(false);
  };

  if (!isOpen) {
    return null;
  }

  return (
    <div className={`${sidebarWidth} bg-card border-l border-border flex flex-col h-full transition-[width] duration-200`}>
      <div className="p-4 border-b border-border flex items-center justify-between">
        <h3 className="font-semibold">Artifacts</h3>
        <div className="flex items-center gap-2">
          {sessionId && (sortedArtifacts.length > 0 || sortedUploads.length > 0) && (
            <a
              href={`${BACKEND_URL}/api/files/download-session/${sessionId}`}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 text-xs text-primary hover:underline"
              title="Download all files from this session as zip"
            >
              <Download size={14} />
              Download all
            </a>
          )}
          {hasInlinePreview && (
            <button
              onClick={() => setExpanded(prev => !prev)}
              className="text-muted-foreground hover:text-foreground"
              title={expanded ? 'Narrow inspector' : 'Widen inspector'}
            >
              {expanded ? <PanelRightClose size={16} /> : <PanelRightOpen size={16} />}
            </button>
          )}
          <button onClick={onToggle} className="text-muted-foreground hover:text-foreground" title="Close right panel">
            <X size={18} />
          </button>
        </div>
      </div>

      <div className="flex-1 min-h-0 flex">
        <div className={`${hasInlinePreview ? 'w-[21rem] border-r border-border' : 'w-full'} overflow-y-auto p-2`}>
          <div className="mb-3">
            <h4 className="text-xs uppercase tracking-wide text-muted-foreground px-1 mb-2">Agent Artifacts</h4>
            {sortedArtifacts.length === 0 ? (
              <div className="text-center text-muted-foreground p-3 text-sm bg-secondary/40 rounded-lg">
                No artifacts yet
              </div>
            ) : (
              <div className="space-y-2">
                {sortedArtifacts.map((artifact, i) => {
                  const selectedClass = artifact.file_id === selected?.fileId ? 'ring-1 ring-primary/60 bg-secondary/90' : '';
                  return (
                    <div
                      key={artifact.file_id || i}
                      className={`p-3 bg-secondary rounded-lg hover:bg-secondary/80 transition-colors ${selectedClass}`}
                    >
                      <div className="flex items-start gap-2">
                        <FileText size={16} className="text-primary mt-0.5" />
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium truncate">{artifact.filename}</p>
                          <p className="text-xs text-muted-foreground">{formatSize(artifact.size)}</p>
                          <p className="text-xs text-muted-foreground">{formatDate(artifact.timestamp)}</p>
                          {artifact.source && (
                            <p className="text-xs text-muted-foreground">Source: {artifact.source}</p>
                          )}
                          {artifact.validation && (
                            <p className={`text-xs mt-1 ${artifact.validation.status === 'invalid' ? 'text-red-400' : artifact.validation.status === 'warn' ? 'text-amber-300' : 'text-emerald-400'}`}>
                              {artifact.validation.kind}: {artifact.validation.status}
                            </p>
                          )}
                        </div>
                      </div>
                      <div className="mt-2 flex items-center gap-3 text-xs">
                        {artifact.file_id && (
                          <>
                            <button
                              onClick={() => openPreview(artifact.file_id, artifact.filename)}
                              className="inline-flex items-center gap-1 text-primary hover:underline"
                            >
                              <Eye size={12} />
                              Read
                            </button>
                            <a
                              href={`${BACKEND_URL}/api/files/download/${artifact.file_id}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center gap-1 text-primary hover:underline"
                            >
                              <Download size={12} />
                              Download
                            </a>
                          </>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          <div>
            <h4 className="text-xs uppercase tracking-wide text-muted-foreground px-1 mb-2">Uploaded Files</h4>
            {sortedUploads.length === 0 ? (
              <div className="text-center text-muted-foreground p-3 text-sm bg-secondary/40 rounded-lg">
                No uploads yet
              </div>
            ) : (
              <div className="space-y-2">
                {sortedUploads.map((upload, i) => {
                  const selectedClass = upload.file_id === selected?.fileId ? 'ring-1 ring-primary/60 bg-secondary/90' : '';
                  return (
                    <div key={upload.file_id || i} className={`p-3 bg-secondary rounded-lg hover:bg-secondary/80 transition-colors ${selectedClass}`}>
                      <div className="flex items-start gap-2">
                        <Upload size={16} className="text-sky-400 mt-0.5" />
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium truncate">{upload.filename}</p>
                          <p className="text-xs text-muted-foreground">{formatSize(upload.size)}</p>
                        </div>
                      </div>
                      <div className="mt-2 flex items-center gap-3 text-xs">
                        <button
                          onClick={() => openPreview(upload.file_id, upload.filename)}
                          className="inline-flex items-center gap-1 text-primary hover:underline"
                        >
                          <Eye size={12} />
                          Read
                        </button>
                        <a
                          href={`${BACKEND_URL}/api/files/download/${upload.file_id}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-1 text-primary hover:underline"
                        >
                          <Download size={12} />
                          Download
                        </a>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>

        {hasInlinePreview && (
          <div className="flex-1 min-w-0 flex flex-col">
            <div className="px-4 py-3 border-b border-border flex items-center justify-between">
              <div className="min-w-0">
                <p className="font-medium truncate">{selected?.filename || preview?.filename || 'Inspector'}</p>
                {preview?.size !== undefined && (
                  <p className="text-xs text-muted-foreground">{formatSize(preview.size)}</p>
                )}
              </div>
              <button
                className="text-muted-foreground hover:text-foreground"
                onClick={closePreview}
                title="Close inspector"
              >
                <X size={18} />
              </button>
            </div>
            <div className="flex-1 overflow-auto p-4">
              {previewLoading && (
                <div className="h-full flex items-center justify-center text-muted-foreground gap-2">
                  <Loader2 size={16} className="animate-spin" />
                  Loading preview...
                </div>
              )}
              {!previewLoading && previewError && (
                <div className="text-red-400 text-sm">{previewError}</div>
              )}
              {!previewLoading && !previewError && preview && preview.kind === 'text' && (
                <pre className="text-xs whitespace-pre-wrap break-words [overflow-wrap:anywhere] bg-secondary p-3 rounded-lg">
                  {preview.text || ''}
                </pre>
              )}
              {!previewLoading && !previewError && preview && preview.kind === 'image' && preview.data_url && (
                <div className="h-full flex items-center justify-center">
                  <img src={preview.data_url} alt={preview.filename} className="max-w-full max-h-full object-contain rounded" />
                </div>
              )}
              {!previewLoading && !previewError && preview && preview.kind === 'binary' && (
                <div className="text-sm text-muted-foreground flex items-center gap-2">
                  <ImageIcon size={16} />
                  {preview.message || 'No inline preview available for this file type.'}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
