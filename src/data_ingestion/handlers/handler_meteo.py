import pandas as pd
import logging
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

    def load(
        self, start_date: str = None, end_date: str = None, forecast: bool = False
    ) -> pd.DataFrame:
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