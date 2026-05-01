import logging

from fastapi import APIRouter, HTTPException

from models.schemas import AirQualityResponse
from services.openaq import fetch_air_quality

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/air-quality", response_model=AirQualityResponse)
async def get_air_quality() -> AirQualityResponse:
    try:
        return await fetch_air_quality()
    except Exception as exc:
        logger.error("Failed to fetch air quality: %s", exc, exc_info=True)
        raise HTTPException(status_code=502, detail="Air quality data unavailable")
