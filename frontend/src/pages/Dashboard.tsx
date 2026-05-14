import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api/client';
import type { Coverage, SimulationRun } from '../types/api';
import { StatCard } from '../components/StatCard';
import { SeverityBadge } from '../components/SeverityBadge';

export function Dashboard() {
  const [coverage, setCoverage] = useState<Coverage | null>(null);
  const [runs, setRuns] = useState<SimulationRun[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    Promise.all([api.getCoverage(), api.getRuns()])
      .then(([cov, r]) => { setCoverage(cov); setRuns(r); })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div style={{ color: '#6b7280' }}>Loading dashboard...</div>;
  if (error) return <div style={{ color: '#991b1b' }}>Error: {error}</div>;

  const totalAlerts = Object.values(coverage?.alerts_by_severity ?? {}).reduce((s, v) => s + v, 0);
  const recentRuns = runs.slice(0, 5);

  return (
    <div>
      <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: '#1e2a3a', marginBottom: '1.5rem' }}>
        Dashboard
      </h1>

      <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', marginBottom: '1.5rem' }}>
        <StatCard label="Total Scenarios" value={coverage?.total_scenarios ?? 0} />
        <StatCard label="Total Runs" value={runs.length} />
        <StatCard label="Total Alerts" value={totalAlerts} color="#c2410c" />
        <StatCard
          label="Coverage Rate"
          value={`${coverage?.coverage_rate ?? 0}%`}
          color={(coverage?.coverage_rate ?? 0) >= 70 ? '#065f46' : '#92400e'}
        />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '1.5rem' }}>
        <div style={{ background: '#fff', borderRadius: 8, padding: '1.2rem', boxShadow: '0 1px 4px rgba(0,0,0,0.08)' }}>
          <h2 style={{ fontSize: '0.95rem', fontWeight: 600, color: '#1e2a3a', marginBottom: '1rem' }}>Alerts by Severity</h2>
          {Object.entries(coverage?.alerts_by_severity ?? {}).length === 0
            ? <p style={{ color: '#9ca3af', fontSize: '0.88rem' }}>No alerts yet. Run some scenarios.</p>
            : Object.entries(coverage?.alerts_by_severity ?? {}).map(([sev, count]) => (
              <div key={sev} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                <SeverityBadge value={sev} />
                <span style={{ fontWeight: 600, color: '#374151' }}>{count}</span>
              </div>
            ))
          }
        </div>

        <div style={{ background: '#fff', borderRadius: 8, padding: '1.2rem', boxShadow: '0 1px 4px rgba(0,0,0,0.08)' }}>
          <h2 style={{ fontSize: '0.95rem', fontWeight: 600, color: '#1e2a3a', marginBottom: '1rem' }}>MITRE Coverage</h2>
          <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
            {['covered', 'not_detected', 'not_tested'].map(status => {
              const count = coverage?.technique_coverage?.filter(t => t.status === status).length ?? 0;
              return (
                <div key={status} style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#1e2a3a' }}>{count}</div>
                  <SeverityBadge value={status} />
                </div>
              );
            })}
          </div>
        </div>
      </div>

      <div style={{ background: '#fff', borderRadius: 8, padding: '1.2rem', boxShadow: '0 1px 4px rgba(0,0,0,0.08)' }}>
        <h2 style={{ fontSize: '0.95rem', fontWeight: 600, color: '#1e2a3a', marginBottom: '1rem' }}>Recent Runs</h2>
        {recentRuns.length === 0
          ? <p style={{ color: '#9ca3af', fontSize: '0.88rem' }}>No runs yet. <Link to="/scenarios">Run a scenario</Link>.</p>
          : (
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
              <thead>
                <tr style={{ borderBottom: '2px solid #f3f4f6' }}>
                  <th style={{ textAlign: 'left', padding: '0.4rem 0.6rem', color: '#374151' }}>Run ID</th>
                  <th style={{ textAlign: 'left', padding: '0.4rem 0.6rem', color: '#374151' }}>Scenario</th>
                  <th style={{ textAlign: 'left', padding: '0.4rem 0.6rem', color: '#374151' }}>Status</th>
                  <th style={{ textAlign: 'left', padding: '0.4rem 0.6rem', color: '#374151' }}>Started</th>
                </tr>
              </thead>
              <tbody>
                {recentRuns.map(run => (
                  <tr key={run.id} style={{ borderBottom: '1px solid #f9fafb' }}>
                    <td style={{ padding: '0.4rem 0.6rem' }}>
                      <Link to={`/runs/${run.id}`} style={{ color: '#1d4ed8', fontFamily: 'monospace', fontSize: '0.8rem' }}>
                        {run.id.slice(0, 30)}...
                      </Link>
                    </td>
                    <td style={{ padding: '0.4rem 0.6rem', color: '#4b5563' }}>{run.scenario_id}</td>
                    <td style={{ padding: '0.4rem 0.6rem' }}><SeverityBadge value={run.status} /></td>
                    <td style={{ padding: '0.4rem 0.6rem', color: '#6b7280' }}>{new Date(run.started_at).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
      </div>
    </div>
  );
}
