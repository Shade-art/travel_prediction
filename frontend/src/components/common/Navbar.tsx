import React, { useEffect, useState } from 'react';
import { NavLink } from 'react-router-dom';
import { Car, BarChart3, LineChart, Sparkles, Activity, ShieldAlert } from 'lucide-react';
import { api } from '../../api/endpoints';

export const Navbar: React.FC = () => {
  const [apiOnline, setApiOnline] = useState<boolean | null>(null);

  useEffect(() => {
    let isMounted = true;
    const checkHealth = async () => {
      try {
        const res = await api.getHealth();
        if (isMounted) setApiOnline(res.status === 'healthy');
      } catch {
        if (isMounted) setApiOnline(false);
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  const navLinkClass = ({ isActive }: { isActive: boolean }) =>
    `flex items-center gap-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-all duration-150 ${
      isActive
        ? 'bg-amber-500/10 text-amber-400 border border-amber-500/30 shadow-sm'
        : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
    }`;

  return (
    <header className="sticky top-0 z-50 bg-[#0B0F19]/90 backdrop-blur-md border-b border-slate-800/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Logo & Brand */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-400 to-amber-600 flex items-center justify-center shadow-lg shadow-amber-500/20 text-slate-950 font-bold">
            <Car className="w-5 h-5 stroke-[2.5]" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-base tracking-tight text-white">NYC TRANSIT</span>
              <span className="text-[10px] font-mono tracking-wider uppercase px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30">
                Phase 1
              </span>
            </div>
            <p className="text-[11px] text-slate-400 hidden sm:block">
              Demand Analysis & Prediction System
            </p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex items-center gap-1.5">
          <NavLink to="/" end className={navLinkClass}>
            <BarChart3 className="w-4 h-4" />
            <span>Overview</span>
          </NavLink>
          <NavLink to="/analytics" className={navLinkClass}>
            <LineChart className="w-4 h-4" />
            <span>Demand Analytics</span>
          </NavLink>
          <NavLink to="/prediction" className={navLinkClass}>
            <Sparkles className="w-4 h-4 text-amber-400" />
            <span>Demand Prediction</span>
          </NavLink>
        </nav>

        {/* Live System Status Indicator */}
        <div className="hidden lg:flex items-center gap-2.5 pl-4 border-l border-slate-800 text-xs">
          {apiOnline === true ? (
            <div className="flex items-center gap-2 text-emerald-400 font-mono text-[11px] bg-emerald-950/40 border border-emerald-800/50 px-2.5 py-1 rounded-full">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse-dot" />
              <span>API ONLINE</span>
            </div>
          ) : apiOnline === false ? (
            <div className="flex items-center gap-1.5 text-rose-400 font-mono text-[11px] bg-rose-950/40 border border-rose-800/50 px-2.5 py-1 rounded-full">
              <ShieldAlert className="w-3.5 h-3.5" />
              <span>OFFLINE (FALLBACK)</span>
            </div>
          ) : (
            <div className="flex items-center gap-1.5 text-slate-400 font-mono text-[11px]">
              <Activity className="w-3.5 h-3.5 animate-spin" />
              <span>CONNECTING</span>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
