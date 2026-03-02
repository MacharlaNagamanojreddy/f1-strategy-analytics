🏎️ F1 Performance & Strategy Analysis Platform

A full-stack Formula 1 analytics platform that processes live telemetry, race-weekend data, and real driver laps to generate pace insights, tyre degradation curves, and race strategy predictions.
Powered by a modern React dashboard, a Node.js backend, and a Python analytics engine built on ML models and simulation algorithms.
<img width="2048" height="1088" alt="result" src="https://github.com/user-attachments/assets/7bd97b7a-39f7-4648-898c-501185b8a051" />

🚀 Features
📡 Telemetry Ingestion

Live timing & delta feed support

Lap–by–lap data processing

Driver pace, throttle, brake, speed & GPS

🧠 Analytics Engine

Pace prediction models

Real data tyre degradation modelling

Monte Carlo–based strategy simulation

Undercut/overcut feasibility scoring

Pit window optimisation

🎛️ Interactive Dashboard

Stint comparison

Tyre wear visualisation

Predicted lap times

Strategy recommendations

Simulation outputs (CSV/PDF export)

🧩 Real Data Tyre Degradation Module

A specialised module that uses real race data (e.g., Hamilton — Monaco 2023) to learn tyre degradation curves and simulate race outcomes.

Key Capabilities:

Load historical driver lap times

Clean & filter outliers, pit laps, warm-up laps

Fit linear/polynomial tyre degradation models

Generate base lap time + per-lap degradation

Run Monte Carlo simulations

Compute predicted stint time & optimal pit lap

Inputs:

First Stint Tyre

Second Stint Tyre

Pit Lap

Monte Carlo Runs

Outputs:

Estimated base lap time

Tyre degradation rate

Race time distribution

Strategy score

🧠 Tech Stack
Frontend

React

Tailwind CSS

React Router

Axios

Recharts/D3

Backend

Node.js

Express.js

MongoDB (Mongoose)

JWT Authentication

Analytics Engine

Python

Pandas, NumPy

Scikit-Learn

Custom strategy simulation algorithms

Statistical degradation modelling

🗂 Folder Structure
f1-analysis-platform/
│
├── backend/                # Node.js + Express API
│   ├── src/
│   ├── server.js
│   └── config.env.example
│
├── frontend/               # React Data Dashboard
│   ├── src/
│   ├── App.jsx
│   └── .env.example
│
└── analytics/              # Python ML/Simulation Engine
    ├── telemetry/
    ├── degradation/
    │   ├── model_fitter.py
    │   ├── monte_carlo.py
    │   ├── visualizer.py
    │   └── hamilton_monaco_2023.csv
    └── strategy/
🔧 Local Development Setup
1️⃣ Backend Setup
cp backend/config.env.example backend/config.env
npm --prefix backend install
npm --prefix backend run start
2️⃣ Frontend Setup
cp frontend/.env.example frontend/.env
npm --prefix frontend install
npm --prefix frontend run start
3️⃣ Analytics Engine Setup
cd analytics
pip install -r requirements.txt
python main.py
🌐 Running URLs

Frontend:
http://localhost:3000

Backend:
http://localhost:5000

Analytics Engine (Streamlit UI):
http://localhost:8501

🔍 How the Analysis Pipeline Works
Algorithm Flow (Mermaid)
<img width="4060" height="737" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/d81eb0fb-271f-41e7-a317-35926d35ddf6" />

🔬 Real Data Modelling Pipeline
<img width="2790" height="235" alt="mermaid-diagram (1)" src="https://github.com/user-attachments/assets/f16071f9-5a24-4dea-8582-7dedf74fbaae" />

📦 Deployment

Production deployment steps are provided in:

docs/DEPLOYMENT.md

Supports:

Docker & Docker Compose

NGINX reverse proxy

Railway / Render / AWS / VPS

Environment variable configuration

🧑‍💻 Author

Macharla Naga Manoj Reddy
F1 Performance & Strategy Analysis Platform — Prototype Release

If this project fuels your curiosity, ⭐ the repo!
