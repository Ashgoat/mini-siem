log_file = "/var/log/auth.log"

compteur = 0

with open(log_file, "r") as fichier:
    for ligne in fichier:
        compteur += 1

print("Nombre total de lignes :", compteur)