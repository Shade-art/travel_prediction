from pydantic import BaseModel, Field
from typing import List, Optional

class HourlyDataPoint(BaseModel):
    hour: int = Field(..., ge=0, le=23)
    formatted_hour: str
    pickups: int
    weekday_pickups: int
    weekend_pickups: int
    is_peak: bool

class HourlyAnalyticsResponse(BaseModel):
    filter_area: Optional[str] = None
    filter_weekday: Optional[str] = None
    total_pickups: int
    data: List[HourlyDataPoint]

class AreaDataPoint(BaseModel):
    area_id: str
    area_name: str
    borough: str
    total_pickups: int
    percentage: float
    avg_hourly_pickups: float
    peak_hour: int
    peak_hour_formatted: str
    zone_type: str  # Commercial, Airport, Residential, Entertainment

class AreaAnalyticsResponse(BaseModel):
    total_areas: int
    total_pickups: int
    disclaimer: str = "Taxis operate point-to-point without fixed transit routes. Demand is indexed by pickup zones and geographic catchment clusters."
    data: List[AreaDataPoint]

class WeekdayDataPoint(BaseModel):
    day_index: int = Field(..., ge=0, le=6, description="0=Monday, 6=Sunday")
    day_name: str
    short_name: str
    total_pickups: int
    daily_average: float
    percentage: float

class HeatmapCell(BaseModel):
    day_index: int
    day_name: str
    hour: int
    formatted_hour: str
    pickups: int
    intensity: float = Field(..., ge=0, le=100, description="Normalized intensity percentage (0-100%)")

class WeeklyAnalyticsResponse(BaseModel):
    filter_area: Optional[str] = None
    weekday_distribution: List[WeekdayDataPoint]
    heatmap: List[HeatmapCell]
