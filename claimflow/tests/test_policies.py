import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.models import Policy
from sqlalchemy.orm import Session

client = TestClient(app)

@pytest.fixture
def db_session():
    # Create a new database session for each test
    db = next(get_db())
    yield db
    # Cleanup code can be added here if necessary

def test_create_policy(db_session):
    response = client.post(
        "/policies",
        json={"policy_number": "POL123", "coverage_amount": 10000, "user_id": 1},
    )
    assert response.status_code == 201
    assert response.json()["policy_number"] == "POL123"

def test_get_policies(db_session):
    response = client.get("/policies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Ensure the response is a list

def test_policy_creation_invalid_data(db_session):
    response = client.post(
        "/policies",
        json={"policy_number": "", "coverage_amount": -100, "user_id": 1},
    )
    assert response.status_code == 422  # Unprocessable Entity for invalid data

def test_policy_association_with_user(db_session):
    # Assuming a user with id 1 exists
    response = client.post(
        "/policies",
        json={"policy_number": "POL124", "coverage_amount": 5000, "user_id": 1},
    )
    assert response.status_code == 201
    policy = response.json()
    assert policy["user_id"] == 1  # Check if the policy is associated with the correct user