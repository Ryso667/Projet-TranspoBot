-- =============================================================
-- BASE DE DONNÉES
-- =============================================================
CREATE DATABASE IF NOT EXISTS transport_db;
USE transport_db;

-- =============================================================
-- 1. TABLE CHAUFFEUR
-- =============================================================
CREATE TABLE CHAUFFEUR (
    id_chauffeur INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    telephone VARCHAR(20),
    email VARCHAR(100),
    numero_permis VARCHAR(50),
    statut VARCHAR(50)
) ENGINE=InnoDB;

-- =============================================================
-- 2. TABLE VEHICULE
-- =============================================================
CREATE TABLE VEHICULE (
    immatriculation VARCHAR(20) PRIMARY KEY,
    id_type INT,
    modele VARCHAR(50),
    marque VARCHAR(50),
    typeVehicule VARCHAR(50),
    kilometrage INT,
    statut VARCHAR(50),
    capacite INT
) ENGINE=InnoDB;

-- =============================================================
-- 3. TABLE LIGNE
-- =============================================================
CREATE TABLE LIGNE (
    id_ligne INT AUTO_INCREMENT PRIMARY KEY,
    nom_ligne VARCHAR(100),
    distance_totale_km FLOAT
) ENGINE=InnoDB;

-- =============================================================
-- 4. TABLE ARRET
-- =============================================================
CREATE TABLE ARRET (
    id_arret INT AUTO_INCREMENT PRIMARY KEY,
    nom_arret VARCHAR(100),
    localisation VARCHAR(255)
) ENGINE=InnoDB;

-- =============================================================
-- 5. TABLE LIGNE_ARRET
-- =============================================================
CREATE TABLE LIGNE_ARRET (
    id_ligne INT,
    id_arret INT,
    ordre INT,

    PRIMARY KEY (id_ligne, id_arret),

    FOREIGN KEY (id_ligne) REFERENCES LIGNE(id_ligne)
        ON DELETE CASCADE ON UPDATE CASCADE,

    FOREIGN KEY (id_arret) REFERENCES ARRET(id_arret)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =============================================================
-- 6. TABLE TRAJET
-- =============================================================
CREATE TABLE TRAJET (
    id_trajet INT AUTO_INCREMENT PRIMARY KEY,
    id_ligne INT,
    immatriculation VARCHAR(20),
    id_chauffeur INT,
    id_arret_depart INT,
    id_arret_arrivee INT,
    date_heure_depart DATETIME,
    date_heure_arrivee DATETIME,
    statut VARCHAR(50),
    nombrePlaces INT,

    FOREIGN KEY (id_ligne) REFERENCES LIGNE(id_ligne)
        ON DELETE SET NULL ON UPDATE CASCADE,

    FOREIGN KEY (immatriculation) REFERENCES VEHICULE(immatriculation)
        ON DELETE SET NULL ON UPDATE CASCADE,

    FOREIGN KEY (id_chauffeur) REFERENCES CHAUFFEUR(id_chauffeur)
        ON DELETE SET NULL ON UPDATE CASCADE,

    FOREIGN KEY (id_arret_depart) REFERENCES ARRET(id_arret)
        ON DELETE SET NULL ON UPDATE CASCADE,

    FOREIGN KEY (id_arret_arrivee) REFERENCES ARRET(id_arret)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =============================================================
-- 7. TABLE TRAJET_ARRET
-- =============================================================
CREATE TABLE TRAJET_ARRET (
    id_trajet INT,
    id_arret INT,
    ordre INT,

    PRIMARY KEY (id_trajet, id_arret),

    FOREIGN KEY (id_trajet) REFERENCES TRAJET(id_trajet)
        ON DELETE CASCADE ON UPDATE CASCADE,

    FOREIGN KEY (id_arret) REFERENCES ARRET(id_arret)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =============================================================
-- 8. TABLE TARIFICATION
-- =============================================================
CREATE TABLE TARIFICATION (
    id_arret_depart INT,
    id_arret_arrivee INT,
    prix FLOAT,

    PRIMARY KEY (id_arret_depart, id_arret_arrivee),

    FOREIGN KEY (id_arret_depart) REFERENCES ARRET(id_arret)
        ON DELETE CASCADE ON UPDATE CASCADE,

    FOREIGN KEY (id_arret_arrivee) REFERENCES ARRET(id_arret)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =============================================================
-- 9. TABLE INCIDENT (🔥 AVEC CHAUFFEUR)
-- =============================================================
CREATE TABLE INCIDENT (
    id_incident INT AUTO_INCREMENT PRIMARY KEY,
    id_trajet INT,
    immatriculation VARCHAR(20),
    id_chauffeur INT, -- 🔥 IMPORTANT
    type_incident VARCHAR(100),
    description TEXT,
    date_incident DATETIME DEFAULT CURRENT_TIMESTAMP,
    gravite VARCHAR(20),

    FOREIGN KEY (id_trajet) REFERENCES TRAJET(id_trajet)
        ON DELETE SET NULL ON UPDATE CASCADE,

    FOREIGN KEY (immatriculation) REFERENCES VEHICULE(immatriculation)
        ON DELETE SET NULL ON UPDATE CASCADE,

    FOREIGN KEY (id_chauffeur) REFERENCES CHAUFFEUR(id_chauffeur)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;