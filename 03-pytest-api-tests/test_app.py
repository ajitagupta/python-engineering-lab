import pytest
from app import app

@pytest.fixture
def client():
    return app.test_client()

def test_missing_sport_returns_400(client):
    response = client.post("/workouts", json={})
    assert response.status_code == 400
    assert "sport" in response.get_json()["error"]

def test_invalid_sport_returns_400(client):
    response = client.post("/workouts", json={"sport": "banana"})
    assert response.status_code == 400
    assert "sport" in response.get_json()["error"]

def test_missing_distance_returns_400(client):
    response = client.post("/workouts", json={"sport": "run", "duration_min": 30})
    assert response.status_code == 400
    assert "distance_km" in response.get_json()["error"]

def test_negative_distance_returns_400(client):
    response = client.post("/workouts", json={"sport": "run", "distance_km": -5, "duration_min": 30})
    assert response.status_code == 400
    assert "distance_km" in response.get_json()["error"]

def test_valid_workout_returns_200(client):
    response = client.post("/workouts", json={"sport": "run", "distance_km": 6, "duration_min": 35})
    assert response.status_code == 200
    assert response.get_json()["sport"] == "run"

def test_valid_rest_day_returns_200(client):
    response = client.post("/workouts", json={"sport": "rest"})
    assert response.status_code == 200
    assert response.get_json()["sport"] == "rest"

def test_valid_workout_id_returns_200(client):
    response = client.get("/workouts/1")
    assert response.status_code == 200
    assert response.get_json()["id"] == 1

def test_invalid_workout_id_returns_404(client):
    response = client.get("/workouts/9999")
    assert response.status_code == 404
    assert "not found" in response.get_json()["error"]
