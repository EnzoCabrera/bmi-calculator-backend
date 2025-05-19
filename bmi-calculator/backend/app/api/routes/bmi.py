from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from app.db.session import get_db
from app.services.bmi_service import calculate_bmi
from app.db.models import User, UserBMI
from app.services.endpoint_limit_service import check_bmi_limit, get_rate_limiter, post_rate_limiter
from datetime import datetime

router = APIRouter()

# Request variables to calculate BMI
class CalculateBMI(BaseModel):
    weight: float
    height: float

# Calculating the user's BMI and saving it to the DB
@router.put("/create", dependencies=[Depends(post_rate_limiter)])
def create_bmi(data: CalculateBMI, db: Session = Depends(get_db), user: User = Depends(get_current_user), _: None = Depends(check_bmi_limit)):
    if data.height <= 0:
        raise HTTPException(status_code=400, detail="Height must be greater than zero")
    if data.weight <= 0:
        raise HTTPException(status_code=400, detail="Weight must be greater than zero")

    try:
        user_bmi = calculate_bmi(db, user_id=user.id, weight=data.weight, height=data.height)
        return {
            "bmi": user_bmi.bmi_value,
            "bmi_status_id": user_bmi.bmi_status_id,
            "created_at": datetime.utcnow(),
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Endpoint to get user's bmi
@router.get("/latest-by-id", dependencies=[Depends(get_rate_limiter)])
def get_bmi(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
        user_bmi: UserBMI = (db.query(UserBMI).filter(UserBMI.user_id == user.id).order_by(UserBMI.created_at.desc()).first())

        if not user_bmi:
            raise HTTPException(status_code=404, detail="User not found")

        return user_bmi