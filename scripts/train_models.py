import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.model_trainer import RenewableModelTrainer


def main():
    """
    Entraine les modèles pour les 3 types de producteurs.
    """

    producers = ["solar", "wind", "hydro"]

    for producer in producers:
        try:
            logging.info(f"*entrainement du modèle {producer}...")

            trainer = RenewableModelTrainer(producer)
            results = trainer.train_models()

            logging.info(f"Résultats {producer}.")
            for model_name, metrics in results.items():
                logging.info(
                    f"{model_name}: MAE={metrics['mae']:.3f}, R²={metrics['r2']:.3f}."
                )

        except Exception as e:
            logging.error(f"Erreur lors de l'entrainement {producer}: {e}.")
            continue


if __name__ == "__main__":
    #  créer le dossier models s'il n'existe pas.
    os.makedirs("src/models/saved", exist_ok=True)
    main()
