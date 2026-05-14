import React, { useEffect, useState } from 'react';
import { api } from '../api/client';
import type { Coverage as CoverageType } from '../types/api';
import { StatCard } from '../components/StatCard';
import { SeverityBadge } from '../components/SeverityBadge';

export function Coverage() {
  const [coverage, setCoverage] = useState<CoverageType | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getCoverage().then(setCoverage).finally(() => setLoading(false));
  }, []);

  if (loading) return <div style={{ color: '#6b7280' }}>Loading coverage data...</div>;
  if (!coverage) return <div style={{ color: '#991b1b' }}>Failed to load coverage</div>;

  return (
    <div>
      <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: '#1e2a3a', marginBottom: '1.5rem' }}>
        MITRE ATT&CK Coverage Matrix
      </h1>

      <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', marginBottom: '1.5rem' }}>
        <StatCard label="Total Scenarios" value={coverage.total_scenarios} />
        <StatCard label="Techniques" value={coverage.total_techniques} />
        <StatCard label="Tactics" value={coverage.total_tactics} />
        <StatCard label="Coverage Rate" value={`${coverage.coverage_rate}%`}
          color={coverage.coverage_rate >= 70 ? '#065f46' : '#92400e'} />
      </div>

      <div style={{ background: '#fff', borderRadius: 8, boxShadow: '0 1px 4px rgba(0,0,0,0.08)', overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.87rem' }}>
          <thead>
            <tr style={{ background: '#f9fafb', borderBottom: '2px solid #e5e7eb' }}>
              <th style={{ textAlign: 'left', padding: '0.7rem 1rem', color: '#374151' }}>Scenario</th>
              <th style={{ textAlign: 'left', padding: '0.7rem 0.8rem', color: '#374151' }}>Tactic</th>
              <th style={{ textAlign: 'left', padding: '0.7rem 0.8rem', color: '#374151' }}>Technique ID</th>
              <th style={{ textAlign: 'left', padding: '0.7rem 0.8rem', color: '#374151' }}>Technique Name</th>
              <th style={{ textAlign: 'left', padding: '0.7rem 0.8rem', color: '#374151' }}>Status</th>
            </tr>
          </thead>
          <tbody>
            {coverage.technique_coverage.map(tc => (
              <tr key={tc.scenario_id} style={{ borderBottom: '1px solid #f3f4f6' }}>
                <td style={{ padding: '0.7rem 1rem', color: '#374151', fontWeight: 500 }}>{tc.scenario_id}</td>
                <td style={{ padding: '0.7rem 0.8rem', color: '#4b5563' }}>{tc.tactic}</td>
                <td style={{ padding: '0.7rem 0.8rem', fontFamily: 'monospace', color: '#1d4ed8', fontSize: '0.83rem' }}>{tc.technique_id}</td>
                <td style={{ padding: '0.7rem 0.8rem', color: '#4b5563' }}>{tc.technique_name}</td>
                <td style={{ padding: '0.7rem 0.8rem' }}><SeverityBadge value={tc.status} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
