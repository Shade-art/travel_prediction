import React from 'react';
import { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  badgeText?: string;
  badgeType?: 'neutral' | 'success' | 'warning' | 'info';
  accentColor?: 'amber' | 'blue' | 'emerald' | 'purple';
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  badgeText,
  badgeType = 'neutral',
  accentColor = 'amber',
}) => {
  const accentStyles = {
    amber: {
      border: 'hover:border-amber-500/40',
      iconBg: 'bg-amber-500/10 text-amber-400 border border-amber-500/20',
      glow: 'group-hover:shadow-amber-500/5',
    },
    blue: {
      border: 'hover:border-sky-500/40',
      iconBg: 'bg-sky-500/10 text-sky-400 border border-sky-500/20',
      glow: 'group-hover:shadow-sky-500/5',
    },
    emerald: {
      border: 'hover:border-emerald-500/40',
      iconBg: 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20',
      glow: 'group-hover:shadow-emerald-500/5',
    },
    purple: {
      border: 'hover:border-purple-500/40',
      iconBg: 'bg-purple-500/10 text-purple-400 border border-purple-500/20',
      glow: 'group-hover:shadow-purple-500/5',
    },
  }[accentColor];

  const badgeStyles = {
    neutral: 'bg-slate-800 text-slate-300 border-slate-700',
    success: 'bg-emerald-950/60 text-emerald-300 border-emerald-800/40',
    warning: 'bg-amber-950/60 text-amber-300 border-amber-800/40',
    info: 'bg-sky-950/60 text-sky-300 border-sky-800/40',
  }[badgeType];

  return (
    <div
      className={`group relative bg-[#111827]/80 rounded-xl p-5 border border-slate-800 transition-all duration-200 shadow-sm hover:shadow-lg ${accentStyles.border} ${accentStyles.glow}`}
    >
      <div className="flex items-start justify-between">
        <span className="text-xs font-semibold tracking-wider uppercase text-slate-400">
          {title}
        </span>
        <div className={`p-2 rounded-lg ${accentStyles.iconBg}`}>
          <Icon className="w-4 h-4" />
        </div>
      </div>

      <div className="mt-3 flex items-baseline gap-2">
        <span className="text-2xl sm:text-3xl font-extrabold tracking-tight text-white font-mono">
          {typeof value === 'number' ? value.toLocaleString() : value}
        </span>
        {badgeText && (
          <span
            className={`text-[11px] font-mono px-2 py-0.5 rounded-full border ${badgeStyles}`}
          >
            {badgeText}
          </span>
        )}
      </div>

      {subtitle && (
        <p className="mt-1.5 text-xs text-slate-400 font-normal truncate">
          {subtitle}
        </p>
      )}
    </div>
  );
};
