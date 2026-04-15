from fastapi import APIRouter, Query
from database import get_connection, get_cursor

router = APIRouter()


@router.get("/trajets")
def get_trajets(statut: str = Query(None), limite: int = Query(50)):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        sql = """
            SELECT t.*, 
                   c.nom AS chauffeur_nom, c.prenom AS chauffeur_prenom,
                   v.marque AS vehicule_marque, v.modele AS vehicule_modele
            FROM TRAJET t
            LEFT JOIN CHAUFFEUR c ON t.id_chauffeur = c.id_chauffeur
            LEFT JOIN VEHICULE v ON t.immatriculation = v.immatriculation
        """
        params = []
        if statut:
            sql += " WHERE t.statut = %s"
            params.append(statut)
        sql += " ORDER BY t.date_heure_depart DESC LIMIT %s"
        params.append(limite)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        for row in rows:
            for key in ['date_heure_depart', 'date_heure_arrivee']:
                if row.get(key) and hasattr(row[key], 'isoformat'):
                    row[key] = row[key].isoformat()
        return rows
    finally:
        cursor.close()
        conn.close()
