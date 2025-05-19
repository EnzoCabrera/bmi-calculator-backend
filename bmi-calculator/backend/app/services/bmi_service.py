from sqlalchemy.orm import Session
from app.db.models import UserBMI

# Calculating the inputted BMI
def calculate_bmi(db: Session, user_id: int, weight: float, height: float):

    if height <= 0:
        raise ValueError("Altura deve ser maior que zero")
    if weight <= 0:
        raise ValueError("Peso deve ser maior que zero")

    if height > 2.72:
        height /= 100

    user_bmi = UserBMI(user_id=user_id)

    bmi = round(weight / (height ** 2), 2)

    if bmi < 18.5:
        status_id = 1
    elif bmi < 25:
        status_id = 2
    elif bmi < 30:
        status_id = 3
    else:
        status_id = 4

    user_bmi.weight = weight
    user_bmi.height = height
    user_bmi.bmi_value = bmi
    user_bmi.bmi_status_id = status_id


    db.add(user_bmi)
    db.commit()
    db.refresh(user_bmi)


    return user_bmi
