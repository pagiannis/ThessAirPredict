import math
import random
from datetime import datetime

from models.schemas import ForecastPoint


def _daily_factor(hour: int) -> float:
    """Rush-hour-weighted daily pattern: peaks ~8h and ~18h, low overnight."""
    morning = math.exp(-0.5 * ((hour - 8) / 3) ** 2)
    evening = math.exp(-0.5 * ((hour - 18) / 3) ** 2)
    return 0.18 * (morning + evening) - 0.06  # range ≈ [-0.06, +0.30]


def generate(current_aqi: int, hours: int = 48, step_h: int = 3) -> list[ForecastPoint]:
    """
    Pattern-based 48-hour forecast seeded from current AQI.
    Uses a sinusoidal daily cycle (rush-hour peaks) plus day-to-day drift.
    Replace with an ML/Claude API model when training data is available.
    """
    seed = int(datetime.now().strftime("%Y%m%d"))
    rng = random.Random(seed)

    now_hour = datetime.now().hour
    points: list[ForecastPoint] = []

    for h in range(0, hours + 1, step_h):
        hour = (now_hour + h) % 24
        daily = _daily_factor(hour)

        # Slow multi-day drift
        drift = 0.04 * math.sin(2 * math.pi * h / 72)

        noise = rng.gauss(0, 2.5)
        aqi = round(current_aqi * (1 + daily + drift) + noise)
        aqi = max(0, min(500, aqi))

        label = "Now" if h == 0 else f"+{h}h"
        points.append(ForecastPoint(time=label, aqi=aqi))

    return points
