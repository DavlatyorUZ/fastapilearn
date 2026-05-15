from app.config import Settings


def test_settings_defaults():
    # Using the actual .env values that are loaded
    from app.config import settings as s
    assert s.allowed_origins is not None
    assert s.environment in ["development", "production"]
    assert isinstance(s.debug, bool)


def test_origins_list_property():
    settings = Settings(
        database_url="postgresql://user:pass@localhost/db",
        secret_key="testsecret",
        algorithm="HS256",
        access_token_expire_minutes=30,
        allowed_origins="http://localhost:3000,http://example.com",
    )
    origins = settings.origins_list
    assert len(origins) == 2
    assert "http://localhost:3000" in origins
    assert "http://example.com" in origins


def test_is_production_false():
    settings = Settings(
        database_url="postgresql://user:pass@localhost/db",
        secret_key="testsecret",
        algorithm="HS256",
        access_token_expire_minutes=30,
        environment="development",
    )
    assert settings.is_production is False


def test_is_production_true():
    settings = Settings(
        database_url="postgresql://user:pass@localhost/db",
        secret_key="testsecret",
        algorithm="HS256",
        access_token_expire_minutes=30,
        environment="production",
    )
    assert settings.is_production is True