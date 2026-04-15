from fastapi import APIRouter, Query
from database import get_connection, get_cursor

router = APIRouter()


@router.get("/chauffeurs")
def get_chauffeurs(statut: str = Query(None)):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        if statut:
            cursor.execute("SELECT * FROM CHAUFFEUR WHERE statut = %s", (statut,))
        else:
            cursor.execute("SELECT * FROM CHAUFFEUR")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
