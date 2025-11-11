import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "Programming Class" in activities

def test_signup_for_activity_success():
    response = client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    assert response.status_code == 200
    # Verify the student was added
    activities = client.get("/activities").json()
    assert "test@mergington.edu" in activities["Chess Club"]["participants"]

def test_signup_for_nonexistent_activity():
    response = client.post("/activities/Nonexistent Club/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"