import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell
} from 'recharts';
import { AreaDataPoint } from '../../api/types';

interface AreaDemandChartProps {
  data: AreaDataPoint[];
  title?: string;
  limit?: number;
}

const COLORS = [
  '#F59E0B', // Midtown Center
  '#FBBF24', // Times Square
  '#38BDF8', // JFK
  '#0284C7', // Upper East Side
  '#6366F1', // Financial District
  '#8B5CF6', // Upper West Side
  '#EC4899', // East Village
  '#10B981', // LaGuardia
  '#14B8A6', // Williamsburg
  '#64748B', // Astoria
];

export const AreaDemandChart: React.FC<AreaDemandChartProps> = ({
  data,
  title = "Demand Distribution by Pickup Area",
  limit = 10,
}) => {
  const displayData = data.slice(0, limit);

  return (
    <div className="bg-[#111827] rounded-xl p-5 border border-slate-800 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-100 uppercase tracking-wider">
            {title}
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Geographic catchment ranking by aggregate passenger trip volume
          </p>
        </div>
      </div>

      <div className="h-[320px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={displayData}
            layout="vertical"
            margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
          >
            <XAxis
              type="number"
              stroke="#64748B"
              fontSize={11}
              tickLine={false}
              tickFormatter={(v) => `${(v / 1000).toFixed(0)}k`}
            />
            <YAxis
              type="category"
              dataKey="area_name"
              stroke="#94A3B8"
              fontSize={11}
              tickLine={false}
              width={140}
              tickFormatter={(v) => v.length > 20 ? `${v.substring(0, 18)}...` : v}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#0F172A',
                borderColor: '#334155',
                borderRadius: '8px',
                fontSize: '12px',
              }}
              formatter={(value: any, _: any, props: any) => [
                `${Number(value).toLocaleString()} trips (${props.payload.percentage}% share)`,
                'Volume',
              ]}
              labelStyle={{ color: '#F8FAFC', fontWeight: 600 }}
            />
            <Bar dataKey="total_pickups" radius={[0, 4, 4, 0]}>
              {displayData.map((_, index) => (
                <Cell
                  key={`cell-area-${index}`}
                  fill={COLORS[index % COLORS.length]}
                  fillOpacity={0.85}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
