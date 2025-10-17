# src/frontend/app.py
import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
import sys
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de l'API
API_BASE_URL = "http://localhost:8000"

# Configuration de la page
st.set_page_config(
    page_title="Prédiction Production Énergie Renouvelable",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Style CSS personnalisé
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .success-prediction {
        border-left: 5px solid #28a745;
    }
    .warning-prediction {
        border-left: 5px solid #ffc107;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .api-status-connected {
        color: #28a745;
        font-weight: bold;
    }
    .api-status-disconnected {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Header principal
st.markdown(
    '<div class="main-header">Prédiction de Production d\'Énergie Renouvelable</div>',
    unsafe_allow_html=True,
)


# Fonctions pour interagir avec l'API
def test_api_connection():
    """Teste la connexion à l'API"""
    try:
        response = requests.get(f"{API_BASE_URL}/status", timeout=5)
        if response.status_code == 200:
            return True, "API connectée"
        else:
            return False, f"API erreur: {response.status_code}"
    except Exception as e:
        return False, f"API non accessible: {str(e)}"


def get_models_status():
    """Récupère le statut des modèles via l'API"""
    try:
        response = requests.get(f"{API_BASE_URL}/models/status", timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"models_status": {}}
    except Exception as e:
        st.error(f"Erreur récupération statut modèles: {e}")
        return {"models_status": {}}


def predict_via_api(producer_type: str, features: dict):
    """Fait une prédiction via l'API FastAPI"""
    try:
        endpoint = f"{API_BASE_URL}/predict/{producer_type}"
        response = requests.post(endpoint, json=features, timeout=30)

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur API: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de connexion à l'API: {e}")
        return None


def get_forecast_via_api(producer_type: str):
    """Récupère les prévisions via l'API"""
    try:
        endpoint = f"{API_BASE_URL}/forecast/{producer_type}"
        response = requests.get(endpoint, timeout=30)

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur API prévisions: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de connexion pour prévisions: {e}")
        return None


def get_all_forecasts_via_api():
    """Récupère toutes les prévisions via l'API"""
    try:
        endpoint = f"{API_BASE_URL}/forecast/all"
        response = requests.get(endpoint, timeout=30)

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur API toutes prévisions: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de connexion pour toutes prévisions: {e}")
        return None


def get_forecast_status_via_api():
    """Récupère le statut des prévisions via l'API"""
    try:
        endpoint = f"{API_BASE_URL}/forecast/status"
        response = requests.get(endpoint, timeout=10)

        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "stats": {}}

    except requests.exceptions.RequestException:
        return {"status": "error", "stats": {}}


# Sidebar pour la navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choisir une section:",
    [
        "Accueil",
        "Prédiction Manuelle",
        "Prévisions Automatiques",
        "Statistiques Modèles",
    ],
)

# Statut de l'API dans la sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Statut de l'API")

api_connected, api_message = test_api_connection()
if api_connected:
    st.sidebar.markdown(
        f'<p class="api-status-connected">{api_message}</p>', unsafe_allow_html=True
    )
else:
    st.sidebar.markdown(
        f'<p class="api-status-disconnected">{api_message}</p>', unsafe_allow_html=True
    )
    st.sidebar.info(
        "Assurez-vous que l'API FastAPI est démarrée sur http://localhost:8000"
    )

# Page d'accueil
if page == "Accueil":
    st.header("Bienvenue dans l'interface de prédiction")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Producteurs", "3 types")

    with col2:
        st.metric("Modèles ML", "Ridge, XGBoost, Random Forest")

    with col3:
        st.metric("Prédictions", "Production quotidienne (kWh)")

    st.markdown("---")

    # Vérification des modèles disponibles via API
    st.subheader("État des Modèles")

    if not api_connected:
        st.error("Impossible de récupérer l'état des modèles - API non connectée")
    else:
        models_status = get_models_status()
        models_data = models_status.get("models_status", {})

        cols = st.columns(3)
        colors = {"solar": "🟡", "wind": "🔵", "hydro": "🟢"}
        names = {"solar": "Solaire", "wind": "Éolien", "hydro": "Hydraulique"}

        for idx, producer_type in enumerate(["solar", "wind", "hydro"]):
            with cols[idx]:
                status = models_data.get(producer_type, {})
                if status.get("loaded", False):
                    st.success(f"{colors[producer_type]} {names[producer_type]}")
                    st.write(f"Type: {status.get('model_type', 'Inconnu')}")
                    st.write(f"Scaler: {'✅' if status.get('has_scaler') else '❌'}")
                else:
                    st.error(f"{colors[producer_type]} {names[producer_type]}")
                    st.write("Modèle non chargé")
                    if status.get("error"):
                        st.write(f"Erreur: {status['error']}")

    # Instructions
    st.markdown("---")
    st.subheader("Instructions d'utilisation")
    st.write(
        """
    1. **Prédiction Manuelle** : Saisissez les paramètres météo pour obtenir une prédiction instantanée via l'API
    2. **Prévisions Automatiques** : Génère des prévisions pour les prochains jours via l'API
    3. **Statistiques Modèles** : Vérifiez l'état et testez vos modèles via l'API
    
    **Note** : Toutes les prédictions passent par l'API FastAPI sur http://localhost:8000
    """
    )

