from uuid import uuid4


def test_register_and_login(client):
    email = f"auth_test+{uuid4()}@example.com"  # pragma: allowlist secret
    password = "pass" + "word123"

    register = client.post(
        "/auth/register", json={"email": email, "password": password}
    )
    assert register.status_code == 200
    user = register.json()
    assert user["email"] == email

    login = client.post("/auth/login", json={"email": email, "password": password})
    assert login.status_code == 200
    token = login.json()["access_token"]
    assert isinstance(token, str)


def test_register_duplicate_email(client):
    email = f"auth_test+{uuid4()}@example.com"  # pragma: allowlist secret
    password = "pass" + "word123"

    client.post("/auth/register", json={"email": email, "password": password})
    duplicate = client.post(
        "/auth/register", json={"email": email, "password": password}
    )
    assert duplicate.status_code == 400


def test_login_wrong_password(client):
    email = f"auth_test+{uuid4()}@example.com"  # pragma: allowlist secret
    password = "pass" + "word123"
    wrong_password = "wrongpass"

    client.post("/auth/register", json={"email": email, "password": password})
    login = client.post(
        "/auth/login", json={"email": email, "password": wrong_password}
    )
    assert login.status_code == 401
