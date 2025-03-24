from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.auth import hash_password, verify_password, create_access_token, get_current_user
from app.api.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.db.session import get_db
from app.db.models import User

router = APIRouter()

class RegisterUser(BaseModel):
    email: str
    full_name: str
    password: str

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.post("/users/register")
def register_user(user: RegisterUser, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)

    new_user = User(email=user.email,
                    password_hash=hashed_password, full_name=user.full_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}
