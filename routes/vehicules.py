from fastapi import APIRouter, Query
from database import get_connection, get_cursor

router = APIRouter()


@router.get("/vehicules")
def get_vehicules(statut: str = Query(None)):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        if statut:
            cursor.execute("SELECT * FROM VEHICULE WHERE statut = %s", (statut,))
        else:
            cursor.execute("SELECT * FROM VEHICULE")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
