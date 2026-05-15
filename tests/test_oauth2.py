from datetime import datetime, timedelta, timezone
from jose import jwt
import pytest

from app.oauth2 import (
    create_access_token,
    create_refresh_token,
    verify_access_token,
    verify_refresh_token,
    get_current_user,
)
from app.config import settings


def test_create_access_token():
    token = create_access_token(data={"user_id": 1})
    assert token is not None
    assert isinstance(token, str)


def test_create_refresh_token():
    token = create_refresh_token(data={"user_id": 1})
    assert token is not None
    assert isinstance(token, str)


def test_verify_access_token_valid():
    token = create_access_token(data={"user_id": 1})
    credentials_exception = Exception("Invalid credentials")

    result = verify_access_token(token, credentials_exception)
    assert result is not None
    assert result.id == "1"


def test_verify_access_token_invalid():
    credentials_exception = Exception("Invalid credentials")

    with pytest.raises(Exception):
        verify_access_token("invalid_token", credentials_exception)


def test_verify_refresh_token_valid():
    token = create_refresh_token(data={"user_id": 1})

    user_id = verify_refresh_token(token)
    assert user_id == "1" or user_id == 1  # Can be int or string depending on JWT encoding


def test_verify_refresh_token_invalid():
    user_id = verify_refresh_token("invalid_token")
    assert user_id is None


def test_verify_refresh_token_missing_user_id():
    """Token without user_id should return None"""
    payload = {
        "exp": datetime.now(timezone.utc) + timedelta(days=7)
    }
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

    user_id = verify_refresh_token(token)
    assert user_id is None


def test_get_current_user(client, db, test_user):
    """Test getting current user with valid token"""
    from app.oauth2 import get_current_user
    from app.database import get_db
    from fastapi.security import OAuth2PasswordBearer

    # Create token
    token = create_access_token(data={"user_id": test_user.id})

    # Override dependency
    def override_get_db():
        try:
            yield db
        finally:
            pass

    client.app.dependency_overrides[get_db] = override_get_db

    # Call get_current_user directly
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
    user = get_current_user(token=token, db=db)

    assert user is not None
    assert user.id == test_user.id
    assert user.email == test_user.email

    client.app.dependency_overrides.clear()


def test_get_current_user_invalid_token(db):
    """Test get_current_user with invalid token"""
    from app.oauth2 import get_current_user

    with pytest.raises(Exception):
        get_current_user(token="invalid_token", db=db)


def test_get_current_user_nonexistent_user(db):
    """Test get_current_user with token for non-existent user"""
    from app.oauth2 import get_current_user

    # Create token for user that doesn't exist
    token = create_access_token(data={"user_id": 99999})

    with pytest.raises(Exception):
        get_current_user(token=token, db=db)