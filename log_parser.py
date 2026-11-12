import re

log_file = "test_logs.txt"

pattern = r"^(\S+)\s+(\S+)\s+([\w-]+)\[(\d+)\]:\s+(.*)$"

tentatives = {}

with open(log_file, "r") as fichier:
    for ligne in fichier:
        resultat = re.search(pattern, ligne)

        if resultat:
            date = resultat.group(1)
            machine = resultat.group(2)
            service = resultat.group(3)
            pid = resultat.group(4)
            message = resultat.group(5)

            if "Failed password" in message:

                resultat_ip = re.search(
                    r"from (\d{1,3}(?:\.\d{1,3}){3})",
                    message
                )

                if resultat_ip:
                    ip = resultat_ip.group(1)

                    if ip in tentatives:
                        tentatives[ip] += 1
                    else:
                        tentatives[ip] = 1

                    print("Connexion échouée détectée !")
                    print("Détail :", message)

            evenement = {
                "date": date,
                "machine": machine,
                "service": service,
                "pid": pid,
                "message": message
            }

            print(evenement)

print("Nombre de tentatives par IP :", tentatives)
for ip, compteur in tentatives.items():
    if compteur >= 5:
        print("ALERTE : Brute Force détecté depuis", ip)
        print("Nombre de tentatives :", compteur)