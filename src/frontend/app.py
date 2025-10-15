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
Notre app de prédiction boostée par l'IA   
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
    st.subheader("Bienvenue sur l'application 🌍")
    st.write("Utilisez le menu à gauche pour explorer les fonctionnalités et lancer vos prédictions d'énergie solaire, éolienne ou hydroélectrique.")

# =========================
# Status API
# =========================
elif page == "Status API":
    st.subheader("Vérification du statut de l'API 🔌")
    try:
        response = requests.get(f"{API_URL}/status")
        if response.ok:
            st.success("✅ API en ligne")
            st.json(response.json())
        else:
            st.error(f"❌ Erreur API ({response.status_code})")
    except Exception as e:
        st.error(f"Impossible de contacter l'API : {e}")

# =========================
# Fonction générique de prédiction (sans affichage de features)
# =========================
def make_prediction(endpoint_name: str, emoji: str):
    st.subheader(f"Prédiction {endpoint_name.capitalize()} {emoji}")
    
    pred_date = st.date_input("📅 Sélectionnez une date", value=date.today())

    if st.button(f"Lancer la prédiction {endpoint_name}"):
        with st.spinner("⏳ Calcul de la prédiction..."):
            try:
                # On envoie uniquement la date — le backend récupère les features météo
                payload = {"date": str(pred_date)}
                response = requests.post(f"{API_URL}/predict/{endpoint_name}", json=payload)

                if response.ok:
                    data = response.json()
                    st.success(f"✅ Prédiction {endpoint_name} réussie !")
                    st.metric(label="Type de production", value=data.get("producer_type", "N/A"))
                    st.metric(label="Prédiction (kWh)", value=round(data.get("prediction_kwh", 0), 2))
                    st.info(f"Statut du modèle : {data.get('status', 'Inconnu')}")
                else:
                    try:
                        err_detail = response.json().get("detail", response.text)
                    except Exception:
                        err_detail = response.text
                    st.error(f"Erreur API : {err_detail}")
            except Exception as e:
                st.error(f"Erreur de connexion : {e}")

# =========================
# Onglets de prédiction
# =========================
if page == "Prédiction Solaire":
    make_prediction("solar", "🌞")

elif page == "Prédiction Éolienne":
    make_prediction("wind", "💨")

elif page == "Prédiction Hydro":
    make_prediction("hydro", "💧")

# =========================
# Status des modèles
# =========================
elif page == "Status des Modèles":
    st.subheader("État des modèles 🤖")
    try:
        response = requests.get(f"{API_URL}/models/status")
        if response.ok:
            data = response.json()
            for model, info in data.items():
                status = "✅ Chargé" if info.get("loaded") else "❌ Non chargé"
                st.write(f"{model.capitalize()} : {status}")
        else:
            st.error(f"Erreur lors de la récupération du status ({response.status_code})")
    except Exception as e:
        st.error(f"Impossible de contacter l'API : {e}")
