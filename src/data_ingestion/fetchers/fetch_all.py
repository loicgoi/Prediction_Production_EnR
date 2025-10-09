import logging
import os
import pandas as pd
from src.data_ingestion.handlers.handler_meteo import WeatherDataHandler
from src.data_ingestion.handlers.handler_hubeau import HubeauDataHandler
from src.data_ingestion.handlers.etl_supabase import SupabaseHandler, CSVDataHandler
from src.config.settings import settings


def fetch_all(
    latitude: float = None, longitude: float = None, hubeau_station: str = None
):
    """Charge toutes les données, nettoie et les pousse dans Supabase."""

    latitude = latitude or settings.montpellier_latitude
    longitude = longitude or settings.montpellier_longitude
    hubeau_station = hubeau_station or settings.hubeau_station

    logging.info("Début de la récupération des données")

    # Initialiser SupabaseHandler
    supabase_handler = SupabaseHandler()

    # Données API météo
    solar_handler = WeatherDataHandler(
        latitude=latitude, longitude=longitude, data_type="solar"
    )
    wind_handler = WeatherDataHandler(
        latitude=latitude, longitude=longitude, data_type="wind"
    )

    # Charger les données avec des dates par défaut
    today = pd.Timestamp.today().date()

    solar_forecast = solar_handler.load(forecast=True)
    solar_history = solar_handler.load(
        start_date="2016-09-01", end_date=today.strftime("%Y-%m-%d"), forecast=False
    )
    wind_forecast = wind_handler.load(forecast=True)
    wind_history = wind_handler.load(
        start_date="2016-09-01", end_date=today.strftime("%Y-%m-%d"), forecast=False
    )

    # Données API Hub'Eau
    hubeau_handler = HubeauDataHandler(
        code_station=hubeau_station,
        start_date="2022-07-01",
        end_date=today.strftime("%Y-%m-%d"),
    )
    df_hydro = hubeau_handler.load()
    if not df_hydro.empty:
        hubeau_handler.clean()

    # Données CSV locales
    data_raw_path = settings.data_raw_path
    prod_solar_csv = os.path.join(data_raw_path, "prod_solaire.csv")
    prod_wind_csv = os.path.join(data_raw_path, "prod_eolienne.csv")
    prod_hydro_csv = os.path.join(data_raw_path, "prod_hydro.csv")

    df_solar_prod = (
        pd.read_csv(prod_solar_csv)
        if os.path.exists(prod_solar_csv)
        else pd.DataFrame()
    )
    df_wind_prod = (
        pd.read_csv(prod_wind_csv) if os.path.exists(prod_wind_csv) else pd.DataFrame()
    )
    df_hydro_prod = (
        pd.read_csv(prod_hydro_csv)
        if os.path.exists(prod_hydro_csv)
        else pd.DataFrame()
    )

    # Pousser tout dans Supabase
    csv_handler = CSVDataHandler(supabase_handler)

    # Préparer les données pour le retour
    results = {
        "hubeau": df_hydro,
        "solar_forecast": solar_forecast,
        "solar_history": solar_history,
        "wind_forecast": wind_forecast,
        "wind_history": wind_history,
        "solar_production": df_solar_prod,
        "wind_production": df_wind_prod,
        "hydro_production": df_hydro_prod,
    }

    # Upload vers Supabase
    try:
        if not df_hydro.empty:
            csv_handler.upload_to_supabase(df_hydro, "hubeau")
        if not solar_forecast.empty:
            csv_handler.upload_to_supabase(solar_forecast, "solar_forecast")
        if not solar_history.empty:
            csv_handler.upload_to_supabase(solar_history, "solar_history")
        if not wind_forecast.empty:
            csv_handler.upload_to_supabase(wind_forecast, "wind_forecast")
        if not wind_history.empty:
            csv_handler.upload_to_supabase(wind_history, "wind_history")
        if not df_solar_prod.empty:
            csv_handler.upload_to_supabase(df_solar_prod, "prod_solaire")
        if not df_wind_prod.empty:
            csv_handler.upload_to_supabase(df_wind_prod, "prod_eolienne")
        if not df_hydro_prod.empty:
            csv_handler.upload_to_supabase(df_hydro_prod, "prod_hydro")
    except Exception as e:
        logging.error(f"Erreur lors de l'upload Supabase: {e}")

    logging.info("Récupération et insertion terminées")

    return results
