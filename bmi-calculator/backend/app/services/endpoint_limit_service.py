from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from app.db.session import get_db
from app.db.models import Training, User

def check_endpoint_limit(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    limit = datetime.utcnow() - timedelta(days=90)

    last_request = (db.query(Training).filter(Training.user_id == user.id).filter(Training.created_at >= limit).first())

    if last_request:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Para mais treinos e dietas, necessário plano plus")