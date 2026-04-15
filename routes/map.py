from fastapi import APIRouter
from database import get_connection, get_cursor

router = APIRouter()


@router.get("/map-data")
def get_map_data():
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute(
            """
            SELECT
                t.id_trajet,
                t.id_ligne,
                c.nom AS chauffeur_nom,
                c.prenom AS chauffeur_prenom,
                v.immatriculation AS vehicule_immat,
                v.marque AS vehicule_marque,
                v.typeVehicule AS vehicule_type,
                l.nom_ligne AS ligne_nom,
                ad.nom_arret AS arret_depart_nom,
                ad.localisation AS arret_depart_localisation,
                aa.nom_arret AS arret_arrivee_nom,
                aa.localisation AS arret_arrivee_localisation,
                la.id_arret AS ligne_arret_id,
                ar.nom_arret AS ligne_arret_nom,
                ar.localisation AS ligne_arret_localisation,
                la.ordre AS ligne_arret_ordre
            FROM TRAJET t
            LEFT JOIN CHAUFFEUR c ON t.id_chauffeur = c.id_chauffeur
            LEFT JOIN VEHICULE v ON t.immatriculation = v.immatriculation
            LEFT JOIN LIGNE l ON t.id_ligne = l.id_ligne
            LEFT JOIN ARRET ad ON t.id_arret_depart = ad.id_arret
            LEFT JOIN ARRET aa ON t.id_arret_arrivee = aa.id_arret
            LEFT JOIN LIGNE_ARRET la ON la.id_ligne = t.id_ligne
            LEFT JOIN ARRET ar ON la.id_arret = ar.id_arret
            WHERE t.statut = 'en cours'
            ORDER BY t.id_trajet, la.ordre
            """
        )
        rows = cursor.fetchall()

        trajets_by_id = {}
        for row in rows:
            traj_id = row["id_trajet"]
            if traj_id not in trajets_by_id:
                base = {
                    "id_trajet": traj_id,
                    "id_ligne": row["id_ligne"],
                    "chauffeur_nom": row["chauffeur_nom"],
                    "chauffeur_prenom": row["chauffeur_prenom"],
                        "vehicule_immat": row["vehicule_immat"],
                    "vehicule_marque": row["vehicule_marque"],
                    "vehicule_type": row["vehicule_type"],
                    "ligne_nom": row["ligne_nom"],
                    "arret_depart_nom": row["arret_depart_nom"],
                    "arret_depart_localisation": row["arret_depart_localisation"],
                    "arret_arrivee_nom": row["arret_arrivee_nom"],
                    "arret_arrivee_localisation": row["arret_arrivee_localisation"],
                    "ligne_stops": [],
                }
                trajets_by_id[traj_id] = base

            if row["ligne_arret_id"] is not None:
                trajets_by_id[traj_id]["ligne_stops"].append({
                    "id_arret": row["ligne_arret_id"],
                    "nom_arret": row["ligne_arret_nom"],
                    "localisation": row["ligne_arret_localisation"],
                    "ordre": row["ligne_arret_ordre"],
                })

        trajets_en_cours = list(trajets_by_id.values())

        cursor.execute(
            """
            SELECT id_arret, nom_arret, localisation
            FROM ARRET
            ORDER BY nom_arret ASC
            """
        )
        arrets = cursor.fetchall()

        return {
            "trajets_en_cours": trajets_en_cours,
            "arrets": arrets,
        }
    finally:
        cursor.close()
        conn.close()
