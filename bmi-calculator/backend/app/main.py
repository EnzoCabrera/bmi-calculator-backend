from fastapi import FastAPI
from app.api.openapi import custom_openapi
from app.api.routes import user, bmi, diet, training, history
from app.db.session import engine
from app.db.models import Base
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://bmifit.vercel.app", "http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.openapi = lambda: custom_openapi(app)

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Register API routes
app.include_router(user.router, prefix="/api/users")
app.include_router(bmi.router, prefix="/api/bmi")
app.include_router(diet.router, prefix="/api/diets")
app.include_router(training.router, prefix="/api/trainings")
app.include_router(history.router, prefix="/api/history")

