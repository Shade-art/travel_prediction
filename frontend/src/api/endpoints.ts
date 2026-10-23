import { apiClient } from './client';
import {
  HealthResponse,
  SummaryData,
  HourlyAnalyticsResponse,
  AreaAnalyticsResponse,
  WeeklyAnalyticsResponse,
  PredictionRequest,
  PredictionResponse
} from './types';

export const api = {
  getHealth: () => apiClient<HealthResponse>('/health'),

  getSummary: () => apiClient<SummaryData>('/summary'),

  getHourlyAnalytics: (area?: string) => {
    const query = area && area !== 'all' ? `?area=${encodeURIComponent(area)}` : '';
    return apiClient<HourlyAnalyticsResponse>(`/analytics/hourly${query}`);
  },

  getAreaAnalytics: () => apiClient<AreaAnalyticsResponse>('/analytics/areas'),

  getWeeklyAnalytics: (area?: string) => {
    const query = area && area !== 'all' ? `?area=${encodeURIComponent(area)}` : '';
    return apiClient<WeeklyAnalyticsResponse>(`/analytics/weekly${query}`);
  },

  predictDemand: (payload: PredictionRequest) =>
    apiClient<PredictionResponse>('/predict', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
};
