from datetime import datetime, timedelta
from fastapi import FastAPI, Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from app.db.session import get_db
from app.db.models import Training, User, UserBMI
from redis import Redis
import redis
import os
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.Redis(
  host=os.getenv("REDIS_HOST"),
  port=os.getenv("REDIS_PORT"),
  password=os.getenv("REDIS_PASSWORD"),
  ssl=True
)

app = FastAPI()

GET_MAX_ATTEMPTS = 5
GET_BLOCK_SECONDS = 10

def get_client_id(user: User = Depends(get_current_user)) -> str:
    return f"user:{user.id}"

def get_rate_limiter(user: User = Depends(get_current_user)):
    client_id = get_client_id(user)
    key = f"get_rate_limit:{client_id}"

    attempts = redis_client.get(key)

    if attempts:
        attempts = int(attempts)

        if attempts >= GET_MAX_ATTEMPTS:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=f"Você excedeu o número de tentativas. Tente novamente em {GET_BLOCK_SECONDS} segundos.")

        redis_client.incr(key)

    else:
        redis_client.set(key, 1, ex=GET_BLOCK_SECONDS)


POST_MAX_ATTEMPTS = 3
POST_BLOCK_SECONDS = 30

def post_rate_limiter(user: User = Depends(get_current_user)):
    cliente_id = get_client_id(user)
    key = f"post_rate_limit:{cliente_id}"

    attempts = redis_client.get(key)

    if attempts:
        attempts = int(attempts)

        if attempts >= POST_MAX_ATTEMPTS:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=f"Você excedeu o número de tentativas. Tente novamente em {POST_BLOCK_SECONDS} segundos.")

        redis_client.incr(key)

    else:
        redis_client.set(key, 1, ex=POST_BLOCK_SECONDS)


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