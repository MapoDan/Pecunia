from app.services.auth import GoogleIdentity, _hash_secret


def test_google_identity_shape() -> None:
    identity = GoogleIdentity(subject="google-sub", email="user@example.com", display_name="User Example")
    assert identity.subject == "google-sub"
    assert identity.email == "user@example.com"


def test_session_hash_is_deterministic_and_not_plaintext() -> None:
    token = "session-token"
    assert _hash_secret(token) == _hash_secret(token)
    assert _hash_secret(token) != token
