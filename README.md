#  Mini-SIEM

## 1. Présentation du projet

Ce projet consiste à développer un Mini-SIEM (Security Information and Event Management) en Python.

L'objectif est de surveiller des fichiers de logs Linux, détecter des comportements suspects et générer des alertes de sécurité.

## 2. Technologies utilisées

- Python
- Linux (Ubuntu / WSL)
- Regex
- SQLite
- Pandas
- Streamlit
- Git et GitHub

## 3. Fonctionnalités

- Lecture des fichiers de logs.
- Extraction des informations avec Regex.
- Détection des tentatives de connexion échouées.
- Détection des attaques Brute Force.
- Identification des adresses IP suspectes.
- Enregistrement des événements et alertes dans SQLite.
- Tableau de bord interactif avec Streamlit.
- Visualisation des statistiques de sécurité.
- Tests automatisés avec unittest.

## 4. Architecture

Logs Linux → Python → Regex → Détection → SQLite → Streamlit

## 5. Lancement du projet

Activer l'environnement virtuel :

```bash
source venv/bin/activate
```

Lancer l'analyse :

```bash
python main.py
```

Lancer le tableau de bord :

```bash
streamlit run app.py
```

## 6. Tests

Exécuter les tests :

```bash
python -m unittest tests_jour9.py
```

## 7. Conclusion

Ce projet permet de comprendre les principes fondamentaux d'un SIEM et de mettre en pratique la programmation Python, l'analyse de logs, la détection d'incidents et la visualisation de données.