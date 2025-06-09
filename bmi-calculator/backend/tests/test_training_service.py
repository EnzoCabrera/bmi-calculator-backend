from unittest.mock import patch
from app.services.training_service import calculate_training, parse_training_description
from app.db.models import Training, UserBMI


# Testing if data are been saving correctly in the DB
def test_calculate_training_with_mock(db_session):
    user_bmi = UserBMI(user_id=1, bmi_value=24.9, bmi_status_id=2)
    training = Training()

    fake_response = "Treino: Exercício A: 3x12; Exercício B: 3x10;"

    with patch("app.services.training_service.generate_training_with_openai") as mock_openai:
        mock_openai.return_value = fake_response

        result = calculate_training(
            db=db_session,
            user_bmi=user_bmi,
            bmi_status_id=2,
            user_id=1,
            training=training,
        )

        assert result.description == fake_response
        assert result.user_id == 1
        assert result.bmi_status_id == 2

def test_parse_training_description():
    unparsed_text = ("Segunda: Exercicio 1: 4x10; Exercicio 2: 3x12;"
                     "Terça: Exercicio 3: 3x10; Exercicio 4: 3x10;"
                     "Quarta: Exercicio 5: 4x10; Exercicio 6: 3x10;"
                     "Quinta: Exercicio 7: 3x12; Exercicio 8: 4x10;"
                     "Sexta: Exercicio 9: 4x15; Exercicio 10: 3x10;")

    expected = [
        {
            "day": "Segunda",
            "exercises": [
                {"exercicio": "Exercicio 1", "repeticoes": "4x10"},
                {"exercicio": "Exercicio 2", "repeticoes": "3x12"},
            ],
        },
        {
            "day": "Terça",
            "exercises": [
                {"exercicio": "Exercicio 3", "repeticoes": "3x10"},
                {"exercicio": "Exercicio 4", "repeticoes": "3x10"},
            ],
        },
        {
            "day": "Quarta",
            "exercises": [
                {"exercicio": "Exercicio 5", "repeticoes": "4x10"},
                {"exercicio": "Exercicio 6", "repeticoes": "3x10"},
            ],
        },
        {
            "day": "Quinta",
            "exercises": [
                {"exercicio": "Exercicio 7", "repeticoes": "3x12"},
                {"exercicio": "Exercicio 8", "repeticoes": "4x10"},
            ]
        },
        {
            "day": "Sexta",
            "exercises": [
                {"exercicio": "Exercicio 9", "repeticoes": "4x15"},
                {"exercicio": "Exercicio 10", "repeticoes": "3x10"},
            ]
        }
    ]

    assert parse_training_description(unparsed_text) == expected