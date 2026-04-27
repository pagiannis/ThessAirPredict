from typing import Literal
from pydantic import BaseModel

AqiLabel = Literal["Good", "Moderate", "Unhealthy", "Very Unhealthy", "Hazardous"]
Trend = Literal["up", "down", "stable"]


class PollutantReading(BaseModel):
    name: str
    value: float
    unit: str
    trend: Trend


class StationReading(BaseModel):
    name: str
    x: float
    y: float
    aqi: int


class AirQualityResponse(BaseModel):
    aqi: int
    aqi_label: AqiLabel
    updated_at: str
    pollutants: list[PollutantReading]
    stations: list[StationReading]


class ForecastPoint(BaseModel):
    time: str
    aqi: int


class ForecastResponse(BaseModel):
    forecast: list[ForecastPoint]
