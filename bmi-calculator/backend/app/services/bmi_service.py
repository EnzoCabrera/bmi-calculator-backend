from sqlalchemy.orm import Session
from app.db.models import UserBMI, History

# Calculating the inputted BMI
def calculate_bmi(db: Session, user_id: int, weight: float, height: float):

    user_bmi = db.query(UserBMI).filter(UserBMI.user_id == user_id).order_by(UserBMI.created_at.desc()).first()

    if height <= 0:
        raise ValueError("Altura deve ser maior que zero")

    if not user_bmi:
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

    history = History(
        user_id=user_id,
        bmi_value=bmi,
        weight=weight
    )

    db.add(user_bmi)
    db.add(history)
    db.commit()
    db.refresh(user_bmi)
    db.refresh(history)

    return user_bmi
    return history