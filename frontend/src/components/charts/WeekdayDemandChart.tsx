import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Cell
} from 'recharts';
import { WeekdayDataPoint } from '../../api/types';

interface WeekdayDemandChartProps {
  data: WeekdayDataPoint[];
  title?: string;
}

export const WeekdayDemandChart: React.FC<WeekdayDemandChartProps> = ({
  data,
  title = "Weekday Demand Distribution",
}) => {
  const maxVal = Math.max(...data.map(d => d.total_pickups), 1);

  return (
    <div className="bg-[#111827] rounded-xl p-5 border border-slate-800 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-100 uppercase tracking-wider">
            {title}
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Total simulated passenger trips grouped by day of week
          </p>
        </div>
      </div>

      <div className="h-[280px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" vertical={false} />
            <XAxis
              dataKey="short_name"
              stroke="#64748B"
              fontSize={11}
              tickLine={false}
            />
            <YAxis
              stroke="#64748B"
              fontSize={11}
              tickLine={false}
              tickFormatter={(v) => v >= 1000 ? `${(v / 1000).toFixed(0)}k` : v}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#0F172A',
                borderColor: '#334155',
                borderRadius: '8px',
                fontSize: '12px',
              }}
              labelStyle={{ color: '#F8FAFC', fontWeight: 600, marginBottom: '4px' }}
              formatter={(value: any) => [`${Number(value).toLocaleString()} pickups`, 'Total Pickups']}
            />
            <Bar dataKey="total_pickups" radius={[4, 4, 0, 0]}>
              {data.map((entry, index) => {
                // Give peak day (e.g. Friday) a brighter amber accent, others graduated blue/slate
                const isMax = entry.total_pickups === maxVal;
                return (
                  <Cell
                    key={`cell-${index}`}
                    fill={isMax ? '#F59E0B' : '#0284C7'}
                    fillOpacity={isMax ? 0.95 : 0.75}
                  />
                );
              })}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
