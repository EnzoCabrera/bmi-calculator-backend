from unittest.mock import patch
from app.services.diets_service import calculate_diet
from app.db.models import UserBMI, Diet

# Testing if data are been saving correctly in the DB
def test_calculate_diet_with_mock(db_session):
    user_bmi = UserBMI(user_id=1, bmi_value=24.9, bmi_status_id=2)
    diet = Diet()

    fake_response = "Manhã: Aveia, 50g; Banana, 1 unidade; Noite: Batata-doce, 100g; Peito de frango grelhado, 150g; "


    with patch('app.services.diets_service.generate_diets_with_openai') as mock_openai:
        mock_openai.return_value = fake_response

        result = calculate_diet(
            db=db_session,
            user_bmi=user_bmi,
            bmi_status_id=2,
            user_id=1,
            diet=diet,
        )

        assert result.description == fake_response
        assert result.user_id == 1
        assert result.bmi_status_id == 2