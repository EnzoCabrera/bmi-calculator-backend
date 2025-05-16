from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from app.db.session import get_db
from app.db.models import Diet, User, UserBMI
from app.services.diets_service import calculate_diet
from app.services.endpoint_limit_service import check_endpoint_limit

router = APIRouter()

class DietCreate(BaseModel):
    intolerances: List[str]

class DietResponse(BaseModel):
    id: int
    user_id: int
    bmi_status_id: int
    description: str

    class Config:
        from_attributes = True


# Creating a new diet and saving it to the DB
@router.post("/create", response_model=DietResponse)
def create_diet(diet: DietCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user), _: None = Depends(check_endpoint_limit)):
    user_bmi = db.query(UserBMI).filter(User.id == user.id).first()

    if not user_bmi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="IMC do usuário não encontrado")

    existing_diet = db.query(Diet).filter(Diet.user_id == user.id).first()

    try:
        result = calculate_diet(
            db=db,
            user_bmi=user_bmi,
            bmi_status_id=user_bmi.bmi_status_id,
            user_id=user.id,
            diet=Diet(),
            intolerances=diet.intolerances
        )

        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Getting the user's diet by their ID
@router.get("/by-id")
def diets_by_id(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user_diet: UserBMI = (
        db.query(UserBMI)
        .filter(User.id == user.id)
        .order_by(UserBMI.created_at.desc())
        .first()
    )

    if not user_diet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    diet: Diet = (
        db.query(Diet)
        .filter(Diet.user_id == user.id)
        .order_by(Diet.id.desc())
        .first()
    )
    return diet


# Getting all diets in the DB
# @router.get("/get-all")
# def get_diets(db: Session = Depends(get_db)):
#     diets = db.query(Diet).all()
#     return diets






