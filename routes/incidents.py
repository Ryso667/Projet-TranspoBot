from fastapi import APIRouter
from database import get_connection, get_cursor

router = APIRouter()


@router.get("/incidents")
def get_incidents():
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        sql = """
            SELECT i.*,
                   c.nom AS chauffeur_nom, c.prenom AS chauffeur_prenom,
                   v.marque AS vehicule_marque, v.immatriculation AS vehicule_immat
            FROM INCIDENT i
            LEFT JOIN CHAUFFEUR c ON i.id_chauffeur = c.id_chauffeur
            LEFT JOIN VEHICULE v ON i.immatriculation = v.immatriculation
            ORDER BY i.date_incident DESC
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            if row.get('date_incident') and hasattr(row['date_incident'], 'isoformat'):
                row['date_incident'] = row['date_incident'].isoformat()
        return rows
    finally:
        cursor.close()
        conn.close()