# Page de prédiction manuelle
elif page == "Prédiction Manuelle":
    st.header("Prédiction Manuelle")
    st.write(
        "Saisissez les paramètres météorologiques pour obtenir une prédiction de production via l'API"
    )

    if not api_connected:
        st.error("API non connectée - Impossible de faire des prédictions")
        st.info(
            "Veuillez démarrer l'API FastAPI avec: `python main.py api` ou `uvicorn src.api.main:app --reload`"
        )
    else:
        # Sélection du type de producteur
        producer_type = st.selectbox(
            "Type de producteur:",
            ["solar", "wind", "hydro"],
            format_func=lambda x: {
                "solar": "Solaire",
                "wind": "Éolien",
                "hydro": "Hydraulique",
            }[x],
        )

        # Formulaire selon le type de producteur
        with st.form("prediction_form"):
            if producer_type == "solar":
                st.subheader("Paramètres Solaires")
                col1, col2 = st.columns(2)

                with col1:
                    temperature = st.number_input(
                        "Température moyenne (°C)",
                        value=20.0,
                        min_value=-30.0,
                        max_value=50.0,
                    )
                    radiation = st.number_input(
                        "Radiation solaire (kWh/m²)",
                        value=4.5,
                        min_value=0.0,
                        max_value=10.0,
                    )
                    sunshine = st.number_input(
                        "Durée d'ensoleillement (s)",
                        value=40000.0,
                        min_value=0.0,
                        max_value=86400.0,
                    )

                with col2:
                    cloud_cover = st.number_input(
                        "Couverture nuageuse (%)",
                        value=30.0,
                        min_value=0.0,
                        max_value=100.0,
                    )
                    humidity = st.number_input(
                        "Humidité relative (%)",
                        value=60.0,
                        min_value=0.0,
                        max_value=100.0,
                    )

                features = {
                    "temperature_2m_mean": temperature,
                    "shortwave_radiation_sum_kwh_m2": radiation,
                    "sunshine_duration": sunshine,
                    "cloud_cover_mean": cloud_cover,
                    "relative_humidity_2m_mean": humidity,
                }

            elif producer_type == "wind":
                st.subheader("Paramètres Éoliens")
                col1, col2 = st.columns(2)

                with col1:
                    wind_speed = st.number_input(
                        "Vitesse vent max (m/s)",
                        value=8.0,
                        min_value=0.0,
                        max_value=50.0,
                    )
                    wind_gusts = st.number_input(
                        "Rafales max (m/s)", value=12.0, min_value=0.0, max_value=80.0
                    )

                with col2:
                    wind_direction = st.number_input(
                        "Direction vent (°)",
                        value=180.0,
                        min_value=0.0,
                        max_value=360.0,
                    )
                    temperature = st.number_input(
                        "Température moyenne (°C)",
                        value=15.0,
                        min_value=-30.0,
                        max_value=50.0,
                    )

                features = {
                    "wind_speed_10m_max": wind_speed,
                    "wind_gusts_10m_max": wind_gusts,
                    "wind_direction_10m_dominant": wind_direction,
                    "temperature_2m_mean": temperature,
                }

            else:  # hydro
                st.subheader("Paramètres Hydrauliques")
                debit = st.number_input(
                    "Débit (L/s)", value=1500.0, min_value=0.0, max_value=10000.0
                )

                features = {"debit_l_s": debit}

            # Bouton de prédiction
            submitted = st.form_submit_button("Lancer la Prédiction via API")

            if submitted:
                with st.spinner("Prédiction en cours via l'API..."):
                    result = predict_via_api(producer_type, features)

                    if result:
                        prediction = result["prediction_kwh"]

                        # Afficher le résultat
                        st.markdown("---")
                        st.markdown(
                            f'<div class="prediction-card success-prediction">',
                            unsafe_allow_html=True,
                        )

                        col1, col2 = st.columns([1, 2])

                        with col1:
                            st.metric(
                                label="Production Prédite",
                                value=f"{prediction:.2f} kWh",
                                delta=None,
                            )

                        with col2:
                            st.write("**Paramètres utilisés:**")
                            for feature, value in features.items():
                                st.write(f"- `{feature}`: {value}")
                            st.write(f"**Type de producteur:** {producer_type}")
                            st.write("**Source:** API FastAPI")

                        st.markdown("</div>", unsafe_allow_html=True)

                        # Graphique de simulation
                        st.subheader("Simulation d'impact")
                        fig, ax = plt.subplots(figsize=(10, 4))

                        # Simulation basique pour la visualisation
                        if producer_type == "solar":
                            param_name = "shortwave_radiation_sum_kwh_m2"
                            x_label = "Radiation solaire (kWh/m²)"
                            x_range = np.linspace(0, 10, 20)
                        elif producer_type == "wind":
                            param_name = "wind_speed_10m_max"
                            x_label = "Vitesse du vent (m/s)"
                            x_range = np.linspace(0, 25, 20)
                        else:  # hydro
                            param_name = "debit_l_s"
                            x_label = "Débit (L/s)"
                            x_range = np.linspace(0, 5000, 20)

                        # Simulation des prédictions pour le graphique
                        simulated_predictions = []
                        for x_val in x_range:
                            sim_features = features.copy()
                            sim_features[param_name] = x_val
                            sim_result = predict_via_api(producer_type, sim_features)
                            if sim_result:
                                simulated_predictions.append(
                                    sim_result["prediction_kwh"]
                                )
                            else:
                                simulated_predictions.append(0)

                        if simulated_predictions:
                            ax.plot(x_range, simulated_predictions, linewidth=2)
                            ax.axvline(
                                x=features[param_name],
                                color="r",
                                linestyle="--",
                                label="Valeur actuelle",
                            )
                            ax.set_xlabel(x_label)
                            ax.set_ylabel("Production (kWh)")
                            ax.set_title(f"Impact du paramètre sur la production")
                            ax.legend()
                            ax.grid(True, alpha=0.3)
                            st.pyplot(fig)

