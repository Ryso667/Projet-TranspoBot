USE railway;

INSERT INTO CHAUFFEUR (nom, prenom, telephone, email, numero_permis, statut) VALUES
('Diallo', 'Mamadou', '+221 77 123 4567', 'mamadou.diallo@transpo.sn', 'SN-2018-001', 'actif'),
('Ndiaye', 'Ibrahima', '+221 76 234 5678', 'ibrahima.ndiaye@transpo.sn', 'SN-2019-002', 'actif'),
('Fall', 'Ousmane', '+221 78 345 6789', 'ousmane.fall@transpo.sn', 'SN-2017-003', 'actif'),
('Sow', 'Abdoulaye', '+221 77 456 7890', 'abdoulaye.sow@transpo.sn', 'SN-2020-004', 'actif'),
('Mbaye', 'Cheikh', '+221 76 567 8901', 'cheikh.mbaye@transpo.sn', 'SN-2016-005', 'actif'),
('Sarr', 'Moussa', '+221 78 678 9012', 'moussa.sarr@transpo.sn', 'SN-2021-006', 'inactif'),
('Diouf', 'Lamine', '+221 77 789 0123', 'lamine.diouf@transpo.sn', 'SN-2015-007', 'actif'),
('Ba', 'Tidiane', '+221 76 890 1234', 'tidiane.ba@transpo.sn', 'SN-2022-008', 'inactif');

INSERT INTO VEHICULE (immatriculation, modele, marque, typeVehicule, kilometrage, statut, capacite) VALUES
('DK-1234-A', 'Urbanus 300', 'Mercedes', 'Bus', 125000, 'en service', 80),
('DK-5678-B', 'Citaro G', 'Mercedes', 'Bus', 98000, 'en service', 100),
('DK-9012-C', 'Lion City', 'MAN', 'Bus', 210000, 'maintenance', 75),
('DK-3456-D', 'Crossway', 'Irisbus', 'Bus', 155000, 'en service', 60),
('DK-7890-E', 'Corolla', 'Toyota', 'Taxi', 78000, 'en service', 4),
('DK-2345-F', 'Yaris', 'Toyota', 'Yango', 45000, 'en service', 4),
('DK-6789-G', 'Sandero', 'Dacia', 'Taxi', 132000, 'hors service', 4),
('DK-0123-H', 'Duster', 'Dacia', 'Yango', 56000, 'en service', 4),
('DK-4567-I', 'Sprinter', 'Mercedes', 'Bus', 88000, 'en service', 30),
('DK-8901-J', 'Crafter', 'Volkswagen', 'Bus', 172000, 'maintenance', 25);

INSERT INTO LIGNE (nom_ligne, distance_totale_km) VALUES
('Ligne 1 Dakar-Plateau', 12.5),
('Ligne 2 Dakar-Rufisque', 28.0),
('Ligne 3 Dakar-Pikine', 18.3),
('Ligne 4 Dakar-Guédiawaye', 22.7),
('Ligne 5 Dakar-Thiaroye', 15.8);

INSERT INTO ARRET (nom_arret, localisation) VALUES
('Gare Routière Dakar', 'Dakar Centre, Lat: 14.6937, Long: -17.4441'),
('Place de lIndépendance', 'Plateau, Dakar'),
('Marché Sandaga', 'Médina, Dakar'),
('Université Cheikh Anta Diop', 'Fann, Dakar'),
('Pikine Gare', 'Pikine, Dakar'),
('Thiaroye', 'Thiaroye, Dakar'),
('Guédiawaye Centre', 'Guédiawaye, Dakar'),
('Rufisque Centre', 'Rufisque, Dakar'),
('Hôpital Principal', 'Plateau, Dakar'),
('Almadies', 'Ngor, Dakar');

