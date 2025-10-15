import logging
import pandas as pd
from src.data_ingestion.utils.data_cleaner import DataCleaner
from src.data_ingestion.fetchers.fetch_hubeau import get_hubeau_data


class HubeauDataHandler:
    """Handler pour données Hub'Eau."""

    def __init__(self, code_station: str, start_date=None, end_date=None):
        self.code_station = code_station
        self.start_date = start_date
        self.end_date = end_date
        self.df = pd.DataFrame()

    def load(self):
        try:
            self.df = get_hubeau_data(self.code_station, self.start_date, self.end_date)
            logging.info(f"{len(self.df)} enregistrements Hub'Eau chargés")
        except Exception as e:
            logging.error(f"Erreur Hub'Eau: {e}")
        return self.df

    def clean(self):
        if self.df.empty:
            return
        self.df = DataCleaner.clean_hydro_data(self.df)
        logging.info(f"Nettoyage terminé Hub'Eau: {len(self.df)} enregistrements")