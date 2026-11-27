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


def test_list_tasks_filters_before_pagination() -> None:
    store = TaskStore()
    for i in range(10):
        store.create_task(TaskCreate(title=f"Task {i}"))
    for task_id in (7, 8, 9):
        store.update_task(task_id, TaskUpdate(status=TaskStatus.done))

    page = store.list_tasks(status=TaskStatus.done, limit=2)
    assert [t.id for t in page] == [7, 8]

    page = store.list_tasks(status=TaskStatus.done, offset=2, limit=2)
    assert [t.id for t in page] == [9]


def test_list_tasks_query_filters_before_pagination() -> None:
    store = TaskStore()
    for i in range(6):
        store.create_task(TaskCreate(title="match" if i >= 4 else "other"))

    page = store.list_tasks(q="match", limit=1)
    assert [t.id for t in page] == [5]


def test_update_task_without_tags_preserves_tags_and_refreshes_updated_at() -> None:
    store = TaskStore()
    created = store.create_task(TaskCreate(title="Keep tags", tags=["a", "b"]))
    original_updated_at = created.updated_at

    updated = store.update_task(created.id, TaskUpdate(title="Renamed"))
    assert updated is not None
    assert updated.tags == ["a", "b"]
    assert updated.updated_at > original_updated_at


def test_update_task_with_empty_tags_clears_tags() -> None:
    store = TaskStore()
    created = store.create_task(TaskCreate(title="Clear tags", tags=["a"]))

    updated = store.update_task(created.id, TaskUpdate(tags=[]))
    assert updated is not None
    assert updated.tags == []


def test_delete_missing_task_returns_none() -> None:
    store = TaskStore()
    assert store.delete_task(999) is None
