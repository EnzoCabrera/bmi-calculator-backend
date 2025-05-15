from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from app.db.session import get_db
from app.db.models import User, UserBMI

router = APIRouter()

class UserBMIHIstory(BaseModel):
    user_id: int
    weight: float
    bmi_value: float

    class Config:
        orm_mode = True

@router.get("/latest-by-id", response_model=UserBMIHIstory)
def history_by_id(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user_bmi = (db.query(UserBMI).filter(UserBMI.user_id == user.id).order_by(UserBMI.id.desc()).first())

    if not user_bmi:
        raise HTTPException(status_code=404, detail="History not found")

    return user_bmi