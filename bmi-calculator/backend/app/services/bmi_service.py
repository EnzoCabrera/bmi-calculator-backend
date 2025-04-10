from sqlalchemy.orm import Session
from app.db.models import UserBMI


def calculate_bmi(db: Session, user_id: int, weight: float, height: float):
    if height <= 0:
        raise ValueError("Altura deve ser maior que zero")

    bmi = round(weight / (height ** 2), 2)

    if bmi < 18.5:
        status_id = 1
    elif bmi < 25:
        status_id = 2
    elif bmi < 30:
        status_id = 3
    else:
        status_id = 4


    user_bmi = UserBMI(
        user_id=user_id,
        bmi_value=bmi,
        bmi_status_id=status_id,
    )

    db.add(user_bmi)
    db.commit()
    db.refresh(user_bmi)

    return user_bmi