"""
Realistic Mock NYC Taxi Demand Dataset for Phase 1.
All data is simulated based on real NYC TLC (Taxi & Limousine Commission)
yellow & green taxi trip patterns and geographic catchment zones.
"""
from typing import Dict, List, Any

# Curated NYC Taxi Zones with characteristics
TAXI_ZONES: List[Dict[str, Any]] = [
    {
        "area_id": "NYC-001",
        "area_name": "Midtown Center",
        "borough": "Manhattan",
        "zone_type": "Commercial & Transit",
        "base_weight": 1.25,
        "peak_hour": 18,
        "description": "High density corporate, retail, and Grand Central commuter corridor."
    },
    {
        "area_id": "NYC-002",
        "area_name": "JFK International Airport",
        "borough": "Queens",
        "zone_type": "Airport & Transit",
        "base_weight": 0.95,
        "peak_hour": 16,
        "description": "Major international hub with steady flight arrivals and long-distance transfers."
    },
    {
        "area_id": "NYC-003",
        "area_name": "Financial District",
        "borough": "Manhattan",
        "zone_type": "Commercial / Financial",
        "base_weight": 0.88,
        "peak_hour": 17,
        "description": "Wall Street and Lower Manhattan commuter corridor with steep weekday rush spikes."
    },
    {
        "area_id": "NYC-004",
        "area_name": "Times Square / Theater District",
        "borough": "Manhattan",
        "zone_type": "Entertainment & Tourism",
        "base_weight": 1.15,
        "peak_hour": 21,
        "description": "World-famous theater and tourist hotspot with heavy evening and late-night demand."
    },
    {
        "area_id": "NYC-005",
        "area_name": "Upper East Side",
        "borough": "Manhattan",
        "zone_type": "Residential / Medical",
        "base_weight": 0.92,
        "peak_hour": 8,
        "description": "High residential density generating consistent morning outbound commute."
    },
    {
        "area_id": "NYC-006",
        "area_name": "Upper West Side",
        "borough": "Manhattan",
        "zone_type": "Residential / Cultural",
        "base_weight": 0.85,
        "peak_hour": 9,
        "description": "Residential corridor near Lincoln Center and Central Park."
    },
    {
        "area_id": "NYC-007",
        "area_name": "East Village / Lower East Side",
        "borough": "Manhattan",
        "zone_type": "Dining & Nightlife",
        "base_weight": 0.82,
        "peak_hour": 23,
        "description": "Vibrant hospitality and nightlife district surging on Thursday-Saturday evenings."
    },
    {
        "area_id": "NYC-008",
        "area_name": "LaGuardia Airport",
        "borough": "Queens",
        "zone_type": "Airport & Transit",
        "base_weight": 0.80,
        "peak_hour": 17,
        "description": "Key domestic gateway serving business and regional travelers."
    },
    {
        "area_id": "NYC-009",
        "area_name": "Williamsburg",
        "borough": "Brooklyn",
        "zone_type": "Mixed Residential & Nightlife",
        "base_weight": 0.65,
        "peak_hour": 22,
        "description": "Inter-borough transit hotspot with heavy cross-river weekend traffic."
    },
    {
        "area_id": "NYC-010",
        "area_name": "Astoria",
        "borough": "Queens",
        "zone_type": "Residential & Dining",
        "base_weight": 0.52,
        "peak_hour": 8,
        "description": "Fast-growing outer borough residential corridor with morning Manhattan transit."
    }
]

# Base hourly distribution curve representing typical 24-hour cycle (hourly index 0-23)
# Based on typical NYC TLC yellow taxi pickup curve
BASE_HOURLY_PATTERN: List[Dict[str, float]] = [
    {"hour": 0, "weekday_factor": 0.45, "weekend_factor": 0.95},
    {"hour": 1, "weekday_factor": 0.30, "weekend_factor": 0.85},
    {"hour": 2, "weekday_factor": 0.20, "weekend_factor": 0.70},
    {"hour": 3, "weekday_factor": 0.15, "weekend_factor": 0.45},
    {"hour": 4, "weekday_factor": 0.18, "weekend_factor": 0.28},
    {"hour": 5, "weekday_factor": 0.32, "weekend_factor": 0.22},
    {"hour": 6, "weekday_factor": 0.65, "weekend_factor": 0.28},
    {"hour": 7, "weekday_factor": 0.95, "weekend_factor": 0.38},
    {"hour": 8, "weekday_factor": 1.35, "weekend_factor": 0.52},
    {"hour": 9, "weekday_factor": 1.25, "weekend_factor": 0.70},
    {"hour": 10, "weekday_factor": 1.10, "weekend_factor": 0.88},
    {"hour": 11, "weekday_factor": 1.12, "weekend_factor": 1.05},
    {"hour": 12, "weekday_factor": 1.18, "weekend_factor": 1.15},
    {"hour": 13, "weekday_factor": 1.15, "weekend_factor": 1.20},
    {"hour": 14, "weekday_factor": 1.22, "weekend_factor": 1.22},
    {"hour": 15, "weekday_factor": 1.28, "weekend_factor": 1.25},
    {"hour": 16, "weekday_factor": 1.38, "weekend_factor": 1.22},
    {"hour": 17, "weekday_factor": 1.55, "weekend_factor": 1.28},
    {"hour": 18, "weekday_factor": 1.68, "weekend_factor": 1.32}, # Peak weekday demand
    {"hour": 19, "weekday_factor": 1.52, "weekend_factor": 1.38},
    {"hour": 20, "weekday_factor": 1.35, "weekend_factor": 1.42},
    {"hour": 21, "weekday_factor": 1.20, "weekend_factor": 1.45},
    {"hour": 22, "weekday_factor": 0.98, "weekend_factor": 1.38},
    {"hour": 23, "weekday_factor": 0.72, "weekend_factor": 1.18},
]

# Baseline weekly distribution factors (Monday=0 to Sunday=6)
WEEKDAY_PATTERNS = [
    {"day_index": 0, "day_name": "Monday", "short_name": "Mon", "weight": 0.92},
    {"day_index": 1, "day_name": "Tuesday", "short_name": "Tue", "weight": 1.02},
    {"day_index": 2, "day_name": "Wednesday", "short_name": "Wed", "weight": 1.08},
    {"day_index": 3, "day_name": "Thursday", "short_name": "Thu", "weight": 1.15},
    {"day_index": 4, "day_name": "Friday", "short_name": "Fri", "weight": 1.28},
    {"day_index": 5, "day_name": "Saturday", "short_name": "Sat", "weight": 1.18},
    {"day_index": 6, "day_name": "Sunday", "short_name": "Sun", "weight": 0.87},
]

# Base multiplier to produce realistic aggregate volume for simulated period
BASE_ZONE_HOURLY_VOLUME = 380

def get_zone_by_name(name: str):
    name_clean = name.strip().lower()
    for z in TAXI_ZONES:
        if z["area_name"].lower() == name_clean or z["area_id"].lower() == name_clean:
            return z
    # Check partial match
    for z in TAXI_ZONES:
        if name_clean in z["area_name"].lower():
            return z
    return None
