import uuid


def test_invitation_flow(client):
    unique_id = uuid.uuid4().hex[:8]
    email_a = f"owner-{unique_id}@example.com"
    password = "strongpassword"
    client.post("/auth/register", json={"email": email_a, "password": password})
    token_a = client.post(
        "/auth/login", json={"email": email_a, "password": password}
    ).json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    workspace_name = f"Test Workspace {unique_id}"
    workspace_pk = client.post(
        "/workspaces", json={"name": workspace_name}, headers=headers_a
    ).json()["pk"]
    headers_ws_a = {**headers_a, "X-Workspace": workspace_pk}

    email_b = f"member-{unique_id}@example.com"
    client.post("/auth/register", json={"email": email_b, "password": password})
    token_b = client.post(
        "/auth/login", json={"email": email_b, "password": password}
    ).json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    invitation = client.post(
        "/invitations", json={"email": email_b}, headers=headers_ws_a
    )
    assert invitation.status_code == 200
    invitation_pk = invitation.json()["pk"]

    accept = client.post(f"/invitations/{invitation_pk}/accept", headers=headers_b)
    assert accept.status_code == 200

    workspaces = client.get("/workspaces", headers=headers_b)
    assert len(workspaces.json()) == 1
