import asyncio
import time
from datetime import datetime, timezone
from typing import Any

import httpx

from config import settings, THESS_LAT, THESS_LON
from models.schemas import PollutantReading, StationReading

OPENAQ_BASE = "https://api.openaq.org/v3"
SEARCH_RADIUS_M = 25_000 # how far to look for stations around Thessaloniki (in meters)
CACHE_TTL = 300  # seconds

_cache: dict[str, tuple[Any, float]] = {}

# Human-readable overrides for EEA station codes returned by OpenAQ
_STATION_NAMES: dict[str, str] = {
    "GR0018A": "Thessaloniki",
    "GR0020A": "Kordelio",
    "GR0046A": "Sindos",
}

# Only these stations are surfaced to the frontend
_ALLOWED_STATIONS = {"Thessaloniki", "Panorama", "Kordelio", "Sindos"}

# EPA AQI breakpoints (µg/m³, converted from ppb at 25°C) — must match ml/preprocessing.py
_NO2_BP = [
    (0.0,    100.0,   0,  50),
    (100.0,  188.0,  51, 100),
    (188.0,  677.0, 101, 150),
    (677.0, 1221.0, 151, 200),
    (1221.0, 2350.0, 201, 300),
]
_O3_BP = [
    (0.0,   118.0,   0,  50),
    (118.0, 157.0,  51, 100),
    (157.0, 196.0, 101, 150),
    (196.0, 392.0, 151, 200),
    (392.0, 784.0, 201, 300),
]
_SO2_BP = [
    (0.0,    92.0,   0,  50),
    (92.0,  197.0,  51, 100),
    (197.0, 485.0, 101, 150),
    (485.0, 797.0, 151, 200),
    (797.0, 1583.0, 201, 300),
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


def _piecewise_aqi(conc: float, breakpoints: list) -> int:
    for c_lo, c_hi, i_lo, i_hi in breakpoints:
        if c_lo <= conc <= c_hi:
            return round((i_hi - i_lo) / (c_hi - c_lo) * (conc - c_lo) + i_lo)
    return 300


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
) -> tuple[int, float | None, str | None]:
    resp = await client.get(
        f"{OPENAQ_BASE}/sensors/{sensor_id}/measurements",
        params={"limit": 1},
    )
    if resp.status_code != 200:
        return sensor_id, None, None
    results = resp.json().get("results", [])
    if not results:
        return sensor_id, None, None
    r = results[0]
    value = r.get("value")
    ts = r.get("period", {}).get("datetimeLast", {}).get("utc")
    return (
        sensor_id,
        float(value) if (value is not None and float(value) >= 0) else None,
        ts,
    )


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
    poll_by_loc: dict[int, dict[str, float]] = {}
    latest_ts: str | None = None

    for sensor_id, value, ts in sensor_results:
        if ts and (latest_ts is None or ts > latest_ts):
            latest_ts = ts
        if value is None:
            continue
        loc_id, param_name = sensor_to_loc[sensor_id]
        param_values.setdefault(param_name, []).append(value)
        if param_name in {"no2", "o3", "so2"}:
            poll_by_loc.setdefault(loc_id, {})[param_name] = value

    station_readings: list[StationReading] = []
    for loc_id, readings in poll_by_loc.items():
        meta = loc_meta[loc_id]
        if meta["name"] not in _ALLOWED_STATIONS:
            continue
        no2_aqi = _piecewise_aqi(readings.get("no2", 0.0), _NO2_BP)
        o3_aqi  = _piecewise_aqi(readings.get("o3",  0.0), _O3_BP)
        so2_aqi = _piecewise_aqi(readings.get("so2", 0.0), _SO2_BP)
        station_readings.append(
            StationReading(
                name=meta["name"],
                lat=meta["lat"],
                lon=meta["lon"],
                aqi=max(no2_aqi, o3_aqi, so2_aqi),
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

    no2_aqi     = _piecewise_aqi(_avg(param_values.get("no2", [])), _NO2_BP)
    o3_aqi      = _piecewise_aqi(_avg(param_values.get("o3",  [])), _O3_BP)
    so2_aqi     = _piecewise_aqi(_avg(param_values.get("so2", [])), _SO2_BP)
    overall_aqi = max(no2_aqi, o3_aqi, so2_aqi)

    return {
        "aqi": overall_aqi,
        "aqi_label": _aqi_label(overall_aqi),
        "updated_at": latest_ts or datetime.now(timezone.utc).isoformat(),
        "pollutants": pollutants,
        "stations": station_readings,
    }


async def fetch_air_quality() -> dict:
    key = "air_quality"
    prev: dict | None = None
    if key in _cache:
        value, ts = _cache[key]
        if time.monotonic() - ts < CACHE_TTL:
            return value
        prev = value  # expired — keep for trend comparison

    result = await _fetch()

    if prev:
        prev_vals = {p.name: p.value for p in prev["pollutants"]}
        for p in result["pollutants"]:
            old = prev_vals.get(p.name)
            if old and old > 0:
                delta = (p.value - old) / old
                if delta > 0.05:
                    p.trend = "up"
                elif delta < -0.05:
                    p.trend = "down"

    _cache[key] = (result, time.monotonic())
    return result
