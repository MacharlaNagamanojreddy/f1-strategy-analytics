# 🏎️ F1 Strategy Analytics

A race strategy simulation platform inspired by Formula 1 performance engineering.

It combines:
- Interactive strategy exploration in Streamlit
- Monte Carlo simulation for risk-aware race outcomes
- Real race-data tyre degradation modeling using FastF1

![F1 Strategy Analytics](https://github.com/user-attachments/assets/7efd5e97-d4e1-47e2-a526-f8b3050717d2)

## 🚀 Features

### 🖥️ Interactive Dashboard
- Select first and second stint compounds
- Configure pit lap and Monte Carlo run count
- View average race time, risk (standard deviation), and best simulated time
- Inspect full race-time distribution with histogram

### 🧠 Smart Strategy Engine
- Two-stint race model across 60 laps
- Compound-specific base pace and degradation rates
- Pit stop loss modeling
- Stochastic traffic and lap noise integration

### 🎲 Monte Carlo Analysis
- Repeated simulation runs (100 to 2000 from UI)
- Probabilistic distribution of total race time
- Strategy risk profiling with mean and variance metrics

### 📡 Real Data Degradation Model
- FastF1 ingestion with local caching (`fastf1_cache/`)
- Driver lap extraction and filtering by tyre compound
- Linear degradation fitting on Medium compound laps
- Built-in tracks in UI:
  - Monaco GP 2023 (HAM)
  - Silverstone/British GP 2023 (HAM)

## 🧠 Tech Stack

### App Layer
- Python
- Streamlit

### Analytics Layer
- NumPy
- Pandas
- Matplotlib
- Scikit-Learn

### Data Layer
- FastF1

## 🗂 Folder Structure

```text
f1-strategy-analytics/
│
├── app.py                   # Streamlit dashboard
├── requirements.txt         # Python dependencies
├── src/
│   ├── strategy_engine.py   # Lap-level strategy simulation
│   ├── monte_carlo.py       # Monte Carlo execution logic
│   └── real_data_model.py   # FastF1 degradation fitting
│
├── notebooks/
│   └── exploration.ipynb    # Analysis and experimentation
│
├── fastf1_cache/            # Cached FastF1 responses
└── reports/                 # Optional exported outputs
```

## 🔧 Local Development Setup

### 1. Environment Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Dashboard

```bash
streamlit run app.py
```

### Running URL
- Dashboard: `http://localhost:8501`

## 📅 How Strategy Simulation Works

### Inputs
- First stint tyre
- Second stint tyre
- Pit lap
- Monte Carlo run count

### Outputs
- Average total race time
- Risk (standard deviation)
- Best simulated race time
- Distribution plot
- Real-data base lap time and degradation slope

### Algorithm Pipeline
1. Simulate each lap with compound pace + degradation.
2. Apply pit-loss at selected pit lap.
3. Add stochastic traffic and noise effects.
4. Repeat across Monte Carlo runs.
5. Aggregate and visualize race-time distribution.

## 🔬 Real Data Mode

1. Choose `Monaco` or `Silverstone` in the dashboard.
2. Click `Load Real Data Model`.
3. The app fetches FastF1 race data, filters HAM Medium laps, and fits a linear model.
4. The app returns:
   - Estimated base lap time (intercept)
   - Degradation per lap (slope)

## 📦 Notes

- First FastF1 fetch can be slower due to API download.
- Subsequent runs are faster via cache reuse.
- Internet connection is required for uncached sessions.

## 👨‍💻 Author

Macharla Naga Manoj Reddy  
F1 Strategy Analytics - Prototype Release

If this project was useful, please ⭐ the repo.
