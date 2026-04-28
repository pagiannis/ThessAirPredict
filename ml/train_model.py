"""
Train an AQI forecast model and export model.pkl.

After training, copy model.pkl to server/model/model.pkl.
Run: python train_model.py
"""

import pickle
from pathlib import Path

from preprocessing import load_raw, build_features
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

MODEL_OUT = Path("model.pkl")


def train():
    df = load_raw()
    X, y = build_features(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    mae = mean_absolute_error(y_test, model.predict(X_test))
    print(f"Test MAE: {mae:.2f} AQI points")

    with open(MODEL_OUT, "wb") as f:
        pickle.dump(model, f)
    print(f"Model saved → {MODEL_OUT}")
    print("Next: copy model.pkl to server/model/model.pkl")


if __name__ == "__main__":
    train()
