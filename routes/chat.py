import os
import re
from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI
from database import get_connection, get_cursor

router = APIRouter()

SYSTEM_PROMPT = """Tu es TranspoBot, un assistant IA expert en gestion de transport urbain au Sénégal.
Tu as accès à une base de données MySQL appelée railway avec les tables suivantes :

- CHAUFFEUR(id_chauffeur, nom, prenom, telephone, email, numero_permis, statut)
- VEHICULE(immatriculation, modele, marque, typeVehicule, kilometrage, statut, capacite)
- LIGNE(id_ligne, nom_ligne, distance_totale_km)
- ARRET(id_arret, nom_arret, localisation)
- LIGNE_ARRET(id_ligne, id_arret, ordre)
- TRAJET(id_trajet, id_ligne, immatriculation, id_chauffeur, id_arret_depart, id_arret_arrivee, date_heure_depart, date_heure_arrivee, statut, nombrePlaces)
- TRAJET_ARRET(id_trajet, id_arret, ordre)
- TARIFICATION(id_arret_depart, id_arret_arrivee, prix)
- INCIDENT(id_incident, id_trajet, immatriculation, id_chauffeur, type_incident, description, date_incident, gravite)

Valeurs possibles pour statut VEHICULE : 'en service', 'maintenance', 'hors service'
Valeurs possibles pour statut CHAUFFEUR : 'actif', 'inactif'
Valeurs possibles pour statut TRAJET : 'terminé', 'en cours', 'annulé'
Valeurs possibles pour gravite INCIDENT : 'faible', 'moyen', 'grave'

Quand l'utilisateur pose une question, génère une requête SQL SELECT appropriée pour répondre.
Retourne TOUJOURS ta réponse dans ce format exact :

RÉPONSE: [Ta réponse en langage naturel en français ici]
SQL:
```sql
[La requête SQL ici]
```

Règles importantes :
- Génère UNIQUEMENT des requêtes SELECT (jamais INSERT, UPDATE, DELETE, DROP, etc.)
- Utilise des JOINs quand nécessaire pour enrichir les données
- Sois concis et précis dans tes réponses en français
- Si la question ne concerne pas les transports, réponds poliment que tu ne peux répondre qu'aux questions sur le système de transport
"""


class ChatRequest(BaseModel):
    question: str


def extract_sql(text: str):
    match = re.search(r"```sql\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    match = re.search(r"SQL:\s*(.+?)(?:\n\n|$)", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def extract_answer(text: str):
    match = re.search(r"RÉPONSE:\s*(.+?)(?:\nSQL:|```sql|$)", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    lines = text.split('\n')
    for line in lines:
        if line.strip() and not line.startswith('SQL:') and not line.startswith('```'):
            return line.strip()
    return text.strip()


@router.post("/chat")
def chat(request: ChatRequest):
    question = request.question.strip()

    if not question:
        return {"answer": "Veuillez poser une question.", "sql": None, "results": []}

    if len(question) > 500:
        return {"answer": "Question trop longue. Veuillez limiter à 500 caractères.", "sql": None, "results": []}

    api_key = os.environ.get("GROK_API_KEY")
    if not api_key:
        return {"answer": "Clé API Grok non configurée.", "sql": None, "results": []}

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1"
    )

    try:
        response = client.chat.completions.create(
            model="grok-3-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ],
            temperature=0.1
        )
        ai_text = response.choices[0].message.content
    except Exception as e:
        return {"answer": f"Erreur lors de l'appel à l'IA : {str(e)}", "sql": None, "results": []}

    sql_query = extract_sql(ai_text)
    answer = extract_answer(ai_text)

    if not sql_query:
        return {"answer": answer or ai_text, "sql": None, "results": []}

    if not sql_query.strip().upper().startswith("SELECT"):
        return {
            "answer": "Pour des raisons de sécurité, seules les requêtes SELECT sont autorisées.",
            "sql": sql_query,
            "results": []
        }

    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        for row in results:
            for key, val in row.items():
                if hasattr(val, 'isoformat'):
                    row[key] = val.isoformat()
        return {"answer": answer, "sql": sql_query, "results": results}
    except Exception as e:
        return {
            "answer": f"La requête SQL a échoué : {str(e)}",
            "sql": sql_query,
            "results": []
        }
    finally:
        cursor.close()
        conn.close()
