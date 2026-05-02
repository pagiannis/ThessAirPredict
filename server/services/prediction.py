"""
ML inference: loads the trained RandomForest from server/model/model.pkl
and generates a 48-hour AQI forecast given current OpenAQ readings.

Feature order must match ml/preprocessing.py FEATURE_COLS exactly:
  [hour_sin, hour_cos, day_of_week, month_sin, month_cos, hours_ahead,
   no2_conc, o3_conc, co_conc, so2_conc,
   aqi_lag_1h, aqi_lag_3h, aqi_lag_6h,
   temperature, humidity, precipitation, wind_speed]

Weather comes from Open-Meteo's hourly forecast so each horizon h uses the
predicted weather at t+h, matching how training weather was looked up at t+h.

Lag approximation: aqi_lag_1h/3h/6h are all set to the current live AQI.
Training uses real historical lags; this mismatch is a known limitation.
"""

import logging
import math
import pickle
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx
import pandas as pd

logger = logging.getLogger(__name__)

from config import THESS_LAT, THESS_LON
from models.schemas import ForecastPoint

_MODEL_PATH = Path(__file__).parent.parent / "model" / "model.pkl"
_model = None

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


async def _fetch_weather_forecast(hours: int = 48) -> list[dict]:
    """Returns a list of weather dicts for hours 0..hours (hourly, UTC-aligned).

    Index h in the returned list corresponds to current_time + h hours, matching
    the horizon used when building each forecast point in generate_forecast().
    """
    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude":      THESS_LAT,
                "longitude":     THESS_LON,
                "hourly":        "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
                "timezone":      "UTC",
                "forecast_days": 3,
            },
        )
        resp.raise_for_status()
        hourly = resp.json()["hourly"]

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:00")
    try:
        start_idx = hourly["time"].index(now_str)
    except ValueError:
        start_idx = 0

    result: list[dict] = []
    for h in range(hours + 1):
        idx = start_idx + h
        if idx < len(hourly["temperature_2m"]):
            result.append({
                "temperature":   hourly["temperature_2m"][idx],
                "humidity":      hourly["relative_humidity_2m"][idx],
                "precipitation": hourly["precipitation"][idx],
                "wind_speed":    hourly["wind_speed_10m"][idx],
            })
        else:
            result.append(_WEATHER_DEFAULTS)
    return result


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
    model       = _load_model()
    poll        = _extract_pollutants(air_data["pollutants"])
    current_aqi = air_data["aqi"]

    try:
        weather_forecast = await _fetch_weather_forecast(hours)
    except Exception as exc:
        logger.warning("Weather forecast unavailable (%s); using defaults", exc)
        weather_forecast = [_WEATHER_DEFAULTS] * (hours + 1)

    now    = datetime.now()
    points = []

    for h in range(0, hours + 1, step_h):
        if h == 0:
            # Use the live AQI reading directly for the "Now" point
            points.append(ForecastPoint(time="Now", aqi=air_data["aqi"]))
            continue

        future  = now + timedelta(hours=h)
        weather = weather_forecast[h] if h < len(weather_forecast) else _WEATHER_DEFAULTS
        features = pd.DataFrame([{
            "hour_sin":      math.sin(2 * math.pi * future.hour / 24),
            "hour_cos":      math.cos(2 * math.pi * future.hour / 24),
            "day_of_week":   future.weekday(),
            "month_sin":     math.sin(2 * math.pi * (future.month - 1) / 12),
            "month_cos":     math.cos(2 * math.pi * (future.month - 1) / 12),
            "hours_ahead":   h,
            "no2_conc":      poll["no2_conc"],
            "o3_conc":       poll["o3_conc"],
            "co_conc":       poll["co_conc"],
            "so2_conc":      poll["so2_conc"],
            "aqi_lag_1h":    current_aqi,
            "aqi_lag_3h":    current_aqi,
            "aqi_lag_6h":    current_aqi,
            "temperature":   weather["temperature"],
            "humidity":      weather["humidity"],
            "precipitation": weather["precipitation"],
            "wind_speed":    weather["wind_speed"],
        }])

        aqi = int(round(model.predict(features)[0]))
        aqi = max(0, min(500, aqi))
        points.append(ForecastPoint(time=f"+{h}h", aqi=aqi))

    return points
