from fastapi import FastAPI
from app.api.routes import user, bmi
from app.db.session import engine
from app.db.models import Base

# Initialize FastAPI
app = FastAPI()

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Register API routes
app.include_router(user.router, prefix="/api/users")
app.include_router(bmi.router, prefix="/api/bmi")

# Teste
@app.get("/")
def read_root():
    return {"message": "FastAPI running inside Docker!"}
