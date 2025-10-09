import logging
from src.data_ingestion.fetchers.fetch_all import fetch_all

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    logging.info("Démarrage du pipeline de données")

    try:
        # Récupération de toutes les données
        results = fetch_all()

        # Log des résultats
        for key, df in results.items():
            if hasattr(df, "shape"):  # C'est un DataFrame
                logging.info(f"{key}: {len(df)} enregistrements récupérés")
            else:
                logging.info(f"{key}: Données récupérées")

        logging.info("Pipeline terminé avec succès !")

    except Exception as e:
        logging.error(f"Erreur lors de l'exécution du pipeline: {e}")
        raise


if __name__ == "__main__":
    main()
