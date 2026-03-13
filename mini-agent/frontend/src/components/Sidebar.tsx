'use client';

import { Plus, Trash2, MessageSquare, PlugZap } from 'lucide-react';
import { Session } from '@/lib/types';

interface SidebarProps {
  sessions: Session[];
  currentSessionId: string;
  onSelectSession: (sessionId: string) => void;
  onNewSession: () => void;
  onClearSessions: () => void;
  onOpenConnections: () => void;
}

export function Sidebar({
  sessions,
  currentSessionId,
  onSelectSession,
  onNewSession,
  onClearSessions,
  onOpenConnections
}: SidebarProps) {
  return (
    <div className="w-64 bg-card border-r border-border flex flex-col h-full">
      <div className="p-4 border-b border-border space-y-3">
        <div className="rounded-2xl border border-border bg-secondary/40 p-3 shadow-[0_16px_40px_rgba(5,10,24,0.32)]">
          <div className="flex items-center gap-2">
            <img
              src="/branding/polymorph-badge-mark.png"
              alt="PolyMorph badge"
              className="h-9 w-9 rounded-xl object-cover ring-1 ring-cyan-400/25"
            />
            <div className="min-w-0">
              <p className="text-xs font-semibold leading-tight truncate">PolyMorph</p>
              <p className="text-[10px] text-muted-foreground truncate">Agentic Harness</p>
            </div>
          </div>
          <div className="mt-3 rounded-xl border border-border/70 bg-background/40 px-3 py-2">
            <p className="text-[11px] font-medium text-foreground/90">Model-agnostic operator surface</p>
            <p className="mt-1 text-[10px] text-muted-foreground">Voice, tools, files, and persistent execution in one place.</p>
            <img
              src="/branding/ember-wave-mark.png"
              alt="PolyMorph waveform accent"
              className="mt-3 h-9 w-full object-contain opacity-90"
            />
          </div>
        </div>
        <button
          onClick={onNewSession}
          className="w-full flex items-center justify-center gap-2 bg-primary text-primary-foreground rounded-lg px-4 py-2 hover:bg-primary/90 transition-colors"
        >
          <Plus size={18} />
          New Chat
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-2">
        {sessions.length === 0 ? (
          <div className="text-center text-muted-foreground p-4 text-sm">
            No conversations yet
          </div>
        ) : (
          sessions.map(session => (
            <button
              key={session.id}
              onClick={() => onSelectSession(session.id)}
              className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-left text-sm transition-colors ${
                session.id === currentSessionId
                  ? 'bg-primary/20 text-primary'
                  : 'hover:bg-secondary text-foreground'
              }`}
            >
              <MessageSquare size={16} />
              <span className="truncate flex-1">
                {session.title || 'New conversation'}
              </span>
            </button>
          ))
        )}
      </div>

      <div className="p-4 border-t border-border">
        <button
          onClick={onOpenConnections}
          className="w-full mb-3 flex items-center justify-center gap-2 text-foreground hover:text-primary text-sm transition-colors"
        >
          <PlugZap size={16} />
          Connections
        </button>
        <button
          onClick={onClearSessions}
          className="w-full flex items-center justify-center gap-2 text-muted-foreground hover:text-destructive text-sm transition-colors"
        >
          <Trash2 size={16} />
          Clear all
        </button>
      </div>
    </div>
  );
}
