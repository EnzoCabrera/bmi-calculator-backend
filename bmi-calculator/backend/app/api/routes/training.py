from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from app.db.session import get_db
from app.db.models import Training, User, UserBMI
from app.services.training_service import calculate_training

router = APIRouter()

# Getting all trainings in the DB
@router.get("/get-all")
def get_trainings(db: Session = Depends(get_db)):
    trainings = db.query(Training).all()
    return trainings

# Getting the user's training by their ID
@router.get("/by-id")
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
@router.put("/create", response_model=TrainingResponse)
def create_training(training: TrainingCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    user_bmi = db.query(UserBMI).filter(UserBMI.user_id == user.id).first()

    if not user_bmi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="IMC do usuário não encontrado")

    existing_training = db.query(Training).filter(Training.user_id == user.id).first()

    if not existing_training:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Treino do usuário não encontrado")

    try:
        result = calculate_training(
            db=db,
            user_bmi=user_bmi,
            bmi_status_id=user_bmi.bmi_status_id,
            user_id=user.id,
            training=existing_training,
            free_time=training.free_time
        )

        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
