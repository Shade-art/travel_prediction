from fastapi import APIRouter
from app.schemas.summary import SummaryResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter(tags=["Summary"])

@router.get("/summary", response_model=SummaryResponse)
async def get_summary():
    """
    Returns executive KPI metrics across the transit dataset:
    - Total simulated pickups
    - Average hourly volume
    - Peak demand hour
    - Busiest pickup zone
    """
    return AnalyticsService.get_summary()
