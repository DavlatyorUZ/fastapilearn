from app import models


def test_create_post(client, auth_headers, test_category):
    response = client.post(
        "/posts/",
        json={
            "title": "New Post",
            "content": "New content",
            "published": True,
            "category_id": test_category.id
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Post"
    assert data["content"] == "New content"


def test_create_post_without_auth(client):
    response = client.post(
        "/posts/",
        json={
            "title": "New Post",
            "content": "New content"
        }
    )
    assert response.status_code == 401


def test_get_all_posts(client, test_post):
    response = client.get("/posts/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_all_posts_with_search(client, test_post):
    response = client.get("/posts/?search=Test")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_all_posts_pagination(client, test_post):
    response = client.get("/posts/?limit=10&skip=0")
    assert response.status_code == 200


def test_get_post(client, test_post):
    response = client.get(f"/posts/{test_post.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_post.id


def test_get_post_not_found(client):
    response = client.get("/posts/999")
    assert response.status_code == 404


def test_update_post(client, test_post, auth_headers):
    response = client.put(
        f"/posts/{test_post.id}",
        json={
            "title": "Updated Title",
            "content": "Updated content"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"


def test_update_post_not_owner(client, test_user, db, test_post, auth_headers):
    """Test that another user cannot update the post"""
    # Create another user
    from app.utils.hashing import hash_password
    other_user = models.User(
        username="otheruser",
        email="other@example.com",
        password=hash_password("password")
    )
    db.add(other_user)
    db.commit()

    # Get token for other user
    from app.oauth2 import create_access_token
    other_token = create_access_token(data={"user_id": other_user.id})
    other_headers = {"Authorization": f"Bearer {other_token}"}

    response = client.put(
        f"/posts/{test_post.id}",
        json={"title": "Hacked Title"},
        headers=other_headers
    )
    assert response.status_code == 403


def test_update_post_not_found(client, auth_headers):
    response = client.put(
        "/posts/999",
        json={"title": "Updated Title"},
        headers=auth_headers
    )
    assert response.status_code == 404


def test_delete_post(client, test_post, auth_headers):
    response = client.delete(f"/posts/{test_post.id}", headers=auth_headers)
    assert response.status_code == 204


def test_delete_post_not_owner(client, test_user, db, test_post, auth_headers):
    """Test that another user cannot delete the post"""
    from app.utils.hashing import hash_password
    other_user = models.User(
        username="otheruser2",
        email="other2@example.com",
        password=hash_password("password")
    )
    db.add(other_user)
    db.commit()

    from app.oauth2 import create_access_token
    other_token = create_access_token(data={"user_id": other_user.id})
    other_headers = {"Authorization": f"Bearer {other_token}"}

    response = client.delete(f"/posts/{test_post.id}", headers=other_headers)
    assert response.status_code == 403


def test_partial_update_post(client, test_post, auth_headers):
    response = client.patch(
        f"/posts/{test_post.id}",
        json={"title": "Partially Updated"},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Partially Updated"


def test_partial_update_not_owner(client, test_user, db, test_post, auth_headers):
    from app.utils.hashing import hash_password
    other_user = models.User(
        username="otheruser3",
        email="other3@example.com",
        password=hash_password("password")
    )
    db.add(other_user)
    db.commit()

    from app.oauth2 import create_access_token
    other_token = create_access_token(data={"user_id": other_user.id})
    other_headers = {"Authorization": f"Bearer {other_token}"}

    response = client.patch(
        f"/posts/{test_post.id}",
        json={"title": "Hacked"},
        headers=other_headers
    )
    assert response.status_code == 403