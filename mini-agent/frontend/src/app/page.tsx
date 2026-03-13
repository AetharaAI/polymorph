'use client';

import { useState, useEffect, useRef } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { Menu, FileText } from 'lucide-react';
import { ChatWindow } from '@/components/ChatWindow';
import { InputBar } from '@/components/InputBar';
import { Sidebar } from '@/components/Sidebar';
import { StatusBar } from '@/components/StatusBar';
import { ArtifactSidebar } from '@/components/ArtifactSidebar';
import { ConnectionsPanel } from '@/components/ConnectionsPanel';
import { useChat } from '@/hooks/useChat';
import { useVoiceChat } from '@/hooks/useVoiceChat';
import { useFiles } from '@/hooks/useFiles';
import { VoicePanel } from '@/components/VoicePanel';
import { Session, ToolHealthSummary, ProviderHealth, DiagnosticsResponse } from '@/lib/types';
import { getDiagnostics, getHealth, listSessions } from '@/lib/api';

const STORAGE_KEY = 'aetherops_sessions_v1';
const CURRENT_SESSION_KEY = 'aetherops_current_session_v1';

export default function Home() {
  const [sessionId, setSessionId] = useState<string>('');
  const [sessions, setSessions] = useState<Session[]>([]);
  const [isLeftSidebarOpen, setIsLeftSidebarOpen] = useState(true);
  const [isRightSidebarOpen, setIsRightSidebarOpen] = useState(true);
  const [isConnectionsOpen, setIsConnectionsOpen] = useState(false);
  const [toolHealth, setToolHealth] = useState<ToolHealthSummary | null>(null);
  const [providerHealth, setProviderHealth] = useState<ProviderHealth | null>(null);
  const [diagnostics, setDiagnostics] = useState<DiagnosticsResponse | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const { messages, isLoading, toolCalls, usage, artifacts, send } = useChat(sessionId);
  const {
    messages: voiceMessages,
    isLoading: isVoiceLoading,
    error: voiceError,
    config: voiceConfig,
    selectedVoiceId,
    setSelectedVoiceId,
    sendTurn: sendVoiceTurn,
  } = useVoiceChat(sessionId);
  const { files, upload, remove: removeFile, loadFiles } = useFiles(sessionId);

  // Initialize session
  useEffect(() => {
    let cancelled = false;

    const init = async () => {
      const storedRaw = localStorage.getItem(STORAGE_KEY);
      const storedSessions = storedRaw ? (JSON.parse(storedRaw) as Session[]) : [];
      const storedCurrent = localStorage.getItem(CURRENT_SESSION_KEY) || '';

      try {
        const backendSessions = await listSessions(100);
        if (cancelled) return;
        const merged = [...backendSessions, ...storedSessions].reduce<Session[]>((acc, next) => {
          if (acc.some(s => s.id === next.id)) return acc;
          acc.push({
            id: next.id,
            title: next.title || 'New conversation',
            updated_at: next.updated_at,
            message_count: next.message_count,
          });
          return acc;
        }, []);

        const sorted = merged.sort((a, b) => (b.updated_at || 0) - (a.updated_at || 0));
        setSessions(sorted);

        const initial =
          (storedCurrent && sorted.find(s => s.id === storedCurrent)?.id) ||
          sorted[0]?.id ||
          '';

        if (initial) {
          setSessionId(initial);
          localStorage.setItem(CURRENT_SESSION_KEY, initial);
        } else {
          createNewSession();
        }
      } catch {
        if (cancelled) return;
        setSessions(storedSessions);
        if (storedCurrent && storedSessions.some(s => s.id === storedCurrent)) {
          setSessionId(storedCurrent);
        } else if (storedSessions.length > 0) {
          setSessionId(storedSessions[0].id);
        } else {
          createNewSession();
        }
      }
    };

    void init();
    return () => {
      cancelled = true;
    };
  }, []);

  // Save sessions to localStorage
  useEffect(() => {
    if (sessions.length > 0) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(sessions));
    }
  }, [sessions]);

  useEffect(() => {
    if (!sessionId) return;
    localStorage.setItem(CURRENT_SESSION_KEY, sessionId);
    void loadFiles();
  }, [sessionId, loadFiles]);

  useEffect(() => {
    let mounted = true;

    const loadHealthAndDiagnostics = async () => {
      try {
        const [health, diag] = await Promise.all([getHealth(), getDiagnostics()]);
        if (mounted) {
          setToolHealth(health.tools ?? null);
          setProviderHealth((health.provider as ProviderHealth) ?? null);
          setDiagnostics(diag as DiagnosticsResponse);
        }
      } catch {
        if (mounted) {
          setToolHealth(null);
          setProviderHealth(null);
          setDiagnostics(null);
        }
      }
    };

    void loadHealthAndDiagnostics();
    const timer = window.setInterval(loadHealthAndDiagnostics, 15000);
    return () => {
      mounted = false;
      window.clearInterval(timer);
    };
  }, []);

  const createNewSession = () => {
    const newId = uuidv4();
    setSessionId(newId);
    setSessions(prev => [{ id: newId, title: 'New conversation', updated_at: Date.now(), message_count: 0 }, ...prev]);
    localStorage.setItem(CURRENT_SESSION_KEY, newId);
  };

  const handleSelectSession = (id: string) => {
    setSessionId(id);
    localStorage.setItem(CURRENT_SESSION_KEY, id);
  };

  const handleClearSessions = () => {
    localStorage.removeItem(STORAGE_KEY);
    localStorage.removeItem(CURRENT_SESSION_KEY);
    setSessions([]);
    createNewSession();
  };

  const handleSend = async (text: string, fileIds: string[]) => {
    const currentTitle = sessions.find(s => s.id === sessionId)?.title || '';
    const shouldRetitle = messages.length === 0 || !currentTitle || currentTitle === 'New conversation';
    if (shouldRetitle) {
      const title = text.slice(0, 40) + (text.length > 40 ? '...' : '');
      setSessions(prev => prev.map(s =>
        s.id === sessionId ? { ...s, title, updated_at: Date.now() } : s
      ));
    } else {
      setSessions(prev => prev.map(s =>
        s.id === sessionId ? { ...s, updated_at: Date.now() } : s
      ));
    }

    await send(text, fileIds);
  };

  const handleVoiceTurn = async (transcript: string) => {
    await sendVoiceTurn(transcript);
  };

  const handleAddFile = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files) {
      for (const file of Array.from(files)) {
        await upload(file);
      }
    }
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  if (!sessionId) {
    return (
      <div className="h-screen flex items-center justify-center bg-background">
        <div className="animate-pulse">Loading...</div>
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-background">
      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        multiple
        onChange={handleFileChange}
        className="hidden"
      />

      {/* Main layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Sidebar */}
        {isLeftSidebarOpen && (
          <Sidebar
            sessions={sessions}
            currentSessionId={sessionId}
            onSelectSession={handleSelectSession}
            onNewSession={createNewSession}
            onClearSessions={handleClearSessions}
            onOpenConnections={() => setIsConnectionsOpen(true)}
          />
        )}

        {/* Chat area */}
        <div className="flex-1 flex flex-col">
          {/* Top toolbar with sidebar toggles */}
          <div className="h-10 border-b border-border flex items-center px-2 gap-2">
            <button
              onClick={() => setIsLeftSidebarOpen(!isLeftSidebarOpen)}
              className="p-1.5 hover:bg-secondary rounded transition-colors"
              title={isLeftSidebarOpen ? "Hide conversations" : "Show conversations"}
            >
              <Menu size={18} />
            </button>
            <div className="flex-1 flex items-center justify-center">
              <div className="pointer-events-none inline-flex items-center gap-2 rounded-full border border-border/80 bg-card/60 px-3 py-1 shadow-[0_8px_30px_rgba(2,6,23,0.22)]">
                <img
                  src="/branding/polymorph-badge-mark.png"
                  alt="PolyMorph toolbar badge"
                  className="h-5 w-5 rounded-md object-cover ring-1 ring-cyan-400/25"
                />
                <span className="text-xs font-medium tracking-[0.08em] text-foreground/90">POLYMORPH</span>
              </div>
            </div>
            <button
              onClick={() => setIsRightSidebarOpen(!isRightSidebarOpen)}
              className={`p-1.5 hover:bg-secondary rounded transition-colors ${artifacts.length > 0 ? 'text-primary' : ''}`}
              title={isRightSidebarOpen ? "Hide artifacts" : "Show artifacts"}
            >
              <FileText size={18} />
            </button>
          </div>

          <ChatWindow
            messages={messages}
            toolCalls={toolCalls}
            isLoading={isLoading}
          />

          <VoicePanel
            messages={voiceMessages}
            isLoading={isVoiceLoading}
            error={voiceError}
            config={voiceConfig}
            selectedVoiceId={selectedVoiceId}
            onVoiceIdChange={setSelectedVoiceId}
          />

          <InputBar
            onSend={handleSend}
            onVoiceTurn={handleVoiceTurn}
            isLoading={isLoading}
            isVoiceLoading={isVoiceLoading}
            files={files}
            onAddFile={handleAddFile}
            onRemoveFile={removeFile}
          />
        </div>

        {/* Right Sidebar - Artifacts */}
        <ArtifactSidebar
          sessionId={sessionId}
          artifacts={artifacts}
          uploads={files}
          isOpen={isRightSidebarOpen}
          onToggle={() => setIsRightSidebarOpen(!isRightSidebarOpen)}
        />
      </div>

      {/* Status bar */}
      <StatusBar
        usage={usage}
        toolHealth={toolHealth}
        providerHealth={providerHealth}
        diagnostics={diagnostics}
      />

      <ConnectionsPanel
        isOpen={isConnectionsOpen}
        onClose={() => setIsConnectionsOpen(false)}
      />
    </div>
  );
}
