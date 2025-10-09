import pandas as pd
import logging
<<<<<<< HEAD
<<<<<<< HEAD
from src.data_ingestion.fetchers.fetch_open_meteo_eolien import (
    get_wind_forecast,
    get_wind_history,
)
from src.data_ingestion.fetchers.fetch_open_meteo_solaire import (
    get_solar_forecast,
    get_solar_history,
)
from src.data_ingestion.utils.data_cleaner import DataCleaner


class WeatherDataHandler:
    """Gestionnaire pour charger et nettoyer les données météorologiques."""

    def __init__(self, latitude: float, longitude: float, data_type: str):
        if data_type not in ["solar", "wind"]:
            raise ValueError("data_type doit être 'solar' ou 'wind'")

        self.latitude = latitude
        self.longitude = longitude
        self.data_type = data_type
        self.df = pd.DataFrame()
=======
from .etl_supabase import APIDataHandler
from data_ingestion.fetchers.fetch_open_meteo_eolien import (
=======
from src.data_ingestion.fetchers.fetch_open_meteo_eolien import (
>>>>>>> 65ccff1 (refacto code + ajout du main.py fonctionnel)
    get_wind_forecast,
    get_wind_history,
)
from src.data_ingestion.fetchers.fetch_open_meteo_solaire import (
    get_solar_forecast,
    get_solar_history,
)
from src.data_ingestion.utils.data_cleaner import DataCleaner


class WeatherDataHandler:
    """Gestionnaire pour charger et nettoyer les données météorologiques."""

    def __init__(self, latitude: float, longitude: float, data_type: str):
        if data_type not in ["solar", "wind"]:
            raise ValueError("data_type doit être 'solar' ou 'wind'")

        self.latitude = latitude
        self.longitude = longitude
<<<<<<< HEAD

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
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
=======
        self.data_type = data_type
        self.df = pd.DataFrame()
>>>>>>> 65ccff1 (refacto code + ajout du main.py fonctionnel)

    def load(
        self, start_date: str = None, end_date: str = None, forecast: bool = False
    ) -> pd.DataFrame:
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 65ccff1 (refacto code + ajout du main.py fonctionnel)
        """Charge les données météo depuis Open-Meteo."""
        try:
            if self.data_type == "solar":
                if forecast:
                    self.df = get_solar_forecast(self.latitude, self.longitude)
                else:
                    self.df = get_solar_history(
                        self.latitude, self.longitude, start_date, end_date
                    )
            else:  # wind
                if forecast:
                    self.df = get_wind_forecast(self.latitude, self.longitude)
                else:
                    self.df = get_wind_history(
                        self.latitude, self.longitude, start_date, end_date
                    )
<<<<<<< HEAD

            # Nettoyage
            if not self.df.empty:
                if self.data_type == "solar":
                    self.df = DataCleaner.clean_solar_data(self.df)
                else:
                    self.df = DataCleaner.clean_wind_data(self.df)

            logging.info(
                f"Données {self.data_type} chargées: {len(self.df)} enregistrements"
            )
            return self.df

        except Exception as e:
            logging.warning(f"Erreur météo {self.data_type}: {e}")
            return pd.DataFrame()
=======
        """
        Charge les données météorologiques.
        """
        self.df = self.loader_function(
            start_date=start_date, end_date=end_date, forecast=forecast
        )
        return self.df
=======
>>>>>>> 65ccff1 (refacto code + ajout du main.py fonctionnel)

            # Nettoyage
            if not self.df.empty:
                if self.data_type == "solar":
                    self.df = DataCleaner.clean_solar_data(self.df)
                else:
                    self.df = DataCleaner.clean_wind_data(self.df)

            logging.info(
                f"Données {self.data_type} chargées: {len(self.df)} enregistrements"
            )
            return self.df

<<<<<<< HEAD
        logging.info(f"Nettoyage terminé. {len(self.df)} enregistrements conservés.")
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
=======
        except Exception as e:
            logging.warning(f"Erreur météo {self.data_type}: {e}")
            return pd.DataFrame()
>>>>>>> 65ccff1 (refacto code + ajout du main.py fonctionnel)
