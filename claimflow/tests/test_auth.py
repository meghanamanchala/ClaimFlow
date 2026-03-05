import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/register", json={"name": "Test User", "email": "test@example.com", "password": "password123"})
    assert response.status_code == 201
    assert "access_token" in response.json()

def test_login_user():
    response = client.post("/login", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_user():
    response = client.post("/login", json={"email": "invalid@example.com", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}

def test_register_existing_user():
    client.post("/register", json={"name": "Test User", "email": "test@example.com", "password": "password123"})
    response = client.post("/register", json={"name": "Test User", "email": "test@example.com", "password": "password123"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}