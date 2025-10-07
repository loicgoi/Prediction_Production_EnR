from datetime import date
import pandas as pd
from typing import Dict, Any
from .base_producer import BaseProducer
<<<<<<< HEAD
from src.data_ingestion.utils.data_cleaner import DataCleaner
=======
from ..data_ingestion.etl_supabase import CSVDataHandler
from ..data_ingestion.data_cleaner import DataCleaner
>>>>>>> cbfd918 (Refacto de tout le code existant pour harmonisation et que tout soit fonctionnel)


class HydroProducer(BaseProducer):
    """
    Producteur d'énergie hydraulique.
    """

    def __init__(self, name: str, location: str, nominal_power: float, data_file: str):
        """
        Initialise un producteur hydraulique.
        """
        super().__init__(name, location, nominal_power)
        self.data_file = data_file
<<<<<<< HEAD
=======
        self.data_handler = CSVDataHandler(data_file)
>>>>>>> cbfd918 (Refacto de tout le code existant pour harmonisation et que tout soit fonctionnel)

    def load_production_data(self, start_date: date, end_date: date) -> pd.DataFrame:
        """
        Charge les données de production hydraulique entre deux dates.
        """
        try:
<<<<<<< HEAD
            # Charger directement avec pandas
            df = pd.read_csv(self.data_file)
=======
            df = self.data_handler.load()
>>>>>>> cbfd918 (Refacto de tout le code existant pour harmonisation et que tout soit fonctionnel)

            # Nettoyage spécifique aux données de production hydraulique
            df = DataCleaner.clean_production_data(df, "hydro")

            # Filtrer par date
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"]).dt.date
                filtered_df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
                return filtered_df

            return df

        except Exception as e:
            self.logger.error(
                f"Erreur lors du chargement des données de production hydraulique: {e}"
            )
            return pd.DataFrame()

    def calculate_statistics(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """
        Calcule des statistiques sur la production hydraulique pour une période donnée.
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
