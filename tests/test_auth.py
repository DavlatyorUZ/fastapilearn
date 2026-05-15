from app import models


def test_login_success(client, test_user):
    response = client.post(
        "/login",
        data={
            "username": "test@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_email(client, test_user):
    response = client.post(
        "/login",
        data={
            "username": "wrong@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 403


def test_login_invalid_password(client, test_user):
    response = client.post(
        "/login",
        data={
            "username": "test@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 403


def test_login_missing_credentials(client):
    response = client.post("/login", data={})
    assert response.status_code == 422


def test_refresh_token_success(client, test_user):
    """Test refresh token endpoint"""
    # First login to get tokens
    login_response = client.post(
        "/login",
        data={
            "username": "test@example.com",
            "password": "testpassword"
        }
    )
    refresh_token = login_response.json()["refresh_token"]

    # Use refresh token
    response = client.post(
        "/refresh",
        json={"refresh_token": refresh_token}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_refresh_token_invalid(client):
    response = client.post(
        "/refresh",
        json={"refresh_token": "invalid_token"}
    )
    assert response.status_code == 401


def test_refresh_token_nonexistent_user(client):
    """Test refresh with token for deleted user"""
    from app.oauth2 import create_refresh_token

    # Create token for non-existent user
    token = create_refresh_token(data={"user_id": 99999})

    response = client.post(
        "/refresh",
        json={"refresh_token": token}
    )
    assert response.status_code == 404


def test_logout(client):
    response = client.post("/logout")
    assert response.status_code == 200
    assert "message" in response.json()