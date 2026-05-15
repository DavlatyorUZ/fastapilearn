from app import models


def test_category_tablename():
    assert models.Category.__tablename__ == "categories"


def test_user_tablename():
    assert models.User.__tablename__ == "users"


def test_post_tablename():
    assert models.Post.__tablename__ == "posts"


def test_category_fields():
    assert hasattr(models.Category, "id")
    assert hasattr(models.Category, "name")
    assert hasattr(models.Category, "description")
    assert hasattr(models.Category, "created_at")
    assert hasattr(models.Category, "posts")


def test_user_fields():
    assert hasattr(models.User, "id")
    assert hasattr(models.User, "username")
    assert hasattr(models.User, "email")
    assert hasattr(models.User, "password")
    assert hasattr(models.User, "phone")
    assert hasattr(models.User, "created_at")
    assert hasattr(models.User, "posts")


def test_post_fields():
    assert hasattr(models.Post, "id")
    assert hasattr(models.Post, "title")
    assert hasattr(models.Post, "content")
    assert hasattr(models.Post, "published")
    assert hasattr(models.Post, "rating")
    assert hasattr(models.Post, "created_at")
    assert hasattr(models.Post, "owner_id")
    assert hasattr(models.Post, "category_id")
    assert hasattr(models.Post, "owner")
    assert hasattr(models.Post, "category")


def test_category_relationship(db, test_category):
    from app import models
    category = db.query(models.Category).filter_by(id=test_category.id).first()
    assert category is not None


def test_user_relationship(db, test_user):
    from app import models
    user = db.query(models.User).filter_by(id=test_user.id).first()
    assert user is not None


def test_post_relationship(db, test_post):
    from app import models
    post = db.query(models.Post).filter_by(id=test_post.id).first()
    assert post is not None
    assert post.owner is not None
    assert post.category is not None