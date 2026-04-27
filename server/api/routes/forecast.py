from fastapi import APIRouter, HTTPException

from models.schemas import ForecastResponse
from services import forecaster
from services.openaq import fetch_air_quality

router = APIRouter()


@router.get("/forecast", response_model=ForecastResponse)
async def get_forecast():
    try:
        aq = await fetch_air_quality()
        points = forecaster.generate(aq["aqi"])
        return ForecastResponse(forecast=points)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))
