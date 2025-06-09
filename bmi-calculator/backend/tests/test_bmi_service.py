import pytest
from app.services.bmi_service import calculate_bmi

# Testing the calculator of BMI
def test_calculate_bmi_value(db_session):
    user_id = 1
    weight = 50
    height = 1.80

    result = calculate_bmi(db_session ,user_id, weight, height)
    assert result.bmi_value == round(weight / (height ** 2), 2)

# Testing if the user_id is correct
def test_calculate_user_id(db_session):
    user_id = 1
    weight = 50
    height = 1.80

    result = calculate_bmi(db_session ,user_id, weight, height)
    assert result.user_id == user_id

# Testing underweight status_id
def test_calculate_bmi_underweight(db_session):
    user_id = 1
    weight = 50
    height = 1.80

    result = calculate_bmi(db_session ,user_id, weight, height)
    assert result.bmi_status_id == 1

# Testing normal weight status_id
def test_calculate_bmi_normal(db_session):
    user_id = 2
    weight = 68
    height = 1.75

    result = calculate_bmi(db_session ,user_id, weight, height)
    assert result.bmi_status_id == 2


# Testing overweight status_id
def test_calculate_bmi_overweight(db_session):
    user_id = 3
    weight = 85
    height = 1.75

    result = calculate_bmi(db_session ,user_id, weight, height)
    assert result.bmi_status_id == 3


# Testing obese status_id
def test_calculate_bmi_obese(db_session):
    user_id = 4
    weight = 100
    height = 1.65

    result = calculate_bmi(db_session ,user_id, weight, height)
    assert result.bmi_status_id == 4


# Testing invalid weight
def test_calculate_bmi_invalid_weight(db_session):
    user_id = 5
    weight = 70
    height = 0

    with pytest.raises(ValueError):
        calculate_bmi(db_session ,user_id, weight, height)