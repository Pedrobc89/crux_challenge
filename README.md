# 🧪 Crux Backend Take-Home Assignment

## Overview

This project implements a mock backend and frontend system that:

- Serves **random**, **tabular**, and **time series** data from an API service (with simulated latency)
- Aggregates those responses via a streaming backend endpoint
- Displays the data in a simple single-page Vue application

The system is split into **three services**:

- A FastAPI `api_service` with endpoints for grabbing data and simulated latency
- A FastAPI `backend` with an aggregator and mock API endpoints
- A Vue 3 `frontend` served via Vite (dev) or Nginx (prod)

---

## 🧰 Tech Stack

- **Backend**: FastAPI, Python 3.12, httpx, asyncio
- **Frontend**: Vue 3 + Vite, Chart.js
- **Containerization**: Docker, Docker Compose

---

## 🚀 Setup & Execution

### 🐳 Prerequisites

- Docker
- Docker Compose
- Ports 5173 and 8080 must be open and unused

### ▶️ Run All Services

```bash
docker-compose up --build
```

- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend: [http://localhost:8080](http://localhost:8080)

---

### 🔌 Available Endpoints (api_service)

| Endpoint       | Description                             |
| -------------- | --------------------------------------- |
| `/random-int`  | Returns a random integer (with latency) |
| `/table`       | Returns 250 sampled rows from CSV       |
| `/time-series` | Returns 3000 time-series points         |

### 🔌 Available Endpoints (backend)

| Endpoint          | Description                          |
| ----------------- | ------------------------------------ |
| `/aggregate-data` | Streams results from the three above |

---

## 🎛️ Frontend Features

- Click **"Get Data"** to fetch all three types of data
- Responses appear **incrementally** as they're streamed
- Displays:

  - A number
  - A time series line chart
  - A table (unformatted)

---

## 🧠 Assumptions & Trade-offs

- The aggregator uses `StreamingResponse` to simulate real-time delivery over HTTP.
  In production, **SSE** or **WebSocket** would be preferable for reliability.
- The frontend uses `fetch()` instead of Axios due to browser limitations with streaming HTTP responses.
- The system assumes a relatively small CSV file and does not implement pagination or chunking.
- No automated testing was implemented to prioritize completing a functional, full-stack streaming solution within the given time constraints. In a real-world project, unit and integration tests would be added early in development.

---

## 🤖 AI Tools Used

- **ChatGPT (GPT-4)** was used for:

  - Exploring fast async patterns in FastAPI
  - Validating Vue reactivity and Chart.js integration
  - Generating the initial project structure and Docker configs

Manual testing, debugging, and final logic tuning were done by hand.

---

## 🧪 Improvements (with more time)

- Add input validation and error boundaries
- Persist time series selections for comparison
- Switch to Server-Sent Events for more robust streaming
- Implement end-to-end and integration tests with `pytest` + `playwright`

---
