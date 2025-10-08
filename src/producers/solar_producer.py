<<<<<<< HEAD
import pandas as pd
from .base_producer import BaseProducer
<<<<<<< HEAD
from src.data_ingestion.utils.data_cleaner import DataCleaner
=======
from data_ingestion.handlers.etl_supabase import CSVDataHandler
from data_ingestion.utils.data_cleaner import DataCleaner
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
from datetime import date
from typing import Dict, Any
=======
from datetime import date
import pandas as pd
from typing import Dict, Any
from .base_producer import BaseProducer
from ..data_ingestion.etl_supabase import CSVDataHandler
from ..data_ingestion.data_cleaner import DataCleaner
>>>>>>> cbfd918 (Refacto de tout le code existant pour harmonisation et que tout soit fonctionnel)


class SolarProducer(BaseProducer):
    """
    Producteur d'énergie solaire.
    """

    def __init__(self, name: str, location: str, nominal_power: float, data_file: str):
        """
        Initialise un producteur solaire.
<<<<<<< HEAD

        Args:
            name (str): Nom du producteur
            location (str): Localisation du producteur
            nominal_power (float): Puissance nominale en KWc
            data_file (str): Chemin vers le fichier de données de production
        """
        super().__init__(name, location, nominal_power)
        self.data_file = data_file

    def load_production_data(self, start_date: date, end_date: date) -> pd.DataFrame:
        """
        Charge les données solaires depuis un CSV

        Args:
            start_date (date): Date de début
            end_date (date): Date de fin

        Returns:
            pd.DataFrame: DataFrame avec les données de production solaire
        """
        try:
            # Charger directement avec pandas
            df = pd.read_csv(self.data_file)

            # Nettoyage spécifique au données solaires
            df = DataCleaner.clean_production_data(df, "solar")

=======
        """
        super().__init__(name, location, nominal_power)
        self.data_file = data_file
        self.data_handler = CSVDataHandler(data_file)

    def load_production_data(self, start_date: date, end_date: date) -> pd.DataFrame:
        """
        Charge les données de production solaire entre deux dates.
        """
        try:
            df = self.data_handler.load()

            # Nettoyage spécifique aux données de production solaire
            df = DataCleaner.clean_production_data(df, "solar")

            # Filtrer par date
>>>>>>> cbfd918 (Refacto de tout le code existant pour harmonisation et que tout soit fonctionnel)
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"]).dt.date
                filtered_df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
                return filtered_df

            return df

        except Exception as e:
            self.logger.error(
<<<<<<< HEAD
                f"Erreur lors du chargement des données de production solaire: {e}."
=======
                f"Erreur lors du chargement des données de production solaire: {e}"
>>>>>>> cbfd918 (Refacto de tout le code existant pour harmonisation et que tout soit fonctionnel)
            )
            return pd.DataFrame()

    def calculate_statistics(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """
        Calcule des statistiques sur la production solaire pour une période donnée.
<<<<<<< HEAD

        Args:
            start_date (date): Date de début
            end_date (date): Date de fin

        Returns:
            Dict[str, Any]: Dictionnaire avec les statistiques calculées
        """

=======
        """
>>>>>>> cbfd918 (Refacto de tout le code existant pour harmonisation et que tout soit fonctionnel)
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
