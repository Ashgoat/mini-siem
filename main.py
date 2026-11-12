import sqlite3
import re
from datetime import datetime

# =====================================
# 1. CONNEXION À LA BASE DE DONNÉES
# =====================================

connexion = sqlite3.connect("siem.db")
curseur = connexion.cursor()

print("Connexion à la base de données réussie.")

# =====================================
# 2. CRÉATION DES TABLES
# =====================================

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

curseur.execute("""
CREATE TABLE IF NOT EXISTS alertes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    type TEXT,
    ip TEXT,
    description TEXT
)
""")

connexion.commit()

print("Tables vérifiées.")

# =====================================
# 3. LECTURE DES LOGS
# =====================================

fichier_log = "test_logs.txt"

with open(fichier_log, "r") as fichier:
    lignes = fichier.readlines()

print("\nNombre de lignes lues :", len(lignes))

# =====================================
# 4. ANALYSE DES LOGS
# =====================================

tentatives = {}

machine = "LAPTOP-JEOKA4OH"

for ligne in lignes:

    resultat = re.search(
        r"(\w+)\[(\d+)\]: (.*)",
        ligne
    )

    if resultat:

        service = resultat.group(1)
        pid = resultat.group(2)
        message = resultat.group(3)

        date = datetime.now().isoformat()

        # Vérification de l'existence de l'événement
        curseur.execute("""
        SELECT * FROM evenements
        WHERE machine = ?
        AND service = ?
        AND pid = ?
        AND message = ?
        """, (machine, service, pid, message))

        evenement_existant = curseur.fetchone()

        # Enregistrement uniquement si l'événement est nouveau
        if evenement_existant is None:

            curseur.execute("""
            INSERT INTO evenements
            (date, machine, service, pid, message)
            VALUES (?, ?, ?, ?, ?)
            """, (date, machine, service, pid, message))

            print("Nouvel événement enregistré.")

        else:

            print("Événement déjà présent, ignoré.")

    # =====================================
    # 5. DÉTECTION DES CONNEXIONS ÉCHOUÉES
    # =====================================

    if "Failed password" in ligne:

        resultat_ip = re.search(
            r"from (\d{1,3}(?:\.\d{1,3}){3})",
            ligne
        )

        if resultat_ip:

            ip = resultat_ip.group(1)

            if ip in tentatives:

                tentatives[ip] += 1

            else:

                tentatives[ip] = 1

# =====================================
# 6. DÉTECTION DES ATTAQUES BRUTE FORCE
# =====================================

print("\n===== ANALYSE DES TENTATIVES =====")

for ip, compteur in tentatives.items():

    print("IP :", ip)
    print("Tentatives échouées :", compteur)

    if compteur >= 5:

        description = (
            str(compteur)
            + " tentatives de connexion échouées détectées"
        )

        # Vérification de l'existence de l'alerte
        curseur.execute("""
        SELECT * FROM alertes
        WHERE type = ? AND ip = ?
        """, ("Brute Force", ip))

        alerte_existante = curseur.fetchone()

        if alerte_existante is None:

            curseur.execute("""
            INSERT INTO alertes
            (date, type, ip, description)
            VALUES (?, ?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d"),
                "Brute Force",
                ip,
                description
            ))

            print("ALERTE détectée et enregistrée !")

        else:

            print("Cette alerte existe déjà.")

# =====================================
# 7. SAUVEGARDE DES DONNÉES
# =====================================

connexion.commit()

print("\n================================")
print("ANALYSE TERMINÉE AVEC SUCCÈS")
print("================================")

# =====================================
# 8. AFFICHAGE DES STATISTIQUES
# =====================================

curseur.execute("SELECT COUNT(*) FROM evenements")
nombre_evenements = curseur.fetchone()[0]

curseur.execute("SELECT COUNT(*) FROM alertes")
nombre_alertes = curseur.fetchone()[0]

print("\nNombre total d'événements :", nombre_evenements)
print("Nombre total d'alertes :", nombre_alertes)

# =====================================
# 9. FERMETURE DE LA CONNEXION
# =====================================

connexion.close()

print("\nConnexion à la base de données fermée.")