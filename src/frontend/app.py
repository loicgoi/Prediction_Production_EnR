import streamlit as st
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
Notre super app de prédiction boostée par l'IA.  
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
# Fonction générique pour prédiction
# =========================
def make_prediction(endpoint_name: str):
    st.subheader(f"Prédiction {endpoint_name.capitalize()}")
    
    pred_date = st.date_input("Sélectionnez une date", value=date.today())

    if st.button(f"Lancer la prédiction {endpoint_name}"):
        try:
            # On envoie juste la date dans le body, l'API récupère les features météo automatiquement
            payload = {"date": str(pred_date)}
            response = requests.post(f"{API_URL}/predict/{endpoint_name}", json=payload)

            if response.ok:
                st.success(f"Prédiction {endpoint_name} reçue !")
                data = response.json()
                st.write(f"**Type de production :** {data['producer_type']}")
                st.write(f"**Prédiction (kWh) :** {data['prediction_kwh']}")
                st.write(f"**Statut :** {data['status']}")
            else:
                st.error(f"Erreur API : {response.text}")
        except Exception as e:
            st.error(f"Erreur de connexion : {e}")

# =========================
# Prédictions selon l'onglet
# =========================
# =========================
# Prédictions selon l'onglet
# =========================
if page == "Prédiction Solaire":
    st.subheader("Prédiction Solaire 🌞")
    
    pred_date = st.date_input("Sélectionnez une date", value=date.today())

    if st.button("Lancer la prédiction solaire"):
        try:
            # On envoie juste la date dans le body, l'API récupère les features météo automatiquement
            payload = {"date": str(pred_date)}
            response = requests.post(f"{API_URL}/predict/solar", json=payload)

            if response.ok:
                data = response.json()
                st.success(f"Prédiction solaire reçue !")
                st.write(f"**Type de production :** {data['producer_type']}")
                st.write(f"**Prédiction (kWh) :** {data['prediction_kwh']}")
                st.write(f"**Statut :** {data['status']}")
            else:
                # Si l'API renvoie un détail (comme pour missing fields)
                try:
                    st.error(f"Erreur API : {response.json()['detail']}")
                except:
                    st.error(f"Erreur API : {response.text}")
        except Exception as e:
            st.error(f"Erreur de connexion : {e}")

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
            for model, info in data.items():
                status = "✅ Chargé" if info.get("loaded") else "❌ Non chargé"
                st.write(f"{model.capitalize()} : {status}")
        else:
            st.error("Erreur lors de la récupération du status des modèles")
    except Exception as e:
        st.error(f"Impossible de contacter l'API : {e}")
