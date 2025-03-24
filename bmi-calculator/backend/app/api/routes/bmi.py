from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.calculation import calculate_bmi

router = APIRouter()

class CalculateBMI(BaseModel):
    weight: float
    height: float

@router.post("/")
def get_bmi(data: CalculateBMI):
    if data.height <= 0:
        raise HTTPException(status_code=400, detail="Height must be greater than zero")
    if data.weight <= 0:
        raise HTTPException(status_code=400, detail="Weight must be greater than zero")

    bmi = calculate_bmi(data.weight, data.height)
    return {f"bmi: {bmi:.2f}"}