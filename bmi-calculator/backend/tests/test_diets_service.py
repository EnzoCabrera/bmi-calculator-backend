from unittest.mock import patch
from tests.conftest import DummyTexts
from app.services.diets_service import calculate_diet, sanitize_diet_text, parse_diet_description
from app.db.models import UserBMI, Diet

# Testing if data are been saving correctly in the DB
def test_calculate_diet_with_mock(client, db_session):
    user_bmi = UserBMI(user_id=1, bmi_value=24.9, bmi_status_id=2)
    diet = Diet()

    fake_response = DummyTexts.test_diet

    with patch('app.services.diets_service.generate_diets_with_openai') as mock_openai:
        mock_openai.return_value = DummyTexts.test_diet

        result = calculate_diet(
            db=db_session,
            user_bmi=user_bmi,
            bmi_status_id=2,
            user_id=1,
            diet=diet,
            intolerances=[],
        )

        assert result.description == fake_response
        assert result.user_id == 1
        assert result.bmi_status_id == 2

def test_sanitize_diet_text():
    unsanitized_text = """
        Café da Manhã:ovos mexidos;;  pão integral  ;
        Almoço:arroz , feijão ,  carne assada.. 
        Café da Tarde:  bolo  de  cenoura , suco de laranja ; ;
        Jantar : sopa  de legumes , pão ; 
        Ingredientes :  água , sal ,  legumes
        """

    expected = (
        "Café da Manhã: ovos mexidos; pão integral; "
        "Almoço: arroz, feijão, carne assada. "
        "Café da Tarde: bolo de cenoura, suco de laranja; "
        "Jantar: sopa de legumes, pão; "
        "Ingredientes: água, sal, legumes"
    )

    assert sanitize_diet_text(unsanitized_text) == expected

def test_parse_diet_description():
    unparsed_text = "Segunda: Café da Manhã: Prato: Pão com ovo; Ingredientes: Pão, ovo, manteiga Almoço: Prato: Arroz e feijão; Ingredientes: Arroz, feijão, carne Café da Tarde: Prato: Bolo; Ingredientes: Farinha, açúcar, ovo Jantar: Prato: Sopa; Ingredientes: Legumes, sal Terça: Café da Manhã: Prato: Tapioca; Ingredientes: Goma, queijo Almoço: Prato: Macarrão; Ingredientes: Massa, molho, carne Café da Tarde: Prato: Iogurte; Ingredientes: Iogurte natural Jantar: Prato: Omelete; Ingredientes: Ovo, tomate, cebola"

    expected = [
        {
            "day": "Segunda",
            "meals": [
                {"meal": "Café da Manhã", "dish": "Pão com ovo", "ingredients": "Pão, ovo, manteiga"},
                {"meal": "Almoço", "dish": "Arroz e feijão", "ingredients": "Arroz, feijão, carne"},
                {"meal": "Café da Tarde", "dish": "Bolo", "ingredients": "Farinha, açúcar, ovo"},
                {"meal": "Jantar", "dish": "Sopa", "ingredients": "Legumes, sal"},
            ],
        },
        {
            "day": "Terça",
            "meals": [
                {"meal": "Café da Manhã", "dish": "Tapioca", "ingredients": "Goma, queijo"},
                {"meal": "Almoço", "dish": "Macarrão", "ingredients": "Massa, molho, carne"},
                {"meal": "Café da Tarde", "dish": "Iogurte", "ingredients": "Iogurte natural"},
                {"meal": "Jantar", "dish": "Omelete", "ingredients": "Ovo, tomate, cebola"},
            ],
        },
    ]

    assert parse_diet_description(unparsed_text) == expected