"""
Centralized Mock Data Generator for NYC Taxi Demand Analysis & Passenger Prediction.
All data is deterministically simulated using a fixed seed to represent realistic
temporal (hourly/weekly) and spatial (catchment zone) patterns inspired by NYC TLC trip records.
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
import streamlit as st

DATA_CLASSIFICATION = "Simulated NYC TLC Taxi Telemetry - Phase 1 Mock Data"
DATA_DISCLAIMER = (
    "DISCLAIMER: Simulated mock telemetry generated deterministically "
    "for Phase 1 prototyping (Seed 42). It serves as a benchmark baseline."
)

REAL_DATA_CLASSIFICATION = "Authentic NYC TLC Yellow Taxi Telemetry - March 2016"
REAL_DATA_DISCLAIMER = (
    "GENUINE NYC TLC TELEMETRY: Processed and aggregated from 12,210,952 actual "
    "yellow taxi trip records recorded across New York City during March 2016."
)

# Curated NYC Taxi Zones with realistic spatial attributes
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

# Baseline hourly factors for standard 24-hour cycle
BASE_HOURLY_PATTERN = {
    0: {"weekday": 0.45, "weekend": 0.95},
    1: {"weekday": 0.30, "weekend": 0.85},
    2: {"weekday": 0.20, "weekend": 0.70},
    3: {"weekday": 0.15, "weekend": 0.45},
    4: {"weekday": 0.18, "weekend": 0.28},
    5: {"weekday": 0.32, "weekend": 0.22},
    6: {"weekday": 0.65, "weekend": 0.28},
    7: {"weekday": 0.95, "weekend": 0.38},
    8: {"weekday": 1.35, "weekend": 0.52},
    9: {"weekday": 1.25, "weekend": 0.70},
    10: {"weekday": 1.10, "weekend": 0.88},
    11: {"weekday": 1.12, "weekend": 1.05},
    12: {"weekday": 1.18, "weekend": 1.15},
    13: {"weekday": 1.15, "weekend": 1.20},
    14: {"weekday": 1.22, "weekend": 1.22},
    15: {"weekday": 1.28, "weekend": 1.25},
    16: {"weekday": 1.38, "weekend": 1.22},
    17: {"weekday": 1.55, "weekend": 1.28},
    18: {"weekday": 1.68, "weekend": 1.32},  # Peak weekday evening rush
    19: {"weekday": 1.52, "weekend": 1.38},
    20: {"weekday": 1.35, "weekend": 1.42},
    21: {"weekday": 1.20, "weekend": 1.45},
    22: {"weekday": 0.98, "weekend": 1.38},
    23: {"weekday": 0.72, "weekend": 1.18},
}

# Baseline weekday weights (Monday=0 to Sunday=6)
WEEKDAY_WEIGHTS = {
    0: {"name": "Monday", "short": "Mon", "weight": 0.92, "is_weekend": False},
    1: {"name": "Tuesday", "short": "Tue", "weight": 1.02, "is_weekend": False},
    2: {"name": "Wednesday", "short": "Wed", "weight": 1.08, "is_weekend": False},
    3: {"name": "Thursday", "short": "Thu", "weight": 1.15, "is_weekend": False},
    4: {"name": "Friday", "short": "Fri", "weight": 1.28, "is_weekend": False},
    5: {"name": "Saturday", "short": "Sat", "weight": 1.18, "is_weekend": True},
    6: {"name": "Sunday", "short": "Sun", "weight": 0.87, "is_weekend": True},
}

BASE_ZONE_HOURLY_VOLUME = 380


def generate_mock_dataset(days: int = 28, seed: int = 42) -> pd.DataFrame:
    """
    Generates a deterministic, realistic mock NYC taxi demand dataset.
    Uses fixed random seed 42 to ensure exact reproducibility across runs.
    """
    rng = np.random.RandomState(seed)

    # Anchor date: 4 full weeks ending yesterday
    start_date = datetime(2026, 9, 28, 0, 0, 0)  # A Monday

    records = []

    for day_offset in range(days):
        current_day = start_date + timedelta(days=day_offset)
        date_str = current_day.strftime("%Y-%m-%d")
        day_of_week = current_day.weekday()
        day_meta = WEEKDAY_WEIGHTS[day_of_week]
        is_weekend = day_meta["is_weekend"]
        day_weight = day_meta["weight"]

        for hour in range(24):
            dt_timestamp = current_day.replace(hour=hour)
            hour_factor = (
                BASE_HOURLY_PATTERN[hour]["weekend"]
                if is_weekend
                else BASE_HOURLY_PATTERN[hour]["weekday"]
            )
            formatted_hour = f"{hour:02d}:00"

            for zone in TAXI_ZONES:
                zone_weight = zone["base_weight"]
                is_peak_hour = zone["peak_hour"] == hour
                synergy = 1.22 if is_peak_hour else 1.0

                # Deterministic baseline volume
                base_calc = BASE_ZONE_HOURLY_VOLUME * zone_weight * hour_factor * day_weight * synergy

                # Controlled Gaussian jitter for realism (sd ~ 5% of base), bounded and deterministic
                jitter = rng.normal(loc=0.0, scale=0.05 * base_calc)
                pickups = int(max(10, round(base_calc + jitter)))

                records.append({
                    "timestamp": dt_timestamp,
                    "date": date_str,
                    "date_dt": current_day.date(),
                    "hour": hour,
                    "formatted_hour": formatted_hour,
                    "day_of_week": day_of_week,
                    "day_name": day_meta["name"],
                    "day_short": day_meta["short"],
                    "is_weekend": is_weekend,
                    "day_type": "Weekend" if is_weekend else "Weekday",
                    "area_id": zone["area_id"],
                    "pickup_area": zone["area_name"],
                    "borough": zone["borough"],
                    "zone_type": zone["zone_type"],
                    "pickups": pickups,
                })

    df = pd.DataFrame(records)
    return df


import os


@st.cache_data(show_spinner=False)
def load_mock_dataset() -> pd.DataFrame:
    """Provides the deterministic 28-day simulated baseline dataset."""
    return generate_mock_dataset(days=28, seed=42)


@st.cache_data(show_spinner=False)
def load_real_dataset() -> pd.DataFrame:
    """
    Loads the processed real NYC TLC Yellow Taxi dataset (March 2016).
    Aggregated from 12,210,952 trips across 10 catchment zones.
    Falls back to mock dataset if file is absent.
    """
    parquet_path = "data/real_nyc_taxi_march_2016.parquet"
    if os.path.exists(parquet_path):
        df = pd.read_parquet(parquet_path)
        if "date_dt" not in df.columns or not isinstance(df["date_dt"].iloc[0], (datetime, date)):
            df["date_dt"] = pd.to_datetime(df["date"]).dt.date
        return df

    csv_path = "data/real_nyc_taxi_march_2016.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["date_dt"] = pd.to_datetime(df["date"]).dt.date
        return df

    return generate_mock_dataset(days=28, seed=42)


def load_dataset(source: Optional[str] = None) -> pd.DataFrame:
    """
    Centralized data provider for all pages and components.
    Defaults to Real NYC TLC Telemetry (March 2016) if available,
    or switches according to st.session_state['dataset_source'].
    """
    if source is None:
        try:
            source = st.session_state.get("dataset_source", "real")
        except Exception:
            source = "real"

    if source == "mock":
        return load_mock_dataset()
    return load_real_dataset()


def get_dataset_metadata(source: Optional[str] = None) -> Dict[str, Any]:
    """Returns metadata and disclaimer corresponding to the active dataset."""
    if source is None:
        try:
            source = st.session_state.get("dataset_source", "real")
        except Exception:
            source = "real"

    if source == "mock":
        return {
            "source": "mock",
            "name": "Simulated Benchmark Data (Deterministic Seed 42)",
            "short_name": "Phase 1 Simulation",
            "badge": "PHASE 1 • SEED 42",
            "disclaimer": DATA_DISCLAIMER,
            "is_real": False,
            "trip_count_str": "Deterministic Heuristic",
            "observation_window": "4-Week Diurnal Cycle"
        }
    return {
        "source": "real",
        "name": "NYC TLC Real Yellow Taxi Telemetry (March 2016)",
        "short_name": "NYC TLC Telemetry",
        "badge": "NYC TLC • 12.2M TRIPS",
        "disclaimer": REAL_DATA_DISCLAIMER,
        "is_real": True,
        "trip_count_str": "12,210,952 Records Processed",
        "observation_window": "March 1 – March 31, 2016"
    }


def get_all_areas() -> List[str]:
    """Returns list of all available pickup zone names."""
    return [z["area_name"] for z in TAXI_ZONES]


def get_zone_metadata(area_name: str) -> Optional[Dict[str, Any]]:
    """Returns metadata dictionary for a given zone."""
    for z in TAXI_ZONES:
        if z["area_name"].lower() == area_name.lower():
            return z
    return None
