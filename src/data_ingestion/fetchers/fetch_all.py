
import logging
import os
import pandas as pd
from src.data_ingestion.handlers.handler_meteo import WeatherDataHandler
from src.data_ingestion.handlers.handler_hubeau import HubeauDataHandler
from src.data_ingestion.handlers.etl_supabase import SupabaseHandler, DataUploader
from src.data_ingestion.utils.data_cleaner import DataCleaner
from src.config.settings import settings


def manage_forecast_tables(supabase_handler):
    """
    Nettoie COMPLÈTEMENT les tables forecast pour ne garder que les 16 nouveaux jours.
    Les tables history restent intactes pour l'accumulation historique.
    """
    forecast_tables = [
        "raw_solar_forecast",
        "clean_solar_forecast",
        "raw_wind_forecast",
        "clean_wind_forecast",
    ]

    for table in forecast_tables:
        try:
            # Compter le nombre de lignes avant suppression
            count_before = (
                supabase_handler.supabase.table(table)
                .select("date", count="exact")
                .execute()
            )

            # Supprimer TOUTES les données
            supabase_handler.supabase.table(table).delete().gte(
                "date", "1900-01-01"
            ).execute()

            logging.info(
                f"Table {table} vidée ({count_before.count} lignes supprimées.)"
            )

        except Exception as e:
            logging.error(f"Erreur lors du vidage de {table}: {e}.")


