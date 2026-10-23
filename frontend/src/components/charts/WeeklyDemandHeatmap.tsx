import React, { useState } from 'react';
import { HeatmapCell } from '../../api/types';

interface WeeklyDemandHeatmapProps {
  data: HeatmapCell[];
  title?: string;
  subtitle?: string;
}

const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
const HOURS = Array.from({ length: 24 }, (_, i) => i);

export const WeeklyDemandHeatmap: React.FC<WeeklyDemandHeatmapProps> = ({
  data,
  title = "Demand Heatmap (Hour × Weekday)",
  subtitle = "Granular intensity grid of passenger demand across 168 weekly intervals",
}) => {
  const [hoveredCell, setHoveredCell] = useState<HeatmapCell | null>(null);

  // Map data to quick lookup: day_index-hour -> cell
  const cellMap = new Map<string, HeatmapCell>();
  data.forEach((cell) => {
    cellMap.set(`${cell.day_index}-${cell.hour}`, cell);
  });

  // Calculate dynamic color for intensity (0 to 100)
  const getCellColor = (intensity: number) => {
    if (intensity >= 85) return 'bg-amber-400 text-slate-950 font-bold';
    if (intensity >= 70) return 'bg-amber-500/90 text-slate-900';
    if (intensity >= 55) return 'bg-sky-500 text-slate-950';
    if (intensity >= 40) return 'bg-sky-600/80 text-white';
    if (intensity >= 25) return 'bg-indigo-700/70 text-slate-200';
    if (intensity >= 12) return 'bg-slate-800 text-slate-300';
    return 'bg-slate-900 text-slate-500';
  };

  return (
    <div className="bg-[#111827] rounded-xl p-5 border border-slate-800 shadow-sm overflow-hidden">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-100 uppercase tracking-wider">
            {title}
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">{subtitle}</p>
        </div>

        {/* Hovered cell readout */}
        <div className="h-6 flex items-center">
          {hoveredCell ? (
            <div className="text-xs font-mono bg-slate-800/90 border border-slate-700 px-2.5 py-1 rounded text-amber-300 flex items-center gap-2">
              <span className="font-bold">{hoveredCell.day_name}</span>
              <span>@ {hoveredCell.formatted_hour}</span>
              <span className="text-white font-extrabold">{hoveredCell.pickups.toLocaleString()} pickups</span>
              <span className="text-[10px] text-slate-400">({hoveredCell.intensity}% peak)</span>
            </div>
          ) : (
            <span className="text-[11px] text-slate-500 italic">Hover over any cell for volume telemetry</span>
          )}
        </div>
      </div>

      {/* Heatmap Grid Container */}
      <div className="overflow-x-auto pb-2">
        <div className="min-w-[720px]">
          {/* Header row: hours */}
          <div className="grid grid-cols-[56px_repeat(24,1fr)] gap-1 mb-1.5 text-center">
            <div className="text-[10px] font-mono text-slate-500 text-left pl-1">DAY \ HR</div>
            {HOURS.map((h) => (
              <div key={`h-lbl-${h}`} className="text-[9px] font-mono text-slate-400">
                {h % 3 === 0 ? `${h}h` : ''}
              </div>
            ))}
          </div>

          {/* Matrix rows: days */}
          {DAYS.map((dayName, dayIdx) => (
            <div key={`day-row-${dayIdx}`} className="grid grid-cols-[56px_repeat(24,1fr)] gap-1 mb-1 items-center">
              <div className="text-xs font-mono font-medium text-slate-300 pl-1">{dayName}</div>
              {HOURS.map((hour) => {
                const cell = cellMap.get(`${dayIdx}-${hour}`) || {
                  day_index: dayIdx,
                  day_name: dayName,
                  hour,
                  formatted_hour: `${String(hour).padStart(2, '0')}:00`,
                  pickups: 0,
                  intensity: 0,
                };
                const colorClass = getCellColor(cell.intensity);

                return (
                  <div
                    key={`cell-${dayIdx}-${hour}`}
                    onMouseEnter={() => setHoveredCell(cell)}
                    onMouseLeave={() => setHoveredCell(null)}
                    className={`h-7 rounded transition-all duration-150 cursor-pointer flex items-center justify-center text-[10px] border border-slate-900/60 hover:scale-110 hover:z-10 hover:border-white shadow-sm ${colorClass}`}
                    title={`${cell.day_name} ${cell.formatted_hour}: ${cell.pickups} pickups (${cell.intensity}%)`}
                  />
                );
              })}
            </div>
          ))}
        </div>
      </div>

      {/* Legend */}
      <div className="mt-4 pt-3 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-3 text-xs">
        <span className="text-slate-400 text-[11px] font-mono uppercase tracking-wider">Demand Intensity Scale:</span>
        <div className="flex items-center gap-1.5 font-mono text-[10px] text-slate-400">
          <span className="w-3.5 h-3.5 rounded bg-slate-900 border border-slate-800" />
          <span>Low (0-20%)</span>
          <span className="w-3.5 h-3.5 rounded bg-indigo-700/70 ml-2" />
          <span>Moderate (20-50%)</span>
          <span className="w-3.5 h-3.5 rounded bg-sky-500 ml-2" />
          <span>High (50-80%)</span>
          <span className="w-3.5 h-3.5 rounded bg-amber-400 ml-2" />
          <span className="text-amber-400 font-semibold">Peak Surge (80%+)</span>
        </div>
      </div>
    </div>
  );
};
