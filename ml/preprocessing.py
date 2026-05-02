"""
Data cleaning and feature engineering for the AQI forecast model.

Inputs:  ml/data/thessaloniki_pollutants_YYYY_MM.csv  (no2, o3, co, so2 — hourly)
         ml/data/weather_data_2023_2024.csv           (temperature, humidity, wind — hourly)

Output:  X, y, base_times  via build_features_multistep()

Training design (multi-step forecasting):
  For each (timestamp t, horizon h in [3, 6, ..., 48]):
    Features : pollutant/weather readings at t  +  time-of-day at t+h  +  h
    Target   : AQI at t+h

  Weather at t (not t+h) is used as a feature. Using actual future weather in training
  caused the model to over-rely on temperature as a same-time AQI correlate rather than
  a genuine predictor, hurting generalisation (MAE 6.39 vs 5.75).
  Using FUTURE AQI as the target (not current) prevents data leakage where the model
  would otherwise just learn to invert the AQI formula.

AQI is computed as the max sub-index across NO2, O3, and SO2 using EPA piecewise
breakpoints (converted from ppb to µg/m³). PM2.5 is not available in this dataset.
"""

import glob
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).parent / "data"

# EPA breakpoints (µg/m³) — converted from ppb at 25°C, 1 atm
# Format: (conc_lo, conc_hi, aqi_lo, aqi_hi)
_NO2_BP = [  # 1 ppb NO2 ≈ 1.88 µg/m³
    (0.0,    100.0,   0,  50),
    (100.0,  188.0,  51, 100),
    (188.0,  677.0, 101, 150),
    (677.0, 1221.0, 151, 200),
    (1221.0, 2350.0, 201, 300),
]
_O3_BP = [  # 1 ppb O3 ≈ 1.96 µg/m³
    (0.0,   118.0,   0,  50),
    (118.0, 157.0,  51, 100),
    (157.0, 196.0, 101, 150),
    (196.0, 392.0, 151, 200),
    (392.0, 784.0, 201, 300),
]
_SO2_BP = [  # 1 ppb SO2 ≈ 2.62 µg/m³
    (0.0,   92.0,   0,  50),
    (92.0,  197.0,  51, 100),
    (197.0, 485.0, 101, 150),
    (485.0, 797.0, 151, 200),
    (797.0, 1583.0, 201, 300),
]

HORIZONS = list(range(3, 49, 3))  # [3, 6, 9, ..., 48]

# Pollutant + lag columns come from the base timestamp t
_POLLUTANT_LAG_COLS = [
    "no2_conc", "o3_conc", "co_conc", "so2_conc",
    "aqi_lag_1h", "aqi_lag_3h", "aqi_lag_6h",
]
# Weather columns are looked up at the FUTURE timestamp t+h in build_features_multistep
_WEATHER_COLS = ["temperature", "humidity", "precipitation", "wind_speed"]

_POLLUTANT_WEATHER_COLS = _POLLUTANT_LAG_COLS + _WEATHER_COLS

FEATURE_COLS = ["hour_sin", "hour_cos", "day_of_week", "month_sin", "month_cos", "hours_ahead"] + _POLLUTANT_WEATHER_COLS


def _piecewise_aqi(conc: float, breakpoints: list) -> int:
    for c_lo, c_hi, i_lo, i_hi in breakpoints:
        if c_lo <= conc <= c_hi:
            return round((i_hi - i_lo) / (c_hi - c_lo) * (conc - c_lo) + i_lo)
    return 300  # cap at 300 for out-of-range values


def load_pollutants() -> pd.DataFrame:
    files = sorted(glob.glob(str(DATA_DIR / "thessaloniki_pollutants*.csv")))
    if not files:
        raise FileNotFoundError(f"No pollutant CSVs found in {DATA_DIR}")
    dfs = [pd.read_csv(f, parse_dates=["time"]) for f in files]
    df = pd.concat(dfs, ignore_index=True)
    df = df.sort_values("time").drop_duplicates("time").reset_index(drop=True)
    df = df.drop(columns=["level", "spatial_ref"], errors="ignore")
    return df


def load_weather() -> pd.DataFrame:
    path = DATA_DIR / "weather_data_2023_2024.csv"
    # Skip 3 metadata rows (lat/lon line, values line, blank line); row 4 is the real header
    df = pd.read_csv(path, skiprows=3, parse_dates=["time"])
    df.columns = ["time", "temperature", "humidity", "precipitation", "wind_speed", "wind_gusts"]
    df = df.sort_values("time").drop_duplicates("time").reset_index(drop=True)
    return df


