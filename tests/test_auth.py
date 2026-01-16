def test_login(client, admin_user):
    response = client.post("/auth/login", json={"email": admin_user.email, "password": "secret"})
    assert response.status_code == 200
    assert "access_token" in response.json()
