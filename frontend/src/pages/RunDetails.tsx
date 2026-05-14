import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../api/client';
import type { Alert, LogEvent, SimulationRun, ValidationResult } from '../types/api';
import { SeverityBadge } from '../components/SeverityBadge';

export function RunDetails() {
  const { runId } = useParams<{ runId: string }>();
  const [run, setRun] = useState<SimulationRun | null>(null);
  const [logs, setLogs] = useState<LogEvent[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [validation, setValidation] = useState<ValidationResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!runId) return;
    Promise.all([
      api.getRun(runId),
      api.getRunLogs(runId),
      api.getRunAlerts(runId),
    ]).then(([r, l, a]) => {
      setRun(r); setLogs(l); setAlerts(a);
    }).finally(() => setLoading(false));
  }, [runId]);

  const handleValidate = async () => {
    if (!runId) return;
    const v = await api.validateRun(runId);
    setValidation(v);
  };

  if (loading) return <div style={{ color: '#6b7280' }}>Loading run details...</div>;
  if (!run) return <div style={{ color: '#991b1b' }}>Run not found</div>;

  return (
    <div>
      <div style={{ marginBottom: '1rem' }}>
        <Link to="/runs" style={{ color: '#1d4ed8', fontSize: '0.88rem' }}>← Back to Runs</Link>
      </div>
      <h1 style={{ fontSize: '1.3rem', fontWeight: 700, color: '#1e2a3a', marginBottom: '1.5rem' }}>
        Run Details: <code style={{ fontSize: '1rem', background: '#f1f5f9', padding: '0.1em 0.4em', borderRadius: 4 }}>{run.id}</code>
      </h1>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.5rem' }}>
        <div style={{ background: '#fff', borderRadius: 8, padding: '1.2rem', boxShadow: '0 1px 4px rgba(0,0,0,0.08)' }}>
          <h2 style={{ fontSize: '0.95rem', fontWeight: 600, color: '#1e2a3a', marginBottom: '0.8rem' }}>Run Info</h2>
          <table style={{ fontSize: '0.85rem', width: '100%' }}>
            <tbody>
              {[['Scenario', run.scenario_id], ['Status', run.status], ['Mode', run.mode],
                ['Started', new Date(run.started_at).toLocaleString()],
                ['Finished', run.finished_at ? new Date(run.finished_at).toLocaleString() : 'N/A']
              ].map(([k, v]) => (
                <tr key={k}><td style={{ color: '#6b7280', padding: '0.3rem 0', width: 80 }}>{k}</td><td style={{ color: '#374151', padding: '0.3rem 0' }}>{v}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
        <div style={{ background: '#fff', borderRadius: 8, padding: '1.2rem', boxShadow: '0 1px 4px rgba(0,0,0,0.08)' }}>
          <h2 style={{ fontSize: '0.95rem', fontWeight: 600, color: '#1e2a3a', marginBottom: '0.8rem' }}>Validation</h2>
          {validation
            ? (
              <div style={{ fontSize: '0.85rem' }}>
                <div>Detected: <SeverityBadge value={validation.detected ? 'covered' : 'not_detected'} /></div>
                <div style={{ marginTop: '0.4rem' }}>Alerts: {validation.alerts_count}</div>
                <div style={{ marginTop: '0.4rem' }}>Status: <SeverityBadge value={validation.coverage_status} /></div>
              </div>
            )
            : <button onClick={handleValidate} style={{ background: '#1e2a3a', color: '#fff', border: 'none', borderRadius: 5, padding: '0.4rem 1rem', cursor: 'pointer', fontSize: '0.85rem' }}>
                Validate Run
              </button>
          }
        </div>
      </div>

      {alerts.length > 0 && (
        <div style={{ background: '#fff', borderRadius: 8, padding: '1.2rem', boxShadow: '0 1px 4px rgba(0,0,0,0.08)', marginBottom: '1.5rem' }}>
          <h2 style={{ fontSize: '0.95rem', fontWeight: 600, color: '#1e2a3a', marginBottom: '1rem' }}>Alerts ({alerts.length})</h2>
          {alerts.map(a => (
            <div key={a.id} style={{ background: '#fff7ed', borderLeft: '4px solid #f97316', padding: '0.8rem', borderRadius: '0 6px 6px 0', marginBottom: '0.6rem' }}>
              <div style={{ fontWeight: 500, color: '#c2410c' }}>{a.title}</div>
              <div style={{ fontSize: '0.8rem', color: '#6b7280', marginTop: '0.2rem' }}>
                Rule: <code>{a.rule_id}</code> &nbsp;|&nbsp; <SeverityBadge value={a.severity} /> &nbsp;|&nbsp; {a.mitre_technique_id}
              </div>
              <div style={{ fontSize: '0.82rem', color: '#374151', marginTop: '0.3rem' }}>{a.reason}</div>
            </div>
          ))}
        </div>
      )}

      <div style={{ background: '#fff', borderRadius: 8, padding: '1.2rem', boxShadow: '0 1px 4px rgba(0,0,0,0.08)', marginBottom: '1.5rem' }}>
        <h2 style={{ fontSize: '0.95rem', fontWeight: 600, color: '#1e2a3a', marginBottom: '1rem' }}>Event Timeline ({logs.length})</h2>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #e5e7eb' }}>
                {['#', 'Timestamp', 'Source', 'Event Type', 'Host', 'User', 'Process'].map(h => (
                  <th key={h} style={{ textAlign: 'left', padding: '0.4rem 0.6rem', color: '#374151' }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {logs.map((log, i) => (
                <tr key={log.id} style={{ borderBottom: '1px solid #f9fafb' }}>
                  <td style={{ padding: '0.4rem 0.6rem', color: '#9ca3af' }}>{i + 1}</td>
                  <td style={{ padding: '0.4rem 0.6rem', color: '#374151', whiteSpace: 'nowrap' }}>{new Date(log.timestamp).toLocaleTimeString()}</td>
                  <td style={{ padding: '0.4rem 0.6rem', color: '#4b5563' }}>{log.source}</td>
                  <td style={{ padding: '0.4rem 0.6rem', color: '#4b5563' }}>{log.event_type}</td>
                  <td style={{ padding: '0.4rem 0.6rem', color: '#4b5563' }}>{log.host}</td>
                  <td style={{ padding: '0.4rem 0.6rem', color: '#4b5563' }}>{log.user}</td>
                  <td style={{ padding: '0.4rem 0.6rem', color: '#4b5563' }}>{log.process_name ?? '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div style={{ background: '#fff', borderRadius: 8, padding: '1.2rem', boxShadow: '0 1px 4px rgba(0,0,0,0.08)' }}>
        <h2 style={{ fontSize: '0.95rem', fontWeight: 600, color: '#1e2a3a', marginBottom: '1rem' }}>Export Report</h2>
        <div style={{ display: 'flex', gap: '0.8rem' }}>
          {['html', 'md', 'json'].map(fmt => (
            <a key={fmt} href={api.getReportUrl(run.id, fmt)} target="_blank" rel="noreferrer"
              style={{ background: '#1e2a3a', color: '#fff', padding: '0.4rem 1rem', borderRadius: 5, textDecoration: 'none', fontSize: '0.85rem' }}>
              Export {fmt.toUpperCase()}
            </a>
          ))}
        </div>
      </div>
    </div>
  );
}
