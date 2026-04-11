-- =============================================================
-- SCRIPT D'INSERTION DE DONNEES (data.sql)
-- =============================================================
USE transport_db;

-- 1. CHAUFFEURS (8 chauffeurs)
INSERT INTO CHAUFFEUR (nom, prenom, telephone, email, numero_permis, statut) VALUES
('Diallo', 'Mamadou', '0102030405', 'mamadou.d@mail.com', 'PERMIS-1001', 'Actif'),
('Ndiaye', 'Fatou', '0102030406', 'fatou.n@mail.com', 'PERMIS-1002', 'Actif'),
('Sow', 'Oumar', '0102030407', 'oumar.s@mail.com', 'PERMIS-1003', 'En congé'),
('Keita', 'Salif', '0102030408', 'salif.k@mail.com', 'PERMIS-1004', 'Actif'),
('Traore', 'Aminata', '0102030409', 'aminata.t@mail.com', 'PERMIS-1005', 'Actif'),
('Fall', 'Alioune', '0102030410', 'alioune.f@mail.com', 'PERMIS-1006', 'Inactif'),
('Gueye', 'Cheikh', '0102030411', 'cheikh.g@mail.com', 'PERMIS-1007', 'Actif'),
('Diop', 'Aïssatou', '0102030412', 'aissatou.d@mail.com', 'PERMIS-1008', 'Actif');

-- 2. VEHICULES (10 véhicules : 3 types -> Bus (1), Taxi (2), Yango (3))
INSERT INTO VEHICULE (immatriculation, id_type, modele, marque, typeVehicule, kilometrage, statut, capacite) VALUES
('BUS-001', 1, 'Citaro', 'Mercedes', 'Bus', 120000, 'Actif', 50),
('BUS-002', 1, 'Lion City', 'MAN', 'Bus', 85000, 'Actif', 55),
('BUS-003', 1, 'Urbino', 'Solaris', 'Bus', 210000, 'En maintenance', 45),
('TAX-001', 2, 'Corolla', 'Toyota', 'Taxi', 150000, 'Actif', 4),
('TAX-002', 2, 'Elantra', 'Hyundai', 'Taxi', 95000, 'Actif', 4),
('TAX-003', 2, 'C-Elysee', 'Citroen', 'Taxi', 110000, 'Inactif', 4),
('YGO-001', 3, 'Prius', 'Toyota', 'Yango', 60000, 'Actif', 4),
('YGO-002', 3, 'Civic', 'Honda', 'Yango', 45000, 'Actif', 4),
('YGO-003', 3, 'Yaris', 'Toyota', 'Yango', 30000, 'En maintenance', 4),
('YGO-004', 3, 'Logan', 'Dacia', 'Yango', 12000, 'Actif', 4);

-- 3. LIGNES (5 lignes)
INSERT INTO LIGNE (nom_ligne, distance_totale_km) VALUES
('Ligne A - Centre Ville / Aéroport', 15.5),
('Ligne B - Nord / Sud', 22.0),
('Ligne C - Université / Gare', 8.3),
('Ligne D - Banlieue Est / Marché', 18.7),
('Ligne E - Circulaire', 30.0);

-- 4. ARRETS (15 arrêts)
INSERT INTO ARRET (nom_arret, localisation) VALUES
('Aéroport', 'Terminus Nord'), ('Gare Centrale', 'Centre Ville'),
('Université', 'Campus Est'), ('Marché Central', 'Quartier Commerçant'),
('Hôpital Principal', 'Route Sud'), ('Mairie', 'Place de la République'),
('Stade', 'Quartier Ouest'), ('Centre Commercial', 'Rocade Nord'),
('Lycée Technique', 'Boulevard de la Jeunesse'), ('Place des Indépendances', 'Quartier Historique'),
('Zone Industrielle', 'Périphérique Sud'), ('Parc Botanique', 'Quartier Résidentiel'),
('Gare Routière', 'Sortie Ouest'), ('Port', 'Quartier Maritime'),
('Cité Universitaire', 'Campus Sud');

-- 5. LIGNE_ARRET (Associations)
INSERT INTO LIGNE_ARRET (id_ligne, id_arret, ordre) VALUES
(1, 2, 1), (1, 6, 2), (1, 1, 3),
(2, 7, 1), (2, 2, 2), (2, 5, 3), (2, 11, 4),
(3, 3, 1), (3, 15, 2), (3, 2, 3),
(4, 13, 1), (4, 4, 2), (4, 10, 3), (4, 8, 4),
(5, 2, 1), (5, 6, 2), (5, 4, 3), (5, 5, 4), (5, 12, 5);

-- 6. TARIFICATION
INSERT INTO TARIFICATION (id_arret_depart, id_arret_arrivee, prix) VALUES
(2, 1, 5000), (1, 2, 5000),
(3, 2, 250), (2, 3, 250),
(13, 4, 500), (4, 13, 500);

