import re

texte = "Failed password for admin from 192.168.1.10 port 4567"

# Extraire l'utilisateur
utilisateur = re.search(r"for (\w+)", texte)

# Extraire l'adresse IP
ip = re.search(r"from (\d+\.\d+\.\d+\.\d+)", texte)

# Extraire le port
port = re.search(r"port (\d+)", texte)

if utilisateur:
    print("Utilisateur :", utilisateur.group(1))

if ip:
    print("Adresse IP :", ip.group(1))

if port:
    print("Port :", port.group(1))