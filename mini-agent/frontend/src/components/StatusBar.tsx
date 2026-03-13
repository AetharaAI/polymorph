'use client';

import { useMemo, useState } from 'react';
import { Cpu, Hash, Zap } from 'lucide-react';
import { UsageStats, ToolHealthSummary, ProviderHealth, DiagnosticsResponse } from '@/lib/types';

interface StatusBarProps {
  usage: UsageStats | null;
  toolHealth: ToolHealthSummary | null;
  providerHealth: ProviderHealth | null;
  diagnostics: DiagnosticsResponse | null;
}

function formatBytes(bytes: number): string {
  if (!Number.isFinite(bytes) || bytes <= 0) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let value = bytes;
  let idx = 0;
  while (value >= 1024 && idx < units.length - 1) {
    value /= 1024;
    idx += 1;
  }
  return `${value.toFixed(idx === 0 ? 0 : 1)} ${units[idx]}`;
}

function formatUptime(seconds: number): string {
  const s = Math.max(0, Math.floor(seconds));
  const d = Math.floor(s / 86400);
  const h = Math.floor((s % 86400) / 3600);
  const m = Math.floor((s % 3600) / 60);
  if (d > 0) return `${d}d ${h}h`;
  if (h > 0) return `${h}h ${m}m`;
  return `${m}m`;
}

export function StatusBar({ usage, toolHealth, providerHealth, diagnostics }: StatusBarProps) {
  const [showPanel, setShowPanel] = useState(false);
  const contextRatio = usage
    ? Math.min(1, usage.context_input_tokens / Math.max(usage.context_window, 1))
    : 0;
  const contextPercent = Math.round(contextRatio * 100);
  const memoryPercent = diagnostics?.system.memory_percent ?? 0;
  const asrStatus = diagnostics?.services?.asr?.status || 'unknown';
  const asrClass = asrStatus === 'healthy'
    ? 'text-emerald-400'
    : asrStatus === 'disabled'
      ? 'text-muted-foreground'
      : 'text-amber-400';
  const loadAvg = useMemo(() => diagnostics?.system.load_average || null, [diagnostics]);

  return (
    <div className="border-t border-border bg-secondary">
      {showPanel && diagnostics && (
        <div className="px-4 py-3 border-b border-border text-xs text-muted-foreground grid grid-cols-2 lg:grid-cols-4 gap-3">
          <div className="rounded border border-border bg-background/30 p-2">
            <div className="font-medium text-foreground mb-1">Runtime</div>
            <div>Uptime: {formatUptime(diagnostics.uptime_seconds)}</div>
            <div>PID: {diagnostics.process.pid}</div>
            <div>Threads: {diagnostics.process.threads}</div>
          </div>
          <div className="rounded border border-border bg-background/30 p-2">
            <div className="font-medium text-foreground mb-1">Memory</div>
            <div>Proc RSS: {formatBytes(diagnostics.process.rss_bytes)}</div>
            <div>Host Used: {formatBytes(diagnostics.system.memory_used_bytes)} / {formatBytes(diagnostics.system.memory_total_bytes)}</div>
            <div>Host Memory: {diagnostics.system.memory_percent.toFixed(1)}%</div>
          </div>
          <div className="rounded border border-border bg-background/30 p-2">
            <div className="font-medium text-foreground mb-1">Disk + Load</div>
            <div>Disk Used: {formatBytes(diagnostics.system.disk_used_bytes)} / {formatBytes(diagnostics.system.disk_total_bytes)}</div>
            <div>Host: {diagnostics.system.hostname}</div>
            <div>Load: {loadAvg ? loadAvg.map(v => v.toFixed(2)).join(' / ') : 'n/a'}</div>
          </div>
          <div className="rounded border border-border bg-background/30 p-2">
            <div className="font-medium text-foreground mb-1">Voice Service</div>
            <div className={asrClass}>ASR: {asrStatus}</div>
            <div className="truncate" title={diagnostics.services?.asr?.base_url || ''}>
              {diagnostics.services?.asr?.base_url || 'ASR_BASE_URL not set'}
            </div>
            <div>Model: {diagnostics.services?.asr?.model || 'n/a'}</div>
          </div>
        </div>
      )}

      <div className="h-10 flex items-center justify-between px-4 text-xs text-muted-foreground gap-4">
        <div className="flex items-center gap-4">
          <button
            onClick={() => setShowPanel(prev => !prev)}
            className="flex items-center gap-1 hover:text-foreground transition-colors"
            title="Toggle system health panel"
          >
            <Cpu size={12} />
            {usage?.model || providerHealth?.model || 'PolyMorph'}
          </button>
          {(usage?.provider || providerHealth?.provider) && (
            <span className="text-muted-foreground/90">
              Provider: {usage?.provider || providerHealth?.provider}
            </span>
          )}
          {toolHealth && (
            <>
              <span className={`${toolHealth.status === 'healthy' ? 'text-emerald-400' : 'text-amber-400'}`}>
                Core checks {toolHealth.healthy_count}/{toolHealth.total}
              </span>
              {typeof toolHealth.registered_tool_count === 'number' && (
                <span className="text-muted-foreground/90">
                  Registry {toolHealth.registered_tool_count} tools
                </span>
              )}
            </>
          )}
          {diagnostics && (
            <span>
              Mem {memoryPercent.toFixed(0)}%
            </span>
          )}
          <span className={asrClass}>ASR {asrStatus}</span>
        </div>

        {usage && (
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1">
              <Zap size={12} />
              In: {usage.input_tokens}
            </span>
            <span>Out: {usage.output_tokens}</span>
            <span className="flex items-center gap-1">
              <Hash size={12} />
              {usage.iterations}/{usage.max_iterations || usage.iterations} iters
            </span>
            <span>
              Tool calls: {usage.tool_calls || 0}
            </span>
            <div className="flex items-center gap-2 min-w-[220px]">
              <span className="text-muted-foreground whitespace-nowrap">
                Ctx {usage.context_input_tokens}/{usage.context_window} ({contextPercent}%)
              </span>
              <div className="h-2 flex-1 bg-background/60 rounded overflow-hidden">
                <div
                  className={`h-full ${contextPercent >= 90 ? 'bg-red-500' : contextPercent >= 75 ? 'bg-amber-400' : 'bg-emerald-400'}`}
                  style={{ width: `${contextPercent}%` }}
                />
              </div>
            </div>
            {usage.replay_path && (
              <span className="truncate max-w-[260px]" title={usage.replay_path}>
                Replay: {usage.replay_path.split('/').slice(-2).join('/')}
              </span>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
