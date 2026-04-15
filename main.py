from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routes import vehicules, chauffeurs, trajets, incidents, kpi, chat, map

app = FastAPI(title="TranspoBot API", version="1.0", description="Plateforme de gestion de transport urbain avec IA")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(vehicules.router)
app.include_router(chauffeurs.router)
app.include_router(trajets.router)
app.include_router(incidents.router)
app.include_router(kpi.router)
app.include_router(chat.router)
app.include_router(map.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.get("/vehicules-page")
def vehicules_page():
    return FileResponse("static/vehicules.html")


@app.get("/trajets-page")
def trajets_page():
    return FileResponse("static/trajets.html")


@app.get("/chat-page")
def chat_page():
    return FileResponse("static/chat.html")


@app.get("/map-page")
def map_page():
    return FileResponse("static/map.html")
