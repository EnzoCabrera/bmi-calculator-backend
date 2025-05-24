from datetime import datetime
from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from app.db.session import get_db
from app.db.models import Training, User, UserBMI
from app.services.training_service import calculate_training, parse_training_description
from app.services.endpoint_limit_service import check_endpoint_limit, post_rate_limiter, get_rate_limiter

router = APIRouter(tags=["Training"])


class TrainingDay(BaseModel):
    day: str
    exercises: List[Dict[str, str]]

# Response from creating a workout
class TrainingResponse(BaseModel):
    id: int
    user_id: int
    bmi_status_id: int
    description: str
    parsed_description: List[TrainingDay]

    class Config:
        from_attributes = True


# Creating a new training and saving it to the DB
@router.post("/create", response_model=TrainingResponse, dependencies=[Depends(post_rate_limiter)])
def create_training(db: Session = Depends(get_db), user: User = Depends(get_current_user), _: None = Depends(check_endpoint_limit)):
    user_bmi = db.query(UserBMI).filter(UserBMI.user_id == user.id).first()

    if not user_bmi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="IMC do usuário não encontrado.")
    try:
        result = calculate_training(
            db=db,
            user_bmi=user_bmi,
            bmi_status_id=user_bmi.bmi_status_id,
            user_id=user.id,
            training=Training(),
        )

        parsed = parse_training_description(result.description)

        return {
            "id": result.id,
            "user_id": result.user_id,
            "bmi_status_id": result.bmi_status_id,
            "description": result.description,
            "parsed_description": parsed,
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Getting the user's training by their ID
@router.get("/by-id", response_model=TrainingResponse, dependencies=[Depends(get_rate_limiter)])
def trainings_by_id(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user_training: UserBMI = (
        db.query(UserBMI)
        .filter(User.id == user.id)
        .order_by(UserBMI.created_at.desc())
        .first()
    )

    if not user_training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")

    training: Training = (
        db.query(Training)
        .filter(Training.user_id == user.id)
        .order_by(Training.id.desc())
        .first()
    )

    parsed = parse_training_description(training.description)

    return {
        "id": training.id,
        "user_id": training.user_id,
        "bmi_status_id": training.bmi_status_id,
        "description": training.description,
        "parsed_description": parsed
    }


# Getting all trainings in the DB
# @router.get("/get-all")
# def get_trainings(db: Session = Depends(get_db)):
#     trainings = db.query(Training).all()
#     return trainings






