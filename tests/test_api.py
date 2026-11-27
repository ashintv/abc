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
