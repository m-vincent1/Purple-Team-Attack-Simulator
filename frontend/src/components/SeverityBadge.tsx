import React from 'react';

const COLORS: Record<string, { bg: string; color: string }> = {
  critical: { bg: '#ede9fe', color: '#5b21b6' },
  high:     { bg: '#fee2e2', color: '#991b1b' },
  medium:   { bg: '#fef3c7', color: '#92400e' },
  low:      { bg: '#d1fae5', color: '#065f46' },
  covered:  { bg: '#d1fae5', color: '#065f46' },
  not_detected: { bg: '#fee2e2', color: '#991b1b' },
  not_tested:   { bg: '#f3f4f6', color: '#6b7280' },
  completed: { bg: '#dbeafe', color: '#1d4ed8' },
  running:   { bg: '#fef3c7', color: '#92400e' },
  failed:    { bg: '#fee2e2', color: '#991b1b' },
};

export function SeverityBadge({ value }: { value: string }) {
  const style = COLORS[value.toLowerCase()] ?? { bg: '#f3f4f6', color: '#374151' };
  return (
    <span style={{
      background: style.bg, color: style.color,
      padding: '0.15rem 0.6rem', borderRadius: 4,
      fontSize: '0.75rem', fontWeight: 600, textTransform: 'uppercase',
    }}>
      {value}
    </span>
  );
}
