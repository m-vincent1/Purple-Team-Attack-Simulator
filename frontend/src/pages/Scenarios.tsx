import React, { useEffect, useState } from 'react';
import { api } from '../api/client';
import type { Scenario } from '../types/api';
import { SeverityBadge } from '../components/SeverityBadge';

export function Scenarios() {
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState<string | null>(null);
  const [message, setMessage] = useState('');

  useEffect(() => {
    api.getScenarios()
      .then(setScenarios)
      .finally(() => setLoading(false));
  }, []);

  const handleRun = async (id: string) => {
    setRunning(id);
    setMessage('');
    try {
      const result = await api.runScenario(id);
      setMessage(`✓ Run ${result.run_id} — ${result.alerts_count} alert(s) — ${result.coverage_status}`);
    } catch (e: unknown) {
      setMessage(`Error: ${(e as Error).message}`);
    } finally {
      setRunning(null);
    }
  };

  if (loading) return <div style={{ color: '#6b7280' }}>Loading scenarios...</div>;

  return (
    <div>
      <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: '#1e2a3a', marginBottom: '0.5rem' }}>Scenarios</h1>
      <p style={{ color: '#6b7280', marginBottom: '1.5rem', fontSize: '0.88rem' }}>
        {scenarios.length} synthetic attack scenarios available
      </p>
      {message && (
        <div style={{ background: '#f0fdf4', border: '1px solid #86efac', borderRadius: 6, padding: '0.7rem 1rem', marginBottom: '1rem', fontSize: '0.88rem', color: '#166534' }}>
          {message}
        </div>
      )}
      <div style={{ background: '#fff', borderRadius: 8, boxShadow: '0 1px 4px rgba(0,0,0,0.08)', overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.87rem' }}>
          <thead>
            <tr style={{ background: '#f9fafb', borderBottom: '2px solid #e5e7eb' }}>
              <th style={{ textAlign: 'left', padding: '0.7rem 1rem', color: '#374151', fontWeight: 600 }}>Name</th>
              <th style={{ textAlign: 'left', padding: '0.7rem 0.8rem', color: '#374151', fontWeight: 600 }}>Platform</th>
              <th style={{ textAlign: 'left', padding: '0.7rem 0.8rem', color: '#374151', fontWeight: 600 }}>Tactic</th>
              <th style={{ textAlign: 'left', padding: '0.7rem 0.8rem', color: '#374151', fontWeight: 600 }}>Technique</th>
              <th style={{ textAlign: 'left', padding: '0.7rem 0.8rem', color: '#374151', fontWeight: 600 }}>Severity</th>
              <th style={{ textAlign: 'left', padding: '0.7rem 0.8rem', color: '#374151', fontWeight: 600 }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {scenarios.map(s => (
              <tr key={s.id} style={{ borderBottom: '1px solid #f3f4f6' }}>
                <td style={{ padding: '0.7rem 1rem' }}>
                  <div style={{ fontWeight: 500, color: '#111827' }}>{s.name}</div>
                  <div style={{ fontSize: '0.75rem', color: '#6b7280', marginTop: '0.1rem' }}>{s.id}</div>
                </td>
                <td style={{ padding: '0.7rem 0.8rem', color: '#4b5563' }}>{s.platform}</td>
                <td style={{ padding: '0.7rem 0.8rem', color: '#4b5563' }}>{s.tactic}</td>
                <td style={{ padding: '0.7rem 0.8rem', fontFamily: 'monospace', fontSize: '0.82rem', color: '#1d4ed8' }}>{s.technique_id}</td>
                <td style={{ padding: '0.7rem 0.8rem' }}><SeverityBadge value={s.severity} /></td>
                <td style={{ padding: '0.7rem 0.8rem' }}>
                  <button
                    onClick={() => handleRun(s.id)}
                    disabled={running === s.id}
                    style={{
                      background: running === s.id ? '#9ca3af' : '#1e2a3a',
                      color: '#fff', border: 'none', borderRadius: 5,
                      padding: '0.35rem 0.9rem', cursor: running === s.id ? 'not-allowed' : 'pointer',
                      fontSize: '0.82rem', fontWeight: 500,
                    }}
                  >
                    {running === s.id ? 'Running...' : 'Run'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
