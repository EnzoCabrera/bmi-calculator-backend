from app.db.models import User
from app.api.auth import verify_password

prefix = "/api/users"

def test_register(client, db_session):
    test_user = {
        "email": "email@teste.com",
        "password": "Senha123",
        "full_name": "Testosvaldo da Silva Unitario",
    }

    response = client.post(f"{prefix}/register", json=test_user)
    assert response.status_code == 200
    assert response.json()["message"] == 'Cadastro realizado com sucesso!'

    registered_user = db_session.query(User).filter(User.email == test_user["email"]).first()
    assert registered_user.email == test_user["email"]
    assert registered_user.full_name == test_user["full_name"]
    assert verify_password(test_user["password"], registered_user.password_hash)

def test_register_email_already_registered(client):
    test_user = {
        "email": "test@email.com",
        "password": "Senha123",
        "full_name": "Test User",
    }

    response = client.post(f"{prefix}/register", json=test_user)
    assert response.status_code == 400
    assert response.json()["detail"] == 'Este e-mail já está em uso. Tente outro'

def test_login(client, db_session):
    test_user_login = {
        "email": "test@email.com",
        "password": "123",
    }
    response = client.get(f"{prefix}/get-all")

    response = client.post(f"{prefix}/login", json=test_user_login)
    assert response.status_code == 200

def test_login_email_incorrect(client):
    test_user_login = {
        "email": "wrong@email.com",
        "password": "123",
    }
    response = client.post(f"{prefix}/login", json=test_user_login)
    assert response.status_code == 401
    data = response.json()
    print(data)
    assert data["detail"] == {
                "error": 'E-mail ou senha incorretos. Verifique e tente novamente.',
            }

def test_login_password_incorrect(client, db_session):
    test_user_login = {
        "email": "test@email.com",
        "password": "test",
    }
    response = client.post(f"{prefix}/login", json=test_user_login)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == {
                "error": 'E-mail ou senha incorretos. Verifique e tente novamente.',
            }
