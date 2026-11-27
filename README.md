# TaskHub API

Lightweight FastAPI task-tracking microservice with in-memory storage, filtering, and status statistics.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Endpoints

- `GET /health` — service liveness and task count
- `GET /tasks` — list tasks (supports `status`, `q`, `offset`, `limit`)
- `POST /tasks` — create a new task
- `GET /tasks/{task_id}` — retrieve a single task
- `PATCH /tasks/{task_id}` — partially update a task
- `DELETE /tasks/{task_id}` — remove a task
- `GET /stats` — aggregate task counts by status

## Running Tests

```bash
pytest
```
