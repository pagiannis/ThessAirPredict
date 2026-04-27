import time
from datetime import datetime, timezone
from typing import Any

import httpx

from config import settings
from models.schemas import PollutantReading, StationReading

OPENAQ_BASE = "https://api.openaq.org/v3"
THESS_LAT = 40.6401
THESS_LON = 22.9444
SEARCH_RADIUS_M = 25_000
CACHE_TTL = 300  # seconds

# Rough bounding box for Thessaloniki, used to map lat/lon → 0–100 x/y
_LON_MIN, _LON_MAX = 22.85, 23.05
_LAT_MIN, _LAT_MAX = 40.55, 40.75

_cache: dict[str, tuple[Any, float]] = {}

# PM2.5 AQI breakpoints (US EPA)
_PM25_BP = [
    (0.0, 12.0, 0, 50),
    (12.1, 35.4, 51, 100),
    (35.5, 55.4, 101, 150),
    (55.5, 150.4, 151, 200),
    (150.5, 250.4, 201, 300),
    (250.5, 500.4, 301, 500),
]


def _pm25_to_aqi(conc: float) -> int:
    for c_lo, c_hi, i_lo, i_hi in _PM25_BP:
        if c_lo <= conc <= c_hi:
            return round((i_hi - i_lo) / (c_hi - c_lo) * (conc - c_lo) + i_lo)
    return 500


def _aqi_label(aqi: int) -> str:
    if aqi <= 50:
        return "Good"
    if aqi <= 100:
        return "Moderate"
    if aqi <= 200:
        return "Unhealthy"
    if aqi <= 300:
        return "Very Unhealthy"
    return "Hazardous"


def _to_xy(lat: float, lon: float) -> tuple[float, float]:
    x = (lon - _LON_MIN) / (_LON_MAX - _LON_MIN) * 100
    y = (_LAT_MAX - lat) / (_LAT_MAX - _LAT_MIN) * 100
    return round(max(0, min(100, x)), 1), round(max(0, min(100, y)), 1)


def _avg(vals: list[float]) -> float:
    return sum(vals) / len(vals) if vals else 0.0


async def _fetch() -> dict:
    headers = {"X-API-Key": settings.openaq_api_key} if settings.openaq_api_key else {}

    async with httpx.AsyncClient(headers=headers, timeout=15.0) as client:
        loc_resp = await client.get(
            f"{OPENAQ_BASE}/locations",
            params={
                "coordinates": f"{THESS_LAT},{THESS_LON}",
                "radius": SEARCH_RADIUS_M,
                "limit": 10,
                "order_by": "distance",
            },
        )
        loc_resp.raise_for_status()
        locations = loc_resp.json().get("results", [])

    if not locations:
        raise ValueError("No monitoring stations found near Thessaloniki")

    # Collect measurements; key = lowercase parameter name, value = list of readings
    param_values: dict[str, list[float]] = {}
    station_readings: list[StationReading] = []

    async with httpx.AsyncClient(headers=headers, timeout=15.0) as client:
        for loc in locations[:6]:
            loc_id = loc["id"]
            loc_name = loc.get("name", f"Station {loc_id}")
            coords = loc.get("coordinates", {})
            lat = coords.get("latitude", THESS_LAT)
            lon = coords.get("longitude", THESS_LON)

            latest_resp = await client.get(f"{OPENAQ_BASE}/locations/{loc_id}/latest")
            if latest_resp.status_code != 200:
                continue

            measurements = latest_resp.json().get("results", [])
            pm25_val: float | None = None

            for m in measurements:
                param = m.get("parameter", {})
                name = param.get("name", "").lower()
                value = m.get("value")
                if value is None or value < 0:
                    continue
                param_values.setdefault(name, []).append(float(value))
                if name == "pm25":
                    pm25_val = float(value)

            if pm25_val is not None:
                x, y = _to_xy(lat, lon)
                station_readings.append(
                    StationReading(
                        name=loc_name,
                        x=x,
                        y=y,
                        aqi=_pm25_to_aqi(pm25_val),
                    )
                )

    # Build pollutant list — only include parameters with actual data
    PARAM_META: list[tuple[str, str, str]] = [
        ("pm25", "PM2.5", "µg/m³"),
        ("pm10", "PM10", "µg/m³"),
        ("no2", "NO₂", "µg/m³"),
        ("o3", "O₃", "µg/m³"),
        ("so2", "SO₂", "µg/m³"),
        ("co", "CO", "mg/m³"),
    ]

    pollutants: list[PollutantReading] = []
    for key, display, unit in PARAM_META:
        vals = param_values.get(key, [])
        if not vals:
            continue
        pollutants.append(
            PollutantReading(
                name=display,
                value=round(_avg(vals), 2),
                unit=unit,
                trend="stable",  # trend requires historical data — extended later
            )
        )

    pm25_avg = _avg(param_values.get("pm25", []))
    overall_aqi = _pm25_to_aqi(pm25_avg) if pm25_avg else 0

    return {
        "aqi": overall_aqi,
        "aqi_label": _aqi_label(overall_aqi),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "pollutants": pollutants,
        "stations": station_readings,
    }


async def fetch_air_quality() -> dict:
    key = "air_quality"
    if key in _cache:
        value, ts = _cache[key]
        if time.monotonic() - ts < CACHE_TTL:
            return value
    result = await _fetch()
    _cache[key] = (result, time.monotonic())
    return result
