from unittest.mock import patch
from app.services.training_service import calculate_training
from app.db.models import Training, UserBMI


# Testing if data are been saving correctly in the DB
def test_calculate_training_with_mock(db_session):
    user_bmi = UserBMI(user_id=1, bmi_value=24.9, bmi_status_id=2)
    training = Training(free_time=2)

    fake_response = "Treino: Exercício A: 3x12; Exercício B: 3x10;"

    with patch("app.services.training_service.generate_training_with_openai") as mock_openai:
        mock_openai.return_value = fake_response

        result = calculate_training(
            db=db_session,
            user_bmi=user_bmi,
            bmi_status_id=2,
            user_id=1,
            training=training,
            free_time=2,
        )

        assert result.description == fake_response
        assert result.user_id == 1
        assert result.bmi_status_id == 2
        assert result.free_time == 2