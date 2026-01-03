def setup_owner_and_member(client):
    password = "secret"

    # Owner
    email_owner = "owner12@example.com"
    client.post("/auth/register", json={"email": email_owner, "password": password})
    token_owner = client.post(
        "/auth/login", json={"email": email_owner, "password": password}
    ).json()["access_token"]
    headers_owner = {"Authorization": f"Bearer {token_owner}"}

    # Workspace
    ws_pk = client.post(
        "/workspaces", json={"name": "WS12"}, headers=headers_owner
    ).json()["pk"]
    headers_ws_owner = {"Authorization": f"Bearer {token_owner}", "X-Workspace": ws_pk}

    # Member
    email_member = "member12@example.com"
    client.post("/auth/register", json={"email": email_member, "password": password})
    token_member = client.post(
        "/auth/login", json={"email": email_member, "password": password}
    ).json()["access_token"]
    headers_member = {"Authorization": f"Bearer {token_member}"}

    # Invite + accept
    inv = client.post(
        "/invitations", json={"email": email_member}, headers=headers_ws_owner
    ).json()
    client.post(f"/invitations/{inv['pk']}/accept", headers=headers_member)

    return headers_ws_owner, ws_pk


def test_owner_can_change_role_and_remove_member(client):
    headers_ws_owner, _ = setup_owner_and_member(client)

    # List members
    r = client.get("/members", headers=headers_ws_owner)
    assert r.status_code == 200
    members = r.json()
    assert len(members) == 2  # owner + member

    # Find member (not owner)
    member = next(m for m in members if m["role"] != "owner")
    member_pk = member["pk"]

    # Change role to admin
    r = client.patch(
        f"/members/{member_pk}/role", json={"role": "admin"}, headers=headers_ws_owner
    )
    assert r.status_code == 200
    assert r.json()["role"] == "admin"

    # Remove member
    r = client.delete(f"/members/{member_pk}", headers=headers_ws_owner)
    assert r.status_code == 200

    # List again
    r = client.get("/members", headers=headers_ws_owner)
    assert len(r.json()) == 1  # solo owner


def test_member_cannot_manage_members(client):
    _, ws_pk = setup_owner_and_member(client)

    # Get member token
    password = "secret"
    email_member = "member12@example.com"
    token_member = client.post(
        "/auth/login", json={"email": email_member, "password": password}
    ).json()["access_token"]
    headers_ws_member = {
        "Authorization": f"Bearer {token_member}",
        "X-Workspace": ws_pk,
    }

    # Member tries to list members (permitido)
    r = client.get("/members", headers=headers_ws_member)
    assert r.status_code == 200

    # Member tries to change role → 403
    member_pk = r.json()[0]["pk"]
    r = client.patch(
        f"/members/{member_pk}/role", json={"role": "admin"}, headers=headers_ws_member
    )
    assert r.status_code == 403

    # Member tries to remove → 403
    r = client.delete(f"/members/{member_pk}", headers=headers_ws_member)
    assert r.status_code == 403
