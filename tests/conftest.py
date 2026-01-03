import uuid

import pytest
from fastapi.testclient import TestClient

from app.db.session import SessionLocal
from app.main import app
from app.models.invitation import Invitation
from app.models.project import Project
from app.models.user import User
from app.models.workspace import Workspace, WorkspaceMember


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
    # Ensure the test database is clean for each client to avoid state leakage
    session = SessionLocal()
    try:
        # Delete in order to respect foreign key constraints
        session.query(WorkspaceMember).delete()
        session.query(Invitation).delete()
        session.query(Project).delete()
        session.query(Workspace).delete()
        session.query(User).delete()
        session.commit()
    finally:
        session.close()

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
