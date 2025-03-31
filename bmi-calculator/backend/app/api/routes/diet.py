from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from app.db.session import get_db
from app.db.models import Diet, User, UserBMI

router = APIRouter()

@router.get("/get-all")
def get_diets(db: Session = Depends(get_db)):
    diets = db.query(Diet).all()
    return diets

@router.get("/by-BMI")
def diets_by_BMI(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user_diet: UserBMI = (
        db.query(UserBMI)
        .filter(User.id == user.id)
        .order_by(UserBMI.created_at.desc())
        .first()
    )

    if not user_diet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


    diets_list: Diet = (
        db.query(Diet)
        .filter(Diet.bmi_status_id == user_diet.bmi_status_id)
        .all()
    )
    return diets_list
