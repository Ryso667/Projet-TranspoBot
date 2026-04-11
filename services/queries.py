import mysql.connector
from database import get_connection

def execute_query(query, params=None):
    """Exécute une requête de sélection et retourne les résultats."""
    conn = get_connection()
    if conn is None:
        raise Exception("Connexion MySQL perdue ou indisponible.")
    
    try:
        cursor = conn.cursor(dictionary=True) # Retourne des dictionnaires
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as err:
        raise Exception(f"Erreur SQL : {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def execute_scalar(query, params=None):
    """Exécute une requête et retourne une valeur scalaire unique (ex: COUNT)."""
    conn = get_connection()
    if conn is None:
        raise Exception("Connexion MySQL perdue ou indisponible.")
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        result = cursor.fetchone()
        return result[0] if result else None
    except mysql.connector.Error as err:
        raise Exception(f"Erreur SQL : {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def get_all_vehicules():
    return execute_query("SELECT immatriculation, marque, modele, typeVehicule, statut, capacite FROM VEHICULE")

def get_all_chauffeurs():
    return execute_query("SELECT id_chauffeur, nom, prenom, telephone, statut FROM CHAUFFEUR")

def get_trajets(limit: int = 50, offset: int = 0):
    query = """
    SELECT 
        T.id_trajet, T.immatriculation, 
        CONCAT(C.prenom, ' ', C.nom) as chauffeur,
        L.nom_ligne as ligne,
        AD.nom_arret as depart,
        AA.nom_arret as arrivee,
        T.date_heure_depart, T.date_heure_arrivee, T.statut
    FROM TRAJET T
    LEFT JOIN CHAUFFEUR C ON T.id_chauffeur = C.id_chauffeur
    LEFT JOIN LIGNE L ON T.id_ligne = L.id_ligne
    LEFT JOIN ARRET AD ON T.id_arret_depart = AD.id_arret
    LEFT JOIN ARRET AA ON T.id_arret_arrivee = AA.id_arret
    ORDER BY T.date_heure_depart DESC
    LIMIT %s OFFSET %s
    """
    return execute_query(query, (limit, offset))

def get_all_incidents():
    query = """
    SELECT 
        I.id_incident, I.type_incident, I.description, I.gravite, I.date_incident,
        I.immatriculation, CONCAT(C.prenom, ' ', C.nom) as chauffeur
    FROM INCIDENT I
    LEFT JOIN CHAUFFEUR C ON I.id_chauffeur = C.id_chauffeur
    ORDER BY I.date_incident DESC
    """
    return execute_query(query)

def get_kpi():
    # Statistiques basiques requises
    trajets_semaine = execute_scalar("SELECT COUNT(*) FROM TRAJET WHERE YEARWEEK(date_heure_depart, 1) = YEARWEEK(CURDATE(), 1)") or 0
    trajets_en_cours = execute_scalar("SELECT COUNT(*) FROM TRAJET WHERE statut = 'En cours'") or 0
    vehicules_maintenance = execute_scalar("SELECT COUNT(*) FROM VEHICULE WHERE statut = 'En maintenance'") or 0
    incidents_mois = execute_scalar("SELECT COUNT(*) FROM INCIDENT WHERE MONTH(date_incident) = MONTH(CURDATE()) AND YEAR(date_incident) = YEAR(CURDATE())") or 0
    
    # Chauffeur avec le plus d'incidents
    query_pire_chauffeur = """
        SELECT CONCAT(C.prenom, ' ', C.nom) 
        FROM INCIDENT I
        JOIN CHAUFFEUR C ON I.id_chauffeur = C.id_chauffeur
        GROUP BY I.id_chauffeur, C.prenom, C.nom
        ORDER BY COUNT(*) DESC LIMIT 1
    """
    pire_chauffeur = execute_scalar(query_pire_chauffeur)
    
    # Taux de complétion
    total_trajets = execute_scalar("SELECT COUNT(*) FROM TRAJET WHERE statut IN ('Terminé', 'Annulé')") or 0
    trajets_termines = execute_scalar("SELECT COUNT(*) FROM TRAJET WHERE statut = 'Terminé'") or 0
    taux = (trajets_termines / total_trajets * 100) if total_trajets > 0 else 0
    
    return {
        "trajets_semaine": trajets_semaine,
        "trajets_en_cours": trajets_en_cours,
        "vehicules_maintenance": vehicules_maintenance,
        "incidents_mois": incidents_mois,
        "chauffeur_plus_incidents": pire_chauffeur,
        "taux_completion": round(taux, 2)
    }
