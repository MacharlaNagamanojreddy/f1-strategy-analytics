import fastf1
from fastf1 import get_session
import os
import numpy as np

def load_hamilton_medium_degradation():

    os.makedirs("fastf1_cache", exist_ok=True)
    fastf1.Cache.enable_cache("fastf1_cache")

    session = get_session(2023, 6, 'R')  # Monaco 2023
    session.load()

    laps = session.laps
    ham_laps = laps.pick_drivers('HAM')

    data = ham_laps[['LapNumber', 'LapTime', 'Compound']].copy()
    data = data[data['Compound'] == 'MEDIUM']
    data = data.dropna(subset=['LapTime'])

    data['LapTime_sec'] = data['LapTime'].dt.total_seconds()
    data['StintLap'] = range(1, len(data) + 1)

    coeffs = np.polyfit(data['StintLap'], data['LapTime_sec'], 1)

    slope = coeffs[0]
    intercept = coeffs[1]

    return intercept, slope
