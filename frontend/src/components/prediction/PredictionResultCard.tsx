import React from 'react';
import {
  TrendingUp,
  TrendingDown,
  CheckCircle2,
  Clock,
  MapPin,
  Calendar,
  Sparkles,
  Info
} from 'lucide-react';
import { PredictionResponse } from '../../api/types';
import { Badge } from '../common/Badge';

interface PredictionResultCardProps {
  prediction: PredictionResponse;
}

export const PredictionResultCard: React.FC<PredictionResultCardProps> = ({ prediction }) => {
  const isPositiveDiff = prediction.difference_percentage >= 0;

  const demandVariant = {
    'Peak Surge': 'amber',
    'High': 'blue',
    'Moderate': 'emerald',
    'Low': 'slate',
  }[prediction.demand_level] || 'slate';

  return (
    <div className="bg-[#111827] rounded-xl p-5 border border-slate-800 shadow-sm space-y-5">
      {/* Simulation Disclaimer Alert Banner */}
      <div className="p-3 rounded-lg bg-amber-500/10 border border-amber-500/30 flex items-start gap-2.5 text-xs text-amber-200">
        <Sparkles className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
        <div>
          <span className="font-bold tracking-wide uppercase text-amber-300 mr-1.5">
            Phase 1 Mock / Heuristic Estimate:
          </span>
          <span>{prediction.disclaimer}</span>
        </div>
      </div>

      {/* Primary KPI Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Badge variant={demandVariant as any} size="md">
              {prediction.demand_level}
            </Badge>
            <span className="text-xs text-slate-400 font-mono">
              Confidence Score: {(prediction.confidence_score * 100).toFixed(0)}%
            </span>
          </div>
          <div className="flex items-center gap-2 text-xs text-slate-400">
            <span className="flex items-center gap-1 text-slate-200 font-medium">
              <MapPin className="w-3.5 h-3.5 text-amber-400" />
              {prediction.pickup_area}
            </span>
            <span>•</span>
            <span className="flex items-center gap-1 font-mono">
              <Calendar className="w-3.5 h-3.5 text-sky-400" />
              {prediction.date} ({prediction.day_name})
            </span>
            <span>•</span>
            <span className="flex items-center gap-1 font-mono">
              <Clock className="w-3.5 h-3.5 text-emerald-400" />
              {prediction.formatted_hour}
            </span>
          </div>
        </div>

        {/* Volume Metric & Comparison Callout */}
        <div className="flex items-baseline gap-4 sm:text-right">
          <div>
            <span className="block text-[11px] font-mono text-slate-400 uppercase tracking-wider">
              Simulated Forecast
            </span>
            <span className="text-3xl sm:text-4xl font-extrabold text-amber-400 font-mono">
              {prediction.predicted_pickups.toLocaleString()}
            </span>
            <span className="text-xs text-slate-400 ml-1">pickups/hr</span>
          </div>

          <div className="border-l border-slate-800 pl-4">
            <span className="block text-[11px] font-mono text-slate-400 uppercase tracking-wider">
              vs Historical Avg ({prediction.historical_average.toLocaleString()})
            </span>
            <div
              className={`inline-flex items-center gap-1 text-sm font-bold font-mono px-2 py-0.5 rounded ${
                isPositiveDiff
                  ? 'bg-emerald-950/60 text-emerald-400 border border-emerald-800/50'
                  : 'bg-rose-950/60 text-rose-400 border border-rose-800/50'
              }`}
            >
              {isPositiveDiff ? (
                <TrendingUp className="w-3.5 h-3.5" />
              ) : (
                <TrendingDown className="w-3.5 h-3.5" />
              )}
              <span>
                {isPositiveDiff ? '+' : ''}
                {prediction.difference_percentage}%
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Simulation Drivers / Heuristic Factors */}
      <div>
        <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
          <Info className="w-3.5 h-3.5 text-sky-400" />
          <span>Simulation Model Factors & Drivers:</span>
        </h4>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          {prediction.key_drivers.map((driver, idx) => (
            <div
              key={idx}
              className="flex items-start gap-2 p-2.5 rounded-lg bg-slate-900/60 border border-slate-800 text-xs text-slate-300"
            >
              <CheckCircle2 className="w-3.5 h-3.5 text-amber-400 mt-0.5 shrink-0" />
              <span>{driver}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
