from abc import ABC, abstractmethod
from datetime import date, datetime
import pandas as pd
from typing import Dict, Any, Optional, Tuple
import logging


class BaseProducer(ABC):
    """Classe abstraite pour tous les producteurs d'énergie."""

    def __init__(self, name: str, location: str, nominal_power: float):
        """Initialise un producteur d'énergie.

        Args:
            name (str): Nom du producteur
            location (str): Localisation du producteur
            nominal_power (float): Puissance nominale en KW
        """
        self.name = name
        self.location = location
        self.nominal_power = nominal_power
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def load_production_data(self, start_date: date, end_date: date) -> pd.DataFrame:
        """Charge les données de production entre deux dates.

        Args:
            start_date (date): Date de début
            end_date (date): Date de fin

        Returns:
            pd.DataFrame: DataFrame avec les données de production
        """
        pass

    @abstractmethod
    def calculate_statistics(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """Calcule des statistiques sur la production pour une période donnée.

        Args:
            start_date (date): Date de début
            end_date (date): Date de fin

        Returns:
            Dict[str, Any]: Dictionnaire avec les statistiques calculées
        """
        pass

    def get_production_capacity_factor(self, start_date: date, end_date: date) -> float:
        """Calcule le facteur de capacité du producteur pour une période donnée.

        Args:
            start_date (date): Date de début
            end_date (date): Date de fin

        Returns:
            float: Facteur de capacité (ratio entre production réelle et production maximale)
        """
        df = self.load_production_data(start_date, end_date)
        if df.empty or "production_kwh" not in df.columns:
            return 0.0

        total_production = df["production_kwh"].sum()
        days = (end_date - start_date).days + 1
        max_possible_production = self.nominal_power * 24 * days

        return (
            total_production / max_possible_production
            if max_possible_production > 0
            else 0.0
        )
