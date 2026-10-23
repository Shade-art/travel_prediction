from fastapi import APIRouter, HTTPException, Depends
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.prediction_service import BasePredictionService, get_prediction_service

router = APIRouter(tags=["Prediction"])

@router.post("/predict", response_model=PredictionResponse)
async def predict_demand(
    request: PredictionRequest,
    prediction_service: BasePredictionService = Depends(get_prediction_service)
):
    """
    Simulated passenger demand prediction for a specific pickup area, date, and hour.
    Returns predicted count, comparison with historical average, and 24h comparative profile.
    All outputs are mock/heuristic estimates for Phase 1.
    """
    try:
        response = prediction_service.predict(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to generate demand prediction: {str(e)}"
        )
