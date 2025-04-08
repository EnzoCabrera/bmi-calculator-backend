from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from app.db.session import get_db
from app.db.models import Training, User, UserBMI
from app.services.training_service import calculate_training

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

    training: Training = (
        db.query(Training)
        .filter(Training.user_id == user.id)
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


@router.post("/create", response_model=TrainingResponse)
def create_training(training: TrainingCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

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
            free_time=training.free_time
        )

        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
