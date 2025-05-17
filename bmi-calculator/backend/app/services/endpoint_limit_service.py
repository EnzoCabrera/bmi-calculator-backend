from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from app.db.session import get_db
from app.db.models import Training, User, UserBMI


# Endpoint limiter for diets and trainings creation
def check_endpoint_limit(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role == 1:
        limit = datetime.utcnow() - timedelta(days=90)

        last_request = (db.query(Training).filter(Training.user_id == user.id).filter(Training.created_at >= limit).first())

        if last_request:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Para mais treinos e dietas, necessário plano plus")


# Endpoint limiter for BMI calculation
def check_bmi_limit(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role == 1:
        limit = datetime.utcnow() - timedelta(days=30)

        last_request = (db.query(UserBMI.user_id == user.id).filter(UserBMI.created_at >= limit).first())

        if last_request:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Para calcular novamente o IMC, aguarde um mês ou assine o plano plus")