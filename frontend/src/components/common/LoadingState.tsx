import React from 'react';
import { Loader2 } from 'lucide-react';

interface LoadingStateProps {
  message?: string;
  subMessage?: string;
  minHeight?: string;
}

export const LoadingState: React.FC<LoadingStateProps> = ({
  message = "Loading transit telemetry...",
  subMessage = "Aggregating NYC taxi catchment data",
  minHeight = "min-h-[280px]",
}) => {
  return (
    <div className={`w-full ${minHeight} flex flex-col items-center justify-center p-8 rounded-xl bg-slate-900/50 border border-slate-800/80`}>
      <div className="relative flex items-center justify-center">
        <div className="w-12 h-12 rounded-full border-2 border-amber-500/20 border-t-amber-400 animate-spin" />
        <Loader2 className="w-5 h-5 text-amber-400 absolute animate-pulse" />
      </div>
      <p className="mt-4 text-sm font-semibold text-slate-200">{message}</p>
      {subMessage && <p className="mt-1 text-xs text-slate-500 font-mono">{subMessage}</p>}
    </div>
  );
};
