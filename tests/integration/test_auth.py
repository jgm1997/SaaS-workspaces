from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_and_login():
    email = f"auth_test+{uuid4()}@example.com"
    password = "secret123"

    register = client.post(
        "/auth/register", json={"email": email, "password": password}
    )
    assert register.status_code == 200
    user = register.json()
    assert user["email"] == email

    login = client.post("/auth/login", json={"email": email, "password": password})
    assert login.status_code == 200
    token = login.json()["access_token"]
    assert isinstance(token, str)
