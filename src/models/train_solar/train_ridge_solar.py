# ===============================
# train_solar_ridge.py
# ===============================

import os
import pandas as pd
import numpy as np
import joblib
import logging
from dotenv import load_dotenv
from supabase import create_client, Client
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ===============================
# CONFIGURATION DU LOGGER
# ===============================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===============================
# CHARGEMENT DES VARIABLES D'ENVIRONNEMENT
# ===============================
load_dotenv()  # charge le fichier .env automatiquement

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Les variables SUPABASE_URL et SUPABASE_KEY sont manquantes dans le fichier .env")

# ===============================
# CONNEXION SUPABASE
# ===============================
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    logger.info("Connexion Supabase réussie")
except Exception as e:
    logger.error(f"Erreur de connexion Supabase: {e}")
    raise e


# ===============================
# CHARGEMENT DES DONNÉES SOLAIRES
# ===============================
def load_training_data(producer_type: str):
    """Charge et joint les données depuis Supabase."""
    try:
        if producer_type == "solar":
            weather_data = supabase.table("clean_solar_history").select("*").execute()
            production_data = supabase.table("clean_prod_solaire").select("*").execute()
        else:
            raise ValueError("Type de producteur non pris en charge")

        df_weather = pd.DataFrame(weather_data.data)
        df_production = pd.DataFrame(production_data.data)

        df_weather["date"] = pd.to_datetime(df_weather["date"])
        df_production["date"] = pd.to_datetime(df_production["date"])

        df = pd.merge(df_weather, df_production, on="date", how="inner")
        logger.info(f"Données chargées : {len(df)} lignes")

        return df

    except Exception as e:
        logger.error(f"Erreur de chargement : {e}")
        return pd.DataFrame()


# ===============================
# ENTRAÎNEMENT DU MODÈLE RIDGE
# ===============================
def train_ridge_model(df: pd.DataFrame):
    """Prépare les données, entraîne le modèle Ridge optimisé et l'évalue."""

    FEATURES = [
        "temperature_2m_mean",
        "shortwave_radiation_sum_kwh_m2",
        "sunshine_duration",
        "cloud_cover_mean",
        "relative_humidity_2m_mean",
        "wind_speed_10m_mean"
    ]
    TARGET = "production_kwh"

    X = df[FEATURES]
    y = df[TARGET]

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardisation
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Recherche des meilleurs alpha
    ridge = Ridge()
    param_grid = {"alpha": [0.1, 1, 10, 50, 100]}
    grid = GridSearchCV(ridge, param_grid, cv=5, scoring="r2")
    grid.fit(X_train_scaled, y_train)

    best_ridge = grid.best_estimator_
    logger.info(f"Meilleur alpha trouvé : {grid.best_params_['alpha']}")

    # Évaluation
    y_pred = best_ridge.predict(X_test_scaled)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    logger.info(f"MAE: {mae:.3f} | RMSE: {rmse:.3f} | R²: {r2:.3f}")

    # Sauvegarde du modèle et du scaler
    os.makedirs("models", exist_ok=True)
    joblib.dump(best_ridge, "models/ridge_cv_solar.pkl")
    joblib.dump(scaler, "models/scaler_ridge_solar.pkl")
    logger.info("Modèle et scaler sauvegardés dans /models")

    return best_ridge, scaler


# ===============================
# PIPELINE pour verifier le fonctionnement du script 
# ===============================
# if __name__ == "__main__":
#     logger.info(" Entraînement du modèle Ridge pour la production solaire...")
#     df_solar = load_training_data("solar")

#     if not df_solar.empty:
#         model, scaler = train_ridge_model(df_solar)
#         logger.info(" Entraînement terminé avec succès.")
#     else:
#         logger.error("Aucune donnée chargée, entraînement annulé.")
