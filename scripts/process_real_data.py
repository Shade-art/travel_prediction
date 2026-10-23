"""
ETL and Model Training Pipeline for Real NYC TLC Yellow Taxi Dataset.
Processes raw 'yellow_tripdata_2016-03.csv' (12.2M records) into:
1. Clean, hourly-aggregated dataset: 'data/real_nyc_taxi_march_2016.parquet' and '.csv'
2. Trained Scikit-Learn Gradient Boosting Pipeline: 'models/nyc_taxi_demand_pipeline.joblib'
3. Model evaluation benchmarks and metadata: 'models/model_metrics.json'
"""

import time
import json
import os
from datetime import datetime
import numpy as np
import pandas as pd
import pyarrow.csv as pv
import joblib
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# Define 10 NYC Taxi Catchment Zones with Geographic Bounding Boxes
TAXI_ZONE_CONFIGS = {
    "Midtown Center": {
        "area_id": "NYC-001",
        "borough": "Manhattan",
        "zone_type": "Commercial & Transit",
        "lat": (40.748, 40.765),
        "lon": (-73.988, -73.968)
    },
    "JFK International Airport": {
        "area_id": "NYC-002",
        "borough": "Queens",
        "zone_type": "Airport & Transit",
        "lat": (40.635, 40.665),
        "lon": (-73.805, -73.765)
    },
    "Financial District": {
        "area_id": "NYC-003",
        "borough": "Manhattan",
        "zone_type": "Commercial / Financial",
        "lat": (40.700, 40.718),
        "lon": (-74.018, -74.002)
    },
    "Times Square / Theater District": {
        "area_id": "NYC-004",
        "borough": "Manhattan",
        "zone_type": "Entertainment & Tourism",
        "lat": (40.753, 40.766),
        "lon": (-73.995, -73.981)
    },
    "Upper East Side": {
        "area_id": "NYC-005",
        "borough": "Manhattan",
        "zone_type": "Residential / Medical",
        "lat": (40.765, 40.785),
        "lon": (-73.965, -73.948)
    },
    "Upper West Side": {
        "area_id": "NYC-006",
        "borough": "Manhattan",
        "zone_type": "Residential / Cultural",
        "lat": (40.775, 40.800),
        "lon": (-73.985, -73.965)
    },
    "East Village / Lower East Side": {
        "area_id": "NYC-007",
        "borough": "Manhattan",
        "zone_type": "Dining & Nightlife",
        "lat": (40.718, 40.732),
        "lon": (-73.992, -73.975)
    },
    "LaGuardia Airport": {
        "area_id": "NYC-008",
        "borough": "Queens",
        "zone_type": "Airport & Transit",
        "lat": (40.765, 40.785),
        "lon": (-73.885, -73.860)
    },
    "Williamsburg": {
        "area_id": "NYC-009",
        "borough": "Brooklyn",
        "zone_type": "Mixed Residential & Nightlife",
        "lat": (40.705, 40.725),
        "lon": (-73.968, -73.945)
    },
    "Astoria": {
        "area_id": "NYC-010",
        "borough": "Queens",
        "zone_type": "Residential & Dining",
        "lat": (40.755, 40.778),
        "lon": (-73.935, -73.910)
    }
}

WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
WEEKDAY_SHORTS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def run_etl_and_training(raw_csv_path: str = "yellow_tripdata_2016-03.csv"):
    if not os.path.exists(raw_csv_path):
        raise FileNotFoundError(f"Raw dataset file not found at: {raw_csv_path}")

    print(f"🚀 [1/4] Reading raw NYC taxi dataset: {raw_csv_path}...")
    t0 = time.time()
    
    # Read only required columns using PyArrow C++ multi-threaded reader
    convert_options = pv.ConvertOptions(
        include_columns=["tpep_pickup_datetime", "pickup_longitude", "pickup_latitude"]
    )
    table = pv.read_csv(raw_csv_path, convert_options=convert_options)
    raw_row_count = table.num_rows
    print(f"   ✓ Read {raw_row_count:,} raw taxi trip records in {time.time() - t0:.2f}s.")

    # Convert to Pandas
    t1 = time.time()
    df_raw = table.to_pandas()
    print(f"   ✓ Converted Arrow table to Pandas in {time.time() - t1:.2f}s.")

    # Filter out missing or invalid NYC coordinates
    print("🧹 [2/4] Filtering valid NYC spatial coordinates and mapping zones...")
    df_clean = df_raw.dropna(subset=["tpep_pickup_datetime", "pickup_longitude", "pickup_latitude"])
    df_clean = df_clean[
        (df_clean["pickup_latitude"] >= 40.5) & (df_clean["pickup_latitude"] <= 41.0) &
        (df_clean["pickup_longitude"] >= -74.3) & (df_clean["pickup_longitude"] <= -73.6)
    ]
    df_clean["timestamp"] = pd.to_datetime(df_clean["tpep_pickup_datetime"]).dt.floor("h")

    # Aggregate by zone and hourly timestamp
    zone_aggregates = []
    for zone_name, conf in TAXI_ZONE_CONFIGS.items():
        in_zone = (
            (df_clean["pickup_latitude"] >= conf["lat"][0]) & (df_clean["pickup_latitude"] <= conf["lat"][1]) &
            (df_clean["pickup_longitude"] >= conf["lon"][0]) & (df_clean["pickup_longitude"] <= conf["lon"][1])
        )
        zone_trips = df_clean[in_zone]
        agg = zone_trips.groupby("timestamp").size().reset_index(name="pickups")
        agg["pickup_area"] = zone_name
        agg["area_id"] = conf["area_id"]
        agg["borough"] = conf["borough"]
        agg["zone_type"] = conf["zone_type"]
        zone_aggregates.append(agg)

    df_agg = pd.concat(zone_aggregates, ignore_index=True)

    # Build complete time grid for March 1 to March 31, 2016 (744 hours x 10 zones = 7,440 rows)
    date_range = pd.date_range("2016-03-01 00:00:00", "2016-03-31 23:00:00", freq="h")
    grid = pd.MultiIndex.from_product(
        [date_range, list(TAXI_ZONE_CONFIGS.keys())],
        names=["timestamp", "pickup_area"]
    ).to_frame().reset_index(drop=True)

    # Merge aggregated data onto complete grid
    full_df = pd.merge(grid, df_agg, on=["timestamp", "pickup_area"], how="left")
    
    # Fill metadata and 0 pickups for empty hours
    for zone_name, conf in TAXI_ZONE_CONFIGS.items():
        mask = full_df["pickup_area"] == zone_name
        full_df.loc[mask, "area_id"] = conf["area_id"]
        full_df.loc[mask, "borough"] = conf["borough"]
        full_df.loc[mask, "zone_type"] = conf["zone_type"]

    full_df["pickups"] = full_df["pickups"].fillna(0).astype(int)

    # Generate all standardized schema fields matching mock_data.py
    full_df["date"] = full_df["timestamp"].dt.strftime("%Y-%m-%d")
    full_df["date_dt"] = full_df["timestamp"].dt.date
    full_df["hour"] = full_df["timestamp"].dt.hour
    full_df["formatted_hour"] = full_df["hour"].apply(lambda h: f"{h:02d}:00")
    full_df["day_of_week"] = full_df["timestamp"].dt.day_of_week
    full_df["day_name"] = full_df["day_of_week"].apply(lambda d: WEEKDAY_NAMES[d])
    full_df["day_short"] = full_df["day_of_week"].apply(lambda d: WEEKDAY_SHORTS[d])
    full_df["is_weekend"] = full_df["day_of_week"].isin([5, 6])
    full_df["day_type"] = np.where(full_df["is_weekend"], "Weekend", "Weekday")

    # Sort deterministically
    full_df = full_df.sort_values(by=["timestamp", "area_id"]).reset_index(drop=True)

    # Save to data directory
    os.makedirs("data", exist_ok=True)
    parquet_path = "data/real_nyc_taxi_march_2016.parquet"
    csv_path = "data/real_nyc_taxi_march_2016.csv"
    full_df.to_parquet(parquet_path, index=False)
    full_df.to_csv(csv_path, index=False)

    total_pickups = full_df["pickups"].sum()
    print(f"   ✓ Aggregated {total_pickups:,} pickups across {len(full_df):,} hourly zone buckets.")
    print(f"   ✓ Saved clean dataset to:\n     - {parquet_path}\n     - {csv_path}")

    # Train Scikit-Learn Model Pipeline
    print("🧠 [3/4] Training Scikit-Learn HistGradientBoostingRegressor Pipeline...")
    os.makedirs("models", exist_ok=True)

    # Feature engineering for ML model
    X = full_df[["pickup_area", "hour", "day_of_week", "is_weekend"]].copy()
    X["is_weekend"] = X["is_weekend"].astype(int)
    y = full_df["pickups"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(drop="first", sparse_output=False), ["pickup_area"])
        ],
        remainder="passthrough"
    )

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", HistGradientBoostingRegressor(
            max_iter=300,
            learning_rate=0.08,
            max_leaf_nodes=31,
            random_state=42
        ))
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    r2 = float(r2_score(y_test, y_pred))
    mae = float(mean_absolute_error(y_test, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))

    print(f"   ✓ Model Training Complete:")
    print(f"     - R² Score: {r2:.4f}")
    print(f"     - MAE: {mae:.2f} pickups")
    print(f"     - RMSE: {rmse:.2f} pickups")

    model_path = "models/nyc_taxi_demand_pipeline.joblib"
    joblib.dump(pipeline, model_path)
    print(f"   ✓ Serialized pipeline to {model_path}")

    # Save metrics metadata
    metrics_path = "models/model_metrics.json"
    metrics_data = {
        "model_architecture": "HistGradientBoostingRegressor (scikit-learn)",
        "pipeline_stages": ["OneHotEncoder", "HistGradientBoostingRegressor"],
        "training_source": "NYC TLC Yellow Taxi Trip Telemetry (March 2016)",
        "raw_record_count": int(raw_row_count),
        "total_zone_pickups": int(total_pickups),
        "hourly_zone_samples": int(len(full_df)),
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
        "metrics": {
            "r2_score": round(r2, 4),
            "mae": round(mae, 2),
            "rmse": round(rmse, 2)
        },
        "features": ["pickup_area", "hour", "day_of_week", "is_weekend"],
        "target": "pickups",
        "generated_at": datetime.now().isoformat()
    }
    with open(metrics_path, "w") as f:
        json.dump(metrics_data, f, indent=2)
    print(f"   ✓ Saved model metrics to {metrics_path}")

    print("✨ [4/4] Pipeline execution succeeded!")
    return full_df, pipeline, metrics_data


if __name__ == "__main__":
    run_etl_and_training()