# Page des prévisions automatiques
elif page == "Prévisions Automatiques":
    st.header("Prévisions Automatiques")
    st.write("Génère des prévisions de production pour les prochains jours via l'API")

    if not api_connected:
        st.error("API non connectée - Impossible de générer des prévisions")
    else:
        # ✅ Une seule colonne large
        if st.button("Générer Toutes les Prévisions", type="primary"):
            with st.spinner("Génération des prévisions via l'API..."):
                all_forecasts = get_all_forecasts_via_api()

                if all_forecasts:
                    summary = all_forecasts.get("summary", {})
                    st.success("Prévisions générées avec succès via l'API!")

                    # Affichage résumé
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Jours solaires", summary.get("solar_days", 0))
                    with col2:
                        st.metric("Jours éoliens", summary.get("wind_days", 0))
                    with col3:
                        st.metric("Jours hydrauliques", summary.get("hydro_days", 0))

                    # Affichage détaillé des prévisions
                    for producer_type in ["solar", "wind", "hydro"]:
                        st.subheader(f"Prévisions {producer_type.capitalize()}")
                        predictions = all_forecasts.get(producer_type, [])

                        if predictions:
                            df_data = [
                                {
                                    "Date": pred["date"],
                                    "Production (kWh)": pred["prediction_kwh"],
                                    "Modèle": pred.get("model_type", "Inconnu"),
                                }
                                for pred in predictions
                            ]
                            df = pd.DataFrame(df_data)

                            # ✅ Largeur fluide
                            st.dataframe(df, use_container_width=True)

                            # Graphique des prévisions
                            fig, ax = plt.subplots(figsize=(12, 5))
                            dates = pd.to_datetime(df["Date"])
                            productions = df["Production (kWh)"]

                            ax.plot(dates, productions, "o-", linewidth=2, markersize=6)
                            ax.set_title(
                                f"Prévisions de production {producer_type.capitalize()}"
                            )
                            ax.set_ylabel("Production (kWh)")
                            ax.grid(True, alpha=0.3)
                            plt.xticks(rotation=45)
                            st.pyplot(fig)
                        else:
                            st.warning(
                                f"Aucune prévision disponible pour {producer_type}"
                            )

        # ✅ Statut des prévisions en dessous
        st.markdown("---")
        st.subheader("Statut des Prévisions")
        forecast_status = get_forecast_status_via_api()
        stats = forecast_status.get("stats", {})

        if forecast_status.get("status") == "operational":
            st.success("Système de prévisions opérationnel")
        else:
            st.warning("Système de prévisions dégradé")

        availability = stats.get("forecast_availability", {})

        st.write("**Disponibilité des données:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Solaire", availability.get("solar", 0))
        with col2:
            st.metric("Éolien", availability.get("wind", 0))
        with col3:
            st.metric("Hydraulique", availability.get("hydro", 0))


