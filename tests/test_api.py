from fastapi.testclient import TestClient

from app.main import app, store

client = TestClient(app)


def test_health_and_basic_crud() -> None:
    store._tasks.clear()
    store._next_id = 1

    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

    created = client.post("/tasks", json={"title": "Seed task", "tags": ["api"]})
    assert created.status_code == 201
    task_id = created.json()["id"]

    fetched = client.get(f"/tasks/{task_id}")
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "Seed task"

    deleted = client.delete(f"/tasks/{task_id}")
    assert deleted.status_code == 204


def test_list_tasks_filter_applies_before_pagination() -> None:
    store._tasks.clear()
    store._next_id = 1

    for i in range(6):
        client.post("/tasks", json={"title": f"Task {i}"})
    client.patch("/tasks/6", json={"status": "done"})

    res = client.get("/tasks", params={"status": "done", "limit": 2})
    assert res.status_code == 200
    assert [t["id"] for t in res.json()] == [6]


def test_patch_without_tags_keeps_tags() -> None:
    store._tasks.clear()
    store._next_id = 1

    client.post("/tasks", json={"title": "Tagged", "tags": ["x"]})
    res = client.patch("/tasks/1", json={"title": "Renamed"})
    assert res.status_code == 200
    assert res.json()["tags"] == ["x"]


def test_delete_missing_task_returns_404() -> None:
    store._tasks.clear()
    store._next_id = 1

    res = client.delete("/tasks/999")
    assert res.status_code == 404
