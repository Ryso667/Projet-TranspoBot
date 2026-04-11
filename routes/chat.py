from fastapi import APIRouter
from pydantic import BaseModel
from services.llm_service import generer_sql_et_reponse
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Modèle de la requête entrante
class QuestionRequest(BaseModel):
    question: str

def executer_sql(sql: str):
    """
    Exécute une requête SQL SELECT sur la base MySQL et retourne les résultats.
    """
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "transport_db")
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        resultats = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultats

    except mysql.connector.Error as e:
        raise Exception(f"Erreur MySQL : {str(e)}")

@router.post("/chat")
def chat(request: QuestionRequest):
    """
    Route POST /chat — reçoit une question, génère le SQL via OpenAI,
    l'exécute sur MySQL et retourne la réponse.
    """
    question = request.question.strip()

    # Vérifier que la question n'est pas vide
    if not question:
        return {
            "succes": False,
            "reponse": "Veuillez poser une question.",
            "sql": "",
            "donnees": []
        }

    # Étape 1 : Générer le SQL via OpenAI
    llm_result = generer_sql_et_reponse(question)

    # Si erreur LLM ou question hors sujet
    if llm_result["erreur"] or not llm_result["sql"]:
        return {
            "succes": False,
            "reponse": llm_result["reponse"],
            "sql": "",
            "donnees": []
        }

    sql = llm_result["sql"]
    reponse_naturelle = llm_result["reponse"]

    # Étape 2 : Exécuter le SQL sur MySQL
    try:
        donnees = executer_sql(sql)

        # Résultat vide
        if not donnees:
            return {
                "succes": True,
                "reponse": "Aucun résultat trouvé pour cette question.",
                "sql": sql,
                "donnees": []
            }

        return {
            "succes": True,
            "reponse": reponse_naturelle,
            "sql": sql,
            "donnees": donnees
        }

    except Exception as e:
        return {
            "succes": False,
            "reponse": f"La requête SQL générée contient une erreur : {str(e)}",
            "sql": sql,
            "donnees": []
        }