INSERT INTO LIGNE_ARRET (id_ligne, id_arret, ordre) VALUES
(1, 1, 1), (1, 3, 2), (1, 2, 3), (1, 9, 4),
(2, 1, 1), (2, 5, 2), (2, 6, 3), (2, 8, 4),
(3, 1, 1), (3, 3, 2), (3, 5, 3),
(4, 1, 1), (4, 3, 2), (4, 7, 3),
(5, 1, 1), (5, 5, 2), (5, 6, 3);

INSERT INTO TARIFICATION (id_arret_depart, id_arret_arrivee, prix) VALUES
(1, 2, 200), (1, 3, 150), (1, 4, 300), (1, 5, 500),
(1, 6, 600), (1, 7, 550), (1, 8, 800), (1, 9, 250),
(2, 8, 700), (3, 5, 400), (3, 8, 700), (5, 8, 400);

INSERT INTO TRAJET (id_ligne, immatriculation, id_chauffeur, id_arret_depart, id_arret_arrivee, date_heure_depart, date_heure_arrivee, statut, nombrePlaces) VALUES
(1, 'DK-1234-A', 1, 1, 9, DATE_SUB(NOW(), INTERVAL 1 DAY), DATE_SUB(NOW(), INTERVAL 23 HOUR), 'terminé', 65),
(2, 'DK-5678-B', 2, 1, 8, DATE_SUB(NOW(), INTERVAL 2 DAY), DATE_SUB(NOW(), INTERVAL 45 HOUR), 'terminé', 90),
(3, 'DK-4567-I', 3, 1, 5, DATE_SUB(NOW(), INTERVAL 3 DAY), DATE_SUB(NOW(), INTERVAL 68 HOUR), 'terminé', 25),
(4, 'DK-3456-D', 4, 1, 7, DATE_SUB(NOW(), INTERVAL 4 DAY), DATE_SUB(NOW(), INTERVAL 91 HOUR), 'terminé', 55),
(5, 'DK-8901-J', 5, 1, 6, DATE_SUB(NOW(), INTERVAL 5 DAY), DATE_SUB(NOW(), INTERVAL 114 HOUR), 'terminé', 20),
(1, 'DK-1234-A', 1, 1, 9, DATE_SUB(NOW(), INTERVAL 6 DAY), DATE_SUB(NOW(), INTERVAL 138 HOUR), 'terminé', 70),
(2, 'DK-5678-B', 2, 1, 8, DATE_SUB(NOW(), INTERVAL 2 HOUR), NULL, 'en cours', 85),
(3, 'DK-4567-I', 3, 1, 5, DATE_SUB(NOW(), INTERVAL 1 HOUR), NULL, 'en cours', 28),
(4, 'DK-0123-H', 4, 1, 7, DATE_SUB(NOW(), INTERVAL 30 MINUTE), NULL, 'en cours', 3),
(1, 'DK-1234-A', 1, 1, 9, DATE_SUB(NOW(), INTERVAL 8 DAY), DATE_SUB(NOW(), INTERVAL 186 HOUR), 'terminé', 72),
(2, 'DK-3456-D', 7, 1, 8, DATE_SUB(NOW(), INTERVAL 9 DAY), DATE_SUB(NOW(), INTERVAL 209 HOUR), 'terminé', 58),
(5, 'DK-9012-C', 5, 1, 6, DATE_SUB(NOW(), INTERVAL 10 DAY), DATE_SUB(NOW(), INTERVAL 231 HOUR), 'annulé', 0),
(1, 'DK-5678-B', 2, 1, 9, DATE_SUB(NOW(), INTERVAL 11 DAY), DATE_SUB(NOW(), INTERVAL 255 HOUR), 'terminé', 88),
(3, 'DK-4567-I', 3, 1, 5, DATE_SUB(NOW(), INTERVAL 12 DAY), DATE_SUB(NOW(), INTERVAL 278 HOUR), 'terminé', 30),
(4, 'DK-3456-D', 4, 1, 7, DATE_SUB(NOW(), INTERVAL 13 DAY), DATE_SUB(NOW(), INTERVAL 302 HOUR), 'terminé', 50),
(2, 'DK-5678-B', 2, 1, 8, DATE_SUB(NOW(), INTERVAL 14 DAY), DATE_SUB(NOW(), INTERVAL 325 HOUR), 'terminé', 92),
(5, 'DK-8901-J', 5, 1, 6, DATE_SUB(NOW(), INTERVAL 15 DAY), DATE_SUB(NOW(), INTERVAL 349 HOUR), 'terminé', 22),
(1, 'DK-1234-A', 1, 1, 9, DATE_SUB(NOW(), INTERVAL 16 DAY), DATE_SUB(NOW(), INTERVAL 372 HOUR), 'terminé', 68),
(3, 'DK-0123-H', 4, 1, 5, DATE_SUB(NOW(), INTERVAL 17 DAY), DATE_SUB(NOW(), INTERVAL 395 HOUR), 'terminé', 4),
(4, 'DK-4567-I', 3, 1, 7, DATE_SUB(NOW(), INTERVAL 18 DAY), DATE_SUB(NOW(), INTERVAL 419 HOUR), 'terminé', 26),
(1, 'DK-3456-D', 7, 1, 9, DATE_SUB(NOW(), INTERVAL 19 DAY), DATE_SUB(NOW(), INTERVAL 442 HOUR), 'terminé', 55),
(2, 'DK-1234-A', 1, 1, 8, DATE_SUB(NOW(), INTERVAL 20 DAY), DATE_SUB(NOW(), INTERVAL 465 HOUR), 'terminé', 78),
(5, 'DK-5678-B', 2, 1, 6, DATE_SUB(NOW(), INTERVAL 21 DAY), DATE_SUB(NOW(), INTERVAL 488 HOUR), 'annulé', 0),
(3, 'DK-4567-I', 3, 1, 5, DATE_SUB(NOW(), INTERVAL 22 DAY), DATE_SUB(NOW(), INTERVAL 511 HOUR), 'terminé', 28),
(4, 'DK-8901-J', 5, 1, 7, DATE_SUB(NOW(), INTERVAL 23 DAY), DATE_SUB(NOW(), INTERVAL 534 HOUR), 'terminé', 20);

