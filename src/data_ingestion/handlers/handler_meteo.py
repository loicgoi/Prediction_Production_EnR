import pandas as pd
import logging
from .etl_supabase import APIDataHandler
from data_ingestion.fetchers.fetch_open_meteo_eolien import (
    get_wind_forecast,
    get_wind_history,
)
from data_ingestion.fetchers.fetch_open_meteo_solaire import (
    get_solar_forecast,
    get_solar_history,
)
from data_ingestion.utils.data_cleaner import DataCleaner


class WeatherDataHandler(APIDataHandler):
    """Gestionnaire pour charger, nettoyer et sauvegarder les données météorologiques."""

    def __init__(self, latitude: float, longitude: float, data_type: str):
        """
        Initialise le gestionnaire de données météorologiques.

        Args:
            latitude (float): Latitude de la localisation.
            longitude (float): Longitude de la localisation.
            data_type (str): Type de données météorologiques ('solar' ou 'wind').
        """
        if data_type not in ["solar", "wind"]:
            raise ValueError("data_type doit être 'solar' ou 'wind'")

        self.data_type = data_type
        self.latitude = latitude
        self.longitude = longitude

        # Définition de la fonction de chargement selon le type de données
        if data_type == "solar":
            loader_function = self._load_solar_data
            table_name = "meteo_solaire"
        else:  # wind
            loader_function = self._load_wind_data
            table_name = "meteo_eolien"

        super().__init__(loader_function=loader_function)
        self.table_name = table_name

    def _load_solar_data(
        self, start_date: str = None, end_date: str = None, forecast: bool = False
    ) -> pd.DataFrame:
        """
        Charge les données solaires.
        """
        try:
            if forecast:
                df = get_solar_forecast(
                    latitude=self.latitude,
                    longitude=self.longitude,
                    start_date=start_date,
                    end_date=end_date,
                )
            else:
                df = get_solar_history(
                    latitude=self.latitude,
                    longitude=self.longitude,
                    start_date=start_date,
                    end_date=end_date,
                )
            return df
        except Exception as e:
            logging.error(f"Erreur lors du chargement des données solaires: {e}")
            return pd.DataFrame()

    def _load_wind_data(
        self, start_date: str = None, end_date: str = None, forecast: bool = False
    ) -> pd.DataFrame:
        """
        Charge les données éoliennes.
        """
        try:
            if forecast:
                df = get_wind_forecast(
                    latitude=self.latitude,
                    longitude=self.longitude,
                    start_date=start_date,
                    end_date=end_date,
                )
            else:
                df = get_wind_history(
                    latitude=self.latitude,
                    longitude=self.longitude,
                    start_date=start_date,
                    end_date=end_date,
                )
            return df
        except Exception as e:
            logging.error(f"Erreur lors du chargement des données éoliennes: {e}")
            return pd.DataFrame()

    def load(
        self, start_date: str = None, end_date: str = None, forecast: bool = False
    ) -> pd.DataFrame:
        """
        Charge les données météorologiques.
        """
        self.df = self.loader_function(
            start_date=start_date, end_date=end_date, forecast=forecast
        )
        return self.df

    def clean(self):
        """Nettoie et prépare le DataFrame pour l'insertion en BDD."""
        if self.df.empty:
            logging.warning("Le DataFrame est vide, aucun nettoyage à faire.")
            return

        # Utiliser le DataCleaner selon le type de données
        if self.data_type == "solar":
            self.df = DataCleaner.clean_solar_data(self.df)
        else:  # wind
            self.df = DataCleaner.clean_wind_data(self.df)

        logging.info(f"Nettoyage terminé. {len(self.df)} enregistrements conservés.")
