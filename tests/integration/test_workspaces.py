import uuid


def test_workspace_flow(client):
    email = f"ws_test_{uuid.uuid4().hex}@example.com"  # pragma: allowlist secret
    password = "pass" + "word123"

    register = client.post(
        "/auth/register", json={"email": email, "password": password}
    )
    assert register.status_code == 200

    login = client.post("/auth/login", json={"email": email, "password": password})
    assert login.status_code == 200
    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    workspaces_post = client.post(
        "/workspaces", json={"name": f"My WS {uuid.uuid4().hex}"}, headers=headers
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


def test_access_other_workspace(client, token):
    ws1 = client.post(
        "/workspaces",
        json={"name": f"WS1-{uuid.uuid4().hex}"},
        headers=token,
    ).json()["pk"]
    ws2 = client.post(
        "/workspaces",
        json={"name": f"WS2-{uuid.uuid4().hex}"},
        headers=token,
    ).json()["pk"]

    headers = {
        **token,
        "X-Workspace": ws1,
    }

    request_ws1 = client.get("/projects", headers=headers)
    assert request_ws1.status_code == 200

    request_ws2 = client.get(f"/projects/{ws2}", headers=headers)
    assert request_ws2.status_code == 404
