import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from src.monte_carlo import run_monte_carlo

st.set_page_config(page_title="F1 Strategy Analytics", layout="wide")

st.title("🏎️ F1 Strategy Analytics Dashboard")

st.markdown("Advanced race strategy simulation using probabilistic modeling and real telemetry integration.")

col1, col2 = st.columns(2)

with col1:
    first = st.selectbox("First Stint Tire", ["Soft", "Medium", "Hard"])
    second = st.selectbox("Second Stint Tire", ["Soft", "Medium", "Hard"])
    pit_lap = st.slider("Pit Lap", 10, 40, 26)
    simulations = st.slider("Monte Carlo Runs", 100, 2000, 1000)

if st.button("Run Simulation"):

    mean, std, distribution = run_monte_carlo(first, second, pit_lap, simulations)

    colA, colB, colC = st.columns(3)

    colA.metric("Average Race Time (s)", round(mean, 2))
    colB.metric("Risk (Std Dev)", round(std, 3))
    colC.metric("Best Simulated Time", round(min(distribution), 2))

    fig, ax = plt.subplots(figsize=(10,5))
    ax.hist(distribution, bins=40)
    ax.axvline(mean, linestyle='--')
    ax.set_title("Monte Carlo Race Time Distribution")
    ax.set_xlabel("Total Race Time (seconds)")
    ax.set_ylabel("Frequency")

    st.pyplot(fig)
    
from src.real_data_model import (
    load_hamilton_medium_degradation,
    load_hamilton_medium_degradation_silverstone,
)
from src.telemetry_model import load_saved_model, predict_next_lap, train_latest_model

st.markdown("---")
st.subheader("Real Data Degradation Model (Hamilton - 2023)")

track = st.selectbox("Track", ["Monaco", "Silverstone"], key="track_select")

if st.button("Load Real Data Model"):
    if track == "Monaco":
        base, deg = load_hamilton_medium_degradation()
    else:
        base, deg = load_hamilton_medium_degradation_silverstone()

    st.write(f"Track: {track}")
    st.write(f"Estimated Base Lap Time: {round(base,2)} sec")
    st.write(f"Estimated Degradation per Lap: {round(deg,5)} sec")

st.markdown("---")
st.subheader("Latest Race Car Telemetry Model")
st.write(
    "Train a next-lap pace model from recent completed race weekends. "
    "It uses track, team, driver, tyre age, and car telemetry summaries."
)

race_count = st.slider("Recent race weekends", 1, 5, 3, key="telemetry_race_count")
if st.button("Train / Refresh Telemetry Model"):
    with st.spinner("Loading recent FastF1 race telemetry and training the model..."):
        try:
            st.session_state["telemetry_model_bundle"] = train_latest_model(race_count)
        except Exception as error:
            st.error(f"Could not train the telemetry model: {error}")

bundle = st.session_state.get("telemetry_model_bundle")
if bundle is None:
    try:
        bundle = load_saved_model()
        if bundle is not None:
            st.session_state["telemetry_model_bundle"] = bundle
    except Exception as error:
        st.warning(f"Could not load the saved telemetry model: {error}")

if bundle is not None:
    metrics = bundle["metrics"]
    st.caption("Training events: " + " · ".join(bundle["events"]))
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Validation MAE", f"{metrics['mae_seconds']:.3f} s")
    metric_col2.metric("Validation R²", f"{metrics['r2']:.3f}")
    metric_col3.metric("Validation laps", metrics["validation_laps"])
    st.caption(f"Evaluation: {metrics['validation_method']}")

    validation_data = bundle["validation_data"]
    track_options = sorted(validation_data["Track"].dropna().unique())
    selected_track = st.selectbox("Validation track", track_options, key="prediction_track")
    track_data = validation_data[validation_data["Track"] == selected_track]
    team_options = sorted(track_data["Team"].dropna().unique())
    selected_team = st.selectbox("Team / car", team_options, key="prediction_team")
    team_data = track_data[track_data["Team"] == selected_team]
    driver_options = sorted(team_data["Driver"].dropna().unique())
    selected_driver = st.selectbox("Driver", driver_options, key="prediction_driver")
    examples = team_data[team_data["Driver"] == selected_driver].reset_index(drop=True)
    example_labels = [
        f"Lap {int(row.LapNumber)} · {row.Compound} · tyre age {row.TyreLife:.0f} laps"
        for row in examples.itertuples()
    ]
    selected_example = st.selectbox("Telemetry sample", range(len(examples)), format_func=lambda i: example_labels[i])
    scenario = examples.iloc[selected_example]
    predicted = predict_next_lap(bundle, scenario)
    actual = float(scenario["NextLapTime"])
    prediction_col1, prediction_col2, prediction_col3 = st.columns(3)
    prediction_col1.metric("Predicted next lap", f"{predicted:.3f} s")
    prediction_col2.metric("Actual next lap", f"{actual:.3f} s")
    prediction_col3.metric("Absolute error", f"{abs(predicted - actual):.3f} s")
    st.caption(
        f"Out-of-sample example: {scenario['Driver']} ({scenario['Team']}) at "
        f"{scenario['Track']}, lap {int(scenario['LapNumber'])}."
    )
