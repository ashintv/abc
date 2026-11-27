from app.models import TaskCreate, TaskStatus, TaskUpdate
from app.storage import TaskStore


def test_create_and_fetch_task() -> None:
    store = TaskStore()
    created = store.create_task(TaskCreate(title="Write docs", tags=["docs"]))
    assert created.id == 1
    assert created.status == TaskStatus.todo
    assert store.get_task(1) is not None


def test_update_task_status_and_stats() -> None:
    store = TaskStore()
    t1 = store.create_task(TaskCreate(title="First"))
    t2 = store.create_task(TaskCreate(title="Second"))

    updated = store.update_task(t1.id, TaskUpdate(status=TaskStatus.done, tags=["ops"]))
    assert updated is not None
    assert updated.status == TaskStatus.done
    assert store.stats() == {"todo": 1, "in_progress": 0, "done": 1}
    assert store.get_task(t2.id) is not None