def fetch_all(
    latitude: float = None, longitude: float = None, hubeau_station: str = None
):
    """Charge toutes les données, nettoie et les pousse dans Supabase."""

    latitude = latitude or settings.montpellier_latitude
    longitude = longitude or settings.montpellier_longitude
    hubeau_station = hubeau_station or settings.hubeau_station

    logging.info("Début de la récupération des données")

    # Initialiser SupabaseHandler et DataUploader
    supabase_handler = SupabaseHandler()
    data_uploader = DataUploader(supabase_handler)

    # Nettoyage des tables forecast
    logging.info("Nettoyage des tables forecast...")
    manage_forecast_tables(supabase_handler)

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

    # UPLOAD VERS SUPABASE - AVEC SÉPARATION STRICTE RAW/CLEAN
    try:
        # Données météo SOLAIRES
        if not solar_forecast.empty:
            # Données brutes SANS AUCUNE conversion
            solar_forecast_raw = DataCleaner.prepare_solar_data_raw(solar_forecast)
            data_uploader.upload_raw_dataset(solar_forecast_raw, "solar_forecast")
            # Données clean AVEC conversions
            solar_forecast_clean = DataCleaner.clean_solar_data(solar_forecast)
            data_uploader.upload_clean_dataset(solar_forecast_clean, "solar_forecast")

        if not solar_history.empty:
            solar_history_raw = DataCleaner.prepare_solar_data_raw(solar_history)
            data_uploader.upload_raw_dataset(solar_history_raw, "solar_history")
            solar_history_clean = DataCleaner.clean_solar_data(solar_history)
            data_uploader.upload_clean_dataset(solar_history_clean, "solar_history")

        # Données météo ÉOLIENNES
        if not wind_forecast.empty:
            wind_forecast_raw = DataCleaner.prepare_wind_data_raw(wind_forecast)
            data_uploader.upload_raw_dataset(wind_forecast_raw, "wind_forecast")
            wind_forecast_clean = DataCleaner.clean_wind_data(wind_forecast)
            data_uploader.upload_clean_dataset(wind_forecast_clean, "wind_forecast")

        if not wind_history.empty:
            wind_history_raw = DataCleaner.prepare_wind_data_raw(wind_history)
            data_uploader.upload_raw_dataset(wind_history_raw, "wind_history")
            wind_history_clean = DataCleaner.clean_wind_data(wind_history)
            data_uploader.upload_clean_dataset(wind_history_clean, "wind_history")

        # Données Hub'Eau
        if not df_hydro.empty:
            hubeau_raw = DataCleaner.prepare_hydro_data_raw(df_hydro)
            data_uploader.upload_raw_dataset(hubeau_raw, "hubeau")
            hubeau_clean = DataCleaner.clean_hydro_data(df_hydro)
            data_uploader.upload_clean_dataset(hubeau_clean, "hubeau")

        # Données de production
        if not df_solar_prod.empty:
            solar_prod_raw = DataCleaner.prepare_production_data_raw(
                df_solar_prod, "solar"
            )
            data_uploader.upload_raw_dataset(solar_prod_raw, "prod_solaire")
            solar_prod_clean = DataCleaner.clean_production_data(df_solar_prod, "solar")
            data_uploader.upload_clean_dataset(solar_prod_clean, "prod_solaire")

        if not df_wind_prod.empty:
            wind_prod_raw = DataCleaner.prepare_production_data_raw(
                df_wind_prod, "wind"
            )
            data_uploader.upload_raw_dataset(wind_prod_raw, "prod_eolienne")
            wind_prod_clean = DataCleaner.clean_production_data(df_wind_prod, "wind")
            data_uploader.upload_clean_dataset(wind_prod_clean, "prod_eolienne")

        if not df_hydro_prod.empty:
            hydro_prod_raw = DataCleaner.prepare_production_data_raw(
                df_hydro_prod, "hydro"
            )
            data_uploader.upload_raw_dataset(hydro_prod_raw, "prod_hydro")
            hydro_prod_clean = DataCleaner.clean_production_data(df_hydro_prod, "hydro")
            data_uploader.upload_clean_dataset(hydro_prod_clean, "prod_hydro")

    except Exception as e:
        logging.error(f"Erreur lors de l'upload Supabase: {e}")

    # Préparer les données pour le retour
    results = {
        "hubeau": df_hydro,
        "solar_forecast": solar_forecast,
        "solar_history": solar_history,
        "wind_forecast": wind_forecast,
        "wind_history": wind_history,
        "prod_solaire": df_solar_prod,
        "prod_eolienne": df_wind_prod,
        "prod_hydro": df_hydro_prod,
    }

    logging.info("Récupération et insertion terminées")
    return results

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

    # Initialiser SupabaseHandler et DataUploader
    supabase_handler = SupabaseHandler()
    data_uploader = DataUploader(supabase_handler)

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

    # UPLOAD VERS SUPABASE - AVEC SÉPARATION STRICTE RAW/CLEAN
    try:
        # Données météo SOLAIRES
        if not solar_forecast.empty:
            # Données brutes SANS AUCUNE conversion
            solar_forecast_raw = DataCleaner.prepare_solar_data_raw(solar_forecast)
            data_uploader.upload_raw_dataset(solar_forecast_raw, "solar_forecast")
            # Données clean AVEC conversions
            solar_forecast_clean = DataCleaner.clean_solar_data(solar_forecast)
            data_uploader.upload_clean_dataset(solar_forecast_clean, "solar_forecast")

        if not solar_history.empty:
            solar_history_raw = DataCleaner.prepare_solar_data_raw(solar_history)
            data_uploader.upload_raw_dataset(solar_history_raw, "solar_history")
            solar_history_clean = DataCleaner.clean_solar_data(solar_history)
            data_uploader.upload_clean_dataset(solar_history_clean, "solar_history")

        # Données météo ÉOLIENNES
        if not wind_forecast.empty:
            wind_forecast_raw = DataCleaner.prepare_wind_data_raw(wind_forecast)
            data_uploader.upload_raw_dataset(wind_forecast_raw, "wind_forecast")
            wind_forecast_clean = DataCleaner.clean_wind_data(wind_forecast)
            data_uploader.upload_clean_dataset(wind_forecast_clean, "wind_forecast")

        if not wind_history.empty:
            wind_history_raw = DataCleaner.prepare_wind_data_raw(wind_history)
            data_uploader.upload_raw_dataset(wind_history_raw, "wind_history")
            wind_history_clean = DataCleaner.clean_wind_data(wind_history)
            data_uploader.upload_clean_dataset(wind_history_clean, "wind_history")

        # Données Hub'Eau
        if not df_hydro.empty:
            hubeau_raw = DataCleaner.prepare_hydro_data_raw(df_hydro)
            data_uploader.upload_raw_dataset(hubeau_raw, "hubeau")
            hubeau_clean = DataCleaner.clean_hydro_data(df_hydro)
            data_uploader.upload_clean_dataset(hubeau_clean, "hubeau")

        # Données de production
        if not df_solar_prod.empty:
            solar_prod_raw = DataCleaner.prepare_production_data_raw(
                df_solar_prod, "solar"
            )
            data_uploader.upload_raw_dataset(solar_prod_raw, "prod_solaire")
            solar_prod_clean = DataCleaner.clean_production_data(df_solar_prod, "solar")
            data_uploader.upload_clean_dataset(solar_prod_clean, "prod_solaire")

        if not df_wind_prod.empty:
            wind_prod_raw = DataCleaner.prepare_production_data_raw(
                df_wind_prod, "wind"
            )
            data_uploader.upload_raw_dataset(wind_prod_raw, "prod_eolienne")
            wind_prod_clean = DataCleaner.clean_production_data(df_wind_prod, "wind")
            data_uploader.upload_clean_dataset(wind_prod_clean, "prod_eolienne")

        if not df_hydro_prod.empty:
            hydro_prod_raw = DataCleaner.prepare_production_data_raw(
                df_hydro_prod, "hydro"
            )
            data_uploader.upload_raw_dataset(hydro_prod_raw, "prod_hydro")
            hydro_prod_clean = DataCleaner.clean_production_data(df_hydro_prod, "hydro")
            data_uploader.upload_clean_dataset(hydro_prod_clean, "prod_hydro")

    except Exception as e:
        logging.error(f"Erreur lors de l'upload Supabase: {e}")

    # Préparer les données pour le retour
    results = {
        "hubeau": df_hydro,
        "solar_forecast": solar_forecast,
        "solar_history": solar_history,
        "wind_forecast": wind_forecast,
        "wind_history": wind_history,
        "prod_solaire": df_solar_prod,
        "prod_eolienne": df_wind_prod,
        "prod_hydro": df_hydro_prod,
    }



logging.error(f"Erreur lors de l'upload Supabase: {e}")

logging.info("Récupération et insertion terminées")
    return results