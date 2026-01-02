import uuid


def test_member_cannot_delete_project(client):
    unique_id = uuid.uuid4().hex[:8]
    email_owner = f"owner_{unique_id}@example.com"
    password = "strongpassword"
    client.post("/auth/register", json={"email": email_owner, "password": password})
    token_owner = client.post(
        "/auth/login", json={"email": email_owner, "password": password}
    ).json()["access_token"]
    headers_owner = {"Authorization": f"Bearer {token_owner}"}

    workspace_name = f"Test Workspace {unique_id}"
    workspace_pk = client.post(
        "/workspaces", json={"name": workspace_name}, headers=headers_owner
    ).json()["pk"]
    headers_ws_owner = {**headers_owner, "X-Workspace": workspace_pk}

    email_member = f"member_{unique_id}@example.com"
    client.post("/auth/register", json={"email": email_member, "password": password})
    token_member = client.post(
        "/auth/login", json={"email": email_member, "password": password}
    ).json()["access_token"]
    headers_member = {
        "Authorization": f"Bearer {token_member}",
    }

    invitation = client.post(
        "/invitations", json={"email": email_member}, headers=headers_ws_owner
    ).json()
    client.post(f"/invitations/{invitation['pk']}/accept", headers=headers_member)
    headers_member["X-Workspace"] = workspace_pk

    project_pk = client.post(
        "/projects", json={"name": "Test Project"}, headers=headers_ws_owner
    ).json()["pk"]

    response = client.delete(f"/projects/{project_pk}", headers=headers_member)
    assert response.status_code == 403
