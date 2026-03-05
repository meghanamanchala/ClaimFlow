import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_submit_claim():
    response = client.post("/claims", json={
        "policy_id": 1,
        "claim_amount": 1000.0,
        "description": "Accident damage"
    })
    assert response.status_code == 201
    assert response.json()["description"] == "Accident damage"

def test_get_claims():
    response = client.get("/claims")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_claim_status():
    response = client.patch("/claims/1/status", json={"status": "Approved"})
    assert response.status_code == 200
    assert response.json()["status"] == "Approved"