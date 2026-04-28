"""
ML inference wrapper. Loads the trained model from server/model/model.pkl
and exposes a predict() function for use in routes.
Replace the sinusoidal forecaster.py once model.pkl is in place.
"""

import pickle
from pathlib import Path

import numpy as np

_MODEL_PATH = Path(__file__).parent.parent / "model" / "model.pkl"
_model = None


def _load_model():
    global _model
    if _model is None:
        with open(_MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
    return _model


def predict(features: dict) -> int:
    """Return predicted AQI for the given feature dict."""
    model = _load_model()
    X = np.array([[
        features["hour"],
        features["day_of_week"],
        features["month"],
        features["pm25"],
        features["pm10"],
        features["no2"],
        features["o3"],
        features["so2"],
        features["co"],
    ]])
    return int(round(model.predict(X)[0]))