INSERT INTO INCIDENT (id_trajet, immatriculation, id_chauffeur, type_incident, description, date_incident, gravite) VALUES
(1, 'DK-1234-A', 1, 'Panne mécanique', 'Crevaison pneu avant droit en route', DATE_SUB(NOW(), INTERVAL 1 DAY), 'faible'),
(2, 'DK-5678-B', 2, 'Accident', 'Collision légère avec un véhicule particulier au niveau du marché', DATE_SUB(NOW(), INTERVAL 2 DAY), 'moyen'),
(NULL, 'DK-9012-C', 3, 'Panne mécanique', 'Moteur en surchauffe, mise en maintenance immédiate', DATE_SUB(NOW(), INTERVAL 3 DAY), 'grave'),
(5, 'DK-8901-J', 5, 'Incident voyageur', 'Malaise passager, arrêt d urgence effectué', DATE_SUB(NOW(), INTERVAL 5 DAY), 'moyen'),
(NULL, 'DK-6789-G', 6, 'Panne mécanique', 'Transmission défaillante, véhicule retiré du service', DATE_SUB(NOW(), INTERVAL 8 DAY), 'grave'),
(12, 'DK-9012-C', 5, 'Accident', 'Accrochage avec motocyclette, trajet annulé', DATE_SUB(NOW(), INTERVAL 10 DAY), 'grave'),
(NULL, 'DK-8901-J', 5, 'Vandalisme', 'Sièges vandalisés dans le bus durant la nuit', DATE_SUB(NOW(), INTERVAL 12 DAY), 'moyen'),
(14, 'DK-4567-I', 3, 'Retard', 'Embouteillage important sur la VDN, retard de 45 minutes', DATE_SUB(NOW(), INTERVAL 15 DAY), 'faible');
