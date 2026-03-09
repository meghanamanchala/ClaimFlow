def register_user(client, *, name, email, password, role):
    response = client.post(
        "/register",
        json={
            "name": name,
            "email": email,
            "password": password,
            "role": role,
        },
    )
    assert response.status_code == 200
    return response.json()


def login_user(client, *, email, password):
    response = client.post(
        "/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_register_login_and_me_flow(client):
    register_user(
        client,
        name="Policy User",
        email="policy@example.com",
        password="Secret123!",
        role="policyholder",
    )

    token = login_user(client, email="policy@example.com", password="Secret123!")

    me_response = client.get("/me", headers=auth_headers(token))
    assert me_response.status_code == 200
    payload = me_response.json()
    assert payload["email"] == "policy@example.com"
    assert payload["role"] == "policyholder"


def test_update_profile_persists_changes(client):
    register_user(
        client,
        name="Profile User",
        email="profile@example.com",
        password="Secret123!",
        role="policyholder",
    )
    token = login_user(client, email="profile@example.com", password="Secret123!")

    update_response = client.put(
        "/me",
        json={"name": "Profile User Updated", "email": "profile.updated@example.com"},
        headers=auth_headers(token),
    )
    assert update_response.status_code == 200
    assert update_response.json()["email"] == "profile.updated@example.com"

    refreshed_token = login_user(client, email="profile.updated@example.com", password="Secret123!")

    me_response = client.get("/me", headers=auth_headers(refreshed_token))
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "profile.updated@example.com"


def test_login_rejects_invalid_credentials(client):
    register_user(
        client,
        name="Invalid Login User",
        email="invalid@example.com",
        password="Correct123!",
        role="policyholder",
    )

    response = client.post(
        "/login",
        data={"username": "invalid@example.com", "password": "wrong-pass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
