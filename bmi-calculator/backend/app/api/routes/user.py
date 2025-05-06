from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import timedelta
from app.api.auth import hash_password, verify_password, create_access_token, get_current_user
from app.api.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.db.session import get_db
from app.db.models import User

router = APIRouter()

class RegisterUser(BaseModel):
    email: str
    full_name: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Getting all users in the DB
# @router.get("/")
# def get_users(db: Session = Depends(get_db)):
#     users = db.query(User).all()
#     return users

# Creating a new user and saving to the DB
@router.post("/register")
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

# Creating a JWT token if the inputted email and password are found in the DB
@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer", "user_id": str(db_user.id)}
