import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["mock_data_loaded"] is True
    assert "NYC Taxi" in data["service"]

def test_summary_endpoint():
    response = client.get("/api/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_pickups" in data
    assert data["total_pickups"] > 0
    assert "avg_hourly_pickups" in data
    assert data["avg_hourly_pickups"] > 0
    assert 0 <= data["peak_demand_hour"] <= 23
    assert "peak_demand_hour_formatted" in data
    assert "busiest_pickup_area" in data
    assert data["busiest_pickup_area"] == "Midtown Center"
    assert data["total_monitored_zones"] == 10

def test_analytics_hourly_endpoint_default():
    response = client.get("/api/analytics/hourly")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) == 24
    assert data["data"][0]["hour"] == 0
    assert data["data"][23]["hour"] == 23
    # Verify peak indicator exists
    peak_count = sum(1 for p in data["data"] if p["is_peak"])
    assert peak_count >= 1

def test_analytics_hourly_endpoint_filtered():
    response = client.get("/api/analytics/hourly?area=JFK%20International%20Airport")
    assert response.status_code == 200
    data = response.json()
    assert "JFK International Airport" in data["filter_area"]
    assert len(data["data"]) == 24

def test_analytics_areas_endpoint():
    response = client.get("/api/analytics/areas")
    assert response.status_code == 200
    data = response.json()
    assert data["total_areas"] == 10
    assert len(data["data"]) == 10
    # Check disclaimer mentioning taxi point-to-point nature
    assert "point-to-point" in data["disclaimer"]
    first_area = data["data"][0]
    assert "area_name" in first_area
    assert "percentage" in first_area
    assert first_area["total_pickups"] > 0

def test_analytics_weekly_endpoint():
    response = client.get("/api/analytics/weekly")
    assert response.status_code == 200
    data = response.json()
    assert "weekday_distribution" in data
    assert len(data["weekday_distribution"]) == 7
    assert data["weekday_distribution"][0]["day_name"] == "Monday"
    assert "heatmap" in data
    assert len(data["heatmap"]) == 7 * 24
    # Check heatmap cell properties
    sample_cell = data["heatmap"][0]
    assert "day_name" in sample_cell
    assert "hour" in sample_cell
    assert 0 <= sample_cell["intensity"] <= 100

def test_predict_endpoint_valid():
    payload = {
        "pickup_area": "Midtown Center",
        "date": "2026-10-25",
        "hour": 18
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["pickup_area"] == "Midtown Center"
    assert data["hour"] == 18
    assert data["is_mock"] is True
    assert "Simulated" in data["disclaimer"]
    assert data["predicted_pickups"] > 0
    assert data["historical_average"] > 0
    assert "difference_percentage" in data
    assert "demand_level" in data
    assert len(data["key_drivers"]) > 0
    assert len(data["hourly_curve"]) == 24
    # The 18th point should be target hour
    target_point = next(p for p in data["hourly_curve"] if p["is_target_hour"])
    assert target_point["hour"] == 18

def test_predict_endpoint_invalid_hour():
    payload = {
        "pickup_area": "Midtown Center",
        "date": "2026-10-25",
        "hour": 25  # Invalid hour
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 422

def test_predict_endpoint_invalid_date():
    payload = {
        "pickup_area": "Midtown Center",
        "date": "invalid-date",
        "hour": 10
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 422
