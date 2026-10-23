# Machine Learning Models Directory

This directory contains trained model artifacts, serialized feature preprocessors, and evaluation benchmarks for the **Public Transportation Demand Analysis and Passenger Prediction System**.

---

## 🏆 Active Model Artifact: `nyc_taxi_demand_pipeline.joblib`

The production prediction engine uses a Scikit-Learn pipeline trained on the genuine **NYC TLC Yellow Taxi dataset (March 2016)** containing **12,210,952 trips** aggregated into 7,440 hourly zone observations.

### Model Architecture
- **Pipeline Stages:**
  1. `ColumnTransformer`: `OneHotEncoder(drop='first', sparse_output=False)` for catchment zones.
  2. `HistGradientBoostingRegressor`:
     - Max iterations / trees: `300`
     - Learning rate: `0.08`
     - Max leaf nodes: `31`
     - Random state: `42`
- **Features Ingested:**
  - `pickup_area`: NYC TLC Catchment Zone (10 curated zones across Manhattan, Queens, and Brooklyn)
  - `hour`: Hour of day (`0–23`)
  - `day_of_week`: Day index (`0=Monday, 6=Sunday`)
  - `is_weekend`: Binary flag (`0` for Mon–Fri, `1` for Sat–Sun)
- **Target:**
  - `pickups`: Hourly taxi pickup demand

---

## 📊 Evaluation Benchmarks (Out-of-Sample Test Set)

Metadata file: [`models/model_metrics.json`](file:///Users/hamza/PROJECTS/travel_prediction/models/model_metrics.json)

| Metric | Score | Unit / Description |
| :--- | :--- | :--- |
| **Coefficient of Determination ($R^2$)** | **`0.9818`** | Explains 98.2% of demand variance |
| **Mean Absolute Error (MAE)** | **`85.19`** | Pickups / hour |
| **Root Mean Squared Error (RMSE)** | **`152.01`** | Pickups / hour |
| **Raw Trip Records Processed** | **`12,210,952`** | March 2016 NYC TLC |
| **Total Captured Zone Pickups** | **`6,765,030`** | 10 representative zones |
| **Hourly Bucket Samples** | **`7,440`** | 31 days × 24 hours × 10 zones |

---

## 🔄 Re-training the Model

To re-run the ETL pipeline on `yellow_tripdata_2016-03.csv` and re-train the model:

```bash
python scripts/process_real_data.py
```

Execution takes less than 3 seconds thanks to PyArrow C++ multi-threaded CSV streaming.
