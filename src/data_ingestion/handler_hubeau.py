import pandas as pd
from .etl_supabase import APIDataHandler
import logging
from .fetch_hubeau import get_hubeau_data
from .data_cleaner import DataCleaner


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
