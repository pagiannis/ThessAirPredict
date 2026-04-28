"""
Data cleaning and feature engineering for the AQI forecast model.

Expected input:  ml/data/pollution.xlsx
                 Columns: datetime, pm25, pm10, no2, o3, so2, co
                 Frequency: hourly

Output:          X (features), y (target AQI) ready for train_model.py
"""

import pandas as pd

RAW_PATH = "data/pollution.xlsx"


def load_raw(path: str = RAW_PATH) -> pd.DataFrame:
    # TODO: adjust sheet_name / header row to match actual file
    return pd.read_excel(path, parse_dates=["datetime"])


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["hour"] = df["datetime"].dt.hour
    df["day_of_week"] = df["datetime"].dt.dayofweek
    df["month"] = df["datetime"].dt.month
    return df


def build_features(df: pd.DataFrame):
    df = add_time_features(df)
    feature_cols = ["hour", "day_of_week", "month", "pm25", "pm10", "no2", "o3", "so2", "co"]
    X = df[feature_cols].dropna()
    y = df.loc[X.index, "aqi"]  # TODO: derive aqi column if not present
    return X, y


if __name__ == "__main__":
    df = load_raw()
    X, y = build_features(df)
    print(f"Features shape: {X.shape}, target shape: {y.shape}")
