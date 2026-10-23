import React from 'react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
  ReferenceDot,
  ReferenceLine
} from 'recharts';
import { HourlyCurvePoint } from '../../api/types';

interface PredictionComparisonChartProps {
  data: HourlyCurvePoint[];
  targetHour: number;
  predictedValue: number;
  historicalValue: number;
}

export const PredictionComparisonChart: React.FC<PredictionComparisonChartProps> = ({
  data,
  targetHour,
  predictedValue,
  historicalValue,
}) => {
  const targetPoint = data.find((p) => p.hour === targetHour) || {
    hour: targetHour,
    formatted_hour: `${targetHour}:00`,
    predicted_volume: predictedValue,
    historical_baseline: historicalValue,
    is_target_hour: true,
  };

  return (
    <div className="bg-[#111827] rounded-xl p-5 border border-slate-800 shadow-sm">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-100 uppercase tracking-wider flex items-center gap-2">
            <span>24-Hour Baseline vs Simulated Prediction</span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/30">
              Target: {targetHour}:00
            </span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Hourly demand curve comparison with target prediction interval
          </p>
        </div>
      </div>

      <div className="h-[300px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 15, right: 20, left: -15, bottom: 0 }}>
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
              }}
              labelStyle={{ color: '#F8FAFC', fontWeight: 600, marginBottom: '4px' }}
              formatter={(value: any, name: any) => [
                `${Number(value).toLocaleString()} pickups`,
                name,
              ]}
            />
            <Legend
              wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }}
              iconType="circle"
            />

            {/* Target Hour reference line */}
            <ReferenceLine
              x={targetPoint.formatted_hour}
              stroke="#F59E0B"
              strokeDasharray="3 3"
              label={{
                value: 'Selected Window',
                position: 'top',
                fill: '#F59E0B',
                fontSize: 10,
                fontFamily: 'monospace',
              }}
            />

            {/* Historical Average line */}
            <Line
              type="monotone"
              dataKey="historical_baseline"
              name="Historical 7-Day Average"
              stroke="#64748B"
              strokeWidth={2}
              strokeDasharray="4 4"
              dot={false}
            />

            {/* Predicted volume line */}
            <Line
              type="monotone"
              dataKey="predicted_volume"
              name="Simulated Scenario Forecast"
              stroke="#F59E0B"
              strokeWidth={2.5}
              dot={{ r: 2, fill: '#F59E0B' }}
              activeDot={{ r: 6 }}
            />

            {/* Prominent highlight on target hour predicted point */}
            <ReferenceDot
              x={targetPoint.formatted_hour}
              y={targetPoint.predicted_volume}
              r={7}
              fill="#F59E0B"
              stroke="#FFFFFF"
              strokeWidth={2}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
