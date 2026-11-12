import sqlite3
import re

# 1. Connexion à la base de données
connexion = sqlite3.connect("siem.db")
curseur = connexion.cursor()

# 2. Création de la table des alertes si nécessaire
curseur.execute("""
CREATE TABLE IF NOT EXISTS alertes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    type TEXT,
    ip TEXT,
    description TEXT
)
""")

# 3. Lecture du fichier de logs
log_file = "test_logs.txt"

tentatives = {}

with open(log_file, "r") as fichier:
    for ligne in fichier:

        # Vérifier les connexions échouées
        if "Failed password" in ligne:

            # Extraire l'adresse IP
            resultat_ip = re.search(
                r"from (\d{1,3}(?:\.\d{1,3}){3})",
                ligne
            )

            if resultat_ip:
                ip = resultat_ip.group(1)

                # Compter les tentatives par IP
                if ip in tentatives:
                    tentatives[ip] += 1
                else:
                    tentatives[ip] = 1


# 4. Détecter les attaques et créer les alertes
for ip, compteur in tentatives.items():

    print("IP :", ip)
    print("Tentatives :", compteur)

    if compteur >= 5:

        description = str(compteur) + " tentatives de connexion échouées détectées"

        # Vérifier si cette alerte existe déjà
        curseur.execute("""
        SELECT * FROM alertes
        WHERE type = ? AND ip = ?
        """, ("Brute Force", ip))

        alerte_existante = curseur.fetchone()

        if alerte_existante is None:

            curseur.execute("""
            INSERT INTO alertes (date, type, ip, description)
            VALUES (?, ?, ?, ?)
            """, (
                "2026-11-11",
                "Brute Force",
                ip,
                description
            ))

            connexion.commit()

            print("ALERTE enregistrée dans la base de données !")

        else:
            print("Cette alerte existe déjà.")

# 5. Afficher les alertes enregistrées
curseur.execute("SELECT * FROM alertes")
alertes = curseur.fetchall()

print("\n===== ALERTES ENREGISTRÉES =====")

for alerte in alertes:
    print(alerte)

# 6. Fermer la connexion
connexion.close()