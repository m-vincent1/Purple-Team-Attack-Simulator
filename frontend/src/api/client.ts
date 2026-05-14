import type { Alert, Coverage, LogEvent, Scenario, SimulationRun, ValidationResult } from '../types/api';

const BASE_URL = (import.meta.env.VITE_API_URL as string | undefined) ?? '';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  getScenarios: () => request<Scenario[]>('/api/scenarios'),
  getScenario: (id: string) => request<Scenario>(`/api/scenarios/${id}`),
  runScenario: (id: string) => request<{ run_id: string; events_generated: number; alerts_count: number; coverage_status: string }>(`/api/scenarios/${id}/run`, { method: 'POST' }),
  runAll: () => request<{ results: unknown[]; total: number }>('/api/runs/run-all', { method: 'POST' }),

  getRuns: () => request<SimulationRun[]>('/api/runs'),
  getRun: (id: string) => request<SimulationRun>(`/api/runs/${id}`),
  getRunLogs: (id: string) => request<LogEvent[]>(`/api/runs/${id}/logs`),
  getRunAlerts: (id: string) => request<Alert[]>(`/api/runs/${id}/alerts`),
  validateRun: (id: string) => request<ValidationResult>(`/api/runs/${id}/validate`, { method: 'POST' }),

  getCoverage: () => request<Coverage>('/api/coverage'),

  getReportUrl: (runId: string, format: string) => `${BASE_URL}/api/reports/${runId}?format=${format}`,
};
