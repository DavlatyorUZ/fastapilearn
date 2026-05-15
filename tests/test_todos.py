def test_get_todos(client):
    response = client.get("/todos/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_create_todo(client):
    response = client.post(
        "/todos/",
        json={
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": False
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert "id" in data


def test_update_todo(client):
    # Create first
    create_response = client.post(
        "/todos/",
        json={"title": "Test todo", "description": "Test", "completed": False}
    )
    todo_id = create_response.json()["id"]

    # Update
    response = client.put(
        f"/todos/{todo_id}",
        json={"title": "Updated todo", "description": "Updated", "completed": True}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated todo"
    assert data["completed"] is True


def test_update_todo_not_found(client):
    response = client.put(
        "/todos/999",
        json={"title": "Updated", "description": "Updated", "completed": True}
    )
    assert response.status_code == 404


def test_delete_todo(client):
    # Create first
    create_response = client.post(
        "/todos/",
        json={"title": "Test todo", "description": "Test", "completed": False}
    )
    todo_id = create_response.json()["id"]

    # Delete
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 204


def test_delete_todo_not_found(client):
    response = client.delete("/todos/999")
    assert response.status_code == 404