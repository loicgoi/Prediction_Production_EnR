import logging
import sys
import os

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    """Lance les prédictions"""
    logger.info("LANCEMENT DES PRÉDICTIONS DE PRODUCTION")
    logger.info("=" * 50)

    try:
        from src.prediction.forecast_predictor import ForecastPredictor

        # Initialiser le prédicteur
        predictor = ForecastPredictor()

        # Vérifier le statut
        logger.info("Vérification du statut...")
        stats = predictor.get_prediction_stats()

        logger.info(f"Données disponibles:")
        logger.info(f"Solaire: {stats['forecast_availability']['solar']} jours")
        logger.info(f"Éolien: {stats['forecast_availability']['wind']} jours")
        logger.info(f"Hydraulique: {stats['forecast_availability']['hydro']} jours")

        logger.info(f"Modèles chargés:")
        for prod, status in stats["models_status"].items():
            emoji = "✅" if status.get("loaded") else "❌"
            logger.info(f"{emoji} {prod}: {status.get('model_type', 'Non chargé')}")

        if not stats["ready_for_prediction"]:
            logger.error("Le système n'est pas prêt pour les prédictions")
            logger.info("Actions recommandées:")
            logger.info("1. Récupérer les données: python main.py data")
            logger.info("2. Entraîner les modèles: python main.py train")
            sys.exit(1)

        # Lancer les prédictions
        logger.info("Lancement des prédictions...")
        results = predictor.predict_all_forecasts()

        # Afficher les résultats
        logger.info("PRÉDICTIONS TERMINÉES AVEC SUCCÈS")
        logger.info("=" * 50)
        logger.info(f"RÉSUMÉ:")
        logger.info(f"Prédictions solaires: {len(results['solar'])} jours")
        logger.info(f"Prédictions éoliennes: {len(results['wind'])} jours")
        logger.info(f"Prédictions hydrauliques: {len(results['hydro'])} jours")
        logger.info(f"Total: {results['summary']['total_predictions']} prédictions")

        # Afficher un exemple pour chaque type
        if results["solar"]:
            first = results["solar"][0]
            logger.info(
                f"Exemple solaire - {first['date']}: {first['prediction_kwh']} kWh"
            )

        if results["wind"]:
            first = results["wind"][0]
            logger.info(
                f"Exemple éolien - {first['date']}: {first['prediction_kwh']} kWh"
            )

        if results["hydro"]:
            first = results["hydro"][0]
            logger.info(
                f"Exemple hydro - {first['date']}: {first['prediction_kwh']} kWh"
            )

        logger.info("=" * 50)
        logger.info("Prédictions terminées avec succès!")

    except Exception as e:
        logger.error(f"ERREUR: {e}")
        logger.info("Vérifiez que:")
        logger.info("- Les modèles sont entraînés (python main.py train)")
        logger.info("- Les données sont disponibles (python main.py data)")
        logger.info("- Les fichiers de modèles existent dans src/models/saved/")
        sys.exit(1)


if __name__ == "__main__":
    main()
