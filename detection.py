import re


# Fonction pour compter les tentatives échouées
def compter_tentatives(lignes):

    tentatives = {}

    for ligne in lignes:

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

    return tentatives


# Fonction pour détecter les attaques brute force
def detecter_brute_force(tentatives, seuil=5):

    alertes = {}

    for ip, compteur in tentatives.items():

        if compteur >= seuil:
            alertes[ip] = compteur

    return alertes