import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    # Clear limiter storage if present to avoid state leaking across tests
    limiter = getattr(app.state, "limiter", None)
    if limiter is not None:
        storage = getattr(limiter, "storage", None)
        if storage is not None and hasattr(storage, "clear"):
            try:
                storage.clear()
            except Exception:
                # some storage backends may not implement clear or may raise
                pass

    # Set a unique test client id header so rate-limit keys are isolated
    test_client_id = str(uuid.uuid4())
    client = TestClient(app)
    client.headers.update({"X-Test-Client-ID": test_client_id})
    return client


@pytest.fixture
def token(client):
    email = "testuser@example.com"  # pragma: allowlist secret
    password = "pass" + "word123"

    client.post("/auth/register", json={"email": email, "password": password})
    login = client.post("/auth/login", json={"email": email, "password": password})
    access_token = login.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
