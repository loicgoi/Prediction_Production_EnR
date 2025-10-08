from datetime import date
import pandas as pd
from typing import Dict, Any
import logging

from .base_producer import BaseProducer
from ..data_ingestion.etl_supabase import CSVDataHandler
from ..data_ingestion.data_cleaner import DataCleaner


class EolienProducer(BaseProducer):
    """
    Producteur d'énergie éolienne.
    Gère le chargement, le nettoyage et le calcul de statistiques sur les données de production éolienne.
    """

    def __init__(self, name: str, location: str, nominal_power: float, data_file: str):
        """
        Initialise un producteur éolien.

        Args:
            name (str): Nom du site de production.
            location (str): Localisation du site.
            nominal_power (float): Puissance nominale installée (en kW).
            data_file (str): Chemin du fichier CSV contenant les données éoliennes.
        """
        super().__init__(name, location, nominal_power)
        self.data_file = data_file
        self.data_handler = CSVDataHandler(data_file)
        self.logger = logging.getLogger(__name__)

   
    #  Chargement des données
   
    def load_production_data(self, start_date: date, end_date: date) -> pd.DataFrame:
        """
        Charge et nettoie les données éoliennes entre deux dates.

        Args:
            start_date (date): Date de début.
            end_date (date): Date de fin.

        Returns:
            pd.DataFrame: Données éoliennes nettoyées et filtrées sur la période.
        """
        try:
            # Chargement des données CSV via le handler
            df = self.data_handler.load()

            if df.empty:
                self.logger.warning("Aucune donnée trouvée dans le fichier CSV.")
                return pd.DataFrame()

            # Conversion de la colonne date
            if "time" in df.columns:
                df = df.rename(columns={"time": "date"})

            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            df = df.dropna(subset=["date"])

            # Nettoyage spécifique aux données éoliennes
            df = DataCleaner.clean_production_data(df, "eolien")

            # Filtrage des dates
            df["date"] = df["date"].dt.date
            df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

            self.logger.info(f"{len(df)} lignes chargées pour la période {start_date} → {end_date}")
            return df

        except Exception as e:
            self.logger.error(f"Erreur lors du chargement des données éoliennes : {e}")
            return pd.DataFrame()

   
    #  Calcul des statistiques
   
    def calculate_statistics(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """
        Calcule des statistiques descriptives sur la période donnée.

        Args:
            start_date (date): Date de début.
            end_date (date): Date de fin.

        Returns:
            Dict[str, Any]: Dictionnaire contenant les statistiques de production.
        """
        df = self.load_production_data(start_date, end_date)

        if df.empty:
            self.logger.warning("Aucune donnée disponible pour calculer les statistiques.")
            return {
                "total_production_kwh": 0,
                "average_wind_speed": 0,
                "max_wind_speed": 0,
                "min_wind_speed": 0,
                "average_surface_pressure": 0,
            }

        stats = {}

        # ---- Si la production énergétique est disponible
        if "production_kwh" in df.columns:
            stats["total_production_kwh"] = df["production_kwh"].sum()
            stats["average_daily_production"] = df["production_kwh"].mean()
            stats["max_daily_production"] = df["production_kwh"].max()
            stats["min_daily_production"] = df["production_kwh"].min()

        # ---- Statistiques météorologiques
        if "wind_speed_10m_max" in df.columns:
            stats["average_wind_speed"] = df["wind_speed_10m_max"].mean()
            stats["max_wind_speed"] = df["wind_speed_10m_max"].max()
            stats["min_wind_speed"] = df["wind_speed_10m_max"].min()

        if "surface_pressure_mean" in df.columns:
            stats["average_surface_pressure"] = df["surface_pressure_mean"].mean()

        # ---- Facteur de capacité
        stats["capacity_factor"] = self.get_production_capacity_factor(start_date, end_date)

        return stats