# Page des statistiques des modèles
elif page == "Statistiques Modèles":
    st.header("Statistiques des Modèles")

    if not api_connected:
        st.error("API non connectée - Impossible de récupérer les statistiques")
    else:
        # Vérification détaillée des modèles via API
        st.subheader("État des Modèles via API")

        models_status = get_models_status()
        models_data = models_status.get("models_status", {})

        for producer_type in ["solar", "wind", "hydro"]:
            with st.expander(f"Modèle {producer_type.upper()}", expanded=True):
                status = models_data.get(producer_type, {})

                if status.get("loaded", False):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.success("Modèle chargé via API")
                        st.write(f"**Type:** {status.get('model_type', 'Inconnu')}")
                        st.write(
                            f"**Scaler:** {'Disponible' if status.get('has_scaler') else 'Absent'}"
                        )

                    with col2:
                        st.write("**Test de prédiction:**")
                        # Test avec valeurs par défaut
                        test_features = {}
                        if producer_type == "solar":
                            test_features = {
                                "temperature_2m_mean": 20.0,
                                "shortwave_radiation_sum_kwh_m2": 4.5,
                                "sunshine_duration": 40000.0,
                                "cloud_cover_mean": 30.0,
                                "relative_humidity_2m_mean": 60.0,
                            }
                        elif producer_type == "wind":
                            test_features = {
                                "wind_speed_10m_max": 8.0,
                                "wind_gusts_10m_max": 12.0,
                                "wind_direction_10m_dominant": 180.0,
                                "temperature_2m_mean": 15.0,
                            }
                        else:  # hydro
                            test_features = {"debit_l_s": 1500.0}

                        if st.button(
                            f"Tester {producer_type}", key=f"test_{producer_type}"
                        ):
                            with st.spinner("Test en cours via API..."):
                                result = predict_via_api(producer_type, test_features)
                                if result:
                                    st.success(
                                        f"Prédiction test: {result['prediction_kwh']:.2f} kWh"
                                    )
                                else:
                                    st.error("Erreur lors du test")

                else:
                    st.error("Modèle non chargé")
                    if "error" in status:
                        st.write(f"**Erreur:** {status['error']}")

        # Endpoints API disponibles
        st.subheader("📡 Endpoints API Disponibles")
        endpoints = [
            ("GET", "/status", "Statut de l'API"),
            ("GET", "/models/status", "Statut des modèles"),
            ("POST", "/predict/solar", "Prédiction solaire"),
            ("POST", "/predict/wind", "Prédiction éolienne"),
            ("POST", "/predict/hydro", "Prédiction hydraulique"),
            ("GET", "/forecast/solar", "Prévisions solaires"),
            ("GET", "/forecast/wind", "Prévisions éoliennes"),
            ("GET", "/forecast/hydro", "Prévisions hydrauliques"),
            ("GET", "/forecast/all", "Toutes les prévisions"),
            ("GET", "/forecast/status", "Statut des prévisions"),
        ]

        for method, endpoint, description in endpoints:
            st.write(f"`{method} {endpoint}` - {description}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Interface Streamlit - Production d'Énergie Renouvelable © 2024<br>"
    "Connectée à l'API FastAPI sur " + API_BASE_URL + "</div>",
    unsafe_allow_html=True,
)
