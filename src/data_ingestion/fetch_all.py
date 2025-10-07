from .handler_hubeau import HubeauDataHandler
from .handler_meteo import WeatherDataHandler
from producers.solar_producer import SolarProducer
from producers.wind_producer import WindProducer
from producers.hydro_producer import HydroProducer
from data_ingestion import DataCleaner
from config.settings import settings
from .api_config import DATA_FILES
import os
import pandas as pd
import logging
from datetime import date, timedelta

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
            start_date=date(2022, 1, 1),  # À adapter selon vos données
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
