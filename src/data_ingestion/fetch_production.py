import pandas as pd
import logging
from ..producers.solar_producer import SolarProducer
from ..producers.wind_producer import WindProducer
from ..producers.hydro_producer import HydroProducer
from .api_config import DATA_FILES
from ..config.settings import settings


def fetch_production_data(producer_type: str, start_date=None, end_date=None):
    """
    Récupère les données de production pour un type de producteur donné.

    Args:
        producer_type (str): Type de producteur ('solar', 'wind' ou 'hydro')
        start_date: Date de début (optionnel)
        end_date: Date de fin (optionnel)

    Returns:
        pd.DataFrame: DataFrame avec les données de production
    """
    try:
        if producer_type not in DATA_FILES:
            raise ValueError(f"Type de producteur invalide: {producer_type}")

        # Configuration des producteurs
        producers_config = {
            "solar": {
                "name": "Parc solaire de Montpellier",
                "location": "Montpellier",
                "nominal_power": settings.solar_nominal_power,
                "class": SolarProducer,
            },
            "wind": {
                "name": "Éolienne particulière de Montpellier",
                "location": "Montpellier",
                "nominal_power": settings.wind_nominal_power,
                "class": WindProducer,
            },
            "hydro": {
                "name": "Centrale hydro-électrique de Montpellier",
                "location": "Montpellier",
                "nominal_power": settings.hydro_nominal_power,
                "class": HydroProducer,
            },
        }

        config = producers_config[producer_type]
        producer = config["class"](
            name=config["name"],
            location=config["location"],
            nominal_power=config["nominal_power"],
            data_file=DATA_FILES[producer_type],
        )

        # Définir les dates par défaut si non spécifiées
        if start_date is None:
            start_date = pd.Timestamp("2022-01-01").date()
        if end_date is None:
            end_date = pd.Timestamp.today().date()

        df = producer.load_production_data(start_date, end_date)
        return df

    except Exception as e:
        logging.error(
            f"Erreur lors de la récupération des données de production {producer_type}: {e}"
        )
        return pd.DataFrame()
