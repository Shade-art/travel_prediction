"""
Pytest Test Suite for Data Generation, Analytics Calculations, and Prediction Service.
"""

from datetime import date, datetime
import pytest
import pandas as pd
import numpy as np

from data.mock_data import (
    generate_mock_dataset,
    load_real_dataset,
    get_all_areas,
    get_zone_metadata,
    TAXI_ZONES
)
from services.analytics_service import AnalyticsService
from services.prediction_service import (
    MockPredictionService,
    ScikitLearnPredictionService,
    get_prediction_service
)


@pytest.fixture
def mock_df():
    """Provides a fresh 28-day deterministic mock DataFrame."""
    return generate_mock_dataset(days=28, seed=42)


def test_mock_data_deterministic():
    """Verify that mock data generation with fixed seed 42 is 100% reproducible."""
    df1 = generate_mock_dataset(days=14, seed=42)
    df2 = generate_mock_dataset(days=14, seed=42)
    assert len(df1) == len(df2)
    assert df1["pickups"].equals(df2["pickups"])


def test_mock_data_structure(mock_df):
    """Verify required schema and columns in the mock dataset."""
    expected_cols = [
        "timestamp", "date", "date_dt", "hour", "formatted_hour",
        "day_of_week", "day_name", "day_short", "is_weekend", "day_type",
        "area_id", "pickup_area", "borough", "zone_type", "pickups"
    ]
    for col in expected_cols:
        assert col in mock_df.columns

    assert not mock_df.isnull().any().any()
    assert len(mock_df) == 28 * 24 * len(TAXI_ZONES)
    assert (mock_df["pickups"] > 0).all()


def test_analytics_kpi_computation(mock_df):
    """Verify that KPI calculations accurately extract totals and peak indicators."""
    kpis = AnalyticsService.compute_kpis(mock_df)

    assert kpis["total_pickups"] == mock_df["pickups"].sum()
    assert kpis["avg_hourly_demand"] > 0
    assert 0 <= kpis["peak_hour"] <= 23
    assert ":" in kpis["peak_hour_formatted"]
    assert kpis["busiest_area"] in get_all_areas()
    assert kpis["total_zones"] == len(TAXI_ZONES)
    assert kpis["busiest_area_percentage"] > 0


def test_analytics_filter(mock_df):
    """Verify filtering by date range and selected pickup zones."""
    min_date = mock_df["date_dt"].min()
    end_date = min_date + pd.Timedelta(days=6)
    target_zone = "JFK International Airport"

    filtered = AnalyticsService.filter_data(
        mock_df,
        start_date=min_date,
        end_date=end_date,
        selected_areas=[target_zone]
    )

    assert not filtered.empty
    assert (filtered["date_dt"] >= min_date).all()
    assert (filtered["date_dt"] <= end_date).all()
    assert (filtered["pickup_area"] == target_zone).all()


def test_analytics_hourly_trend(mock_df):
    """Verify hourly trend calculation creates a 24-point diurnal profile."""
    hourly_df = AnalyticsService.get_hourly_trend(mock_df)

    assert len(hourly_df) == 24
    assert list(hourly_df["hour"]) == list(range(24))
    assert (hourly_df["avg_pickups"] > 0).all()
    # At least one hour marked as peak
    assert hourly_df["is_peak"].sum() >= 1


def test_analytics_weekday_distribution(mock_df):
    """Verify weekday aggregation produces 7 ordered days."""
    weekday_df = AnalyticsService.get_weekday_distribution(mock_df)

    assert len(weekday_df) == 7
    assert list(weekday_df["day_of_week"]) == list(range(7))
    assert abs(weekday_df["percentage"].sum() - 100.0) < 0.5


def test_analytics_heatmap_matrix(mock_df):
    """Verify heatmap matrix produces a 7x24 grid without NaNs."""
    matrix, days, hours = AnalyticsService.get_heatmap_matrix(mock_df)

    assert matrix.shape == (7, 24)
    assert len(days) == 7
    assert len(hours) == 24
    assert not np.isnan(matrix).any()
    assert (matrix >= 0).all()


def test_mock_prediction_service_valid(mock_df):
    """Verify that MockPredictionService produces valid simulation output."""
    service = MockPredictionService()
    res = service.predict(
        df_history=mock_df,
        pickup_area="Midtown Center",
        target_date=date(2026, 10, 26),
        target_hour=18
    )

    assert res["pickup_area"] == "Midtown Center"
    assert res["hour"] == 18
    assert res["is_mock"] is True
    assert "Simulated" in res["disclaimer"]
    assert res["predicted_pickups"] > 0
    assert res["historical_average"] > 0
    assert isinstance(res["difference_percentage"], float)
    assert res["demand_level"] in ["Low", "Moderate", "High", "Peak Surge"]
    assert 0.0 <= res["confidence_score"] <= 1.0
    assert len(res["key_drivers"]) >= 2

    # Comparative curve checks
    curve = res["hourly_curve"]
    assert isinstance(curve, pd.DataFrame)
    assert len(curve) == 24
    assert bool(curve.loc[curve["hour"] == 18, "is_target_hour"].values[0]) is True


def test_sklearn_prediction_service_valid():
    """Verify that ScikitLearnPredictionService operates correctly with trained pipeline."""
    service = ScikitLearnPredictionService()
    assert service.is_ready is True

    real_df = load_real_dataset()
    res = service.predict(
        df_history=real_df,
        pickup_area="Midtown Center",
        target_date=date(2026, 3, 15),
        target_hour=18
    )

    assert res["pickup_area"] == "Midtown Center"
    assert res["hour"] == 18
    assert res["is_mock"] is False
    assert "HistGradientBoostingRegressor" in res["model_name"]
    assert res["model_r2"] > 0.95
    assert res["predicted_pickups"] > 500  # Busy Midtown evening
    assert res["historical_average"] > 0
    assert len(res["hourly_curve"]) == 24


def test_real_dataset_integrity():
    """Verify processed NYC TLC March 2016 dataset schema and completeness."""
    real_df = load_real_dataset()
    assert len(real_df) == 31 * 24 * len(TAXI_ZONES)  # 7,440 hourly zone observations
    assert not real_df.isnull().any().any()
    assert real_df["pickups"].sum() > 6_000_000  # Over 6 million pickups captured


def test_prediction_service_invalid_hour(mock_df):
    """Verify input validation throws ValueError on invalid hour."""
    service = get_prediction_service(mode="mock")
    with pytest.raises(ValueError):
        service.predict(
            df_history=mock_df,
            pickup_area="Midtown Center",
            target_date=date(2026, 10, 26),
            target_hour=25  # Invalid
        )
