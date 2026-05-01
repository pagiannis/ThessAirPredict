import logging

from fastapi import APIRouter, HTTPException

from models.schemas import ForecastResponse
from services.openaq import fetch_air_quality
from services.prediction import generate_forecast

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/forecast", response_model=ForecastResponse)
async def get_forecast() -> ForecastResponse:
    try:
        air_data = await fetch_air_quality()
        points   = await generate_forecast(air_data)
        return ForecastResponse(forecast=points)
    except Exception as exc:
        logger.error("Failed to generate forecast: %s", exc, exc_info=True)
        raise HTTPException(status_code=502, detail="Forecast unavailable")
