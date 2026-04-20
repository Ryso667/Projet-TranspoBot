import json
import os
import re
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI
from database import get_connection, get_cursor


router = APIRouter()

# Étape 1 : uniquement du SQL (le texte naturel viendra après exécution en base)
SQL_SYSTEM_PROMPT = """Tu génères une seule requête SQL MySQL (SELECT uniquement) pour répondre à la question.

Base « railway », tables :
- CHAUFFEUR(id_chauffeur, nom, prenom, telephone, email, numero_permis, statut)
- VEHICULE(immatriculation, modele, marque, typeVehicule, kilometrage, statut, capacite)
- LIGNE(id_ligne, nom_ligne, distance_totale_km)
- ARRET(id_arret, nom_arret, localisation)
- LIGNE_ARRET(id_ligne, id_arret, ordre)
- TRAJET(id_trajet, id_ligne, immatriculation, id_chauffeur, id_arret_depart, id_arret_arrivee, date_heure_depart, date_heure_arrivee, statut, nombrePlaces)
- TRAJET_ARRET(id_trajet, id_arret, ordre)
- TARIFICATION(id_arret_depart, id_arret_arrivee, prix)
- INCIDENT(id_incident, id_trajet, immatriculation, id_chauffeur, type_incident, description, date_incident, gravite)

Statuts : VEHICULE 'en service'|'maintenance'|'hors service' ; CHAUFFEUR 'actif'|'inactif' ; TRAJET 'terminé'|'en cours'|'annulé' ; gravite 'faible'|'moyen'|'grave'.

Règles : SELECT uniquement ; JOIN si utile ; requête correcte pour MySQL.

Réponds UNIQUEMENT avec ce bloc (pas de texte avant ni après) :
```sql
... ta requête ...
```
"""

ANSWER_FROM_DATA_PROMPT = """Tu es TranspoBot, assistant pour la gestion de transport urbain au Sénégal.

On te donne la question posée par l'utilisateur et les lignes renvoyées par MySQL (données réelles, déjà exécutées).

Rédige une réponse en français clair, 2 à 6 phrases courtes, ton professionnel et direct.
- Base-toi UNIQUEMENT sur les données fournies ; n'invente aucun chiffre ni nom.
- Si le tableau de données est vide : explique qu'aucun enregistrement ne correspond (sans parler de SQL).
- Parle de chauffeurs, trajets, véhicules, lignes, incidents, etc. Évite le jargon technique (noms de colonnes bruts) sauf si indispensable.
- Ne cite pas de requête SQL, ni « SELECT », ni noms de tables en majuscules.
- Ne numérote pas les phrases type « 1) » ; écris un texte fluide."""


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
    lines = text.split("\n")
    for line in lines:
        if line.strip() and not line.startswith("SQL:") and not line.startswith("```"):
            return line.strip()
    return text.strip()


def summarize_results_fallback(results: list) -> str:
    if not results:
        return "Aucun enregistrement ne correspond à votre question dans la base de données."
    if len(results) == 1 and len(results[0]) == 1:
        col, val = next(iter(results[0].items()))
        return f"D’après la base : {val} ({col})."
    if len(results) == 1:
        parts = [f"{k} : {v}" for k, v in results[0].items()]
        return "Voici l’enregistrement trouvé : " + " · ".join(parts) + "."
    if len(results) <= 5:
        lines = []
        for i, row in enumerate(results, 1):
            bits = ", ".join(f"{k}={v}" for k, v in row.items())
            lines.append(f"{i}) {bits}")
        return f"{len(results)} résultat(s) :\n" + "\n".join(lines)
    return (
        f"La base renvoie {len(results)} ligne(s). "
        "Ouvrez « Détails » ci-dessous pour consulter un extrait tabulaire."
    )


def build_results_json_for_llm(results: list, max_rows: int = 30) -> str:
    slice_ = results[:max_rows]
    s = json.dumps(slice_, ensure_ascii=False, default=str)
    if len(results) > max_rows:
        s += f"\n\n(Indication : {len(results)} lignes au total ; seules les {max_rows} premières sont incluses.)"
    if len(s) > 12000:
        s = s[:12000] + "\n… (données tronquées)"
    return s


def natural_language_answer(client: OpenAI, question: str, results: list) -> str:
    data_block = build_results_json_for_llm(results)
    user_msg = f"Question de l’utilisateur :\n{question}\n\nDonnées renvoyées par la base (JSON) :\n{data_block}"
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": ANSWER_FROM_DATA_PROMPT},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.25,
            max_tokens=600,
        )
        text = (response.choices[0].message.content or "").strip()
        return text if text else summarize_results_fallback(results)
    except Exception:
        return summarize_results_fallback(results)


def make_openai_client() -> Optional[OpenAI]:
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        return None
    return OpenAI(api_key=key, base_url="https://api.groq.com/openai/v1")


@router.post("/chat")
def chat(request: ChatRequest):
    question = request.question.strip()

    if not question:
        return {"answer": "Veuillez poser une question.", "sql": None, "results": []}

    if len(question) > 500:
        return {"answer": "Question trop longue. Veuillez limiter à 500 caractères.", "sql": None, "results": []}

    client = make_openai_client()
    if not client:
        return {
            "answer": "Clé API Groq non configurée. Ajoutez GROQ_API_KEY dans le fichier .env.",
            "sql": None,
            "results": [],
        }

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SQL_SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ],
            temperature=0.1,
            max_tokens=800,
        )
        ai_text = response.choices[0].message.content or ""
    except Exception as e:
        return {"answer": f"Erreur lors de l’appel à l’IA : {str(e)}", "sql": None, "results": []}

    sql_query = extract_sql(ai_text)
    fallback_text = extract_answer(ai_text) or ai_text.strip()

    if not sql_query:
        return {"answer": fallback_text or "Je n’ai pas pu déduire de requête pour cette question.", "sql": None, "results": []}

    if not sql_query.strip().upper().startswith("SELECT"):
        return {
            "answer": "Pour des raisons de sécurité, seules les requêtes SELECT sont autorisées.",
            "sql": sql_query,
            "results": None,
        }

    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        for row in results:
            for key, val in row.items():
                if hasattr(val, "isoformat"):
                    row[key] = val.isoformat()

        final_answer = natural_language_answer(client, question, results)
        return {"answer": final_answer, "sql": sql_query, "results": results}
    except Exception as e:
        return {
            "answer": f"La requête SQL a échoué : {str(e)}",
            "sql": sql_query,
            "results": None,
        }
    finally:
        cursor.close()
        conn.close()
