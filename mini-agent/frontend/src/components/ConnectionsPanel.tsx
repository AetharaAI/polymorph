'use client';

import { useEffect, useMemo, useState } from 'react';
import { Loader2, Save, ShieldCheck, TestTube2, X } from 'lucide-react';
import {
  ConnectionService,
  getConnections,
  ConnectionsResponse,
  saveConnection,
  testConnection,
} from '@/lib/api';

interface ConnectionsPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

type DraftMap = Record<string, Record<string, string>>;
type TestMap = Record<string, { status: string; details: string; latency_ms: number }>;

function statusClass(status: string): string {
  switch (status) {
    case 'healthy':
      return 'text-emerald-400';
    case 'error':
      return 'text-red-400';
    case 'disabled':
      return 'text-muted-foreground';
    case 'configured':
    case 'degraded':
      return 'text-amber-400';
    default:
      return 'text-muted-foreground';
  }
}

export function ConnectionsPanel({ isOpen, onClose }: ConnectionsPanelProps) {
  const [services, setServices] = useState<ConnectionService[]>([]);
  const [secretsStatus, setSecretsStatus] = useState<ConnectionsResponse['secrets'] | null>(null);
  const [draft, setDraft] = useState<DraftMap>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [savingId, setSavingId] = useState<string | null>(null);
  const [testingId, setTestingId] = useState<string | null>(null);
  const [testResults, setTestResults] = useState<TestMap>({});
  const [saveMessage, setSaveMessage] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await getConnections();
      setServices(res.services || []);
      setSecretsStatus(res.secrets || null);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load connections';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      void load();
    }
  }, [isOpen]);

  const mergedDraft = useMemo(() => draft, [draft]);

  const onChange = (serviceId: string, envKey: string, value: string) => {
    setDraft(prev => ({
      ...prev,
      [serviceId]: {
        ...(prev[serviceId] || {}),
        [envKey]: value,
      },
    }));
  };

  const handleTest = async (service: ConnectionService) => {
    setTestingId(service.service_id);
    setSaveMessage(null);
    try {
      const values = mergedDraft[service.service_id] || {};
      const result = await testConnection(service.service_id, values);
      setTestResults(prev => ({ ...prev, [service.service_id]: result }));
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Connection test failed';
      setTestResults(prev => ({
        ...prev,
        [service.service_id]: { status: 'error', details: message, latency_ms: 0 },
      }));
    } finally {
      setTestingId(null);
    }
  };

  const handleSave = async (service: ConnectionService) => {
    setSavingId(service.service_id);
    setSaveMessage(null);
    try {
      const values = mergedDraft[service.service_id] || {};
      const result = await saveConnection(service.service_id, values, false);
      setSaveMessage(
        result.requires_restart
          ? `${service.name} saved. Restart required to apply runtime clients.`
          : `${service.name} saved.`,
      );
      await load();
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Connection save failed';
      setSaveMessage(message);
    } finally {
      setSavingId(null);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex">
      <button
        className="flex-1 bg-black/40"
        onClick={onClose}
        aria-label="Close connections panel"
      />
      <div className="w-full max-w-2xl h-full bg-card border-l border-border flex flex-col">
        <div className="h-12 px-4 border-b border-border flex items-center justify-between">
          <div>
            <h2 className="text-sm font-semibold">Connections & Secrets</h2>
            <p className="text-[11px] text-muted-foreground">Configure endpoints, keys, and infra backends</p>
          </div>
          <button onClick={onClose} className="p-1.5 hover:bg-secondary rounded">
            <X size={16} />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          <div className="rounded border border-border bg-secondary/30 p-3 text-xs text-muted-foreground">
            Secrets are masked and persisted in runtime config. Services marked restart-required update on next backend restart.
            <div className="mt-1">
              Encryption: {secretsStatus?.enabled ? 'enabled' : 'disabled'} ({secretsStatus?.source || 'unknown'})
            </div>
          </div>

          {loading && (
            <div className="text-sm text-muted-foreground flex items-center gap-2">
              <Loader2 size={14} className="animate-spin" />
              Loading connections...
            </div>
          )}

          {error && (
            <div className="rounded border border-red-500/40 bg-red-500/10 p-3 text-sm text-red-300">{error}</div>
          )}

          {saveMessage && (
            <div className="rounded border border-emerald-500/40 bg-emerald-500/10 p-3 text-sm text-emerald-300">
              {saveMessage}
            </div>
          )}

          {services.map(service => {
            const test = testResults[service.service_id];
            const isSaving = savingId === service.service_id;
            const isTesting = testingId === service.service_id;
            return (
              <div key={service.service_id} className="rounded-lg border border-border bg-secondary/20 p-3 space-y-3">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h3 className="text-sm font-semibold">{service.name}</h3>
                    <p className="text-xs text-muted-foreground">{service.description}</p>
                  </div>
                  <div className="text-right">
                    <div className={`text-xs font-medium ${statusClass(test?.status || service.status)}`}>
                      {test?.status || service.status}
                    </div>
                    {service.requires_restart && (
                      <div className="text-[10px] text-amber-400">restart required</div>
                    )}
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {service.fields.map(field => {
                    const currentDraft = mergedDraft[service.service_id]?.[field.env_key];
                    const inputValue = currentDraft ?? field.value ?? '';
                    const placeholder = field.secret
                      ? (field.has_value ? `configured (${field.display_value})` : 'enter secret')
                      : field.value || '';

                    return (
                      <label key={field.env_key} className="space-y-1">
                        <div className="flex items-center justify-between text-[11px] text-muted-foreground">
                          <span>{field.label}</span>
                          <span className="uppercase">{field.source}</span>
                        </div>
                        <input
                          type={field.secret ? 'password' : 'text'}
                          value={inputValue}
                          placeholder={placeholder}
                          onChange={e => onChange(service.service_id, field.env_key, e.target.value)}
                          className="w-full h-9 rounded border border-border bg-background px-2 text-xs focus:outline-none focus:ring-2 focus:ring-primary"
                        />
                        <div className="text-[10px] text-muted-foreground">{field.env_key}</div>
                      </label>
                    );
                  })}
                </div>

                {test && (
                  <div className={`rounded border p-2 text-xs ${
                    test.status === 'healthy'
                      ? 'border-emerald-500/40 bg-emerald-500/10 text-emerald-300'
                      : test.status === 'disabled'
                        ? 'border-border bg-background/40 text-muted-foreground'
                        : 'border-red-500/40 bg-red-500/10 text-red-300'
                  }`}>
                    {test.details} {test.latency_ms ? `(${test.latency_ms} ms)` : ''}
                  </div>
                )}

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => void handleTest(service)}
                    disabled={isTesting || isSaving}
                    className="h-9 px-3 rounded border border-border bg-background text-xs hover:bg-secondary disabled:opacity-50 flex items-center gap-1"
                  >
                    {isTesting ? <Loader2 size={12} className="animate-spin" /> : <TestTube2 size={12} />}
                    Test
                  </button>
                  <button
                    onClick={() => void handleSave(service)}
                    disabled={isSaving || isTesting}
                    className="h-9 px-3 rounded bg-primary text-primary-foreground text-xs hover:bg-primary/90 disabled:opacity-50 flex items-center gap-1"
                  >
                    {isSaving ? <Loader2 size={12} className="animate-spin" /> : <Save size={12} />}
                    Save
                  </button>
                  {service.requires_restart && (
                    <span className="text-[11px] text-amber-400 flex items-center gap-1">
                      <ShieldCheck size={12} />
                      restart to apply clients
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
