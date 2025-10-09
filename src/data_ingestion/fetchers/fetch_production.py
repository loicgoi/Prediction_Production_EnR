import pandas as pd
import logging
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 65ccff1 (refacto code + ajout du main.py fonctionnel)
from src.producers.solar_producer import SolarProducer
from src.producers.wind_producer import WindProducer
from src.producers.hydro_producer import HydroProducer
from src.data_ingestion.api.api_config import DATA_FILES
<<<<<<< HEAD
from src.config.settings import settings
=======
<<<<<<<< HEAD:src/data_ingestion/fetch_production.py
from ..producers.solar_producer import SolarProducer
from ..producers.wind_producer import WindProducer
from ..producers.hydro_producer import HydroProducer
from .api_config import DATA_FILES
from ..config.settings import settings
========
from producers.solar_producer import SolarProducer
from producers.wind_producer import WindProducer
from producers.hydro_producer import HydroProducer
from data_ingestion.api.api_config import DATA_FILES
=======
>>>>>>> 65ccff1 (refacto code + ajout du main.py fonctionnel)
from src.config.settings import settings
>>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels):src/data_ingestion/fetchers/fetch_production.py
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)


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
<<<<<<< HEAD
    # Validation du type de producteur
    if producer_type not in DATA_FILES:
        # On lève explicitement une erreur (ne sera pas capturée plus bas)
        raise ValueError(f"Type de producteur invalide: {producer_type}")

    try:
=======
    try:
        if producer_type not in DATA_FILES:
            raise ValueError(f"Type de producteur invalide: {producer_type}")

>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
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
<<<<<<< HEAD

        # Instanciation du producteur
=======
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
        producer = config["class"](
            name=config["name"],
            location=config["location"],
            nominal_power=config["nominal_power"],
            data_file=DATA_FILES[producer_type],
        )

<<<<<<< HEAD
        # Gestion des dates par défaut
=======
        # Définir les dates par défaut si non spécifiées
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
        if start_date is None:
            start_date = pd.Timestamp("2022-01-01").date()
        if end_date is None:
            end_date = pd.Timestamp.today().date()

<<<<<<< HEAD
        # Chargement des données de production
        df = producer.load_production_data(start_date, end_date)
        return df

    except ValueError:
        # On laisse remonter les ValueError pour que pytest les détecte
        raise

    except Exception as e:
        # Autres erreurs → journalisation et retour d’un DataFrame vide
=======
        df = producer.load_production_data(start_date, end_date)
        return df

    except Exception as e:
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
        logging.error(
            f"Erreur lors de la récupération des données de production {producer_type}: {e}"
        )
        return pd.DataFrame()
