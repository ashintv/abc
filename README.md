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
- `GET /tasks` — list tasks (supports `status`, `q`, `offset`, `limit`). `status` and `q` filters are applied first; `offset` and `limit` then paginate the filtered results.
- `POST /tasks` — create a new task
- `GET /tasks/{task_id}` — retrieve a single task
- `PATCH /tasks/{task_id}` — partially update a task. Omitted fields (including `tags`) are left unchanged, `"tags": []` clears tags, and `updated_at` is refreshed on every update. Returns `404` if the task does not exist.
- `DELETE /tasks/{task_id}` — remove a task. Returns `204` on success and `404` if the task does not exist.
- `GET /stats` — aggregate task counts by status

## Running Tests

```bash
pytest
```
