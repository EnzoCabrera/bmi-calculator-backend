from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from app.db.session import get_db
from app.db.models import User, UserBMI
from app.services.endpoint_limit_service import get_rate_limiter

router = APIRouter(tags=["History"])

# Requested variables to GET the history
class UserBMIHistory(BaseModel):
    user_id: int
    weight: float
    bmi_value: float

    class Config:
        from_attributes = True

# Method to get the latest BMI from user
@router.get("/latest-by-id", response_model=UserBMIHistory, dependencies=[Depends(get_rate_limiter)])
def history_by_id(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user_bmi = (db.query(UserBMI).filter(UserBMI.user_id == user.id).order_by(UserBMI.id.desc()).first())

    if not user_bmi:
        raise HTTPException(status_code=404, detail="Histórico não encontrado.")

    return user_bmi