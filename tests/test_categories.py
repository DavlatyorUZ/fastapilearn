from app import models


def test_create_category(client):
    response = client.post(
        "/categories/",
        json={
            "name": "Tech",
            "description": "Technology related posts"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Tech"
    assert data["description"] == "Technology related posts"


def test_get_all_categories(client, test_category):
    response = client.get("/categories/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_category(client, test_category):
    response = client.get(f"/categories/{test_category.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_category.id
    assert data["name"] == test_category.name


def test_get_category_not_found(client):
    response = client.get("/categories/999")
    assert response.status_code == 404


def test_update_category(client, test_category):
    response = client.put(
        f"/categories/{test_category.id}",
        json={
            "name": "Updated Tech",
            "description": "Updated description"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Tech"


def test_update_category_not_found(client):
    response = client.put(
        "/categories/999",
        json={
            "name": "Updated Tech",
            "description": "Updated description"
        }
    )
    assert response.status_code == 404


def test_delete_category(client, test_category):
    response = client.delete(f"/categories/{test_category.id}")
    assert response.status_code == 204


def test_delete_category_not_found(client):
    response = client.delete("/categories/999")
    assert response.status_code == 404