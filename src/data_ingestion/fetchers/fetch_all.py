<<<<<<< HEAD
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
=======
<<<<<<<< HEAD:src/data_ingestion/fetch_all.py
from .handler_hubeau import HubeauDataHandler
from .handler_meteo import WeatherDataHandler
from ..producers.solar_producer import SolarProducer
from ..producers.wind_producer import WindProducer
from ..producers.hydro_producer import HydroProducer
from ..data_ingestion import DataCleaner
from ..config.settings import settings
from .api_config import DATA_FILES
========
>>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels):src/data_ingestion/fetchers/fetch_all.py
import os
import pandas as pd
import logging
from datetime import date, timedelta

from data_ingestion.handlers.handler_hubeau import HubeauDataHandler
from data_ingestion.handlers.handler_meteo import WeatherDataHandler
from src.config.settings import settings
from data_ingestion.api.api_config import DATA_FILES

from producers.solar_producer import SolarProducer
from producers.wind_producer import WindProducer
from producers.hydro_producer import HydroProducer

RAW_DATA_PATH = "data/raw"


def fetch_all():
    """
    Récupère toutes les données nécessaires pour le projet en utilisant les Producers.
    """
    os.makedirs(RAW_DATA_PATH, exist_ok=True)
    logging.info("Début de la récupération des données")

    # 1. Données hydrométriques (Hub'Eau)
    try:
        hubeau_handler = HubeauDataHandler(
            code_station=settings.hubeau_station,
            start_date="2022-07-01",
            end_date=date.today().strftime("%Y-%m-%d"),
        )

        df_hydro = hubeau_handler.load()
        hubeau_handler.clean()
        df_hydro.to_csv(os.path.join(RAW_DATA_PATH, "data_hubeau.csv"), index=False)
        hubeau_handler.save_to_db("hydro_data")
        logging.info("Données hydrométriques sauvegardées.")

    except Exception as e:
        logging.warning(f"Erreur Hub'Eau : {e}")
        df_hydro = pd.DataFrame()

    # 2. Données météorologiques
    start_date = (date.today() - timedelta(days=365)).strftime("%Y-%m-%d")
    end_date = date.today().strftime("%Y-%m-%d")

    # Météo solaire
    try:
        solar_weather_handler = WeatherDataHandler(
            latitude=settings.montpellier_latitude,
            longitude=settings.montpellier_longitude,
            data_type="solar",
        )

        # Historique
        df_solar_history = solar_weather_handler.load(
            start_date=start_date, end_date=end_date, forecast=False
        )
        if not df_solar_history.empty:
            solar_weather_handler.clean()
            df_solar_history.to_csv(
                os.path.join(RAW_DATA_PATH, "data_solar_history.csv"), index=False
            )
            solar_weather_handler.save_to_db("meteo_solaire")
            logging.info("Données météorologiques solaires historiques sauvegardées.")

        # Prévision
        df_solar_forecast = solar_weather_handler.load(forecast=True)
        if not df_solar_forecast.empty:
            solar_weather_handler.clean()
            df_solar_forecast.to_csv(
                os.path.join(RAW_DATA_PATH, "data_solar_forecast.csv"), index=False
            )
            logging.info("Données météorologiques solaires de prévision sauvegardées.")

    except Exception as e:
        logging.warning(f"Erreur météo solaire : {e}")
        df_solar_forecast, df_solar_history = pd.DataFrame(), pd.DataFrame()

    # Météo éolienne
    try:
        wind_weather_handler = WeatherDataHandler(
            latitude=settings.montpellier_latitude,
            longitude=settings.montpellier_longitude,
            data_type="wind",
        )

        # Historique
        df_wind_history = wind_weather_handler.load(
            start_date=start_date, end_date=end_date, forecast=False
        )
        if not df_wind_history.empty:
            wind_weather_handler.clean()
            df_wind_history.to_csv(
                os.path.join(RAW_DATA_PATH, "data_wind_history.csv"), index=False
            )
            wind_weather_handler.save_to_db("meteo_eolien")
            logging.info("Données météorologiques éoliennes historiques sauvegardées.")

        # Prévision
        df_wind_forecast = wind_weather_handler.load(forecast=True)
        if not df_wind_forecast.empty:
            wind_weather_handler.clean()
            df_wind_forecast.to_csv(
                os.path.join(RAW_DATA_PATH, "data_wind_forecast.csv"), index=False
            )
            logging.info("Données météorologiques éoliennes de prévision sauvegardées.")

    except Exception as e:
        logging.warning(f"Erreur météo éolien : {e}")
        df_wind_forecast, df_wind_history = pd.DataFrame(), pd.DataFrame()

    # 3. Données de production via les Producers
    production_data = {}

    # Producteur Solaire
    try:
        solar_producer = SolarProducer(
            name="Parc solaire de Montpellier",
            location="Montpellier",
            nominal_power=settings.solar_nominal_power,
            data_file=DATA_FILES["solar"],
        )
        df_solar_production = solar_producer.load_production_data(
            start_date=date(2022, 1, 1),
            end_date=date.today(),
        )
        production_data["solar"] = df_solar_production
        logging.info("Données de production solaire chargées via SolarProducer.")

    except Exception as e:
        logging.warning(f"Erreur production solaire : {e}")
        production_data["solar"] = pd.DataFrame()

    # Producteur Éolien
    try:
        wind_producer = WindProducer(
            name="Éolienne particulière de Montpellier",
            location="Montpellier",
            nominal_power=settings.wind_nominal_power,
            data_file=DATA_FILES["wind"],
        )
        df_wind_production = wind_producer.load_production_data(
            start_date=date(2022, 1, 1), end_date=date.today()
        )
        production_data["wind"] = df_wind_production
        logging.info("Données de production éolienne chargées via WindProducer.")

    except Exception as e:
        logging.warning(f"Erreur production éolienne : {e}")
        production_data["wind"] = pd.DataFrame()

    # Producteur Hydraulique
    try:
        hydro_producer = HydroProducer(
            name="Centrale hydro-électrique de Montpellier",
            location="Montpellier",
            nominal_power=settings.hydro_nominal_power,
            data_file=DATA_FILES["hydro"],
        )
        df_hydro_production = hydro_producer.load_production_data(
            start_date=date(2022, 1, 1), end_date=date.today()
        )
        production_data["hydro"] = df_hydro_production
        logging.info("Données de production hydraulique chargées via HydroProducer.")

    except Exception as e:
        logging.warning(f"Erreur production hydraulique : {e}")
        production_data["hydro"] = pd.DataFrame()

    return (
        df_hydro,
        df_solar_forecast,
        df_solar_history,
        df_wind_forecast,
        df_wind_history,
        production_data["solar"],
        production_data["wind"],
        production_data["hydro"],
    )


def fetch_weather_data(
    latitude,
    longitude,
    start_date=None,
    end_date=None,
    data_type="solar",
    forecast=False,
):
    """
    Récupère les données météorologiques pour une localisation et une période données.
    """
    try:
        weather_handler = WeatherDataHandler(
            latitude=latitude, longitude=longitude, data_type=data_type
        )

        df = weather_handler.load(
            start_date=start_date, end_date=end_date, forecast=forecast
        )

        if not df.empty:
            weather_handler.clean()

        return df
    except Exception as e:
        logging.error(
            f"Erreur lors de la récupération des données météorologiques {data_type}: {e}"
        )
        return pd.DataFrame()
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
