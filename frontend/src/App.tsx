import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Navbar } from './components/common/Navbar';
import { OverviewPage } from './pages/OverviewPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { PredictionPage } from './pages/PredictionPage';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col bg-[#0B0F19] text-slate-100 selection:bg-amber-500 selection:text-black">
        {/* Navigation Bar */}
        <Navbar />

        {/* Main Content Area */}
        <main className="flex-1 pb-16">
          <Routes>
            <Route path="/" element={<OverviewPage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
            <Route path="/prediction" element={<PredictionPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="border-t border-slate-800/80 bg-[#0B0F19] py-8 text-xs text-slate-500">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-center sm:text-left">
            <div>
              <p className="font-semibold text-slate-400">
                Public Transportation Demand Analysis and Passenger Prediction System
              </p>
              <p className="mt-0.5 text-[11px] text-slate-600">
                Phase 1 Prototype • NYC TLC Taxi Demand Use Case • Realistic Simulated Data
              </p>
            </div>
            <div className="flex items-center gap-4 text-slate-400 font-mono text-[11px]">
              <span>FastAPI Backend</span>
              <span>•</span>
              <span>React + Vite Frontend</span>
              <span>•</span>
              <span className="text-amber-500/80">Phase 1 Complete</span>
            </div>
          </div>
        </footer>
      </div>
    </BrowserRouter>
  );
};

export default App;
