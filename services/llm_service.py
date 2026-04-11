import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Charger le system prompt depuis le fichier
def get_system_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), "../llm/system_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

# Initialiser le client OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generer_sql_et_reponse(question: str) -> dict:
    """
    Envoie la question à OpenAI et retourne le SQL généré + la réponse naturelle.
    """
    # Vérifier la longueur de la question
    if len(question) > 500:
        return {
            "sql": "",
            "reponse": "Votre question est trop longue. Veuillez la reformuler en moins de 500 caractères.",
            "erreur": True
        }

    try:
        system_prompt = get_system_prompt()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0,
            max_tokens=1000
        )

        contenu = response.choices[0].message.content.strip()

        # Parser le JSON retourné par le LLM
        try:
            resultat = json.loads(contenu)
        except json.JSONDecodeError:
            return {
                "sql": "",
                "reponse": "Le modèle IA n'a pas retourné une réponse valide. Veuillez reformuler votre question.",
                "erreur": True
            }

        sql = resultat.get("sql", "").strip()
        reponse = resultat.get("reponse", "")

        # Validation de sécurité : uniquement SELECT autorisé
        if sql and not sql.upper().startswith("SELECT"):
            return {
                "sql": "",
                "reponse": "Je ne suis pas autorisé à effectuer des modifications sur la base de données.",
                "erreur": True
            }

        return {
            "sql": sql,
            "reponse": reponse,
            "erreur": False
        }

    except Exception as e:
        erreur_str = str(e)

        # Quota OpenAI dépassé
        if "quota" in erreur_str.lower() or "insufficient_quota" in erreur_str.lower():
            return {
                "sql": "",
                "reponse": "Le quota de l'API OpenAI est dépassé. Veuillez contacter l'administrateur.",
                "erreur": True
            }

        # Clé API invalide
        if "api_key" in erreur_str.lower() or "authentication" in erreur_str.lower():
            return {
                "sql": "",
                "reponse": "Clé API OpenAI invalide. Veuillez vérifier la configuration.",
                "erreur": True
            }

        return {
            "sql": "",
            "reponse": f"Erreur lors de la communication avec l'IA : {erreur_str}",
            "erreur": True
        }