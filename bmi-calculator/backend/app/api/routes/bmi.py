from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from app.db.session import get_db
from app.services.bmi_service import calculate_bmi
from app.db.models import User, UserBMI
from app.services.endpoint_limit_service import check_bmi_limit, get_rate_limiter, post_rate_limiter
from datetime import datetime

router = APIRouter(tags=["Bmi"])

# Response from calculating bmi
class BmiResponse(BaseModel):
    bmi_status_id: int
    bmi_value: float
    weight: float
    height: float
    user_id: int
    id: int
    created_at: datetime

# Request variables to calculate BMI
class CalculateBMI(BaseModel):
    weight: float
    height: float

# Calculating the user's BMI and saving it to the DB
@router.post("/create", response_model=BmiResponse, dependencies=[Depends(post_rate_limiter)])
def create_bmi(data: CalculateBMI, db: Session = Depends(get_db), user: User = Depends(get_current_user), _: None = Depends(check_bmi_limit)):
    if data.height <= 0:
        raise HTTPException(status_code=400, detail="Altura deve ser maior que zero.")
    if data.weight <= 0:
        raise HTTPException(status_code=400, detail="Peso deve ser maior que zero.")

    try:
        result = calculate_bmi(
            db=db,
            user_id=user.id,
            weight=data.weight,
            height=data.height,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Endpoint to get user's bmi
@router.get("/latest-by-id", response_model=BmiResponse, dependencies=[Depends(get_rate_limiter)])
def get_bmi(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
        user_bmi: UserBMI = (db.query(UserBMI).filter(UserBMI.user_id == user.id).order_by(UserBMI.created_at.desc()).first())

        if not user_bmi:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")

        return user_bmi