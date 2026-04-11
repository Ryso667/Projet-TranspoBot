from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importation des routeurs
from routes import kpi, vehicules, chauffeurs, trajets, incidents

app = FastAPI(
    title="TranspoBot API",
    description="API REST Backend pour le projet TranspoBot",
    version="1.0.0"
)

# Configuration de CORS pour permettre les requêtes du frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En production, préciser l'URL du frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrement des routes
app.include_router(kpi.router)
app.include_router(vehicules.router)
app.include_router(chauffeurs.router)
app.include_router(trajets.router)
app.include_router(incidents.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API TranspoBot. Rejoignez /docs pour la documentation."}
