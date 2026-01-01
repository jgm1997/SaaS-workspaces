from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_workspace_flow():
    email = "ws_test@example.com"
    password = "secret123"

    register = client.post(
        "/auth/register", json={"email": email, "password": password}
    )
    assert register.status_code == 200

    login = client.post("/auth/login", json={"email": email, "password": password})
    assert login.status_code == 200
    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    workspaces_post = client.post(
        "/workspaces", json={"name": "My WS"}, headers=headers
    )
    assert workspaces_post.status_code == 200
    workspace = workspaces_post.json()
    workspace_pk = workspace["pk"]

    workspaces_get = client.get("/workspaces", headers=headers)
    assert workspaces_get.status_code == 200
    assert len(workspaces_get.json()) == 1
    assert workspaces_get.json()[0]["pk"] == workspace_pk

    headers_with_ws = {
        **headers,
        "X-Workspace": workspace_pk,
    }

    final_request = client.get("/workspaces", headers=headers_with_ws)
    assert final_request.status_code == 200
