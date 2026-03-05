import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.models import User
from sqlalchemy.orm import Session

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def db_session():
    db = next(get_db())
    yield db
    db.close()

def test_user_registration(client, db_session):
    response = client.post("/register", json={
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "testuser@example.com"

def test_user_login(client):
    response = client.post("/login", json={
        "email": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_users_admin(client):
    # Assuming an admin user is already logged in
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Expecting a list of users

def test_user_creation_invalid_email(client):
    response = client.post("/register", json={
        "name": "Invalid User",
        "email": "invalid-email",
        "password": "password123"
    })
    assert response.status_code == 422  # Unprocessable Entity for validation errors

def test_user_login_invalid_credentials(client):
    response = client.post("/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401  # Unauthorized for invalid credentials