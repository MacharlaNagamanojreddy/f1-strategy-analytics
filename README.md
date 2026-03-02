# F1 Strategy Analytics

A Python-based Formula 1 race strategy simulator with Monte Carlo analysis and real race-data tyre degradation modeling.

This project provides:
- Interactive strategy simulation in Streamlit
- Probabilistic race-time outcomes via Monte Carlo runs
- Real-data degradation fitting using FastF1 (Hamilton, 2023 Monaco and Silverstone)

![F1 Strategy Analytics](https://github.com/user-attachments/assets/7efd5e97-d4e1-47e2-a526-f8b3050717d2)

## Features

- **Strategy simulation engine**
  - Two-stint race simulation (`first_tire`, `second_tire`, `pit_lap`)
  - Per-compound base pace and degradation modeling
  - Pit-stop loss modeling
  - Traffic and random lap-noise effects
- **Monte Carlo analysis**
  - Configurable number of simulation runs
  - Mean race time, standard deviation, and best-case result
  - Histogram distribution plot in dashboard
- **Real-data degradation model**
  - FastF1 session ingestion with local caching
  - Medium compound lap extraction for Hamilton
  - Linear fit returning base lap time (intercept) and degradation slope
  - Track options in UI: **Monaco 2023** and **Silverstone 2023**

## Tech Stack

- Python
- Streamlit
- NumPy
- Pandas
- Matplotlib
- FastF1

## Project Structure

```text
f1-strategy-analytics/
├── app.py                    # Streamlit dashboard
├── requirements.txt          # Python dependencies
├── src/
│   ├── strategy_engine.py    # Per-lap strategy simulation logic
│   ├── monte_carlo.py        # Monte Carlo driver for repeated runs
│   └── real_data_model.py    # FastF1-based degradation fitting
├── notebooks/
│   └── exploration.ipynb     # Experimentation notebook
└── fastf1_cache/             # Local API cache (created/used at runtime)
```

## Local Setup

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit app

```bash
streamlit run app.py
```

Open in browser:

- `http://localhost:8501`

## Dashboard Usage

### Strategy Simulation

1. Select first and second stint tyre compounds.
2. Set pit lap and Monte Carlo run count.
3. Click **Run Simulation**.
4. Review average time, risk (std dev), best simulated time, and distribution chart.

### Real Data Degradation

1. Select track (**Monaco** or **Silverstone**).
2. Click **Load Real Data Model**.
3. Review estimated base lap time and degradation per lap from FastF1 race data.

## Notes

- The first FastF1 load can take longer because session data is downloaded and cached in `fastf1_cache/`.
- Internet access is required to fetch uncached FastF1 data.

## Author

Macharla Naga Manoj Reddy
