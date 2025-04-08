from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from app.db.session import get_db
from app.db.models import Diet, User, UserBMI
from app.services.diets_service import calculate_diet

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


class DietResponse(BaseModel):
    id: int
    user_id: int
    bmi_status_id: int
    description: str

    class Config:
        from_attributes = True


@router.post("/create", response_model=DietResponse)
def create_diet(db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    user_bmi = db.query(UserBMI).filter(UserBMI.user_id == user.id).first()

    if not user_bmi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="IMC do usuário não encontrado")

    try:
        result = calculate_diet(
            db=db,
            user_bmi=user_bmi,
            bmi_status_id=user_bmi.bmi_status_id,
            user_id=user.id,
            diet=Diet(),
        )

        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))