import fastf1
from fastf1 import get_session
import os
import numpy as np

def _load_driver_medium_degradation(season, event, driver_code):
    os.makedirs("fastf1_cache", exist_ok=True)
    fastf1.Cache.enable_cache("fastf1_cache")

    session = get_session(season, event, 'R')
    session.load()

    laps = session.laps
    driver_laps = laps.pick_drivers(driver_code)

    data = driver_laps[['LapNumber', 'LapTime', 'Compound']].copy()
    data = data[data['Compound'] == 'MEDIUM']
    data = data.dropna(subset=['LapTime'])

    if data.empty:
        raise ValueError(
            f"No MEDIUM laps found for {driver_code} in {season} event {event}."
        )

    data['LapTime_sec'] = data['LapTime'].dt.total_seconds()
    data['StintLap'] = range(1, len(data) + 1)

    coeffs = np.polyfit(data['StintLap'], data['LapTime_sec'], 1)
    slope = coeffs[0]
    intercept = coeffs[1]

    return intercept, slope

def load_hamilton_medium_degradation():
    return _load_driver_medium_degradation(2023, 6, 'HAM')  # Monaco 2023

def load_hamilton_medium_degradation_silverstone():
    # British Grand Prix 2023 (Silverstone)
    return _load_driver_medium_degradation(2023, 10, 'HAM')
