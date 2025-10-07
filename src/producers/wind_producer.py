from datetime import date
import pandas as pd
from typing import Dict, Any
from .base_producer import BaseProducer
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from src.data_ingestion.utils.data_cleaner import DataCleaner
=======
from ..data_ingestion.etl_supabase import CSVDataHandler
from ..data_ingestion.data_cleaner import DataCleaner
>>>>>>> cbfd918 (Refacto de tout le code existant pour harmonisation et que tout soit fonctionnel)
=======
from data_ingestion.handlers.etl_supabase import CSVDataHandler
from data_ingestion.utils.data_cleaner import DataCleaner
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
=======
from data_ingestion.handlers.etl_supabase import CSVDataHandler
from data_ingestion.utils.data_cleaner import DataCleaner
=======
from ..data_ingestion.etl_supabase import CSVDataHandler
from ..data_ingestion.data_cleaner import DataCleaner
>>>>>>> 0889286 (Refacto de tout le code existant pour harmonisation et que tout soit fonctionnel)
>>>>>>> f4c8067 (Refacto de tout le code existant pour harmonisation et que tout soit fonctionnel)


class WindProducer(BaseProducer):
    """
    Producteur d'énergie éolienne.
    """

    def __init__(self, name: str, location: str, nominal_power: float, data_file: str):
        """
        Initialise un producteur éolien.
        """
        super().__init__(name, location, nominal_power)
        self.data_file = data_file
<<<<<<< HEAD
=======
        self.data_handler = CSVDataHandler(data_file)
>>>>>>> cbfd918 (Refacto de tout le code existant pour harmonisation et que tout soit fonctionnel)

    def load_production_data(self, start_date: date, end_date: date) -> pd.DataFrame:
        """
        Charge les données de production éolienne entre deux dates.
        """
        try:
<<<<<<< HEAD
            # Charger directement avec pandas
            df = pd.read_csv(self.data_file)
=======
            df = self.data_handler.load()
>>>>>>> cbfd918 (Refacto de tout le code existant pour harmonisation et que tout soit fonctionnel)

            # Nettoyage spécifique aux données de production éolienne
            df = DataCleaner.clean_production_data(df, "wind")

            # Filtrer par date
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"]).dt.date
                filtered_df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
                return filtered_df

            return df

        except Exception as e:
            self.logger.error(
                f"Erreur lors du chargement des données de production éolienne: {e}"
            )
            return pd.DataFrame()

    def calculate_statistics(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """
        Calcule des statistiques sur la production éolienne pour une période donnée.
        """
        df = self.load_production_data(start_date, end_date)

        if df.empty or "production_kwh" not in df.columns:
            return {
                "total_production": 0,
                "average_daily_production": 0,
                "max_daily_production": 0,
                "min_daily_production": 0,
                "capacity_factor": 0.0,
            }

        total_production = df["production_kwh"].sum()
        days = (end_date - start_date).days + 1
        average_daily_production = total_production / days
        max_daily_production = df["production_kwh"].max()
        min_daily_production = df["production_kwh"].min()
        capacity_factor = self.get_production_capacity_factor(start_date, end_date)

        return {
            "total_production": total_production,
            "average_daily_production": average_daily_production,
            "max_daily_production": max_daily_production,
            "min_daily_production": min_daily_production,
            "capacity_factor": capacity_factor,
        }
