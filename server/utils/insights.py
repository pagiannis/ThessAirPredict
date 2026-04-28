"""
Post-prediction analysis: trend detection, AQI label, health recommendations.
Will be called by routes after prediction.py returns a forecast.
"""


def detect_trend(current_aqi: int, forecast_aqi: int) -> str:
    delta = forecast_aqi - current_aqi
    if delta > 5:
        return "up"
    if delta < -5:
        return "down"
    return "stable"
