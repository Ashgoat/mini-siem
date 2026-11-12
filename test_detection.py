tentatives = {}

liste_ip = [
    "192.168.1.10",
    "192.168.1.10",
    "192.168.1.10",
    "192.168.1.10",
    "192.168.1.10",
    "10.0.0.8",
    "10.0.0.8"
]

for ip in liste_ip:
    if ip in tentatives:
        tentatives[ip] += 1
    else:
        tentatives[ip] = 1

for ip, compteur in tentatives.items():
    print("IP :", ip, "| Tentatives :", compteur)

    if compteur >= 5:
        print("ALERTE : Brute Force détecté depuis", ip)