import numpy as np
from src.strategy_engine import simulate_with_features

def run_monte_carlo(first_tire, second_tire, pit_lap, simulations=500):
    results = []

    for _ in range(simulations):
        race_time = simulate_with_features(first_tire, second_tire, pit_lap)
        results.append(race_time)

    return np.mean(results), np.std(results), results
