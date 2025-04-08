import os
from dotenv import load_dotenv

# Secret key for JWT
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")