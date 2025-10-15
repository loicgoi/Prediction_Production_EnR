import streamlit as st
import pandas as pd
import requests
from datetime import date

# =========================
# Configuration de la page
# =========================
st.set_page_config(
    page_title="Prédiction Production ENR",
    page_icon="♻️",
    layout="wide"
)

st.title("Application de Prédiction de Production d'énergie renouvelable")
st.markdown("""
Notre super app de prédiction boostée par l'IA . 
Sélectionnez un onglet pour interagir avec l'API.
""")

# =========================
# URL de l'API
# =========================
API_URL = "http://localhost:8000"

# =========================
# Sidebar pour navigation
# =========================
page = st.sidebar.selectbox(
    "Menu",
    ["Accueil", "Status API", "Prédiction Solaire", "Prédiction Éolienne", "Prédiction Hydro", "Status des Modèles"]
)

# =========================
# Accueil
# =========================
if page == "Accueil":
    st.subheader("Bienvenue sur l'application")
    st.write("Utilisez le menu à gauche pour explorer les fonctionnalités et lancer vos prédictions.")

# =========================
# Status API
# =========================
elif page == "Status API":
    st.subheader("Vérification du statut de l'API")
    try:
        response = requests.get(f"{API_URL}/status")
        if response.ok:
            st.success("API en ligne ✅")
            st.json(response.json())
        else:
            st.error("Erreur lors de la récupération du statut")
    except Exception as e:
        st.error(f"Impossible de contacter l'API : {e}")

# =========================
# Fonction pour afficher le tableau stylé
# =========================
def styled_table(df, value_col="Remarque"):
    # On colorie ok en vert et no en rouge
    def color_remark(val):
        color = 'green' if val == "✔️" else 'red'
        return f'color: {color}; font-weight: bold'

    st.dataframe(df.style.applymap(color_remark, subset=[value_col]))

# =========================
# Fonction générique pour prédiction
# =========================
def make_prediction(endpoint_name):
    st.subheader(f"Prédiction {endpoint_name.capitalize()}")
    pred_date = st.date_input("Sélectionnez une date", value=date.today())
    if st.button(f"Lancer la prédiction {endpoint_name}"):
        payload = {"date": str(pred_date)}
        try:
            response = requests.post(f"{API_URL}/predict/{endpoint_name}", json=payload)
            if response.ok:
                st.success(f"Prédiction {endpoint_name} reçue !")
                
                data = response.json()
                
                if isinstance(data, dict):
                    df = pd.DataFrame([data])
                    df['Remarque'] = df['status'].apply(lambda x: "✔️" if x.lower() == "ok" else "❌")
                    styled_table(df[['model_name', 'prediction', 'Remarque']])
                else:
                    st.json(data)
            else:
                st.error(f"Erreur API : {response.text}")
        except Exception as e:
            st.error(f"Erreur de connexion : {e}")

# =========================
# Prédictions selon l'onglet
# =========================
if page == "Prédiction Solaire":
    make_prediction("solar")
elif page == "Prédiction Éolienne":
    make_prediction("wind")
elif page == "Prédiction Hydro":
    make_prediction("hydro")

# =========================
# Status des modèles
# =========================
elif page == "Status des Modèles":
    st.subheader("État des modèles")
    try:
        response = requests.get(f"{API_URL}/models/status")
        if response.ok:
            data = response.json()
            df = pd.DataFrame(data)
            df['Remarque'] = df['status'].apply(lambda x: "✔️" if x.lower() == "ok" else "❌")
            styled_table(df[['model_name', 'Remarque']])
        else:
            st.error("Erreur lors de la récupération du status des modèles")
    except Exception as e:
        st.error(f"Impossible de contacter l'API : {e}")
