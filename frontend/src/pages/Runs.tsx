import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api/client';
import type { SimulationRun } from '../types/api';
import { SeverityBadge } from '../components/SeverityBadge';

export function Runs() {
  const [runs, setRuns] = useState<SimulationRun[]>([]);
  const [loading, setLoading] = useState(true);

  const load = () => {
    api.getRuns().then(setRuns).finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  if (loading) return <div style={{ color: '#6b7280' }}>Loading runs...</div>;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: '#1e2a3a' }}>Simulation Runs</h1>
        <button onClick={load} style={{ background: '#1e2a3a', color: '#fff', border: 'none', borderRadius: 6, padding: '0.4rem 1rem', cursor: 'pointer', fontSize: '0.88rem' }}>
          Refresh
        </button>
      </div>
      {runs.length === 0
        ? <p style={{ color: '#6b7280' }}>No runs yet. Go to <Link to="/scenarios">Scenarios</Link> to run one.</p>
        : (
          <div style={{ background: '#fff', borderRadius: 8, boxShadow: '0 1px 4px rgba(0,0,0,0.08)', overflow: 'hidden' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.87rem' }}>
              <thead>
                <tr style={{ background: '#f9fafb', borderBottom: '2px solid #e5e7eb' }}>
                  <th style={{ textAlign: 'left', padding: '0.7rem 1rem', color: '#374151' }}>Run ID</th>
                  <th style={{ textAlign: 'left', padding: '0.7rem 0.8rem', color: '#374151' }}>Scenario</th>
                  <th style={{ textAlign: 'left', padding: '0.7rem 0.8rem', color: '#374151' }}>Status</th>
                  <th style={{ textAlign: 'left', padding: '0.7rem 0.8rem', color: '#374151' }}>Started</th>
                  <th style={{ textAlign: 'left', padding: '0.7rem 0.8rem', color: '#374151' }}>Details</th>
                </tr>
              </thead>
              <tbody>
                {runs.map(run => (
                  <tr key={run.id} style={{ borderBottom: '1px solid #f3f4f6' }}>
                    <td style={{ padding: '0.7rem 1rem', fontFamily: 'monospace', fontSize: '0.78rem', color: '#374151' }}>
                      {run.id}
                    </td>
                    <td style={{ padding: '0.7rem 0.8rem', color: '#4b5563' }}>{run.scenario_id}</td>
                    <td style={{ padding: '0.7rem 0.8rem' }}><SeverityBadge value={run.status} /></td>
                    <td style={{ padding: '0.7rem 0.8rem', color: '#6b7280', fontSize: '0.82rem' }}>
                      {new Date(run.started_at).toLocaleString()}
                    </td>
                    <td style={{ padding: '0.7rem 0.8rem' }}>
                      <Link to={`/runs/${run.id}`} style={{ color: '#1d4ed8', fontSize: '0.82rem' }}>View</Link>
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
