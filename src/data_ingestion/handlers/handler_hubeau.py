<<<<<<< HEAD
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
=======
import pandas as pd
import logging

from data_ingestion.fetchers.fetch_hubeau import get_hubeau_data
from data_ingestion.utils.data_cleaner import DataCleaner
from .etl_supabase import APIDataHandler


class HubeauDataHandler(APIDataHandler):
    """Gestionnaire pour charger, nettoyer et sauvegarder les données hydrométriques."""

    def __init__(self, code_station: str, start_date: str, end_date: str):
        """
        Initialise le gestionnaire de données Hubeau.
        """
        super().__init__(
            loader_function=get_hubeau_data,
            code_station=code_station,
            start_date=start_date,
            end_date=end_date,
        )
        self.code_station = code_station
        self.table_name = "hydro_data"

    def clean(self):
        """Nettoie et prépare le DataFrame pour l'insertion en BDD."""
        if self.df.empty:
            logging.warning("Le DataFrame est vide, aucun nettoyage à faire.")
            return

        self.df = DataCleaner.clean_hydro_data(self.df)
        logging.info(f"Nettoyage terminé. {len(self.df)} enregistrements conservés.")
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
