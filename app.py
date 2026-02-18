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
    
from src.real_data_model import load_hamilton_medium_degradation

st.markdown("---")
st.subheader("Real Data Degradation Model (Hamilton - Monaco 2023)")

if st.button("Load Real Data Model"):
    base, deg = load_hamilton_medium_degradation()

    st.write(f"Estimated Base Lap Time: {round(base,2)} sec")
    st.write(f"Estimated Degradation per Lap: {round(deg,5)} sec")
