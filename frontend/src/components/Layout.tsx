import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';

const NAV_ITEMS = [
  { to: '/', label: 'Dashboard', icon: '📊' },
  { to: '/scenarios', label: 'Scenarios', icon: '🎯' },
  { to: '/runs', label: 'Runs', icon: '▶️' },
  { to: '/reports', label: 'Reports', icon: '📄' },
  { to: '/coverage', label: 'Coverage', icon: '🛡️' },
];

export function Layout() {
  return (
    <div style={{ display: 'flex', minHeight: '100vh', fontFamily: "'Segoe UI', Arial, sans-serif", background: '#f5f6fa' }}>
      <aside style={{
        width: 220, background: '#1e2a3a', color: '#fff', padding: '1.5rem 0',
        display: 'flex', flexDirection: 'column', flexShrink: 0,
      }}>
        <div style={{ padding: '0 1.5rem 1.5rem', borderBottom: '1px solid #2d3f54' }}>
          <div style={{ fontSize: '1rem', fontWeight: 700, color: '#7c9cbf' }}>🛡️ Purple Team</div>
          <div style={{ fontSize: '0.75rem', color: '#4a6480', marginTop: 2 }}>Attack Simulator</div>
        </div>
        <nav style={{ marginTop: '1rem', flex: 1 }}>
          {NAV_ITEMS.map(item => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              style={({ isActive }) => ({
                display: 'flex', alignItems: 'center', gap: '0.6rem',
                padding: '0.6rem 1.5rem', color: isActive ? '#fff' : '#9ab',
                background: isActive ? '#2d3f54' : 'transparent',
                textDecoration: 'none', fontSize: '0.9rem',
                borderLeft: isActive ? '3px solid #6b8fb5' : '3px solid transparent',
                transition: 'all 0.15s',
              })}
            >
              <span>{item.icon}</span>
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
        <div style={{ padding: '1rem 1.5rem', borderTop: '1px solid #2d3f54', fontSize: '0.7rem', color: '#4a6480' }}>
          Defensive use only
        </div>
      </aside>
      <main style={{ flex: 1, padding: '2rem', overflow: 'auto' }}>
        <Outlet />
      </main>
    </div>
  );
}
