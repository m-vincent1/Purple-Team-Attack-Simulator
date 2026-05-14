import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Dashboard } from './pages/Dashboard';
import { Scenarios } from './pages/Scenarios';
import { Runs } from './pages/Runs';
import { RunDetails } from './pages/RunDetails';
import { Reports } from './pages/Reports';
import { Coverage } from './pages/Coverage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="scenarios" element={<Scenarios />} />
          <Route path="runs" element={<Runs />} />
          <Route path="runs/:runId" element={<RunDetails />} />
          <Route path="reports" element={<Reports />} />
          <Route path="coverage" element={<Coverage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
