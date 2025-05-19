from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from app.db.session import get_db
from app.db.models import Training, User, UserBMI
from app.services.training_service import calculate_training
from app.services.endpoint_limit_service import check_endpoint_limit, post_rate_limiter, get_rate_limiter

router = APIRouter()

class TrainingCreate(BaseModel):
    free_time: int

class TrainingResponse(BaseModel):
    id: int
    user_id: int
    bmi_status_id: int
    free_time: int
    description: str

    class Config:
        from_attributes = True


# Creating a new training and saving it to the DB
@router.post("/create", response_model=TrainingResponse, dependencies=[Depends(post_rate_limiter)])
def create_training(training: TrainingCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user), _: None = Depends(check_endpoint_limit)):
    user_bmi = db.query(UserBMI).filter(UserBMI.user_id == user.id).first()

    if not user_bmi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="IMC do usuário não encontrado")
    try:
        result = calculate_training(
            db=db,
            user_bmi=user_bmi,
            bmi_status_id=user_bmi.bmi_status_id,
            user_id=user.id,
            training=Training(),
            free_time=training.free_time,
        )

        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Getting the user's training by their ID
@router.get("/by-id", dependencies=[Depends(get_rate_limiter)])
def trainings_by_id(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user_training: UserBMI = (
        db.query(UserBMI)
        .filter(User.id == user.id)
        .order_by(UserBMI.created_at.desc())
        .first()
    )

    if not user_training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    training: Training = (
        db.query(Training)
        .filter(Training.user_id == user.id)
        .order_by(Training.id.desc())
        .first()
    )
    return training


# Getting all trainings in the DB
# @router.get("/get-all")
# def get_trainings(db: Session = Depends(get_db)):
#     trainings = db.query(Training).all()
#     return trainings






