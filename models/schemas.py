from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ErrorMessage(BaseModel):
    detail: str

class VehiculeSchema(BaseModel):
    immatriculation: str
    marque: str
    modele: str
    typeVehicule: str
    statut: str
    capacite: int

class ChauffeurSchema(BaseModel):
    id_chauffeur: int
    nom: str
    prenom: str
    telephone: Optional[str]
    statut: str

class TrajetSchema(BaseModel):
    id_trajet: int
    immatriculation: Optional[str]
    chauffeur: Optional[str]
    ligne: Optional[str]
    depart: Optional[str]
    arrivee: Optional[str]
    date_heure_depart: Optional[datetime]
    date_heure_arrivee: Optional[datetime]
    statut: str

class IncidentSchema(BaseModel):
    id_incident: int
    type_incident: str
    description: str
    gravite: str
    date_incident: datetime
    immatriculation: Optional[str]
    chauffeur: Optional[str]

class KPISchema(BaseModel):
    trajets_semaine: int
    trajets_en_cours: int
    vehicules_maintenance: int
    incidents_mois: int
    chauffeur_plus_incidents: Optional[str]
    taux_completion: float
