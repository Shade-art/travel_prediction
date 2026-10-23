from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime

class PredictionRequest(BaseModel):
    pickup_area: str = Field(..., min_length=2, max_length=100, description="NYC Taxi zone / pickup area")
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Target date in YYYY-MM-DD format")
    hour: int = Field(..., ge=0, le=23, description="Hour of pickup (0 to 23)")

    @field_validator("date")
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be a valid calendar date in YYYY-MM-DD format")
        return v

class HourlyCurvePoint(BaseModel):
    hour: int
    formatted_hour: str
    historical_baseline: int
    predicted_volume: int
    is_target_hour: bool

class PredictionResponse(BaseModel):
    pickup_area: str
    date: str
    hour: int
    formatted_hour: str
    day_name: str
    is_weekend: bool
    predicted_pickups: int
    historical_average: int
    difference_percentage: float
    demand_level: str  # "Low", "Moderate", "High", "Peak Surge"
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    key_drivers: List[str]
    hourly_curve: List[HourlyCurvePoint]
    is_mock: bool = True
    disclaimer: str = "Simulated / Heuristic Estimate (Phase 1 Baseline). Algorithmic simulation designed for Phase 1 prototyping; ML model (scikit-learn) will replace this service in Phase 2."
