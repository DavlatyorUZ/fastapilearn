from datetime import datetime
from app import schemas


def test_user_base_schema():
    user = schemas.UserBase(
        username="testuser",
        email="test@example.com"
    )
    assert user.username == "testuser"
    assert user.email == "test@example.com"


def test_user_create_schema():
    user = schemas.UserCreate(
        username="testuser",
        email="test@example.com",
        password="password123"
    )
    assert user.username == "testuser"
    assert user.password == "password123"


def test_user_response_schema():
    user = schemas.UserResponse(
        id=1,
        username="testuser",
        email="test@example.com",
        created_at=datetime.now()
    )
    assert user.id == 1


def test_owner_info_schema():
    owner = schemas.OwnerInfo(
        id=1,
        username="testuser",
        email="test@example.com"
    )
    assert owner.id == 1


def test_category_base_schema():
    category = schemas.CategoryBase(
        name="Test Category",
        description="Test description"
    )
    assert category.name == "Test Category"
    assert category.description == "Test description"


def test_category_create_schema():
    category = schemas.CategoryCreate(
        name="Test Category"
    )
    assert category.name == "Test Category"


def test_category_response_schema():
    category = schemas.CategoryResponse(
        id=1,
        name="Test Category",
        description="Test description",
        created_at=datetime.now()
    )
    assert category.id == 1


def test_post_base_schema():
    post = schemas.PostBase(
        title="Test Post",
        content="Test content",
        published=True,
        category_id=1
    )
    assert post.title == "Test Post"
    assert post.content == "Test content"


def test_post_create_schema():
    post = schemas.PostCreate(
        title="Test Post",
        content="Test content"
    )
    assert post.title == "Test Post"


def test_post_update_schema():
    post = schemas.PostUpdate(
        title="Updated Title",
        content="Updated content",
        published=False
    )
    assert post.title == "Updated Title"
    assert post.published is False


def test_post_response_schema():
    post = schemas.PostResponse(
        id=1,
        title="Test Post",
        content="Test content",
        published=True,
        created_at=datetime.now(),
        owner_id=1
    )
    assert post.id == 1


def test_todo_schema():
    todo = schemas.Todo(
        title="Test Todo",
        description="Test description",
        completed=False
    )
    assert todo.title == "Test Todo"
    assert todo.completed is False


def test_todo_create_schema():
    todo = schemas.TodoCreate(
        title="Test Todo",
        description="Test description",
        completed=False
    )
    assert todo.title == "Test Todo"


def test_token_schema():
    token = schemas.Token(
        access_token="access_token_value",
        refresh_token="refresh_token_value",
        token_type="bearer"
    )
    assert token.access_token == "access_token_value"
    assert token.refresh_token == "refresh_token_value"
    assert token.token_type == "bearer"


def test_token_data_schema():
    token_data = schemas.TokenData(id="1")
    assert token_data.id == "1"


def test_refresh_token_request_schema():
    request = schemas.RefreshTokenRequest(
        refresh_token="refresh_token_value"
    )
    assert request.refresh_token == "refresh_token_value"


def test_password_change_schema():
    password_change = schemas.PasswordChange(
        old_password="oldpassword",
        new_password="newpassword"
    )
    assert password_change.old_password == "oldpassword"
    assert password_change.new_password == "newpassword"