from fastapi import APIRouter, HTTPException
from typing import List
from models.schemas import VehiculeSchema, ErrorMessage
from services.queries import get_all_vehicules

router = APIRouter(prefix="/vehicules", tags=["Vehicules"])

@router.get("/", response_model=List[VehiculeSchema], responses={500: {"model": ErrorMessage}})
def read_vehicules():
    try:
        return get_all_vehicules()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
