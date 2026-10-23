from fastapi import APIRouter
from app.schemas.common import HealthResponse
from app.config import settings

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        service=settings.PROJECT_NAME,
        version=settings.VERSION,
        phase="Phase 1 - Baseline Analytics & Heuristic Prediction",
        mock_data_loaded=True
    )
