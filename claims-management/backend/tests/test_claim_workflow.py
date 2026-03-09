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


def bootstrap_users(client):
    register_user(
        client,
        name="Admin",
        email="admin@example.com",
        password="Secret123!",
        role="admin",
    )
    register_user(
        client,
        name="Agent",
        email="agent@example.com",
        password="Secret123!",
        role="agent",
    )
    register_user(
        client,
        name="Policyholder",
        email="holder@example.com",
        password="Secret123!",
        role="policyholder",
    )

    admin_token = login_user(client, email="admin@example.com", password="Secret123!")
    agent_token = login_user(client, email="agent@example.com", password="Secret123!")
    holder_token = login_user(client, email="holder@example.com", password="Secret123!")

    users_response = client.get("/users", headers=auth_headers(admin_token))
    assert users_response.status_code == 200
    users = users_response.json()

    policyholder = next(user for user in users if user["email"] == "holder@example.com")

    return {
        "admin_token": admin_token,
        "agent_token": agent_token,
        "holder_token": holder_token,
        "policyholder_id": policyholder["id"],
    }


def test_claim_lifecycle_and_tracking(client):
    auth = bootstrap_users(client)

    create_policy_response = client.post(
        "/policies",
        json={
            "policy_number": "POL-2026-0001",
            "coverage_amount": 12000,
            "user_id": auth["policyholder_id"],
        },
        headers=auth_headers(auth["admin_token"]),
    )
    assert create_policy_response.status_code == 200

    claim_response = client.post(
        "/claims",
        json={
            "claimType": "Auto",
            "policyNumber": "POL-2026-0001",
            "incidentDate": "2026-03-01",
            "estimatedAmount": 4200,
            "description": "Front bumper damage",
            "documents": [
                {
                    "fileName": "police-report.pdf",
                    "fileUrl": "https://files.example/police-report.pdf",
                    "fileType": "PDF",
                    "size": 1.7,
                }
            ],
        },
        headers=auth_headers(auth["holder_token"]),
    )
    assert claim_response.status_code == 200
    claim = claim_response.json()
    claim_id = claim["id"]

    tracking_response = client.get(f"/claims/{claim_id}/tracking", headers=auth_headers(auth["holder_token"]))
    assert tracking_response.status_code == 200
    assert tracking_response.json()["status"] == "submitted"

    decision_response = client.patch(
        f"/claims/{claim_id}/decision",
        json={
            "decision": "approved",
            "agentNotes": "Looks valid",
            "approvedAmount": 4000,
        },
        headers=auth_headers(auth["agent_token"]),
    )
    assert decision_response.status_code == 200
    assert decision_response.json()["status"] == "approved"
    assert decision_response.json()["approvedAmount"] == 4000


def test_admin_only_user_listing_guard(client):
    auth = bootstrap_users(client)

    forbidden_response = client.get("/users", headers=auth_headers(auth["holder_token"]))
    assert forbidden_response.status_code == 403
    assert forbidden_response.json()["detail"] == "Insufficient permissions"


def test_policyholder_cannot_open_other_users_claim(client):
    auth = bootstrap_users(client)

    register_user(
        client,
        name="Another Holder",
        email="holder2@example.com",
        password="Secret123!",
        role="policyholder",
    )
    holder2_token = login_user(client, email="holder2@example.com", password="Secret123!")

    users_response = client.get("/users", headers=auth_headers(auth["admin_token"]))
    holder2 = next(user for user in users_response.json() if user["email"] == "holder2@example.com")

    policy_response = client.post(
        "/policies",
        json={
            "policy_number": "POL-2026-0002",
            "coverage_amount": 9000,
            "user_id": holder2["id"],
        },
        headers=auth_headers(auth["admin_token"]),
    )
    assert policy_response.status_code == 200

    claim_response = client.post(
        "/claims",
        json={
            "claimType": "Health",
            "policyNumber": "POL-2026-0002",
            "incidentDate": "2026-03-02",
            "estimatedAmount": 2500,
            "description": "Medical reimbursement",
        },
        headers=auth_headers(holder2_token),
    )
    assert claim_response.status_code == 200

    claim_id = claim_response.json()["id"]
    blocked_response = client.get(f"/claims/{claim_id}", headers=auth_headers(auth["holder_token"]))

    assert blocked_response.status_code == 403
