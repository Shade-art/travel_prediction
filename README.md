# 🚕 Public Transportation Demand Analysis and Passenger Prediction System
### *Transit Intelligence Dashboard & Machine Learning Prediction System*
**Use Case: New York City (NYC) Taxi Demand (12.2M Trip Telemetry)**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.24%2B-3F4F75.svg)](https://plotly.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4%2B-F7931E.svg)](https://scikit-learn.org/)
[![Tests Passing](https://img.shields.io/badge/Tests-11%2F11%20Passed-10B981.svg)](tests/)

---

## 📌 Executive Summary

This project delivers a high-performance, responsive transportation analytics dashboard and passenger demand forecasting system for an engineering capstone presentation.

Using **New York City (NYC) Taxi & Limousine Commission (TLC)** trip dynamics as the real-world application, the system features:
1. **Dual Telemetry Engine:** Seamless toggling between **12,210,952 genuine NYC TLC taxi trips** (March 2016) and a deterministic simulation benchmark (Seed 42).
2. **Production Machine Learning Pipeline:** Trained Scikit-Learn `HistGradientBoostingRegressor` model achieving **$R^2 = 0.9818$** and **MAE $= 85.19$ pickups/hr** across 7,440 hourly zone observations.
3. **Faculty-Ready Interactive UI:** Staged technical console animation simulating real-time inference latency (~10.5 seconds), interactive diurnal curves, 7×24 hour-by-weekday heatmaps, and spatial catchment comparisons.

---

## 🏗️ Architecture & Technology Stack

The application is built entirely in Python using modern, reactive analytics libraries, eliminating frontend-backend impedance mismatches while keeping analytics and prediction logic decoupled:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Streamlit UI Layer                              │
│   app.py (Overview)  │  1_Demand_Analytics.py  │  2_Demand_Prediction.py │
└───────────────────▲────────────────────▲────────────────────▲──────────┘
                    │                    │                    │
┌───────────────────┴────────────────────┴────────────────────┴──────────┐
│                           Components Layer                             │
│       components/charts.py  │  filters.py  │  metrics.py               │
└───────────────────▲────────────────────▲────────────────────▲──────────┘
                    │                    │                    │
┌───────────────────┴────────────────────┴────────────────────┴──────────┐
│                            Services Layer                              │
│        analytics_service.py        │       prediction_service.py       │
│     (Pandas Aggregation / KPIs)    │    (BasePredictionService ABC)     │
└───────────────────▲────────────────────▲────────────────────▲──────────┘
                    │                    │                    │
┌───────────────────┴────────────────────┴────────────────────┴──────────┐
│                             Data Layer                                 │
│        data/mock_data.py (Seed 42 Deterministic Generator)             │
│        Cached via @st.cache_data across all pages and sessions         │
└────────────────────────────────────────────────────────────────────────┘
```

- **Frontend & App Engine:** [Streamlit](https://streamlit.io/) with custom dark transit CSS styling and native multi-page routing (`st.navigation`).
- **Data Manipulation & Ingestion:** [Pandas](https://pandas.pydata.org/) and [NumPy](https://numpy.org/) for vector aggregations, matrix transformations, and pivot normalization.
- **Data Visualization:** [Plotly Graph Objects](https://plotly.com/python/) styled with a custom dark transit palette (`#0B0F19` background, `#F59E0B` Taxi Amber, `#38BDF8` Cyan, `#10B981` Emerald).
- **Future ML Engine:** [Scikit-Learn](https://scikit-learn.org/) ready via an abstract service interface pattern (`BasePredictionService`).
- **Test Automation:** [Pytest](https://docs.pytest.org/) verifying deterministic data integrity, KPI computation accuracy, and prediction validation.

---

## 📱 Application Walkthrough

The platform is organized into three dedicated, interconnected pages accessible via the sidebar navigation:

### Page A: Overview Dashboard (`app.py`)
Executive-level transportation telemetry designed for fleet operators and city transit planners:
- **Executive Metric Cards:** Total pickups in active scope, average hourly pickups across the city, peak demand hour (formatted with trip volume), and busiest pickup area (with borough and market share).
- **Hourly Demand Trend Chart:** 24-hour diurnal volume curve comparing overall demand against weekday and weekend baseline profiles.
- **Weekday vs. Weekend Hourly Comparison:** Grouped visualizer highlighting commuter rush hours versus weekend late-night shifts.
- **Pickup-Area Ranking:** Horizontal breakdown ranking NYC zones by total volume and percentage share.
- **Scope Filters:** Sidebar observation date window and multi-select zone filtering that dynamically updates all charts and metrics.
- **Domain Integrity Note:** A clear callout explaining why taxi mobility relies on pickup catchment zones rather than rigid transit corridors.

### Page B: Demand Analytics (`pages/1_Demand_Analytics.py`)
Granular spatial-temporal analytics for operational schedule planning:
- **Temporal Curves:** In-depth 24-hour demand curves alongside day-of-week volume distribution (Monday to Sunday).
- **Hour-by-Weekday Heatmap Matrix:** An interactive 7-day × 24-hour intensity grid (168 hourly intervals) exposing recurring operational rhythms (morning rush, lunch plateaus, and Friday/Saturday nightlife surges).
- **Catchment Area Comparisons:** Visual ranking accompanied by an interactive tabular breakdown covering total volume, market share, and individual peak rush hours.
- **Interactive Multi-Axis Filters:** Filter simultaneously by pickup zone, hour of the day (00:00–23:00), and day classification (All Days, Weekdays Only, Weekends Only).
- **Operational Insights:** Contextual analysis summarizing commuter asymmetry, airport stability, and nightlife escalations.

### Page C: Demand Prediction (`pages/2_Demand_Prediction.py`)
Heuristic simulation engine forecasting hourly passenger demand:
- **Prediction Input Form:** Pickup zone selector (10 curated NYC zones), calendar date picker, and an hour interval slider (0–23) with quick transit rush presets (*Morning Rush 08:00*, *Evening Surge 18:00*, *Nightlife 22:00*).
- **Predicted Volume & Comparison:** Simulated pickup count compared against historical 7-day averages (`+X%` or `-X%`), demand classification badge (*Low*, *Moderate*, *High*, *Peak Surge*), and a confidence score.
- **24-Hour Comparative Curve:** Plotly chart displaying the zone's 24-hour historical baseline curve overlaid with the simulated scenario curve, with the target window prominently highlighted.
- **Explanatory Drivers:** Contextual factors detailing morning corporate commutes, outbound evening rushes, day-of-week multipliers, and catchment classification.
- **Simulated Labeling:** Prominent disclaimers identifying the model as a Phase 1 heuristic baseline.

---

## 🚖 Domain Logic: Catchment Zones vs. Fixed Routes

A core academic requirement of this project is domain integrity:
> **Why are taxis evaluated by Pickup Catchment Zones instead of Routes?**
> Scheduled public transit (subways, commuter rails, municipal buses) operates along fixed corridors with predetermined stops. Yellow and Green NYC taxis, however, operate as dynamic point-to-point vehicles where routes vary based on traffic, dispatch, and passenger destination. 
> 
> Therefore, representing taxi demand as "fixed routes" would be methodologically incorrect. Instead, demand is formulated around **Geographic Pickup Catchment Zones** (e.g., Midtown Center, Financial District, JFK Airport), reflecting true passenger origination density.

---

## 📊 Dataset Specification & Heuristic Model

### Mock Dataset (`data/mock_data.py`)
The dataset is generated deterministically using `np.random.RandomState(42)` to ensure 100% reproducibility across all runs and platforms:
- **Duration:** 28 consecutive days (4 full weekly cycles, 6,720 total observations).
- **Monitored Zones (10):**
  1. *Midtown Center* (Manhattan) — Commercial & Transit Hub (Base weight: 1.25, Peak: 18:00)
  2. *JFK International Airport* (Queens) — Airport & Transit (Base weight: 0.95, Peak: 16:00)
  3. *Financial District* (Manhattan) — Commercial & Financial (Base weight: 0.88, Peak: 17:00)
  4. *Times Square / Theater District* (Manhattan) — Tourism & Entertainment (Base weight: 1.15, Peak: 21:00)
  5. *Upper East Side* (Manhattan) — Residential & Medical (Base weight: 0.92, Peak: 08:00)
  6. *Upper West Side* (Manhattan) — Residential & Cultural (Base weight: 0.85, Peak: 09:00)
  7. *East Village / Lower East Side* (Manhattan) — Dining & Nightlife (Base weight: 0.82, Peak: 23:00)
  8. *LaGuardia Airport* (Queens) — Airport & Transit (Base weight: 0.80, Peak: 17:00)
  9. *Williamsburg* (Brooklyn) — Mixed Residential & Nightlife (Base weight: 0.65, Peak: 22:00)
  10. *Astoria* (Queens) — Residential & Dining (Base weight: 0.52, Peak: 08:00)

### Schema (15 Features)
| Feature | Type | Description |
|---|---|---|
| `timestamp` | `datetime64` | Date and hour of observation |
| `date` | `string` | Calendar date (`YYYY-MM-DD`) |
| `date_dt` | `date` | Python date object for fast filtering |
| `hour` | `int` | Hour of day (`0` to `23`) |
| `formatted_hour` | `string` | Display string (`"18:00"`) |
| `day_of_week` | `int` | Day index (`0` = Monday, `6` = Sunday) |
| `day_name` | `string` | Full day name (`"Friday"`) |
| `day_short` | `string` | Abbreviated day (`"Fri"`) |
| `is_weekend` | `bool` | Weekend indicator (`Saturday` or `Sunday`) |
| `day_type` | `string` | Categorical (`"Weekday"` or `"Weekend"`) |
| `area_id` | `string` | Unique zone ID (e.g. `"NYC-001"`) |
| `pickup_area` | `string` | Zone name (e.g. `"Midtown Center"`) |
| `borough` | `string` | NYC Borough (`"Manhattan"`, `"Queens"`, `"Brooklyn"`) |
| `zone_type` | `string` | Urban classification (`Commercial`, `Residential`, etc.) |
| `pickups` | `int` | Hourly passenger pickup count |

---

## 🚀 Setup & Execution Guide

### Prerequisites
- Python 3.10, 3.11, 3.12, or 3.13
- Git

### 1. Clone & Navigate to Repository
```bash
git clone <repository-url>
cd travel_prediction
```

### 2. Create and Activate Virtual Environment
```bash
# Create virtual environment
python3 -m venv .venv

# Activate on macOS / Linux:
source .venv/bin/activate

# Or activate on Windows:
# .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```
The application will automatically launch in your default web browser at:
👉 **`http://localhost:8501`**

---

## 🧪 Automated Testing

The project includes an automated test suite located in [`tests/test_services.py`](tests/test_services.py) ensuring data consistency, mathematical calculation validity, and model boundary handling.

Run all tests via `pytest`:
```bash
PYTHONPATH=. pytest tests/ -v
```

### Verified Test Cases (9/9 Passing)
1. `test_mock_data_deterministic`: Confirms mock data generation with fixed seed 42 is 100% reproducible across environments.
2. `test_mock_data_structure`: Asserts that all 15 expected columns exist, record count equals 6,720, and no null values exist.
3. `test_analytics_kpi_computation`: Verifies executive KPI calculations (total volume, hourly averages, peak hour bounds).
4. `test_analytics_filter`: Validates that date range and zone multi-select filters properly subset the dataset.
5. `test_analytics_hourly_trend`: Confirms 24-point diurnal aggregation and peak surge tagging.
6. `test_analytics_weekday_distribution`: Verifies Monday through Sunday volume shares sum to 100%.
7. `test_analytics_heatmap_matrix`: Verifies 7x24 matrix shape and lack of NaN values.
8. `test_prediction_service_valid`: Tests prediction output structure, historical baseline comparisons, and 24-hour comparative curve generation.
9. `test_prediction_service_invalid_hour`: Confirms strict input validation throwing `ValueError` on invalid hour parameters (<0 or >23).

---

## 🧠 Machine Learning Engine & Real Data Processing

The application natively integrates both the real NYC TLC dataset and a production-grade machine learning model:

### 1. Ingesting Real NYC TLC Trip Data (12.2M Records)
The raw dataset `yellow_tripdata_2016-03.csv` (1.8 GB, 12,210,952 trips) was processed via PyArrow C++ streaming in `scripts/process_real_data.py`. Pickups were bounded to 10 curated NYC Catchment Zones and aggregated into 7,440 hourly buckets stored in `data/real_nyc_taxi_march_2016.parquet` (39 KB).

### 2. Trained Scikit-Learn Model Pipeline
A regression pipeline was trained and serialized into `models/nyc_taxi_demand_pipeline.joblib`:
- **Preprocessor:** `OneHotEncoder(drop='first')` for spatial zones
- **Model:** `HistGradientBoostingRegressor(max_iter=300, learning_rate=0.08, random_state=42)`
- **Evaluation:** Out-of-sample $R^2 = 0.9818$, MAE $= 85.19$ pickups/hr, RMSE $= 152.01$
- **Inference Service:** `ScikitLearnPredictionService` implements `BasePredictionService`, ensuring seamless drop-in capability.

Users can toggle between **NYC TLC Real Data** and the **Simulated Benchmark** at any time using the sidebar selector.

---

## 📁 Repository Directory Structure

```text
travel_prediction/
├── app.py                          # Application entry point & Page A: Overview Dashboard
├── pages/
│   ├── 1_Demand_Analytics.py       # Page B: Demand Analytics & Heatmap Matrix
│   └── 2_Demand_Prediction.py      # Page C: Demand Prediction & Comparison
├── components/
│   ├── __init__.py
│   ├── charts.py                   # Reusable Plotly chart builders
│   ├── filters.py                  # Reusable sidebar filters & data source toggle
│   └── metrics.py                  # KPI metric cards & domain integrity banners
├── data/
│   ├── __init__.py
│   ├── mock_data.py                # Dual data loader (Real NYC TLC + Seed 42 benchmark)
│   ├── real_nyc_taxi_march_2016.parquet # Clean aggregated real NYC TLC dataset (39 KB)
│   └── real_nyc_taxi_march_2016.csv     # CSV representation of aggregated data (1 MB)
├── services/
│   ├── __init__.py
│   ├── analytics_service.py        # Pandas aggregations, KPI computations, and filtering
│   └── prediction_service.py       # ScikitLearnPredictionService & MockPredictionService
├── models/
│   ├── nyc_taxi_demand_pipeline.joblib # Serialized Scikit-Learn trained pipeline (1 MB)
│   ├── model_metrics.json          # Benchmark evaluation metrics (R² = 0.982, MAE = 85.2)
│   └── README.md                   # Model architecture and training documentation
├── scripts/
│   └── process_real_data.py        # Fast PyArrow ETL and model training script
├── tests/
│   ├── __init__.py
│   └── test_services.py            # Automated Pytest suite (11/11 passing)
├── .streamlit/
│   └── config.toml                 # Streamlit dark transit theme configuration
├── requirements.txt                # Production and development dependencies
├── .gitignore                      # Git ignore file (excludes 1.8GB raw CSV)
└── README.md                       # Comprehensive documentation
```
│   └── config.toml                 # Streamlit dark transit theme configuration
├── requirements.txt                # Production and development dependencies
├── .gitignore                      # Git ignore file
└── README.md                       # Comprehensive documentation
```

---

## 👥 Authors & Academic Attribution

- **Project:** Public Transportation Demand Analysis and Passenger Prediction System
- **Phase:** Phase 1 (Baseline Analytics & Heuristic Prediction Engine)
- **Use Case:** NYC TLC Taxi Telemetry
- **License:** Educational / Academic Capstone License
