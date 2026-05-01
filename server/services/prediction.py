"""
ML inference: loads the trained RandomForest from server/model/model.pkl
and generates a 48-hour AQI forecast given current OpenAQ readings.

Feature order must match ml/preprocessing.py FEATURE_COLS exactly:
  [hour, day_of_week, month, hours_ahead,
   no2_conc, o3_conc, co_conc, so2_conc,
   temperature, humidity, precipitation, wind_speed]
"""

import logging
import pickle
from datetime import datetime, timedelta
from pathlib import Path

import httpx
import pandas as pd

logger = logging.getLogger(__name__)

from models.schemas import ForecastPoint

_MODEL_PATH = Path(__file__).parent.parent / "model" / "model.pkl"
_model = None

THESS_LAT = 40.6401
THESS_LON = 22.9444

_WEATHER_DEFAULTS = {
    "temperature": 15.0,
    "humidity": 65.0,
    "precipitation": 0.0,
    "wind_speed": 10.0,
}

_DISPLAY_TO_FEATURE = {
    "NO₂": "no2_conc",
    "O₃":  "o3_conc",
    "CO":  "co_conc",
    "SO₂": "so2_conc",
}


def _load_model():
    global _model
    if _model is None:
        with open(_MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
    return _model


async def _fetch_current_weather() -> dict:
    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": THESS_LAT,
                "longitude": THESS_LON,
                "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
            },
        )
        resp.raise_for_status()
        c = resp.json()["current"]
    return {
        "temperature":   c["temperature_2m"],
        "humidity":      c["relative_humidity_2m"],
        "precipitation": c["precipitation"],
        "wind_speed":    c["wind_speed_10m"],
    }


def _extract_pollutants(pollutants: list) -> dict:
    result = {v: 0.0 for v in _DISPLAY_TO_FEATURE.values()}
    for p in pollutants:
        key = _DISPLAY_TO_FEATURE.get(p.name)
        if key:
            result[key] = p.value
    return result


async def generate_forecast(
    air_data: dict,
    hours: int = 48,
    step_h: int = 3,
) -> list[ForecastPoint]:
    model = _load_model()
    poll  = _extract_pollutants(air_data["pollutants"])

    try:
        weather = await _fetch_current_weather()
    except Exception as exc:
        logger.warning("Weather API unavailable (%s); using defaults %s", exc, _WEATHER_DEFAULTS)
        weather = _WEATHER_DEFAULTS

    now    = datetime.now()
    points = []

    for h in range(0, hours + 1, step_h):
        if h == 0:
            # Use the live AQI reading directly for the "Now" point
            points.append(ForecastPoint(time="Now", aqi=air_data["aqi"]))
            continue

        future = now + timedelta(hours=h)
        features = pd.DataFrame([{
            "hour":          future.hour,
            "day_of_week":   future.weekday(),
            "month":         future.month,
            "hours_ahead":   h,
            "no2_conc":      poll["no2_conc"],
            "o3_conc":       poll["o3_conc"],
            "co_conc":       poll["co_conc"],
            "so2_conc":      poll["so2_conc"],
            "temperature":   weather["temperature"],
            "humidity":      weather["humidity"],
            "precipitation": weather["precipitation"],
            "wind_speed":    weather["wind_speed"],
        }])

        aqi = int(round(model.predict(features)[0]))
        aqi = max(0, min(500, aqi))
        points.append(ForecastPoint(time=f"+{h}h", aqi=aqi))

    return points
