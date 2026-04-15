CREATE DATABASE IF NOT EXISTS transport_db;
USE transport_db;

CREATE TABLE IF NOT EXISTS CHAUFFEUR (
    id_chauffeur INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    telephone VARCHAR(20),
    email VARCHAR(100),
    numero_permis VARCHAR(50) UNIQUE,
    statut ENUM('actif', 'inactif') DEFAULT 'actif'
);

CREATE TABLE IF NOT EXISTS VEHICULE (
    immatriculation VARCHAR(20) PRIMARY KEY,
    modele VARCHAR(100),
    marque VARCHAR(100),
    typeVehicule VARCHAR(50),
    kilometrage INT DEFAULT 0,
    statut ENUM('en service', 'maintenance', 'hors service') DEFAULT 'en service',
    capacite INT DEFAULT 50
);

CREATE TABLE IF NOT EXISTS LIGNE (
    id_ligne INT AUTO_INCREMENT PRIMARY KEY,
    nom_ligne VARCHAR(150) NOT NULL,
    distance_totale_km DECIMAL(8,2)
);

CREATE TABLE IF NOT EXISTS ARRET (
    id_arret INT AUTO_INCREMENT PRIMARY KEY,
    nom_arret VARCHAR(150) NOT NULL,
    localisation VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS LIGNE_ARRET (
    id_ligne INT,
    id_arret INT,
    ordre INT,
    PRIMARY KEY (id_ligne, id_arret),
    FOREIGN KEY (id_ligne) REFERENCES LIGNE(id_ligne),
    FOREIGN KEY (id_arret) REFERENCES ARRET(id_arret)
);

CREATE TABLE IF NOT EXISTS TRAJET (
    id_trajet INT AUTO_INCREMENT PRIMARY KEY,
    id_ligne INT,
    immatriculation VARCHAR(20),
    id_chauffeur INT,
    id_arret_depart INT,
    id_arret_arrivee INT,
    date_heure_depart DATETIME,
    date_heure_arrivee DATETIME,
    statut ENUM('terminé', 'en cours', 'annulé') DEFAULT 'en cours',
    nombrePlaces INT DEFAULT 0,
    FOREIGN KEY (id_ligne) REFERENCES LIGNE(id_ligne),
    FOREIGN KEY (immatriculation) REFERENCES VEHICULE(immatriculation),
    FOREIGN KEY (id_chauffeur) REFERENCES CHAUFFEUR(id_chauffeur),
    FOREIGN KEY (id_arret_depart) REFERENCES ARRET(id_arret),
    FOREIGN KEY (id_arret_arrivee) REFERENCES ARRET(id_arret)
);

CREATE TABLE IF NOT EXISTS TRAJET_ARRET (
    id_trajet INT,
    id_arret INT,
    ordre INT,
    PRIMARY KEY (id_trajet, id_arret),
    FOREIGN KEY (id_trajet) REFERENCES TRAJET(id_trajet),
    FOREIGN KEY (id_arret) REFERENCES ARRET(id_arret)
);

CREATE TABLE IF NOT EXISTS TARIFICATION (
    id_arret_depart INT,
    id_arret_arrivee INT,
    prix DECIMAL(10,2),
    PRIMARY KEY (id_arret_depart, id_arret_arrivee),
    FOREIGN KEY (id_arret_depart) REFERENCES ARRET(id_arret),
    FOREIGN KEY (id_arret_arrivee) REFERENCES ARRET(id_arret)
);

CREATE TABLE IF NOT EXISTS INCIDENT (
    id_incident INT AUTO_INCREMENT PRIMARY KEY,
    id_trajet INT NULL,
    immatriculation VARCHAR(20),
    id_chauffeur INT NULL,
    type_incident VARCHAR(100),
    description TEXT,
    date_incident DATETIME,
    gravite ENUM('faible', 'moyen', 'grave') DEFAULT 'faible',
    FOREIGN KEY (id_trajet) REFERENCES TRAJET(id_trajet),
    FOREIGN KEY (immatriculation) REFERENCES VEHICULE(immatriculation),
    FOREIGN KEY (id_chauffeur) REFERENCES CHAUFFEUR(id_chauffeur)
);
