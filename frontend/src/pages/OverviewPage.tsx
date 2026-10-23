import React, { useEffect, useState } from 'react';
import {
  Users,
  Clock,
  TrendingUp,
  MapPin,
  RefreshCw,
  Compass,
  CalendarCheck
} from 'lucide-react';
import { api } from '../api/endpoints';
import {
  SummaryData,
  HourlyDataPoint,
  WeekdayDataPoint,
  AreaDataPoint
} from '../api/types';
import { FALLBACK_SUMMARY, FALLBACK_AREAS } from '../api/mockData';
import { MetricCard } from '../components/common/MetricCard';
import { LoadingState } from '../components/common/LoadingState';
import { ErrorState } from '../components/common/ErrorState';
import { HourlyDemandChart } from '../components/charts/HourlyDemandChart';
import { WeekdayDemandChart } from '../components/charts/WeekdayDemandChart';
import { AreaDemandChart } from '../components/charts/AreaDemandChart';
import { HonestNoteBanner } from '../components/common/HonestNoteBanner';

export const OverviewPage: React.FC = () => {
  const [summary, setSummary] = useState<SummaryData | null>(null);
  const [hourlyData, setHourlyData] = useState<HourlyDataPoint[]>([]);
  const [weekdayData, setWeekdayData] = useState<WeekdayDataPoint[]>([]);
  const [areaData, setAreaData] = useState<AreaDataPoint[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [sumRes, hourlyRes, weeklyRes, areaRes] = await Promise.all([
        api.getSummary().catch(() => FALLBACK_SUMMARY),
        api.getHourlyAnalytics(),
        api.getWeeklyAnalytics(),
        api.getAreaAnalytics(),
      ]);

      setSummary(sumRes);
      setHourlyData(hourlyRes.data);
      setWeekdayData(weeklyRes.weekday_distribution);
      setAreaData(areaRes.data);
    } catch (err: any) {
      setError(err.message || 'Failed to connect to transit analytics API.');
      // Fallback display so page is never broken
      setSummary(FALLBACK_SUMMARY);
      setAreaData(FALLBACK_AREAS);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        <LoadingState message="Connecting to NYC Transit telemetry engine..." />
      </div>
    );
  }

  if (error && !summary) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <ErrorState message={error} onRetry={fetchData} />
      </div>
    );
  }

  const activeSummary = summary || FALLBACK_SUMMARY;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Top Header & Context */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Transit Demand Executive Overview
            </h1>
          </div>
          <p className="mt-1 text-sm text-slate-400 flex items-center gap-2">
            <Compass className="w-4 h-4 text-amber-400" />
            <span>High-level mobility indicators across NYC TLC Taxi catchment clusters</span>
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="hidden sm:flex items-center gap-1.5 text-xs font-mono text-slate-400 bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-lg">
            <CalendarCheck className="w-3.5 h-3.5 text-emerald-400" />
            <span>{activeSummary.sample_date_range}</span>
          </div>

          <button
            onClick={fetchData}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700 transition"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Refresh Telemetry</span>
          </button>
        </div>
      </div>

      {/* Domain Note on Catchment Zones vs Fixed Routes */}
      <HonestNoteBanner compact />

      {/* KPI Cards (Total Pickups, Avg Hourly, Peak Hour, Busiest Area) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Total Pickups"
          value={activeSummary.total_pickups}
          subtitle={`Across ${activeSummary.total_monitored_zones} monitored NYC zones`}
          icon={Users}
          badgeText="Active Period"
          badgeType="info"
          accentColor="amber"
        />

        <MetricCard
          title="Avg Hourly Pickups"
          value={activeSummary.avg_hourly_pickups}
          subtitle="Citywide aggregate volume per hour"
          icon={Clock}
          badgeText="24h Average"
          badgeType="neutral"
          accentColor="blue"
        />

        <MetricCard
          title="Peak Demand Hour"
          value={activeSummary.peak_demand_hour_formatted}
          subtitle={`${activeSummary.peak_demand_hour_pickups.toLocaleString()} pickups during peak rush`}
          icon={TrendingUp}
          badgeText="Surge Window"
          badgeType="warning"
          accentColor="emerald"
        />

        <MetricCard
          title="Busiest Pickup Area"
          value={activeSummary.busiest_pickup_area}
          subtitle={`${activeSummary.busiest_area_percentage}% of all NYC trips (${activeSummary.busiest_pickup_borough})`}
          icon={MapPin}
          badgeText="Highest Density"
          badgeType="success"
          accentColor="purple"
        />
      </div>

      {/* Charts Grid: Hourly Demand Line Chart & Weekday Demand Bar Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <HourlyDemandChart data={hourlyData} />
        <WeekdayDemandChart data={weekdayData} />
      </div>

      {/* Demand Distribution by Pickup Area */}
      <div>
        <AreaDemandChart data={areaData} />
      </div>
    </div>
  );
};
