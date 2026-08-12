from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_calls_returns_seed_data():
    response = client.get("/calls")

    assert response.status_code == 200
    assert len(response.json()) >= 4


def test_patch_call_status():
    response = client.patch("/calls/1", json={"status": "in_progress"})

    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"


def test_unknown_call_returns_404():
    response = client.get("/calls/9999")

    assert response.status_code == 404
