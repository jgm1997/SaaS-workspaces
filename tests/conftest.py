import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def token(client):
    email = "testuser@example.com"  # pragma: allowlist secret
    password = "pass" + "word123"

    client.post("/auth/register", json={"email": email, "password": password})
    login = client.post("/auth/login", json={"email": email, "password": password})
    access_token = login.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
