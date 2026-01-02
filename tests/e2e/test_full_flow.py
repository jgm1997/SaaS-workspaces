import uuid

import requests

BASE_URL = "http://localhost:8000"


def test_full_flow():
    email = f"e2e+{uuid.uuid4()}@example.com"  # pragma: allowlist secret
    password = "pass" + "word123"

    register_user = requests.post(
        f"{BASE_URL}/auth/register", json={"email": email, "password": password}
    )
    assert register_user.status_code == 200

    login_user = requests.post(
        f"{BASE_URL}/auth/login", json={"email": email, "password": password}
    )
    assert login_user.status_code == 200
    token = login_user.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_workspace = requests.post(
        f"{BASE_URL}/workspaces",
        json={"name": f"E2E WS {uuid.uuid4()}"},
        headers=headers,
    )
    assert create_workspace.status_code == 200
    ws_pk = create_workspace.json()["pk"]
    headers_ws = {
        "Authorization": f"Bearer {token}",
        "X-Workspace": ws_pk,
    }

    create_project = requests.post(
        f"{BASE_URL}/projects",
        json={"name": "E2E Project", "description": "End-to-end"},
        headers=headers_ws,
    )
    assert create_project.status_code == 200
    project_pk = create_project.json()["pk"]

    list_projects = requests.get(f"{BASE_URL}/projects", headers=headers_ws)
    assert list_projects.status_code == 200
    assert len(list_projects.json()) == 1
    assert list_projects.json()[0]["pk"] == project_pk
