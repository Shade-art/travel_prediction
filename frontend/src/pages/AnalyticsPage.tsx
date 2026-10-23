import React, { useEffect, useState, useMemo } from 'react';
import {
  Filter,
  RefreshCw,
  MapPin,
  Clock,
  Calendar,
  Layers,
  ChevronRight
} from 'lucide-react';
import { api } from '../api/endpoints';
import {
  HourlyDataPoint,
  WeekdayDataPoint,
  AreaDataPoint,
  HeatmapCell
} from '../api/types';
import { NYC_TAXI_ZONES } from '../api/mockData';
import { LoadingState } from '../components/common/LoadingState';
import { ErrorState } from '../components/common/ErrorState';
import { EmptyState } from '../components/common/EmptyState';
import { HonestNoteBanner } from '../components/common/HonestNoteBanner';
import { HourlyDemandChart } from '../components/charts/HourlyDemandChart';
import { WeekdayDemandChart } from '../components/charts/WeekdayDemandChart';
import { WeeklyDemandHeatmap } from '../components/charts/WeeklyDemandHeatmap';

export const AnalyticsPage: React.FC = () => {
  // Filter states
  const [selectedArea, setSelectedArea] = useState<string>('all');
  const [selectedHour, setSelectedHour] = useState<string>('all'); // 'all' or '0'-'23'
  const [dateRange, setDateRange] = useState<string>('7d');

  // Data states
  const [hourlyData, setHourlyData] = useState<HourlyDataPoint[]>([]);
  const [weekdayData, setWeekdayData] = useState<WeekdayDataPoint[]>([]);
  const [heatmapData, setHeatmapData] = useState<HeatmapCell[]>([]);
  const [areasData, setAreasData] = useState<AreaDataPoint[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async (areaFilter: string) => {
    setLoading(true);
    setError(null);
    try {
      const [hourlyRes, weeklyRes, areasRes] = await Promise.all([
        api.getHourlyAnalytics(areaFilter),
        api.getWeeklyAnalytics(areaFilter),
        api.getAreaAnalytics(),
      ]);

      setHourlyData(hourlyRes.data);
      setWeekdayData(weeklyRes.weekday_distribution);
      setHeatmapData(weeklyRes.heatmap);
      setAreasData(areasRes.data);
    } catch (err: any) {
      setError(err.message || 'Failed to retrieve analytics data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData(selectedArea);
  }, [selectedArea]);

  // Client-side hour filter applied to hourly data if specific hour is chosen
  const filteredHourlyData = useMemo(() => {
    if (selectedHour === 'all') return hourlyData;
    const h = parseInt(selectedHour, 10);
    return hourlyData.filter((item) => item.hour === h);
  }, [hourlyData, selectedHour]);

  const resetFilters = () => {
    setSelectedArea('all');
    setSelectedHour('all');
    setDateRange('7d');
  };

  // Find info on currently selected area
  const currentAreaInfo = areasData.find(
    (a) => a.area_name.toLowerCase() === selectedArea.toLowerCase()
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Demand Analytics & Spatial Distribution
          </h1>
          <p className="mt-1 text-sm text-slate-400">
            Multi-dimensional temporal and geographic catchment breakdown
          </p>
        </div>

        <button
          onClick={() => loadData(selectedArea)}
          className="self-start md:self-auto flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700 transition"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh View</span>
        </button>
      </div>

      {/* Honest Note: Point-to-Point Taxis vs Fixed Routes */}
      <HonestNoteBanner />

      {/* Interactive Filters Bar */}
      <div className="bg-[#111827] rounded-xl p-4 border border-slate-800 shadow-sm">
        <div className="flex items-center gap-2 mb-3 text-xs font-semibold uppercase tracking-wider text-slate-400">
          <Filter className="w-3.5 h-3.5 text-amber-400" />
          <span>Interactive Telemetry Filters</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {/* Pickup Area Filter */}
          <div>
            <label className="block text-[11px] font-mono text-slate-400 mb-1 flex items-center gap-1">
              <MapPin className="w-3 h-3 text-amber-400" />
              <span>Catchment Pickup Area</span>
            </label>
            <select
              value={selectedArea}
              onChange={(e) => setSelectedArea(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700/80 rounded-lg px-3 py-1.5 text-xs text-slate-100 focus:outline-none focus:border-amber-500 font-medium"
            >
              <option value="all">All NYC Monitored Zones (Aggregate)</option>
              {NYC_TAXI_ZONES.map((zone) => (
                <option key={zone} value={zone}>
                  {zone}
                </option>
              ))}
            </select>
          </div>

          {/* Hour Filter */}
          <div>
            <label className="block text-[11px] font-mono text-slate-400 mb-1 flex items-center gap-1">
              <Clock className="w-3 h-3 text-emerald-400" />
              <span>Hour of Day Window</span>
            </label>
            <select
              value={selectedHour}
              onChange={(e) => setSelectedHour(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700/80 rounded-lg px-3 py-1.5 text-xs text-slate-100 focus:outline-none focus:border-amber-500 font-medium"
            >
              <option value="all">Full 24-Hour Cycle (All Hours)</option>
              {Array.from({ length: 24 }, (_, i) => (
                <option key={i} value={String(i)}>
                  {String(i).padStart(2, '0')}:00 ({i % 12 || 12} {i < 12 ? 'AM' : 'PM'})
                </option>
              ))}
            </select>
          </div>

          {/* Date Range Filter */}
          <div>
            <label className="block text-[11px] font-mono text-slate-400 mb-1 flex items-center gap-1">
              <Calendar className="w-3 h-3 text-sky-400" />
              <span>Sampling Window</span>
            </label>
            <select
              value={dateRange}
              onChange={(e) => setDateRange(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700/80 rounded-lg px-3 py-1.5 text-xs text-slate-100 focus:outline-none focus:border-amber-500 font-medium"
            >
              <option value="7d">Last 7 Days (Standard Cycle)</option>
              <option value="weekday">Weekday Aggregate Only (Mon-Fri)</option>
              <option value="weekend">Weekend Aggregate Only (Sat-Sun)</option>
            </select>
          </div>
        </div>

        {/* Active Filter Chips */}
        <div className="mt-3 pt-3 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center gap-2 text-xs">
            <span className="text-slate-500 text-[11px] font-mono">Active Scope:</span>
            <span className="px-2 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/20 font-mono text-[11px]">
              Area: {selectedArea === 'all' ? 'All Monitored Zones' : selectedArea}
            </span>
            <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 font-mono text-[11px]">
              Hour: {selectedHour === 'all' ? '00:00 - 23:00' : `${selectedHour}:00`}
            </span>
          </div>

          {(selectedArea !== 'all' || selectedHour !== 'all') && (
            <button
              onClick={resetFilters}
              className="text-[11px] text-slate-400 hover:text-amber-400 underline transition"
            >
              Reset to Defaults
            </button>
          )}
        </div>
      </div>

      {/* Selected Area Insight Banner (when filtered) */}
      {currentAreaInfo && (
        <div className="bg-slate-900/60 border border-sky-500/30 rounded-xl p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-sky-500/10 text-sky-400 border border-sky-500/20">
              <Layers className="w-5 h-5" />
            </div>
            <div>
              <h4 className="text-sm font-bold text-white flex items-center gap-2">
                <span>{currentAreaInfo.area_name}</span>
                <span className="text-xs font-mono text-sky-400 font-normal">
                  ({currentAreaInfo.borough} • {currentAreaInfo.zone_type})
                </span>
              </h4>
              <p className="text-xs text-slate-400 mt-0.5">
                Total pickups: <strong className="text-white font-mono">{currentAreaInfo.total_pickups.toLocaleString()}</strong> ({currentAreaInfo.percentage}% of city total) • Peak Hour: <strong className="text-amber-300 font-mono">{currentAreaInfo.peak_hour_formatted}</strong>
              </p>
            </div>
          </div>
          <ChevronRight className="w-4 h-4 text-slate-500 hidden sm:block" />
        </div>
      )}

      {/* Main Content Areas */}
      {loading ? (
        <LoadingState message="Aggregating catchment analytics..." />
      ) : error ? (
        <ErrorState message={error} onRetry={() => loadData(selectedArea)} />
      ) : filteredHourlyData.length === 0 ? (
        <EmptyState onResetFilters={resetFilters} />
      ) : (
        <div className="space-y-8">
          {/* Charts: Hourly and Weekday Demand Visualizations */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <HourlyDemandChart
              data={filteredHourlyData}
              title={
                selectedArea === 'all'
                  ? 'Hourly Demand Curve (Citywide)'
                  : `Hourly Demand Curve (${selectedArea})`
              }
            />
            <WeekdayDemandChart
              data={weekdayData}
              title={
                selectedArea === 'all'
                  ? 'Weekday Passenger Volume (All Zones)'
                  : `Weekday Passenger Volume (${selectedArea})`
              }
            />
          </div>

          {/* Granular Heatmap of Demand by Hour and Weekday */}
          <WeeklyDemandHeatmap
            data={heatmapData}
            title={
              selectedArea === 'all'
                ? 'Citywide Demand Heatmap (Hour × Weekday)'
                : `Demand Heatmap for ${selectedArea} (Hour × Weekday)`
            }
          />
        </div>
      )}
    </div>
  );
};
