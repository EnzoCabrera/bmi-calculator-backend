from datetime import datetime, timedelta
from fastapi import FastAPI, Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from app.db.session import get_db
from app.db.models import Training, User, UserBMI, Diet
from redis import Redis
import redis
import os
from dotenv import load_dotenv

load_dotenv()

# environment variables for Redis
redis_client = redis.Redis(
  host=os.getenv("REDIS_HOST"),
  port=os.getenv("REDIS_PORT"),
  password=os.getenv("REDIS_PASSWORD"),
  ssl=True
)


app = FastAPI()


# GET variables
GET_MAX_ATTEMPTS = 5
GET_BLOCK_SECONDS = 10

# Requesting authentication to request the GET endpoints
def get_client_id(user: User = Depends(get_current_user)) -> str:
    return f"user:{user.id}"

# Attempt limiter for GET endpoints
def get_rate_limiter(user: User = Depends(get_current_user)):
    client_id = get_client_id(user)
    key = f"get_rate_limit:{client_id}"

    attempts = redis_client.get(key)

    if attempts:
        attempts = int(attempts)

        if attempts >= GET_MAX_ATTEMPTS:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=f'Muitas tentativas. Tente novamente em {GET_BLOCK_SECONDS} segundos.')

        redis_client.incr(key)

    else:
        redis_client.set(key, 1, ex=GET_BLOCK_SECONDS)


# POST variables
POST_MAX_ATTEMPTS = 3
POST_BLOCK_SECONDS = 30

# Attempt limiter for POST endpoints
def post_rate_limiter(user: User = Depends(get_current_user)):
    cliente_id = get_client_id(user)
    key = f"post_rate_limit:{cliente_id}"

    attempts = redis_client.get(key)

    if attempts:
        attempts = int(attempts)

        if attempts >= POST_MAX_ATTEMPTS:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=f'Muitas tentativas. Tente novamente em {POST_BLOCK_SECONDS} segundos.')

        redis_client.incr(key)

    else:
        redis_client.set(key, 1, ex=POST_BLOCK_SECONDS)


# auth variables
AUTH_MAX_ATTEMPTS = 3
AUTH_BLOCK_SECONDS = 30


# Getting the IP of user to request the endpoint
def auth_client_ip(request: Request) -> str:
    return request.client.host

# Attempt limiter for auth endpoints
def auth_rate_limiter(request: Request):
    client_ip = auth_client_ip(request)
    key = f"rate_limit:ip:{client_ip}"

    attempts = redis_client.get(key)

    if attempts:
        attempts = int(attempts) + 1
        redis_client.set(key, attempts, ex=AUTH_BLOCK_SECONDS)

        if attempts >= AUTH_MAX_ATTEMPTS:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=f'Muitas tentativas. Tente novamente em {AUTH_BLOCK_SECONDS} segundos.')

    else:
        redis_client.set(key, 1, ex=AUTH_BLOCK_SECONDS)



# Endpoint limiter for diets and trainings creation, applied for common users
def check_endpoint_limit(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role == 1:
        limit = datetime.utcnow() - timedelta(days=90)

        last_request = (db.query(Training).filter(Training.user_id == user.id).order_by(Training.created_at.desc()).first())

        if last_request and last_request.created_at >= limit:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Para acessar mais treinos e dietas, aguarde 3 meses ou assine o plano Plus.')


# Endpoint limiter for diets creation, applied for common users
def check_endpoint_limit_diets(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role == 1:
        limit = datetime.utcnow() - timedelta(days=90)

        last_diet = (db.query(Diet).filter(Diet.user_id == user.id).order_by(Diet.created_at.desc()).first())

        if last_diet and last_diet.created_at >= limit:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Para gerar novos treinos e dietas, aguarde 3 meses ou assine o plano Plus.')



# Endpoint limiter for BMI calculation, applied for common users
def check_bmi_limit(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role == 1:
        limit = datetime.utcnow() - timedelta(days=30)

        last_bmi = (db.query(UserBMI).filter(UserBMI.user_id == user.id).order_by(UserBMI.created_at.desc()).first())

        if last_bmi and last_bmi.created_at >= limit:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Para recalcular o IMC, aguarde 1 mês ou assine o plano Plus.')


def endpoint_admin_limit(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not user.role == 3:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Este recurso é exclusivo para administradores.')

