import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

interface ErrorStateProps {
  title?: string;
  message: string;
  onRetry?: () => void;
  minHeight?: string;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  title = "Telemetry Query Error",
  message,
  onRetry,
  minHeight = "min-h-[260px]",
}) => {
  return (
    <div className={`w-full ${minHeight} flex flex-col items-center justify-center p-8 rounded-xl bg-rose-950/20 border border-rose-900/40 text-center`}>
      <div className="p-3 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20">
        <AlertTriangle className="w-6 h-6" />
      </div>
      <h4 className="mt-3 text-base font-bold text-slate-100">{title}</h4>
      <p className="mt-1 text-xs text-rose-300 max-w-md font-mono">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-4 flex items-center gap-2 px-4 py-2 rounded-lg bg-rose-500/20 hover:bg-rose-500/30 text-rose-200 border border-rose-500/40 text-xs font-medium transition"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Retry Request</span>
        </button>
      )}
    </div>
  );
};
