from unittest.mock import patch
from tests.conftest import DummyTexts
from app.db.models import UserBMI, Training

prefix = "/api/trainings"

test_training = DummyTexts.test_training

@patch("app.services.training_service.generate_training_with_openai")
def test_create_training_success(mock_generate_training_with_openai, client):
    mock_generate_training_with_openai.return_value = test_training

    response = client.post(f"{prefix}/create")
    assert response.status_code == 200
    data = response.json()

    assert data["description"] == test_training

@patch("app.services.training_service.generate_training_with_openai")
def test_create_training_no_bmi(mock_generate_training_with_openai, client, db_session):
    mock_generate_training_with_openai.return_value = test_training
    intolerances = {
        "intolerances": ["lactose"]
    }

    db_session.query(UserBMI).delete()
    db_session.commit()

    response = client.post(f"{prefix}/create", json=intolerances)
    assert response.status_code == 404
    data = response.json()

    assert data["detail"] == "Não foi possível encontrar seu IMC. Cadastre suas informações primeiro."

def test_get_training_success(client):
    response = client.get(f"{prefix}/by-id")
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == 1
    assert data["user_id"] == 1

def test_get_training_not_found(client, db_session):
    db_session.query(Training).delete()

    response = client.get(f"{prefix}/by-id")
    assert response.status_code == 404
    assert response.json()["detail"] == 'Você ainda não criou nenhum treino.'

def test_get_training_bmi_not_found(client, db_session):
    db_session.query(UserBMI).delete()

    response = client.get(f"{prefix}/by-id")
    assert response.status_code == 404
    assert response.json()["detail"] == 'Não foi possível encontrar seu IMC. Cadastre suas informações primeiro.'
