import React, { useState } from 'react';
import { Calendar, Clock, MapPin, Sparkles, Send } from 'lucide-react';
import { PredictionRequest } from '../../api/types';
import { NYC_TAXI_ZONES } from '../../api/mockData';

interface PredictionFormProps {
  onSubmit: (params: PredictionRequest) => void;
  isLoading: boolean;
  initialValues?: PredictionRequest;
}

export const PredictionForm: React.FC<PredictionFormProps> = ({
  onSubmit,
  isLoading,
  initialValues,
}) => {
  const todayStr = new Date().toISOString().split('T')[0];

  const [pickupArea, setPickupArea] = useState<string>(
    initialValues?.pickup_area || NYC_TAXI_ZONES[0]
  );
  const [date, setDate] = useState<string>(initialValues?.date || todayStr);
  const [hour, setHour] = useState<number>(initialValues?.hour ?? 18);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({
      pickup_area: pickupArea,
      date,
      hour: Number(hour),
    });
  };

  const setPreset = (presetHour: number) => {
    setHour(presetHour);
  };

  return (
    <div className="bg-[#111827] rounded-xl p-5 border border-slate-800 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-100 uppercase tracking-wider flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-amber-400" />
            <span>Demand Simulation Parameters</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Configure target zone and temporal parameters for heuristic forecast
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Pickup Area Selector */}
        <div>
          <label className="block text-xs font-medium text-slate-300 mb-1 flex items-center gap-1.5">
            <MapPin className="w-3.5 h-3.5 text-amber-400" />
            <span>NYC Pickup Area / Catchment Zone</span>
          </label>
          <select
            value={pickupArea}
            onChange={(e) => setPickupArea(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700/80 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 font-medium"
          >
            {NYC_TAXI_ZONES.map((zone) => (
              <option key={zone} value={zone}>
                {zone}
              </option>
            ))}
          </select>
        </div>

        {/* Date and Hour Row */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1 flex items-center gap-1.5">
              <Calendar className="w-3.5 h-3.5 text-sky-400" />
              <span>Target Date</span>
            </label>
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              required
              className="w-full bg-slate-900 border border-slate-700/80 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 font-mono"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1 flex items-center justify-between">
              <span className="flex items-center gap-1.5">
                <Clock className="w-3.5 h-3.5 text-emerald-400" />
                <span>Target Hour (0-23)</span>
              </span>
              <span className="font-mono text-amber-400 font-bold">
                {String(hour).padStart(2, '0')}:00 ({hour % 12 || 12} {hour < 12 ? 'AM' : 'PM'})
              </span>
            </label>
            <input
              type="range"
              min="0"
              max="23"
              step="1"
              value={hour}
              onChange={(e) => setHour(Number(e.target.value))}
              className="w-full accent-amber-500 cursor-pointer h-2 bg-slate-800 rounded-lg"
            />
            <div className="flex justify-between text-[10px] text-slate-500 font-mono mt-1">
              <span>00:00</span>
              <span>06:00</span>
              <span>12:00</span>
              <span>18:00</span>
              <span>23:00</span>
            </div>
          </div>
        </div>

        {/* Quick Hour Presets */}
        <div className="pt-1">
          <span className="text-[11px] text-slate-400 font-mono block mb-1.5">Common Transit Windows:</span>
          <div className="flex flex-wrap gap-2">
            {[
              { label: 'Morning Commute', h: 8 },
              { label: 'Midday Lunch', h: 12 },
              { label: 'Evening Surge', h: 18 },
              { label: 'Nightlife', h: 22 },
              { label: 'Late Night', h: 3 },
            ].map((p) => (
              <button
                type="button"
                key={p.label}
                onClick={() => setPreset(p.h)}
                className={`text-xs px-2.5 py-1 rounded-md border transition-all ${
                  hour === p.h
                    ? 'bg-amber-500/20 text-amber-300 border-amber-500/40 font-semibold'
                    : 'bg-slate-900 text-slate-400 border-slate-800 hover:text-slate-200 hover:bg-slate-800'
                }`}
              >
                {p.label} ({String(p.h).padStart(2, '0')}:00)
              </button>
            ))}
          </div>
        </div>

        {/* Submit Button */}
        <div className="pt-2">
          <button
            type="submit"
            disabled={isLoading}
            className="w-full flex items-center justify-center gap-2 py-2.5 px-4 rounded-lg bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-bold text-sm shadow-md shadow-amber-500/20 transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <>
                <div className="w-4 h-4 border-2 border-slate-950 border-t-transparent rounded-full animate-spin" />
                <span>Simulating Demand...</span>
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                <span>Predict Demand</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};
