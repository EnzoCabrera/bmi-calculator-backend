from app.db.models import UserBMI

prefix = "/api/history"

def test_get_history_by_id(client):
    response = client.get(f"{prefix}/latest-by-id")
    assert response.status_code == 200
    data = response.json()

    print(data)

    assert data["user_id"] == 1
    assert data["weight"] == 69
    assert data["bmi_value"] == 22.5

def test_get_history_by_id_failure(client, db_session):
    db_session.query(UserBMI).delete()

    response = client.get(f"{prefix}/latest-by-id")
    assert response.status_code == 404
    assert response.json()["detail"] == 'Não encontramos seu histórico.'