from fastapi import APIRouter, HTTPException
from typing import List
from models.schemas import ChauffeurSchema, ErrorMessage
from services.queries import get_all_chauffeurs

router = APIRouter(prefix="/chauffeurs", tags=["Chauffeurs"])

@router.get("/", response_model=List[ChauffeurSchema], responses={500: {"model": ErrorMessage}})
def read_chauffeurs():
    try:
        return get_all_chauffeurs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
