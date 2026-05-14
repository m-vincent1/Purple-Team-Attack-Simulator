import React from 'react';

interface Props {
  label: string;
  value: string | number;
  sub?: string;
  color?: string;
}

export function StatCard({ label, value, sub, color = '#1e2a3a' }: Props) {
  return (
    <div style={{
      background: '#fff', borderRadius: 8, padding: '1.2rem 1.5rem',
      boxShadow: '0 1px 4px rgba(0,0,0,0.08)', flex: '1 1 160px',
    }}>
      <div style={{ fontSize: '0.75rem', color: '#6b7280', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
        {label}
      </div>
      <div style={{ fontSize: '2rem', fontWeight: 700, color, marginTop: '0.3rem' }}>{value}</div>
      {sub && <div style={{ fontSize: '0.78rem', color: '#9ca3af', marginTop: '0.2rem' }}>{sub}</div>}
    </div>
  );
}