-- 7. TRAJETS (20 trajets)
INSERT INTO TRAJET (id_ligne, immatriculation, id_chauffeur, id_arret_depart, id_arret_arrivee, date_heure_depart, date_heure_arrivee, statut, nombrePlaces) VALUES
(1, 'BUS-001', 1, 2, 1, '2024-03-01 08:00:00', '2024-03-01 09:00:00', 'Terminé', 45),
(1, 'BUS-001', 1, 1, 2, '2024-03-01 10:00:00', '2024-03-01 11:15:00', 'Terminé', 38),
(2, 'BUS-002', 2, 7, 11, '2024-03-02 07:30:00', '2024-03-02 08:45:00', 'Terminé', 50),
(2, 'BUS-002', 2, 11, 7, '2024-03-02 17:00:00', '2024-03-02 18:30:00', 'Terminé', 55),
(3, 'TAX-001', 4, 3, 2, '2024-03-02 09:15:00', '2024-03-02 09:40:00', 'Terminé', 2),
(3, 'TAX-002', 5, 15, 2, '2024-03-03 14:00:00', NULL, 'Annulé', 0),
(4, 'TAX-003', NULL, 13, 4, '2024-03-03 16:30:00', '2024-03-03 17:15:00', 'Terminé', 3),
(5, 'BUS-001', 1, 2, 2, '2024-03-04 10:00:00', '2024-03-04 12:00:00', 'Terminé', 20),
(NULL, 'YGO-001', 7, 8, 14, '2024-03-04 11:00:00', '2024-03-04 11:45:00', 'Terminé', 1),
(NULL, 'YGO-002', 8, 4, 1, '2024-03-05 06:00:00', '2024-03-05 06:50:00', 'Terminé', 3),
(1, 'BUS-002', 2, 2, 1, NOW() - INTERVAL 1 HOUR, NULL, 'En cours', 40),
(2, 'BUS-001', 1, 7, 11, NOW() - INTERVAL 30 MINUTE, NULL, 'En cours', 35),
(4, 'TAX-001', 4, 13, 8, NOW() - INTERVAL 15 MINUTE, NULL, 'En cours', 4),
(NULL, 'YGO-004', 8, 10, 6, NOW() - INTERVAL 5 MINUTE, NULL, 'En cours', 2),
(3, 'TAX-002', 5, 3, 15, '2024-03-06 08:00:00', '2024-03-06 08:30:00', 'Terminé', 1),
(5, 'BUS-003', 2, 4, 5, '2024-03-06 09:00:00', NULL, 'Annulé', 0),
(2, 'BUS-001', 1, 11, 7, '2024-03-07 18:00:00', '2024-03-07 19:20:00', 'Terminé', 48),
(4, 'TAX-001', 4, 8, 13, '2024-03-07 12:00:00', '2024-03-07 12:30:00', 'Terminé', 3),
(1, 'BUS-002', 2, 1, 2, NOW() - INTERVAL 2 HOUR, NOW() - INTERVAL 1 HOUR, 'Terminé', 25),
(NULL, 'YGO-001', 7, 14, 8, NOW() + INTERVAL 1 HOUR, NULL, 'Annulé', 0);

-- 8. INCIDENTS (10 incidents)
INSERT INTO INCIDENT (id_trajet, immatriculation, id_chauffeur, type_incident, description, date_incident, gravite) VALUES
(1, 'BUS-001', 1, 'Panne mineure', 'Problème de climatisation', '2024-03-01 08:30:00', 'Faible'),
(3, 'BUS-002', 2, 'Accident', 'Accrochage léger avec une voiture', '2024-03-02 08:15:00', 'Moyenne'),
(6, 'TAX-002', 5, 'Panne majeure', 'Panne moteur, trajet annulé', '2024-03-03 14:10:00', 'Haute'),
(16, 'BUS-003', 2, 'Panne mécanique', 'Fuite d\'huile constatée avant le départ', '2024-03-06 08:50:00', 'Haute'),
(NULL, 'YGO-003', NULL, 'Maintenance', 'Véhicule en révision périodique, hors trajet', '2024-03-06 10:00:00', 'Faible'),
(NULL, 'TAX-003', 5, 'Nettoyage', 'Nettoyage complet suite à vandalisme', '2024-03-08 09:00:00', 'Moyenne'),
(11, 'BUS-002', 2, 'Retard', 'Trafic intense, 30 min de retard', NOW() - INTERVAL 45 MINUTE, 'Faible'),
(12, 'BUS-001', 1, 'Client perturbateur', 'Intervention requise dans le bus', NOW() - INTERVAL 10 MINUTE, 'Moyenne'),
(9, 'YGO-001', 7, 'Crevaison', 'Roue arrière crevée', '2024-03-04 11:20:00', 'Moyenne'),
(NULL, 'BUS-003', NULL, 'Panne électronique', 'Portes qui ne s\'ouvrent plus', '2024-03-09 07:00:00', 'Haute');
