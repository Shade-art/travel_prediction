import React, { useState, useEffect } from 'react';
import { Sparkles, ShieldCheck } from 'lucide-react';
import { api } from '../api/endpoints';
import { PredictionRequest, PredictionResponse } from '../api/types';
import { NYC_TAXI_ZONES } from '../api/mockData';
import { PredictionForm } from '../components/prediction/PredictionForm';
import { PredictionResultCard } from '../components/prediction/PredictionResultCard';
import { PredictionComparisonChart } from '../components/charts/PredictionComparisonChart';
import { LoadingState } from '../components/common/LoadingState';
import { ErrorState } from '../components/common/ErrorState';

export const PredictionPage: React.FC = () => {
  const todayStr = new Date().toISOString().split('T')[0];

  const [prediction, setPrediction] = useState<PredictionResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Initial prediction on page mount to provide immediate value
  const runPrediction = async (params: PredictionRequest) => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.predictDemand(params);
      setPrediction(res);
    } catch (err: any) {
      setError(err.message || 'Failed to generate demand prediction');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runPrediction({
      pickup_area: NYC_TAXI_ZONES[0], // Midtown Center
      date: todayStr,
      hour: 18, // Peak evening rush
    });
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Page Header with Phase 1 Prominent Notice */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Passenger Demand Prediction
            </h1>
            <span className="text-xs font-mono px-2 py-0.5 rounded bg-amber-500/15 text-amber-300 border border-amber-500/30">
              Phase 1 Mock Engine
            </span>
          </div>
          <p className="mt-1 text-sm text-slate-400">
            Heuristic simulation model estimating NYC taxi pickup volume by catchment zone and time interval
          </p>
        </div>

        {/* Phase 1 Prototype badge */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs text-slate-400">
          <ShieldCheck className="w-4 h-4 text-amber-400" />
          <span>Interface ready for Scikit-Learn ML in Phase 2</span>
        </div>
      </div>

      {/* Main Grid: Form on Left, Results on Right */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column: Input Form (4 cols) */}
        <div className="lg:col-span-5 space-y-4">
          <PredictionForm
            onSubmit={runPrediction}
            isLoading={loading}
            initialValues={{
              pickup_area: NYC_TAXI_ZONES[0],
              date: todayStr,
              hour: 18,
            }}
          />

          {/* Architecture note for project evaluation */}
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-400 space-y-2">
            <span className="font-semibold text-slate-200 block uppercase tracking-wider text-[11px] font-mono">
              Phase 1 ML Architecture Compliance:
            </span>
            <p>
              • Predictions are calculated by an isolated <code>MockPredictionService</code> behind a standardized <code>BasePredictionService</code> abstract interface.
            </p>
            <p>
              • In Phase 2, a trained scikit-learn regression/XGBoost model will be injected into this service interface with zero changes to frontend contracts.
            </p>
          </div>
        </div>

        {/* Right Column: Prediction Results & Comparison (7 cols) */}
        <div className="lg:col-span-7 space-y-6">
          {loading ? (
            <LoadingState
              message="Simulating passenger demand profile..."
              subMessage="Evaluating zone weight, diurnal curve, and calendar factors"
            />
          ) : error ? (
            <ErrorState
              title="Prediction Calculation Failed"
              message={error}
              onRetry={() =>
                runPrediction({
                  pickup_area: NYC_TAXI_ZONES[0],
                  date: todayStr,
                  hour: 18,
                })
              }
            />
          ) : prediction ? (
            <>
              {/* Prediction Result KPI Card */}
              <PredictionResultCard prediction={prediction} />

              {/* Historical Demand vs Prediction Chart */}
              <PredictionComparisonChart
                data={prediction.hourly_curve}
                targetHour={prediction.hour}
                predictedValue={prediction.predicted_pickups}
                historicalValue={prediction.historical_average}
              />
            </>
          ) : (
            <div className="p-8 rounded-xl bg-slate-900/40 border border-slate-800 text-center">
              <Sparkles className="w-8 h-8 text-amber-400 mx-auto mb-2 opacity-50" />
              <p className="text-sm text-slate-300 font-medium">
                Select your parameters and click "Predict Demand" to view forecast
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
