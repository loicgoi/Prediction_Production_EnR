import logging
import sys
import os
from datetime import datetime, date

# Ajouter le répertoire src au path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from src.data_ingestion.fetchers.fetch_all import fetch_all
from src.config.settings import settings

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            f'logs/daily_fetch_{datetime.now().strftime("%Y%m%d")}.log'
        ),
        logging.StreamHandler(sys.stdout),
    ],
)


def main():
    """Fonction principale du script quotidien."""
    logging.info("Démarrage de la récupération quotidienne des données")

    try:
        # Récupération de toutes les données
        results = fetch_all()

        # Log des résultats
        for key, df in results.items():
            if hasattr(df, "shape"):  # C'est un DataFrame
                logging.info(f"{key}: {len(df)} enregistrements récupérés")
            else:
                logging.info(f"{key}: Données récupérées")

        logging.info("Récupération quotidienne terminée avec succès")

    except Exception as e:
        logging.error(f"Erreur lors de la récupération: {e}")
        sys.exit(1)
