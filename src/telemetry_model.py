"""Train and persist a next-lap pace model from recent FastF1 race telemetry."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import fastf1
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import GroupShuffleSplit, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


MODEL_PATH = Path("models/latest_lap_time_model.joblib")
CATEGORICAL_FEATURES = ["Track", "Team", "Driver", "Compound"]
NUMERIC_FEATURES = [
    "LapNumber",
    "TyreLife",
    "CurrentLapTime",
    "SpeedMean",
    "SpeedMax",
    "ThrottleMean",
    "BrakeFraction",
    "RPMMean",
    "GearMean",
    "LapDistance",
]
FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES
TARGET = "NextLapTime"


def _completed_race_events(year: int) -> pd.DataFrame:
    schedule = fastf1.get_event_schedule(year, include_testing=False)
    if schedule.empty:
        return schedule

    events = schedule.copy()
    events["EventDate"] = pd.to_datetime(events["EventDate"], errors="coerce")
    events = events[
        (events["RoundNumber"] > 0)
        & events["EventDate"].notna()
        & (events["EventDate"].dt.date <= date.today())
    ]
    return events.sort_values(["EventDate", "RoundNumber"], ascending=False)


def _clean_lap(lap: pd.Series) -> bool:
    lap_time = lap.get("LapTime")
    if pd.isna(lap_time) or pd.notna(lap.get("PitInTime")) or pd.notna(lap.get("PitOutTime")):
        return False
    if "IsAccurate" in lap and not bool(lap.get("IsAccurate")):
        return False
    seconds = lap_time.total_seconds()
    return 45 <= seconds <= 180


def _telemetry_summary(lap) -> dict[str, float] | None:
    try:
        telemetry = lap.get_telemetry()
    except Exception:
        return None

    if telemetry.empty or "Speed" not in telemetry:
        return None

    def mean(channel: str) -> float:
        if channel not in telemetry:
            return float("nan")
        values = pd.to_numeric(telemetry[channel], errors="coerce")
        return float(values.mean()) if values.notna().any() else float("nan")

    brake = mean("Brake")
    if np.isfinite(brake) and brake > 1:
        brake /= 100.0

    distance = (
        pd.to_numeric(telemetry["Distance"], errors="coerce")
        if "Distance" in telemetry
        else None
    )
    return {
        "SpeedMean": mean("Speed"),
        "SpeedMax": float(pd.to_numeric(telemetry["Speed"], errors="coerce").max()),
        "ThrottleMean": mean("Throttle"),
        "BrakeFraction": brake,
        "RPMMean": mean("RPM"),
        "GearMean": mean("nGear"),
        "LapDistance": (
            float(distance.max())
            if distance is not None and distance.notna().any()
            else float("nan")
        ),
    }


def _session_rows(session, year: int, round_number: int) -> list[dict]:
    rows: list[dict] = []
    results = session.results
    driver_info = {}
    if results is not None and not results.empty:
        for _, result in results.iterrows():
            number = str(result.get("DriverNumber", ""))
            driver_info[number] = {
                "Driver": str(result.get("Abbreviation", "UNK")),
                "Team": str(result.get("TeamName", "UNK")),
            }

    for driver_number, driver_laps in session.laps.groupby("DriverNumber", sort=False):
        driver_laps = driver_laps.sort_values("LapNumber").reset_index(drop=True)
        identity = driver_info.get(str(driver_number), {"Driver": str(driver_number), "Team": "UNK"})

        for index in range(len(driver_laps) - 1):
            current = driver_laps.iloc[index]
            following = driver_laps.iloc[index + 1]
            if not _clean_lap(current) or not _clean_lap(following):
                continue
            if int(following["LapNumber"]) != int(current["LapNumber"]) + 1:
                continue
            compound = str(current.get("Compound", "UNKNOWN")).upper()
            if compound != str(following.get("Compound", "UNKNOWN")).upper():
                continue

            summary = _telemetry_summary(driver_laps.iloc[index])
            if summary is None or not np.isfinite(summary["SpeedMean"]):
                continue

            tyre_life = pd.to_numeric(current.get("TyreLife"), errors="coerce")
            rows.append(
                {
                    "Year": year,
                    "Round": round_number,
                    "EventKey": f"{year}-{round_number}",
                    "Track": str(session.event.get("EventName", "Unknown")),
                    **identity,
                    "Compound": compound,
                    "LapNumber": float(current["LapNumber"]),
                    "TyreLife": float(tyre_life) if pd.notna(tyre_life) else np.nan,
                    "CurrentLapTime": float(current["LapTime"].total_seconds()),
                    **summary,
                    "NextLapTime": float(following["LapTime"].total_seconds()),
                }
            )
    return rows


def build_recent_dataset(number_of_races: int = 3, year: int | None = None) -> tuple[pd.DataFrame, list[str]]:
    """Download recent completed race sessions and extract clean next-lap examples."""
    season = year or date.today().year
    cache_dir = Path("fastf1_cache")
    cache_dir.mkdir(exist_ok=True)
    fastf1.Cache.enable_cache(str(cache_dir))

    events = _completed_race_events(season)
    if events.empty and year is None:
        season -= 1
        events = _completed_race_events(season)
    if events.empty:
        raise RuntimeError(f"FastF1 has no completed race events for {season}.")

    rows: list[dict] = []
    loaded_events: list[str] = []
    failures: list[str] = []
    for _, event in events.iterrows():
        round_number = int(event["RoundNumber"])
        name = str(event.get("EventName", f"Round {round_number}"))
        try:
            session = fastf1.get_session(season, round_number, "R")
            session.load(telemetry=True, weather=False, messages=False)
            event_rows = _session_rows(session, season, round_number)
            if event_rows:
                rows.extend(event_rows)
                loaded_events.append(f"{season} {name}")
        except Exception as error:
            failures.append(f"{name}: {error}")
        if len(loaded_events) >= number_of_races:
            break

    if not rows:
        detail = "; ".join(failures[-3:])
        raise RuntimeError(f"Could not extract usable telemetry from completed races. {detail}")

    return pd.DataFrame(rows), loaded_events


def _make_pipeline() -> Pipeline:
    preprocessing = ColumnTransformer(
        transformers=[
            (
                "categories",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                CATEGORICAL_FEATURES,
            ),
            ("numbers", SimpleImputer(strategy="median"), NUMERIC_FEATURES),
        ]
    )
    return Pipeline(
        [
            ("features", preprocessing),
            (
                "model",
                RandomForestRegressor(
                    n_estimators=250,
                    min_samples_leaf=2,
                    max_features=0.9,
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )


def train_latest_model(number_of_races: int = 3, year: int | None = None) -> dict:
    """Fit and save a next-lap prediction model, evaluating on a held-out race."""
    dataset, events = build_recent_dataset(number_of_races=number_of_races, year=year)
    x = dataset[FEATURES]
    y = dataset[TARGET]
    groups = dataset["EventKey"]

    if groups.nunique() > 1:
        splitter = GroupShuffleSplit(n_splits=1, test_size=1 / groups.nunique(), random_state=42)
        train_indices, test_indices = next(splitter.split(x, y, groups))
        validation_method = "held-out race weekend"
    else:
        train_indices, test_indices = train_test_split(
            np.arange(len(dataset)), test_size=0.2, random_state=42
        )
        validation_method = "random lap split (only one race weekend available)"

    if len(train_indices) < 10 or len(test_indices) < 2:
        raise RuntimeError("Not enough clean consecutive laps to train and validate the model.")

    model = _make_pipeline()
    model.fit(x.iloc[train_indices], y.iloc[train_indices])
    actual = y.iloc[test_indices]
    predicted = model.predict(x.iloc[test_indices])
    metrics = {
        "mae_seconds": float(mean_absolute_error(actual, predicted)),
        "r2": float(r2_score(actual, predicted)) if len(actual) > 1 else float("nan"),
        "train_laps": int(len(train_indices)),
        "validation_laps": int(len(test_indices)),
        "validation_method": validation_method,
    }

    validation_data = dataset.iloc[test_indices].copy().reset_index(drop=True)
    bundle = {
        "model": model,
        "metrics": metrics,
        "events": events,
        "validation_data": validation_data,
        "trained_year": int(year or date.today().year),
    }
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, MODEL_PATH)
    return bundle


def load_saved_model() -> dict | None:
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)


def predict_next_lap(bundle: dict, scenario: pd.Series | dict) -> float:
    row = pd.DataFrame([{feature: scenario[feature] for feature in FEATURES}])
    return float(bundle["model"].predict(row)[0])
