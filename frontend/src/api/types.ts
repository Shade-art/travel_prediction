export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  phase: string;
  mock_data_loaded: boolean;
}

export interface SummaryData {
  total_pickups: number;
  avg_hourly_pickups: number;
  peak_demand_hour: number;
  peak_demand_hour_formatted: string;
  peak_demand_hour_pickups: number;
  busiest_pickup_area: string;
  busiest_pickup_borough: string;
  busiest_area_pickups: number;
  busiest_area_percentage: number;
  total_monitored_zones: number;
  sample_date_range: string;
  data_classification: string;
}

export interface HourlyDataPoint {
  hour: number;
  formatted_hour: string;
  pickups: number;
  weekday_pickups: number;
  weekend_pickups: number;
  is_peak: boolean;
}

export interface HourlyAnalyticsResponse {
  filter_area?: string;
  filter_weekday?: string;
  total_pickups: number;
  data: HourlyDataPoint[];
}

export interface AreaDataPoint {
  area_id: string;
  area_name: string;
  borough: string;
  total_pickups: number;
  percentage: number;
  avg_hourly_pickups: number;
  peak_hour: number;
  peak_hour_formatted: string;
  zone_type: string;
}

export interface AreaAnalyticsResponse {
  total_areas: number;
  total_pickups: number;
  disclaimer: string;
  data: AreaDataPoint[];
}

export interface WeekdayDataPoint {
  day_index: number;
  day_name: string;
  short_name: string;
  total_pickups: number;
  daily_average: number;
  percentage: number;
}

export interface HeatmapCell {
  day_index: number;
  day_name: string;
  hour: number;
  formatted_hour: string;
  pickups: number;
  intensity: number; // 0 - 100
}

export interface WeeklyAnalyticsResponse {
  filter_area?: string;
  weekday_distribution: WeekdayDataPoint[];
  heatmap: HeatmapCell[];
}

export interface PredictionRequest {
  pickup_area: string;
  date: string; // YYYY-MM-DD
  hour: number; // 0 - 23
}

export interface HourlyCurvePoint {
  hour: number;
  formatted_hour: string;
  historical_baseline: number;
  predicted_volume: number;
  is_target_hour: boolean;
}

export interface PredictionResponse {
  pickup_area: string;
  date: string;
  hour: number;
  formatted_hour: string;
  day_name: string;
  is_weekend: boolean;
  predicted_pickups: number;
  historical_average: number;
  difference_percentage: number;
  demand_level: 'Low' | 'Moderate' | 'High' | 'Peak Surge' | string;
  confidence_score: number;
  key_drivers: string[];
  hourly_curve: HourlyCurvePoint[];
  is_mock: boolean;
  disclaimer: string;
}
