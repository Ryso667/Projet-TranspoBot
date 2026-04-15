from fastapi import APIRouter
from database import get_connection, get_cursor

router = APIRouter()


@router.get("/kpi")
def get_kpi():
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        result = {}

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM TRAJET
            WHERE date_heure_depart >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        """)
        result["total_trajets_semaine"] = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM TRAJET WHERE statut = 'en cours'")
        result["trajets_en_cours"] = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM TRAJET WHERE statut = 'terminé'")
        result["trajets_termines"] = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM VEHICULE WHERE statut = 'maintenance'")
        result["vehicules_en_maintenance"] = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM INCIDENT
            WHERE MONTH(date_incident) = MONTH(NOW())
            AND YEAR(date_incident) = YEAR(NOW())
        """)
        result["incidents_ce_mois"] = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT c.nom, c.prenom, COUNT(i.id_incident) AS nb
            FROM INCIDENT i
            JOIN CHAUFFEUR c ON i.id_chauffeur = c.id_chauffeur
            GROUP BY i.id_chauffeur
            ORDER BY nb DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        if row:
            result["chauffeur_plus_incidents"] = f"{row['prenom']} {row['nom']}"
        else:
            result["chauffeur_plus_incidents"] = "N/A"

        cursor.execute("SELECT COUNT(*) AS total FROM CHAUFFEUR WHERE statut = 'actif'")
        result["total_chauffeurs_actifs"] = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM VEHICULE")
        result["total_vehicules"] = cursor.fetchone()["total"]

        return result
    finally:
        cursor.close()
        conn.close()
