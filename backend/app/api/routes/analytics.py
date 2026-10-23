from fastapi import APIRouter, Query
from typing import Optional
from app.schemas.analytics import (
    HourlyAnalyticsResponse,
    AreaAnalyticsResponse,
    WeeklyAnalyticsResponse
)
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/hourly", response_model=HourlyAnalyticsResponse)
async def get_hourly_analytics(
    area: Optional[str] = Query(None, description="Optional pickup area/zone name filter")
):
    """
    Returns 24-hour demand distribution (pickups, weekday avg, weekend avg, peak indicators)
    Optionally filtered by pickup area.
    """
    return AnalyticsService.get_hourly_analytics(area_filter=area)

@router.get("/areas", response_model=AreaAnalyticsResponse)
async def get_area_analytics():
    """
    Returns demand distribution across NYC pickup zones.
    Note: Taxis operate point-to-point without fixed routes; demand is tracked by catchment areas.
    """
    return AnalyticsService.get_area_analytics()

@router.get("/weekly", response_model=WeeklyAnalyticsResponse)
async def get_weekly_analytics(
    area: Optional[str] = Query(None, description="Optional pickup area/zone name filter")
):
    """
    Returns day-of-week demand distribution and a 7x24 hour-by-weekday demand heatmap matrix.
    Optionally filtered by pickup area.
    """
    return AnalyticsService.get_weekly_analytics(area_filter=area)
