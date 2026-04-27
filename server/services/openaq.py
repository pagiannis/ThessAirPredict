import asyncio
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

_cache: dict[str, tuple[Any, float]] = {}

# Human-readable overrides for EEA station codes returned by OpenAQ
_STATION_NAMES: dict[str, str] = {
    "GR0018A": "Thessaloniki",
}

# PM2.5 AQI breakpoints (US EPA)
_PM25_BP = [
    (0.0, 12.0, 0, 50),
    (12.1, 35.4, 51, 100),
    (35.5, 55.4, 101, 150),
    (55.5, 150.4, 151, 200),
    (150.5, 250.4, 201, 300),
    (250.5, 500.4, 301, 500),
]

PARAM_META: list[tuple[str, str, str]] = [
    ("pm25", "PM2.5", "µg/m³"),
    ("pm10", "PM10", "µg/m³"),
    ("no2", "NO₂", "µg/m³"),
    ("o3", "O₃", "µg/m³"),
    ("so2", "SO₂", "µg/m³"),
    ("co", "CO", "mg/m³"),
]
_TRACKED = {key for key, _, _ in PARAM_META}


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


def _avg(vals: list[float]) -> float:
    return sum(vals) / len(vals) if vals else 0.0


def _param_name(param: Any) -> str:
    if isinstance(param, dict):
        return param.get("name", "").lower()
    return str(param).lower()


def _station_display_name(raw: str) -> str:
    return _STATION_NAMES.get(raw.upper(), raw.title())


async def _fetch_sensor(
    client: httpx.AsyncClient, sensor_id: int
) -> tuple[int, float | None]:
    resp = await client.get(
        f"{OPENAQ_BASE}/sensors/{sensor_id}/measurements",
        params={"limit": 1},
    )
    if resp.status_code != 200:
        return sensor_id, None
    results = resp.json().get("results", [])
    if not results:
        return sensor_id, None
    value = results[0].get("value")
    return sensor_id, float(value) if (value is not None and float(value) >= 0) else None


async def _fetch() -> dict:
    headers = {"X-API-Key": settings.openaq_api_key}

    async with httpx.AsyncClient(headers=headers, timeout=15.0) as client:
        # Step 1: find nearby stations; response includes embedded sensor list
        loc_resp = await client.get(
            f"{OPENAQ_BASE}/locations",
            params={
                "coordinates": f"{THESS_LAT},{THESS_LON}",
                "radius": SEARCH_RADIUS_M,
                "limit": 10,
            },
        )
        loc_resp.raise_for_status()
        locations = loc_resp.json().get("results", [])

        if not locations:
            raise ValueError("No monitoring stations found near Thessaloniki")

        # Build lookups from the location response
        loc_meta: dict[int, dict] = {}
        sensor_to_loc: dict[int, tuple[int, str]] = {}  # sensor_id → (loc_id, param_name)

        for loc in locations[:6]:
            coords = loc.get("coordinates", {})
            loc_id = loc["id"]
            loc_meta[loc_id] = {
                "name": _station_display_name(loc.get("name", f"Station {loc_id}")),
                "lat": coords.get("latitude", THESS_LAT),
                "lon": coords.get("longitude", THESS_LON),
            }
            for sensor in loc.get("sensors", []):
                name = _param_name(sensor.get("parameter", {}))
                if name in _TRACKED:
                    sensor_to_loc[sensor["id"]] = (loc_id, name)

        # Step 2: fetch latest measurement for every relevant sensor concurrently
        sensor_results = await asyncio.gather(
            *[_fetch_sensor(client, sid) for sid in sensor_to_loc]
        )

    # Aggregate
    param_values: dict[str, list[float]] = {}
    pm25_by_loc: dict[int, float] = {}

    for sensor_id, value in sensor_results:
        if value is None:
            continue
        loc_id, param_name = sensor_to_loc[sensor_id]
        param_values.setdefault(param_name, []).append(value)
        if param_name == "pm25":
            pm25_by_loc[loc_id] = value

    station_readings: list[StationReading] = []
    for loc_id, pm25_val in pm25_by_loc.items():
        meta = loc_meta[loc_id]
        station_readings.append(
            StationReading(
                name=meta["name"],
                lat=meta["lat"],
                lon=meta["lon"],
                aqi=_pm25_to_aqi(pm25_val),
            )
        )

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
                trend="stable",
            )
        )

    pm25_readings = param_values.get("pm25", [])
    overall_aqi = _pm25_to_aqi(_avg(pm25_readings)) if pm25_readings else 0

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
