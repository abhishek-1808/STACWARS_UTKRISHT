"""Bonus: solar radiation regression.

Usage:  python src/model.py [--csv data/SolarPrediction.csv]

Two evaluations are reported:
  * random 80/20 split - what the problem statement asks for, but optimistic,
                         because 5-minute readings from one day are near-duplicates
  * day-grouped split  - whole days held out; the honest estimate
"""
import argparse
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GroupShuffleSplit, train_test_split

from common import load_data, OUT_DIR, DEFAULT_CSV

SEED = 42


def make_features(df):
    X = pd.DataFrame(index=df.index)
    X["Temperature"] = df["Temperature"]
    X["Pressure"] = df["Pressure"]
    X["Humidity"] = df["Humidity"]
    X["WindSpeed"] = df["Speed"]
    # wind direction and time of day are circular -> sin/cos encoding
    X["WindDir_sin"] = np.sin(np.deg2rad(df["WindDirection(Degrees)"]))
    X["WindDir_cos"] = np.cos(np.deg2rad(df["WindDirection(Degrees)"]))
    X["Time_sin"] = np.sin(2 * np.pi * df["MinuteOfDay"] / 1440)
    X["Time_cos"] = np.cos(2 * np.pi * df["MinuteOfDay"] / 1440)
    X["DayOfYear"] = df["Datetime"].dt.dayofyear
    X["MinSinceSunrise"] = df["MinSinceSunrise"]
    X["MinToSunset"] = df["MinToSunset"]
    X["DayFraction"] = (df["MinSinceSunrise"] / df["DayLengthMin"]).clip(0, 1)
    return X


def evaluate(name, model, Xtr, Xte, ytr, yte):
    model.fit(Xtr, ytr)
    pred = model.predict(Xte)
    rmse = float(np.sqrt(mean_squared_error(yte, pred)))
    r2 = float(r2_score(yte, pred))
    print(f"{name:<22} RMSE = {rmse:8.2f}   R2 = {r2:6.3f}")
    return {"model": name, "RMSE": rmse, "R2": r2}


def new_models():
    return {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(
            n_estimators=300, min_samples_leaf=3, n_jobs=-1, random_state=SEED),
    }


def main(csv):
    OUT_DIR.mkdir(exist_ok=True)
    df = load_data(csv)
    X, y = make_features(df), df["Radiation"]
    rows = []

    print("== Random 80/20 split ==")
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=SEED)
    for n, m in new_models().items():
        rows.append({"split": "random", **evaluate(n, m, Xtr, Xte, ytr, yte)})

    print("\n== Day-grouped 80/20 split (whole days held out) ==")
    tr, te = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=SEED)
                  .split(X, y, groups=df["Date"]))
    Xtr, Xte, ytr, yte = X.iloc[tr], X.iloc[te], y.iloc[tr], y.iloc[te]
    rf = None
    for n, m in new_models().items():
        rows.append({"split": "day-grouped", **evaluate(n, m, Xtr, Xte, ytr, yte)})
        if n == "Random Forest":
            rf = m
    pd.DataFrame(rows).to_csv(OUT_DIR / "model_scores.csv", index=False)

    imp = pd.DataFrame({
        "impurity": rf.feature_importances_,
        "permutation": permutation_importance(
            rf, Xte, yte, n_repeats=5, random_state=SEED, n_jobs=-1).importances_mean,
    }, index=X.columns).sort_values("permutation", ascending=False)
    imp.to_csv(OUT_DIR / "feature_importance.csv")
    print("\nFeature importance (Random Forest, held-out days):\n", imp.round(4))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=str(DEFAULT_CSV))
    main(ap.parse_args().csv)
