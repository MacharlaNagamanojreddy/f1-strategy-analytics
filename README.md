# Smart Exam Scheduler

A full-stack university exam scheduling platform that generates conflict-free exam timetables using intelligent algorithms (CSP + Hybrid GA).

Built with:
- A modern React admin interface
- A scalable Node.js backend
- A Python scheduling engine

## Project Snapshot

Add your project screenshot here:

```md
![Smart Exam Scheduler Dashboard](./docs/images/dashboard.png)
```

## Features

### Admin Portal
- JWT-based authentication
- Manage students
- Manage subjects
- Manage teachers
- Manage halls

### Smart Scheduling Engine
- CSP mode:
  - Fast baseline solver
  - Ensures no student exam clashes
  - Assigns halls based on capacity
- Hybrid GA mode:
  - Genetic Algorithm orders subjects
  - CSP places them in the timetable
  - Produces optimized, balanced schedules

### Dashboard
- System statistics
- Quick metrics
- Recent exam schedule preview
- CSV export for schedules

## Tech Stack

### Frontend
- React
- React Router
- Tailwind CSS
- Axios

### Backend
- Node.js
- Express.js
- MongoDB (Mongoose)
- JWT authentication

### Scheduler
- Python
- CSP solver
- Hybrid GA optimization

## Folder Structure

```text
smart-exam-scheduler/
|
|-- backend/        # Node.js + Express API
|   |-- src/
|   |-- server.js
|   `-- config.env.example
|
|-- frontend/       # React Admin UI
|   |-- src/
|   |-- App.jsx
|   `-- .env.example
|
`-- scheduler/      # Python CSP/GA engine
```

## Local Development Setup

### 1. Backend Setup

```bash
cp backend/config.env.example backend/config.env
npm --prefix backend install
npm --prefix backend run start
```

### 2. Frontend Setup

```bash
cp frontend/.env.example frontend/.env
npm --prefix frontend install
npm --prefix frontend run start
```

### Running URLs
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:5000`

## First Login

1. Navigate to `http://localhost:3000/login`
2. Create the initial admin account
3. Use the same credentials for future logins

## How Scheduling Works

### Inputs
- Students
- Subjects
- Halls
- Teacher list

### Outputs
- Clean, conflict-free exam timetable
- Optimized slot assignment
- CSV export

### Algorithm Pipeline
1. Validate entities and capacity constraints.
2. Build subject ordering (direct CSP mode or GA-assisted mode).
3. Assign slots and halls with CSP constraints.
4. Evaluate clashes, hall capacity, and timetable balance.
5. Export the final schedule as CSV.

## Deployment

Docker and production deployment guidance:

`docs/DEPLOYMENT.md`

Supported options:
- Docker Compose
- Cloud deployment
- Nginx reverse proxy
- Railway / Render / VPS

## Author

Macharla Naga Manoj Reddy  
Smart Exam Scheduler - Prototype Release

If this project helps you, star the repository.
