from fastapi import APIRouter, HTTPException
from typing import List
from models.schemas import IncidentSchema, ErrorMessage
from services.queries import get_all_incidents

router = APIRouter(prefix="/incidents", tags=["Incidents"])

@router.get("/", response_model=List[IncidentSchema], responses={500: {"model": ErrorMessage}})
def read_incidents():
    try:
        return get_all_incidents()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
