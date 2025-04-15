from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from app.db.session import get_db
from app.services.bmi_service import calculate_bmi
from app.db.models import User

router = APIRouter()

class CalculateBMI(BaseModel):
    weight: float
    height: float

# Calculating the user's BMI and saving it to the DB
@router.post("/bmi")
def get_bmi(data: CalculateBMI, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if data.height <= 0:
        raise HTTPException(status_code=400, detail="Height must be greater than zero")
    if data.weight <= 0:
        raise HTTPException(status_code=400, detail="Weight must be greater than zero")

    try:
        user_bmi = calculate_bmi(db, user_id=user.id, weight=data.weight, height=data.height)
        return {
            "bmi": user_bmi.bmi_value,
            "bmi_status_id": user_bmi.bmi_status_id,
            "created_at": user_bmi.created_at,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))