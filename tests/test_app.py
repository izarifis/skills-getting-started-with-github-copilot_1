import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_and_unregister():
    # Sign up a new participant
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

    # Try to sign up again (should fail)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400

    # Unregister participant
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]

    # Try to unregister again (should fail)
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 404
