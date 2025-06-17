from app.db.models import UserBMI

prefix = "/api/bmi"

def test_create_bmi_success(client):
    test_bmi = {
        "weight": 80,
        "height": 1.80
    }

    response = client.post(f"{prefix}/create", json=test_bmi)
    assert response.status_code == 200
    data = response.json()

    assert data["weight"] == test_bmi["weight"]
    assert data["height"] == test_bmi["height"]

def test_create_bmi_invalid_input(client):
    test_bmi_invalid_weight = {
        "weight": -80,
        "height": 1.80
    }

    response = client.post(f"{prefix}/create", json=test_bmi_invalid_weight)
    data_invalid_weight = response.json()
    assert response.status_code == 400
    assert data_invalid_weight["detail"] == "Informe um peso válido (maior que zero)."

    test_bmi_invalid_height = {
        "weight": 80,
        "height": -1.80
    }

    response = client.post(f"{prefix}/create", json=test_bmi_invalid_height)
    data_invalid_height = response.json()
    assert response.status_code == 400
    assert data_invalid_height["detail"] == "Informe uma altura válida (maior que zero)."

def test_get_bmi_success(client):
    response = client.get(f"{prefix}/latest-by-id")
    assert response.status_code == 200
    data = response.json()

    assert data["bmi_value"] == 22.5
    assert data["height"] == 1.75
    assert data["weight"] == 69.0
    assert data["user_id"] == 1
    assert data["id"] == 1
    assert data["bmi_status_id"] == 2

def test_get_bmi_not_found(client, db_session):
    db_session.query(UserBMI).delete()
    db_session.commit()
    response = client.get(f"{prefix}/latest-by-id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Não conseguimos encontrar seu perfil. Verifique suas informações."
