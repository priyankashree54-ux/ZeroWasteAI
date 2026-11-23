"""Trains a Random Forest to guess how many kg of food will be left over in a day."""
import joblib, os
import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from data_gen import generate, VENDOR_TYPES

FEATURES = ["day_of_week", "meals_prepared", "expected_footfall", "festival", "rain"]
PATH = "surplus_model.joblib"

def encode(df):
    X = df[FEATURES].copy()
    for v in VENDOR_TYPES:
        X["vt_" + v] = (df["vendor_type"] == v).astype(int)
    return X

def train():
    df = generate()
    X, y = encode(df), df["surplus_kg"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=1)
    m = RandomForestRegressor(n_estimators=200, random_state=1, n_jobs=-1).fit(Xtr, ytr)
    p = m.predict(Xte)
    metrics = {"mae": round(mean_absolute_error(yte, p), 2), "r2": round(r2_score(yte, p), 3)}
    joblib.dump((m, list(X.columns), metrics), PATH)
    return m, list(X.columns), metrics

def load():
    return joblib.load(PATH) if os.path.exists(PATH) else train()

def predict(vendor_type, day_of_week, meals_prepared, expected_footfall, festival, rain):
    m, cols, _ = load()
    row = pd.DataFrame([dict(vendor_type=vendor_type, day_of_week=day_of_week,
                             meals_prepared=meals_prepared, expected_footfall=expected_footfall,
                             festival=festival, rain=rain)])
    X = encode(row).reindex(columns=cols, fill_value=0)
    return round(float(m.predict(X)[0]), 1)

if __name__ == "__main__":
    print(train()[2])