def compute_aqi(df: pd.DataFrame) -> pd.Series:
    no2 = df["no2_conc"].apply(lambda x: _piecewise_aqi(x, _NO2_BP))
    o3  = df["o3_conc"].apply(lambda x: _piecewise_aqi(x, _O3_BP))
    so2 = df["so2_conc"].apply(lambda x: _piecewise_aqi(x, _SO2_BP))
    return pd.concat([no2, o3, so2], axis=1).max(axis=1)


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    hour  = df["time"].dt.hour
    month = df["time"].dt.month
    df["day_of_week"] = df["time"].dt.dayofweek
    df["hour_sin"]    = np.sin(2 * np.pi * hour / 24)
    df["hour_cos"]    = np.cos(2 * np.pi * hour / 24)
    df["month_sin"]   = np.sin(2 * np.pi * (month - 1) / 12)
    df["month_cos"]   = np.cos(2 * np.pi * (month - 1) / 12)
    return df


def load_and_merge() -> pd.DataFrame:
    pollutants = load_pollutants()
    weather    = load_weather()

    # Floor to hour so both timestamp formats align cleanly
    pollutants["time"] = pollutants["time"].dt.floor("h")
    weather["time"]    = weather["time"].dt.floor("h")

    df = pollutants.merge(weather, on="time", how="inner")
    df = add_time_features(df)
    df["aqi"] = compute_aqi(df)

    # Lag features: look up actual AQI at t-1h, t-3h, t-6h by time index.
    # Rows where the lagged timestamp doesn't exist in the data become NaN
    # and are dropped downstream by build_features_multistep's dropna().
    aqi_lookup = df.set_index("time")["aqi"]
    for h, col in [(1, "aqi_lag_1h"), (3, "aqi_lag_3h"), (6, "aqi_lag_6h")]:
        df[col] = aqi_lookup.reindex(df["time"] - pd.Timedelta(hours=h)).values

    return df


def build_features_multistep(df: pd.DataFrame):
    """
    Returns (X, y, base_times) where each row is one (timestamp, horizon) training pair.

    base_times is the original timestamp for each row — used for temporal train/test
    splitting in train_model.py (train on 2023 base times, test on 2024).
    """
    indexed = df.set_index("time")
    all_X, all_y, all_t = [], [], []

    for h in HORIZONS:
        # All base features (pollutants, weather, lags) at current time t
        base = indexed[_POLLUTANT_WEATHER_COLS].copy()

        # Shift future AQI index back by h hours so it aligns with the base timestamp
        delta = pd.Timedelta(hours=h)
        future_aqi = indexed["aqi"].copy()
        future_aqi.index = future_aqi.index - delta

        chunk = base.join(future_aqi.rename("future_aqi"), how="inner").dropna()

        future_time = chunk.index + delta
        chunk = chunk.copy()
        chunk["hour_sin"]    = np.sin(2 * np.pi * future_time.hour / 24)
        chunk["hour_cos"]    = np.cos(2 * np.pi * future_time.hour / 24)
        chunk["day_of_week"] = future_time.dayofweek
        chunk["month_sin"]   = np.sin(2 * np.pi * (future_time.month - 1) / 12)
        chunk["month_cos"]   = np.cos(2 * np.pi * (future_time.month - 1) / 12)
        chunk["hours_ahead"] = h

        all_X.append(chunk[FEATURE_COLS])
        all_y.append(chunk["future_aqi"])
        all_t.append(pd.Series(chunk.index, name="base_time"))

    X          = pd.concat(all_X).reset_index(drop=True)
    y          = pd.concat(all_y).reset_index(drop=True)
    base_times = pd.concat(all_t).reset_index(drop=True)
    return X, y, base_times


if __name__ == "__main__":
    df = load_and_merge()
    X, y, base_times = build_features_multistep(df)
    print(f"Base dataset : {len(df):,} hourly rows  ({df['time'].min()} → {df['time'].max()})")
    print(f"Training rows: {len(X):,}  ({len(HORIZONS)} horizons × base rows)")
    print(f"Features     : {X.shape[1]} — {list(X.columns)}")
    print(f"AQI target   : min={y.min():.0f}  max={y.max():.0f}  mean={y.mean():.1f}  std={y.std():.1f}")
    print(f"\nMissing values:\n{X.isnull().sum().to_string()}")
