from fastapi import APIRouter, HTTPException

from models.schemas import AirQualityResponse
from services.openaq import fetch_air_quality

router = APIRouter()


@router.get("/air-quality", response_model=AirQualityResponse)
async def get_air_quality():
    try:
        return await fetch_air_quality()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))
