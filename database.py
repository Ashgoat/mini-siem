import sqlite3

# 1. Connexion à la base de données
connexion = sqlite3.connect("siem.db")

# 2. Création du curseur
curseur = connexion.cursor()


# 3. Création de la table evenements
curseur.execute("""
CREATE TABLE IF NOT EXISTS evenements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    machine TEXT,
    service TEXT,
    pid TEXT,
    message TEXT
)
""")

print("Table evenements créée avec succès !")


# 4. Création de la table alertes
curseur.execute("""
CREATE TABLE IF NOT EXISTS alertes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    type TEXT,
    ip TEXT,
    description TEXT
)
""")

print("Table alertes créée avec succès !")


# 5. Insertion d'un événement de test
curseur.execute("""
INSERT INTO evenements (date, machine, service, pid, message)
VALUES (?, ?, ?, ?, ?)
""", (
    "2026-11-11",
    "LAPTOP-JEOKA4OH",
    "sshd",
    "1001",
    "Failed password for admin from 192.168.1.10"
))

print("Événement ajouté avec succès !")


# 6. Insertion d'une alerte de test
curseur.execute("""
INSERT INTO alertes (date, type, ip, description)
VALUES (?, ?, ?, ?)
""", (
    "2026-11-11",
    "Brute Force",
    "192.168.1.10",
    "5 tentatives de connexion échouées détectées"
))

print("Alerte enregistrée avec succès !")


# 7. Validation des insertions
connexion.commit()


# 8. Lecture de tous les événements
curseur.execute("SELECT * FROM evenements")
resultats = curseur.fetchall()

print("\nTous les événements :")

for evenement in resultats:
    print(evenement)


# 9. Lecture des événements SSH
curseur.execute("""
SELECT * FROM evenements
WHERE service = 'sshd'
""")

resultats = curseur.fetchall()

print("\nÉvénements SSH :")

for evenement in resultats:
    print(evenement)


# 10. Lecture de toutes les alertes
curseur.execute("SELECT * FROM alertes")
alertes = curseur.fetchall()

print("\nAlertes enregistrées :")

for alerte in alertes:
    print(alerte)


# 11. Fermeture de la connexion
connexion.close()

print("\nConnexion à la base de données fermée.")