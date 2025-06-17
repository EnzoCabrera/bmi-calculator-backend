from unittest.mock import patch
from app.db.models import UserBMI
from app.services.diets_service import sanitize_diet_text

prefix = "/api/diets"

test_diet = """
        Segunda: Refeição Segunda
        Terça: Refeição Terça
        Quarta: Refeição Quarta
        Quinta: Refeição Quinta
        Sexta: Refeição Sexta
        Sábado: Refeição Sábado
        Domingo: Refeição Domingo
        """

@patch("app.services.diets_service.generate_diets_with_openai")
def test_create_diet_success(mock_generate_diets_with_openai, client):
    mock_generate_diets_with_openai.return_value = test_diet
    intolerances = {
        "intolerances": ["lactose"]
    }

    response = client.post(f"{prefix}/create", json=intolerances)
    assert response.status_code == 200
    data = response.json()

    assert data["description"] == sanitize_diet_text(test_diet)

@patch("app.services.diets_service.generate_diets_with_openai")
def test_create_diet_no_bmi(mock_generate_diets_with_openai, client, db_session):
    mock_generate_diets_with_openai.return_value = test_diet
    intolerances = {
        "intolerances": ["lactose"]
    }

    db_session.query(UserBMI).delete()
    db_session.commit()

    response = client.post(f"{prefix}/create", json=intolerances)
    assert response.status_code == 404
    data = response.json()

    assert data["detail"] == "Não foi possível encontrar seu IMC. Cadastre suas informações primeiro."

def test_get_diet_success(client):
    response = client.get(f"{prefix}/by-id")
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == 1
    assert data["user_id"] == 1

def test_get_diet_not_found(client, db_session):
    db_session.query(UserBMI).delete()

    response = client.get(f"{prefix}/by-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Não foi possível encontrar seu IMC. Cadastre suas informações primeiro."
