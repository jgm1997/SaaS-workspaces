import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_project_crud():
    email = f"proj_test_{uuid.uuid4().hex}@example.com"
    password = "secret123"

    register = client.post(
        "/auth/register", json={"email": email, "password": password}
    )
    assert register.status_code == 200

    login = client.post("/auth/login", json={"email": email, "password": password})
    assert login.status_code == 200
    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    workspaces = client.post(
        "/workspaces",
        json={"name": f"Test Workspace {uuid.uuid4().hex}"},
        headers=headers,
    )
    assert workspaces.status_code == 200
    workspace_pk = workspaces.json()["pk"]

    headers_ws = {**headers, "X-Workspace": workspace_pk}

    create_project = client.post(
        "/projects", json={"name": "P1", "description": "Desc"}, headers=headers_ws
    )
    assert create_project.status_code == 200
    project_pk = create_project.json()["pk"]

    list_projects = client.get("/projects", headers=headers_ws)
    assert list_projects.status_code == 200
    assert len(list_projects.json()) == 1

    get_project = client.get(f"/projects/{project_pk}", headers=headers_ws)
    assert get_project.status_code == 200

    update_project = client.put(
        f"/projects/{project_pk}",
        json={"name": "P1 Updated", "description": "Desc Updated"},
        headers=headers_ws,
    )
    assert update_project.status_code == 200
    assert update_project.json()["name"] == "P1 Updated"

    delete_project = client.delete(f"/projects/{project_pk}", headers=headers_ws)
    assert delete_project.status_code == 200
