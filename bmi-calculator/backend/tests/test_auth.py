from unittest.mock import patch, MagicMock
from jose import jwt
from app.api.auth import hash_password, verify_password, create_access_token, get_current_user
from app.api.config import SECRET_KEY, ALGORITHM
from app.db.models import User


def test_hash_password():
    password = "senha"
    hashed_password = hash_password(password)
    assert hashed_password.startswith("$2b$")

def test_verify_password_correct():
    assert verify_password("senha", hash_password("senha"))
    assert verify_password("lmao", hash_password("lmao"))
    assert verify_password("LOREM IPSUM", hash_password("LOREM IPSUM"))
    assert verify_password("senha123", hash_password("senha123"))
    assert verify_password("123456", hash_password("123456"))

def test_verify_password_incorrect():
    assert not verify_password("senha123", hash_password("senha"))
    assert not verify_password("limao", hash_password("lmao"))
    assert not verify_password("LOREM IPSUM", hash_password("lorem ipsum"))
    assert not verify_password("senha", hash_password("senha123"))
    assert not verify_password("0123456", hash_password("123456"))

def test_create_access_token():
    emails = [
        "teste1@email.com",
        "teste2@email.com",
        "teste3@email.com",
        "teste4@email.com",
        "teste5@email.com",
    ]

    with patch('app.api.auth.jwt.encode') as mock_encode:
        mock_encode.side_effect = [f"fake.jwt.token.{i}" for i in range(5)]

        tokens = []
        for email in emails:
            token = create_access_token(data={"sub": email})
            tokens.append(token)

        assert mock_encode.call_count == 5

        assert tokens == [
            "fake.jwt.token.0",
            "fake.jwt.token.1",
            "fake.jwt.token.2",
            "fake.jwt.token.3",
            "fake.jwt.token.4",
        ]

def test_get_current_user():
    emails = [
        "teste1@email.com",
        "teste2@email.com",
        "teste3@email.com",
        "teste4@email.com",
        "teste5@email.com"
    ]

    for email in emails:
        token = jwt.encode({"sub": email}, SECRET_KEY, algorithm=ALGORITHM)
        user = User(email=email)

        mock_query = MagicMock()
        mock_db = MagicMock()

        mock_query.filter.return_value.first.return_value = user
        mock_db.query.return_value = mock_query

        result = get_current_user(token, mock_db)

        assert result == user
        assert result.email == email