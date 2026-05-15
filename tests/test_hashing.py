from app.utils.hashing import hash_password, verify_password


def test_hash_password():
    hashed = hash_password("testpassword")
    assert hashed is not None
    assert hashed != "testpassword"
    assert len(hashed) > 0


def test_hash_password_different_hashes():
    """Same password should produce different hashes (due to salt)"""
    hash1 = hash_password("testpassword")
    hash2 = hash_password("testpassword")
    assert hash1 != hash2


def test_verify_password_correct():
    hashed = hash_password("testpassword")
    result = verify_password("testpassword", hashed)
    assert result is True


def test_verify_password_incorrect():
    hashed = hash_password("testpassword")
    result = verify_password("wrongpassword", hashed)
    assert result is False


def test_verify_password_empty():
    hashed = hash_password("testpassword")
    result = verify_password("", hashed)
    assert result is False