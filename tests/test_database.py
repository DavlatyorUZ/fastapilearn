from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db


def test_base_declarative():
    from app import models
    assert hasattr(models.Category, "__tablename__")
    assert hasattr(models.User, "__tablename__")
    assert hasattr(models.Post, "__tablename__")


def test_get_db_yields_session():
    """Test that get_db is a generator that yields a session"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    gen = override_get_db()
    session = next(gen)
    assert session is not None
    # Cleanup
    gen.close()
    Base.metadata.drop_all(bind=engine)