import React from 'react';
import { Database, FilterX } from 'lucide-react';

interface EmptyStateProps {
  title?: string;
  message?: string;
  onResetFilters?: () => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title = "No Demand Records Found",
  message = "No transit trip records match the current filter criteria. Try expanding the hour or pickup zone filter.",
  onResetFilters,
}) => {
  return (
    <div className="w-full min-h-[240px] flex flex-col items-center justify-center p-8 rounded-xl bg-slate-900/40 border border-slate-800 text-center">
      <div className="p-3 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
        <Database className="w-6 h-6" />
      </div>
      <h4 className="mt-3 text-sm font-bold text-slate-200">{title}</h4>
      <p className="mt-1 text-xs text-slate-400 max-w-sm">{message}</p>
      {onResetFilters && (
        <button
          onClick={onResetFilters}
          className="mt-4 flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium transition"
        >
          <FilterX className="w-3.5 h-3.5" />
          <span>Reset Filters</span>
        </button>
      )}
    </div>
  );
};
