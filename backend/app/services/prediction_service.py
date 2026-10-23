from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any
from app.data.mock_taxi_data import (
    TAXI_ZONES,
    BASE_HOURLY_PATTERN,
    WEEKDAY_PATTERNS,
    BASE_ZONE_HOURLY_VOLUME,
    get_zone_by_name
)
from app.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
    HourlyCurvePoint
)

class BasePredictionService(ABC):
    """
    Abstract Service Interface for Passenger Demand Prediction.
    In Phase 2, this interface can be implemented by ScikitLearnPredictionService
    or PyTorchPredictionService without modifying any API routes or schemas.
    """
    @abstractmethod
    def predict(self, request: PredictionRequest) -> PredictionResponse:
        pass


class MockPredictionService(BasePredictionService):
    """
    Phase 1 Heuristic Simulation Engine.
    Simulates NYC TLC taxi passenger demand using zone baselines,
    temporal cycles, calendar factors, and time-of-day rush curves.
    """
    def predict(self, request: PredictionRequest) -> PredictionResponse:
        # Validate or match pickup area
        zone = get_zone_by_name(request.pickup_area)
        if not zone:
            # Fallback to closest default or Midtown Center
            zone = TAXI_ZONES[0]

        # Parse date
        target_date = datetime.strptime(request.date, "%Y-%m-%d")
        weekday_idx = target_date.weekday()  # 0=Monday, 6=Sunday
        day_info = WEEKDAY_PATTERNS[weekday_idx]
        day_name = day_info["day_name"]
        is_weekend = weekday_idx in (5, 6)

        hour = request.hour
        formatted_hour = f"{hour:02d}:00"

        # Lookup hourly factors
        pattern = next((p for p in BASE_HOURLY_PATTERN if p["hour"] == hour), BASE_HOURLY_PATTERN[12])
        hour_factor = pattern["weekend_factor"] if is_weekend else pattern["weekday_factor"]
        day_weight = day_info["weight"]
        zone_weight = zone["base_weight"]

        # Synergy factor if this is zone's peak hour
        is_zone_peak = (zone["peak_hour"] == hour)
        synergy = 1.25 if is_zone_peak else 1.0

        # Calculate historical average for this zone at this specific hour across all 7 days
        weekly_sum_at_hour = sum(
            int(round(BASE_ZONE_HOURLY_VOLUME * zone_weight * (
                pattern["weekend_factor"] if d["day_index"] in (5, 6) else pattern["weekday_factor"]
            ) * d["weight"]))
            for d in WEEKDAY_PATTERNS
        )
        historical_average = int(round(weekly_sum_at_hour / 7))

        # Predicted pickups for this specific date and hour
        # Add slight date variation (based on day of month) for realism
        calendar_mod = 1.0 + ((target_date.day % 7) - 3) * 0.02
        raw_prediction = BASE_ZONE_HOURLY_VOLUME * zone_weight * hour_factor * day_weight * synergy * calendar_mod
        predicted_pickups = max(15, int(round(raw_prediction)))

        # Difference vs historical average
        if historical_average > 0:
            diff_pct = round(((predicted_pickups - historical_average) / historical_average) * 100, 1)
        else:
            diff_pct = 0.0

        # Demand classification
        if diff_pct >= 25 or predicted_pickups > 700:
            demand_level = "Peak Surge"
        elif diff_pct >= 10 or predicted_pickups > 500:
            demand_level = "High"
        elif diff_pct <= -15 or predicted_pickups < 200:
            demand_level = "Low"
        else:
            demand_level = "Moderate"

        # Drivers & insights
        drivers: List[str] = []
        if is_zone_peak:
            drivers.append(f"Primary peak window for {zone['area_name']} around {hour:02d}:00 ({zone['zone_type']})")
        if hour in (8, 9):
            drivers.append("Morning commuter influx into commercial and transit hubs")
        elif hour in (17, 18, 19):
            drivers.append("Evening rush hour outbound & cross-borough commute surge")
        elif hour >= 21 and is_weekend:
            drivers.append("Weekend nightlife and hospitality travel spike")
        elif hour <= 5:
            drivers.append("Off-peak late-night window with reduced citywide transit volume")

        drivers.append(f"{day_name} baseline demand factor ({day_weight:.2f}x)")
        drivers.append(f"Catchment profile: {zone['borough']} ({zone['zone_type']})")

        # Confidence score (mocked heuristic confidence)
        confidence = 0.88 if 6 <= hour <= 22 else 0.76

        # Build 24-hour comparative curve for this zone on target date
        hourly_curve: List[HourlyCurvePoint] = []
        for p in BASE_HOURLY_PATTERN:
            h = p["hour"]
            h_factor = p["weekend_factor"] if is_weekend else p["weekday_factor"]
            h_synergy = 1.25 if zone["peak_hour"] == h else 1.0

            # Historical baseline for that hour across 7 days
            h_hist_sum = sum(
                int(round(BASE_ZONE_HOURLY_VOLUME * zone_weight * (
                    p["weekend_factor"] if d["day_index"] in (5, 6) else p["weekday_factor"]
                ) * d["weight"]))
                for d in WEEKDAY_PATTERNS
            )
            h_hist_avg = int(round(h_hist_sum / 7))

            # Predicted profile for target date
            h_pred = int(round(BASE_ZONE_HOURLY_VOLUME * zone_weight * h_factor * day_weight * h_synergy * calendar_mod))

            hourly_curve.append(HourlyCurvePoint(
                hour=h,
                formatted_hour=f"{h:02d}:00",
                historical_baseline=h_hist_avg,
                predicted_volume=h_pred,
                is_target_hour=(h == hour)
            ))

        return PredictionResponse(
            pickup_area=zone["area_name"],
            date=request.date,
            hour=hour,
            formatted_hour=formatted_hour,
            day_name=day_name,
            is_weekend=is_weekend,
            predicted_pickups=predicted_pickups,
            historical_average=historical_average,
            difference_percentage=diff_pct,
            demand_level=demand_level,
            confidence_score=confidence,
            key_drivers=drivers,
            hourly_curve=hourly_curve,
            is_mock=True,
            disclaimer="Simulated / Heuristic Estimate (Phase 1 Baseline). Algorithmic simulation designed for Phase 1 prototyping; ML model (scikit-learn) will replace this service in Phase 2."
        )


# Factory / Dependency Injection provider
_service_instance: BasePredictionService = MockPredictionService()

def get_prediction_service() -> BasePredictionService:
    """
    Returns the active prediction service instance.
    Swap with ML / ScikitLearn service in Phase 2.
    """
    return _service_instance
