from fastapi import APIRouter, HTTPException
from models.schemas import KPISchema, ErrorMessage
from services.queries import get_kpi

router = APIRouter(prefix="/kpi", tags=["KPI Dashboard"])

@router.get("/", response_model=KPISchema, responses={500: {"model": ErrorMessage}})
def read_kpi():
    try:
        return get_kpi()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
