from typing import Optional

from fastapi import FastAPI, HTTPException, Query, Response, status

from app.models import Task, TaskCreate, TaskStatus, TaskUpdate
from app.storage import TaskStore

app = FastAPI(title="TaskHub API", version="0.1.0")
store = TaskStore()


@app.get("/health")
def health() -> dict[str, object]:
    return {"status": "ok", "tasks_count": store.count()}


@app.get("/tasks", response_model=list[Task])
def list_tasks(
    status_filter: Optional[TaskStatus] = Query(default=None, alias="status"),
    q: Optional[str] = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
) -> list[Task]:
    return store.list_tasks(status=status_filter, q=q, offset=offset, limit=limit)


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> Task:
    return store.create_task(payload)


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    task = store.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskUpdate) -> Task:
    task = store.update_task(task_id, payload)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> Response:
    if store.delete_task(task_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/stats")
def get_stats() -> dict[str, int]:
    return store.stats()
