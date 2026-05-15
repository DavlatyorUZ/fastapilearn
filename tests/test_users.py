from app import models


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "new@example.com"
    assert "id" in data
    assert "password" not in data


def test_create_user_duplicate_email(client, test_user):
    response = client.post(
        "/users/",
        json={
            "username": "anotheruser",
            "email": "test@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 400
    assert "email" in response.json()["detail"].lower()


def test_get_user(client, test_user):
    response = client.get(f"/users/{test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["email"] == test_user.email


def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404


def test_change_password_success(client, test_user, auth_headers):
    response = client.put(
        "/users/me/password",
        json={
            "old_password": "testpassword",
            "new_password": "newpassword123"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    assert "message" in response.json()


def test_change_password_wrong_old_password(client, test_user, auth_headers):
    response = client.put(
        "/users/me/password",
        json={
            "old_password": "wrongpassword",
            "new_password": "newpassword123"
        },
        headers=auth_headers
    )
    assert response.status_code == 400


def test_change_password_same_as_old(client, test_user, auth_headers):
    response = client.put(
        "/users/me/password",
        json={
            "old_password": "testpassword",
            "new_password": "testpassword"
        },
        headers=auth_headers
    )
    assert response.status_code == 400


def test_change_password_unauthorized(client):
    response = client.put(
        "/users/me/password",
        json={
            "old_password": "testpassword",
            "new_password": "newpassword123"
        }
    )
    assert response.status_code == 401