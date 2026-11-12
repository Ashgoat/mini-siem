import streamlit as st
import sqlite3
import pandas as pd

# ==========================================
# 1. CONFIGURATION DE LA PAGE
# ==========================================

st.set_page_config(
    page_title="Mini-SIEM",
    page_icon="🔐",
    layout="wide"
)

# ==========================================
# 2. TITRE DE L'APPLICATION
# ==========================================

st.title("🔐 Mini-SIEM")
st.subheader("Tableau de bord de sécurité")

st.write(
    "Surveillance des événements "
    "et des alertes de sécurité."
)

# ==========================================
# 3. CONNEXION À LA BASE DE DONNÉES
# ==========================================

connexion = sqlite3.connect("siem.db")
curseur = connexion.cursor()

# ==========================================
# 4. RÉCUPÉRATION DES ÉVÉNEMENTS
# ==========================================

curseur.execute("SELECT * FROM evenements")
evenements = curseur.fetchall()

# ==========================================
# 5. RÉCUPÉRATION DES ALERTES
# ==========================================

curseur.execute("SELECT * FROM alertes")
alertes = curseur.fetchall()

# ==========================================
# 6. CRÉATION DES TABLEAUX PANDAS
# ==========================================

df_evenements = pd.DataFrame(
    evenements,
    columns=[
        "ID",
        "Date",
        "Machine",
        "Service",
        "PID",
        "Message"
    ]
)

df_alertes = pd.DataFrame(
    alertes,
    columns=[
        "ID",
        "Date",
        "Type",
        "Adresse IP",
        "Description"
    ]
)

# ==========================================
# 7. AFFICHAGE DES STATISTIQUES
# ==========================================

st.header("📊 Statistiques")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Nombre d'événements",
        value=len(evenements)
    )

with col2:
    st.metric(
        label="Nombre d'alertes",
        value=len(alertes)
    )

with col3:
    if not df_alertes.empty:
        nombre_ip = df_alertes["Adresse IP"].nunique()
    else:
        nombre_ip = 0

    st.metric(
        label="Adresses IP suspectes",
        value=nombre_ip
    )

# ==========================================
# 8. AFFICHAGE DES ÉVÉNEMENTS
# ==========================================

st.header("📋 Événements enregistrés")

if not df_evenements.empty:

    st.dataframe(
        df_evenements,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("Aucun événement enregistré.")

# ==========================================
# 9. AFFICHAGE DES ALERTES AVEC FILTRE IP
# ==========================================

st.header("🚨 Alertes de sécurité")

if not df_alertes.empty:

    liste_ip = ["Toutes"] + sorted(
        df_alertes["Adresse IP"].unique().tolist()
    )

    ip_selectionnee = st.selectbox(
        "Filtrer par adresse IP :",
        liste_ip
    )

    if ip_selectionnee == "Toutes":

        df_filtre = df_alertes

    else:

        df_filtre = df_alertes[
            df_alertes["Adresse IP"] == ip_selectionnee
        ]

    st.dataframe(
        df_filtre,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("Aucune alerte enregistrée.")

# ==========================================
# 10. GRAPHIQUE DES ALERTES PAR ADRESSE IP
# ==========================================

st.header("📊 Alertes par adresse IP")

if not df_alertes.empty:

    alertes_par_ip = df_alertes["Adresse IP"].value_counts()

    st.bar_chart(alertes_par_ip)

else:
    st.info("Aucune donnée disponible pour le graphique.")

# ==========================================
# 11. GRAPHIQUE DES ÉVÉNEMENTS PAR SERVICE
# ==========================================

st.header("📈 Événements par service")

if not df_evenements.empty:

    evenements_par_service = df_evenements["Service"].value_counts()

    st.bar_chart(evenements_par_service)

else:
    st.info("Aucun événement disponible.")

# ==========================================
# 12. GRAPHIQUE DES ALERTES PAR TYPE
# ==========================================

st.header("📊 Alertes par type")

if not df_alertes.empty:

    alertes_par_type = df_alertes["Type"].value_counts()

    st.bar_chart(alertes_par_type)

else:
    st.info("Aucune alerte disponible.")

# ==========================================
# 13. FERMETURE DE LA CONNEXION
# ==========================================

connexion.close()