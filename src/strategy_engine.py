import random
import numpy as np

tires = {
    "Soft": {"base": 90, "deg": 0.25},
    "Medium": {"base": 91.5, "deg": 0.15},
    "Hard": {"base": 93, "deg": 0.08}
}

def simulate_with_features(first_tire, second_tire, pit_lap, total_laps=60, pit_loss=22):
    total_time = 0

    for lap in range(1, total_laps + 1):

        if lap < pit_lap:
            base = tires[first_tire]["base"]
            deg = tires[first_tire]["deg"]
            stint_lap = lap

        elif lap == pit_lap:
            base = tires[first_tire]["base"]
            deg = tires[first_tire]["deg"]
            stint_lap = lap
            total_time += pit_loss

        else:
            base = tires[second_tire]["base"]
            deg = tires[second_tire]["deg"]
            stint_lap = lap - pit_lap

        lap_time = base + deg * stint_lap

        # Traffic probability
        if random.random() < 0.05:
            lap_time += random.uniform(0.3, 1.0)

        # Noise
        lap_time += random.uniform(-0.1, 0.1)

        total_time += lap_time

    return total_time
