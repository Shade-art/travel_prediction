from pydantic import BaseModel, Field

class SummaryResponse(BaseModel):
    total_pickups: int = Field(..., description="Total simulated taxi pickups in the current analytical dataset")
    avg_hourly_pickups: float = Field(..., description="Average taxi pickups per hour across all zones")
    peak_demand_hour: int = Field(..., ge=0, le=23, description="Hour of the day with the highest aggregate pickup volume (0-23)")
    peak_demand_hour_formatted: str = Field(..., description="Formatted string for peak demand hour, e.g. 18:00 (6 PM)")
    peak_demand_hour_pickups: int = Field(..., description="Aggregate pickup count during peak hour")
    busiest_pickup_area: str = Field(..., description="Name of the zone/area with highest demand")
    busiest_pickup_borough: str = Field(..., description="Borough of the busiest area")
    busiest_area_pickups: int = Field(..., description="Total pickups in the busiest area")
    busiest_area_percentage: float = Field(..., description="Share of total pickups in the busiest area")
    total_monitored_zones: int = Field(..., description="Number of tracked NYC zones")
    sample_date_range: str = Field(..., description="Date range represented in this dataset")
    data_classification: str = Field(default="Simulated NYC TLC Taxi Telemetry - Phase 1 Mock Data")
