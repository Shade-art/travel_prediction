import React from 'react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend
} from 'recharts';
import { HourlyDataPoint } from '../../api/types';

interface HourlyDemandChartProps {
  data: HourlyDataPoint[];
  title?: string;
  showComparison?: boolean;
}

export const HourlyDemandChart: React.FC<HourlyDemandChartProps> = ({
  data,
  title = "24-Hour Passenger Demand Distribution",
  showComparison = true,
}) => {
  return (
    <div className="bg-[#111827] rounded-xl p-5 border border-slate-800 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-100 uppercase tracking-wider">
            {title}
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Average hourly pickup volume indexed across 24-hour cycle
          </p>
        </div>
      </div>

      <div className="h-[280px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="colorPickups" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#F59E0B" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#F59E0B" stopOpacity={0.0} />
              </linearGradient>
              <linearGradient id="colorWeekday" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#38BDF8" stopOpacity={0.25} />
                <stop offset="95%" stopColor="#38BDF8" stopOpacity={0.0} />
              </linearGradient>
              <linearGradient id="colorWeekend" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#A855F7" stopOpacity={0.2} />
                <stop offset="95%" stopColor="#A855F7" stopOpacity={0.0} />
              </linearGradient>
            </defs>

            <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" vertical={false} />
            <XAxis
              dataKey="formatted_hour"
              stroke="#64748B"
              fontSize={11}
              tickLine={false}
              interval={2}
            />
            <YAxis
              stroke="#64748B"
              fontSize={11}
              tickLine={false}
              tickFormatter={(v) => v >= 1000 ? `${(v / 1000).toFixed(1)}k` : v}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#0F172A',
                borderColor: '#334155',
                borderRadius: '8px',
                fontSize: '12px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.5)',
              }}
              labelStyle={{ color: '#F8FAFC', fontWeight: 600, marginBottom: '4px' }}
              itemStyle={{ color: '#CBD5E1' }}
            />
            <Legend
              wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }}
              iconType="circle"
            />

            <Area
              type="monotone"
              dataKey="pickups"
              name="Aggregate Volume"
              stroke="#F59E0B"
              strokeWidth={2.5}
              fillOpacity={1}
              fill="url(#colorPickups)"
            />

            {showComparison && (
              <>
                <Area
                  type="monotone"
                  dataKey="weekday_pickups"
                  name="Weekday Avg"
                  stroke="#38BDF8"
                  strokeWidth={1.5}
                  strokeDasharray="4 4"
                  fillOpacity={1}
                  fill="url(#colorWeekday)"
                />
                <Area
                  type="monotone"
                  dataKey="weekend_pickups"
                  name="Weekend Avg"
                  stroke="#A855F7"
                  strokeWidth={1.5}
                  strokeDasharray="2 2"
                  fillOpacity={1}
                  fill="url(#colorWeekend)"
                />
              </>
            )}
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
