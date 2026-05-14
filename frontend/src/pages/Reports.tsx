import React, { useEffect, useState } from 'react';
import { api } from '../api/client';
import type { SimulationRun } from '../types/api';
import { SeverityBadge } from '../components/SeverityBadge';

export function Reports() {
  const [runs, setRuns] = useState<SimulationRun[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getRuns()
      .then(r => setRuns(r.filter(run => run.status === 'completed')))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div style={{ color: '#6b7280' }}>Loading...</div>;

  return (
    <div>
      <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: '#1e2a3a', marginBottom: '1.5rem' }}>Reports</h1>
      {runs.length === 0
        ? <p style={{ color: '#6b7280' }}>No completed runs yet. Run some scenarios first.</p>
        : (
          <div style={{ background: '#fff', borderRadius: 8, boxShadow: '0 1px 4px rgba(0,0,0,0.08)', overflow: 'hidden' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.87rem' }}>
              <thead>
                <tr style={{ background: '#f9fafb', borderBottom: '2px solid #e5e7eb' }}>
                  <th style={{ textAlign: 'left', padding: '0.7rem 1rem', color: '#374151' }}>Run ID</th>
                  <th style={{ textAlign: 'left', padding: '0.7rem 0.8rem', color: '#374151' }}>Scenario</th>
                  <th style={{ textAlign: 'left', padding: '0.7rem 0.8rem', color: '#374151' }}>Date</th>
                  <th style={{ textAlign: 'left', padding: '0.7rem 0.8rem', color: '#374151' }}>Export</th>
                </tr>
              </thead>
              <tbody>
                {runs.map(run => (
                  <tr key={run.id} style={{ borderBottom: '1px solid #f3f4f6' }}>
                    <td style={{ padding: '0.7rem 1rem', fontFamily: 'monospace', fontSize: '0.78rem', color: '#374151' }}>{run.id}</td>
                    <td style={{ padding: '0.7rem 0.8rem', color: '#4b5563' }}>{run.scenario_id}</td>
                    <td style={{ padding: '0.7rem 0.8rem', color: '#6b7280', fontSize: '0.82rem' }}>{new Date(run.started_at).toLocaleString()}</td>
                    <td style={{ padding: '0.7rem 0.8rem' }}>
                      <div style={{ display: 'flex', gap: '0.5rem' }}>
                        {['html', 'md', 'json'].map(fmt => (
                          <a key={fmt} href={api.getReportUrl(run.id, fmt)} target="_blank" rel="noreferrer"
                            style={{ background: '#1e2a3a', color: '#fff', padding: '0.2rem 0.6rem', borderRadius: 4, textDecoration: 'none', fontSize: '0.78rem' }}>
                            {fmt.toUpperCase()}
                          </a>
                        ))}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )
      }
    </div>
  );
}
