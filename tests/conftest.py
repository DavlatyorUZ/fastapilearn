import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app import models
from app.oauth2 import create_access_token


# In-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db):
    from app.utils.hashing import hash_password
    user = models.User(
        username="testuser",
        email="test@example.com",
        password=hash_password("testpassword"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_category(db):
    category = models.Category(
        name="Test Category",
        description="Test description"
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@pytest.fixture
def test_post(db, test_user, test_category):
    post = models.Post(
        title="Test Post",
        content="Test content",
        owner_id=test_user.id,
        category_id=test_category.id,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@pytest.fixture
def auth_headers(test_user):
    token = create_access_token(data={"user_id": test_user.id})
    return {"Authorization": f"Bearer {token}"}