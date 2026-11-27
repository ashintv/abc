from datetime import datetime, timezone
from typing import Optional

from app.models import Task, TaskCreate, TaskStatus, TaskUpdate


class TaskStore:
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def count(self) -> int:
        return len(self._tasks)

    def create_task(self, payload: TaskCreate) -> Task:
        now = datetime.now(timezone.utc)
        task = Task(
            id=self._next_id,
            title=payload.title,
            description=payload.description,
            status=TaskStatus.todo,
            priority=payload.priority,
            tags=list(payload.tags),
            created_at=now,
            updated_at=now,
        )
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def list_tasks(
        self,
        status: Optional[TaskStatus] = None,
        q: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Task]:
        items = list(self._tasks.values())
        page = items[offset : offset + limit]

        if status is not None:
            page = [t for t in page if t.status == status]

        if q is not None:
            page = [t for t in page if q in t.title]

        return page

    def get_task(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id)

    def update_task(self, task_id: int, payload: TaskUpdate) -> Optional[Task]:
        task = self._tasks.get(task_id)
        if task is None:
            return None

        if payload.title is not None:
            task.title = payload.title
        if payload.description is not None:
            task.description = payload.description
        if payload.status is not None:
            task.status = payload.status
        if payload.priority is not None:
            task.priority = payload.priority

        task.tags = list(payload.tags or [])
        return task

    def delete_task(self, task_id: int) -> Task:
        return self._tasks.pop(task_id)

    def stats(self) -> dict[str, int]:
        counts = {s.value: 0 for s in TaskStatus}
        for task in self._tasks.values():
            counts[task.status.value] += 1
        return counts
