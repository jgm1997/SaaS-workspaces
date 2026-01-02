def test_login_rate_limit(client):
    email = "ratelimit@example.com"
    password = "secret"

    client.post("/auth/register", json={"email": email, "password": password})

    # 5 intentos correctos
    for _ in range(5):
        r = client.post("/auth/login", json={"email": email, "password": password})
        assert r.status_code == 200

    # 6º intento → bloqueado
    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code == 429
