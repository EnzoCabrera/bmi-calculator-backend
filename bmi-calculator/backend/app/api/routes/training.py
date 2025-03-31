from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from app.db.session import get_db
from app.db.models import Training, User, UserBMI

router = APIRouter()

@router.get("/get-all")
def get_trainings(db: Session = Depends(get_db)):
    trainings = db.query(Training).all()
    return trainings

@router.get("/by-BMI")
def trainings_by_BMI(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user_training: UserBMI = (
        db.query(UserBMI)
        .filter(User.id == user.id)
        .order_by(UserBMI.created_at.desc())
        .first()
    )

    if not user_training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


    trainings_list: Training = (
        db.query(Training)
        .filter(Training.bmi_status_id == user_training.bmi_status_id)
        .all()
    )
    return trainings_list
