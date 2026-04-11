from fastapi import APIRouter, HTTPException, Query
from typing import List
from models.schemas import TrajetSchema, ErrorMessage
from services.queries import get_trajets

router = APIRouter(prefix="/trajets", tags=["Trajets"])

@router.get("/", response_model=List[TrajetSchema], responses={500: {"model": ErrorMessage}})
def read_trajets(skip: int = Query(0, ge=0), limit: int = Query(50, le=100)):
    try:
        return get_trajets(limit=limit, offset=skip)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
