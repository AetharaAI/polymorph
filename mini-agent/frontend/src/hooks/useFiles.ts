import { useState, useCallback } from 'react';
import { uploadFile, listFiles, UploadResponse } from '@/lib/api';
import { FileAttachment } from '@/lib/types';

export function useFiles(sessionId: string) {
  const [files, setFiles] = useState<FileAttachment[]>([]);
  const [isUploading, setIsUploading] = useState(false);

  const upload = useCallback(async (file: File) => {
    setIsUploading(true);
    try {
      const response = await uploadFile(sessionId, file);
      const attachment: FileAttachment = {
        file_id: response.file_id,
        filename: response.filename,
        size: response.size
      };
      setFiles(prev => [...prev, attachment]);
      return attachment;
    } finally {
      setIsUploading(false);
    }
  }, [sessionId]);

  const remove = useCallback((fileId: string) => {
    setFiles(prev => prev.filter(f => f.file_id !== fileId));
  }, []);

  const loadFiles = useCallback(async () => {
    try {
      const fileList = await listFiles(sessionId);
      setFiles(fileList.map(f => ({
        file_id: f.file_id,
        filename: f.filename,
        size: f.size
      })));
    } catch (e) {
      console.error('Failed to load files:', e);
    }
  }, [sessionId]);

  const clear = useCallback(() => {
    setFiles([]);
  }, []);

  return {
    files,
    isUploading,
    upload,
    remove,
    loadFiles,
    clear
  };
}
