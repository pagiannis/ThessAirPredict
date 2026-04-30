"""
Train an AQI forecast model and save model.pkl.

Run from the ml/ directory (with .venv active):
    python train_model.py

After training, copy model.pkl to server/model/model.pkl.
"""

import pickle
from pathlib import Path

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

from preprocessing import load_and_merge, build_features_multistep

MODEL_OUT = Path("model.pkl")


def print_feature_importances(model, feature_names):
    pairs = sorted(zip(feature_names, model.feature_importances_), key=lambda x: x[1], reverse=True)
    print("\nFeature importances:")
    for name, imp in pairs:
        bar = "█" * int(imp * 50)
        print(f"  {name:<22} {bar} {imp:.3f}")


def train():
    print("Loading and merging data...")
    df = load_and_merge()

    print("Building multi-step training set...")
    X, y, base_times = build_features_multistep(df)
    print(f"  {len(X):,} training pairs  |  {X.shape[1]} features")

    print("\nSplitting: train=2023 base times, test=2024 base times...")
    train_mask = base_times.dt.year < 2024
    test_mask  = base_times.dt.year >= 2024
    X_train, X_test = X[train_mask], X[test_mask]
    y_train, y_test = y[train_mask], y[test_mask]
    print(f"  Train: {len(X_train):,} rows  |  Test: {len(X_test):,} rows")

    print("\nTraining RandomForest...")
    model = RandomForestRegressor(
        n_estimators=300,
        min_samples_leaf=3,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2  = r2_score(y_test, y_pred)
    print(f"\n  MAE : {mae:.2f} AQI points")
    print(f"  R²  : {r2:.3f}")

    print_feature_importances(model, X.columns)

    with open(MODEL_OUT, "wb") as f:
        pickle.dump(model, f)

    print(f"\nModel saved → {MODEL_OUT}")
    print("Next step: copy model.pkl to ../server/model/model.pkl")


if __name__ == "__main__":
    train()
