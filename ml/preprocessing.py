"""
Data cleaning and feature engineering for the AQI forecast model.

Inputs:  ml/data/thessaloniki_pollutants_YYYY_MM.csv  (no2, o3, co, so2 — hourly)
         ml/data/weather_data_2023_2024.csv           (temperature, humidity, wind — hourly)

Output:  X (features DataFrame), y (AQI Series) ready for train_model.py

AQI is computed as the max sub-index across NO2, O3, and SO2 using EPA piecewise
breakpoints (converted from ppb to µg/m³). PM2.5 is not available in this dataset.
"""

import glob
from pathlib import Path

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

FEATURE_COLS = [
    "hour", "day_of_week", "month",
    "no2_conc", "o3_conc", "co_conc", "so2_conc",
    "temperature", "humidity", "precipitation", "wind_speed",
]


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
    df["hour"]        = df["time"].dt.hour
    df["day_of_week"] = df["time"].dt.dayofweek
    df["month"]       = df["time"].dt.month
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
    return df


def build_features(df: pd.DataFrame):
    X = df[FEATURE_COLS].dropna()
    y = df.loc[X.index, "aqi"]
    return X, y


if __name__ == "__main__":
    df = load_and_merge()
    X, y = build_features(df)
    print(f"Dataset:  {len(df):,} rows  ({df['time'].min()} → {df['time'].max()})")
    print(f"Features: {X.shape[1]} columns — {list(X.columns)}")
    print(f"AQI:      min={y.min()}  max={y.max()}  mean={y.mean():.1f}  std={y.std():.1f}")
    print(f"\nMissing values per column:\n{df[FEATURE_COLS + ['aqi']].isnull().sum()}")
