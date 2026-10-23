import { SummaryData, AreaDataPoint } from './types';

export const FALLBACK_SUMMARY: SummaryData = {
  total_pickups: 618420,
  avg_hourly_pickups: 3681.1,
  peak_demand_hour: 18,
  peak_demand_hour_formatted: "18:00 (6 PM)",
  peak_demand_hour_pickups: 42150,
  busiest_pickup_area: "Midtown Center",
  busiest_pickup_borough: "Manhattan",
  busiest_area_pickups: 94820,
  busiest_area_percentage: 15.3,
  total_monitored_zones: 10,
  sample_date_range: "Representative 7-Day NYC Transit Cycle (Simulated)",
  data_classification: "Simulated NYC TLC Taxi Telemetry - Phase 1 Mock Data"
};

export const NYC_TAXI_ZONES = [
  "Midtown Center",
  "JFK International Airport",
  "Financial District",
  "Times Square / Theater District",
  "Upper East Side",
  "Upper West Side",
  "East Village / Lower East Side",
  "LaGuardia Airport",
  "Williamsburg",
  "Astoria"
];

export const FALLBACK_AREAS: AreaDataPoint[] = [
  { area_id: "NYC-001", area_name: "Midtown Center", borough: "Manhattan", total_pickups: 94820, percentage: 15.3, avg_hourly_pickups: 564.4, peak_hour: 18, peak_hour_formatted: "18:00 (6 PM)", zone_type: "Commercial & Transit" },
  { area_id: "NYC-004", area_name: "Times Square / Theater District", borough: "Manhattan", total_pickups: 87210, percentage: 14.1, avg_hourly_pickups: 519.1, peak_hour: 21, peak_hour_formatted: "21:00 (9 PM)", zone_type: "Entertainment & Tourism" },
  { area_id: "NYC-002", area_name: "JFK International Airport", borough: "Queens", total_pickups: 72050, percentage: 11.7, avg_hourly_pickups: 428.9, peak_hour: 16, peak_hour_formatted: "16:00 (4 PM)", zone_type: "Airport & Transit" },
  { area_id: "NYC-005", area_name: "Upper East Side", borough: "Manhattan", total_pickups: 69780, percentage: 11.3, avg_hourly_pickups: 415.4, peak_hour: 8, peak_hour_formatted: "08:00 (8 AM)", zone_type: "Residential / Medical" },
  { area_id: "NYC-003", area_name: "Financial District", borough: "Manhattan", total_pickups: 66720, percentage: 10.8, avg_hourly_pickups: 397.1, peak_hour: 17, peak_hour_formatted: "17:00 (5 PM)", zone_type: "Commercial / Financial" },
  { area_id: "NYC-006", area_name: "Upper West Side", borough: "Manhattan", total_pickups: 64450, percentage: 10.4, avg_hourly_pickups: 383.6, peak_hour: 9, peak_hour_formatted: "09:00 (9 AM)", zone_type: "Residential / Cultural" },
  { area_id: "NYC-007", area_name: "East Village / Lower East Side", borough: "Manhattan", total_pickups: 62190, percentage: 10.1, avg_hourly_pickups: 370.2, peak_hour: 23, peak_hour_formatted: "23:00 (11 PM)", zone_type: "Dining & Nightlife" },
  { area_id: "NYC-008", area_name: "LaGuardia Airport", borough: "Queens", total_pickups: 60670, percentage: 9.8, avg_hourly_pickups: 361.1, peak_hour: 17, peak_hour_formatted: "17:00 (5 PM)", zone_type: "Airport & Transit" },
  { area_id: "NYC-009", area_name: "Williamsburg", borough: "Brooklyn", total_pickups: 49280, percentage: 8.0, avg_hourly_pickups: 293.3, peak_hour: 22, peak_hour_formatted: "22:00 (10 PM)", zone_type: "Mixed Residential & Nightlife" },
  { area_id: "NYC-010", area_name: "Astoria", borough: "Queens", total_pickups: 39430, percentage: 6.4, avg_hourly_pickups: 234.7, peak_hour: 8, peak_hour_formatted: "08:00 (8 AM)", zone_type: "Residential & Dining" },
];
