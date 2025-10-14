import joblib
import pandas as pd
import numpy as np
import os
import logging
from sklearn.preprocessing import StandardScaler


class ModelPredictor:
    def __init__(self, producer_type: str):
        self.producer_type = producer_type
        self.model = None
        self.scaler = None
        self.logger = logging.getLogger(__name__)
        self._load_model()

    def _load_model(self):
        """
        Charge le modèle et le scaler sauvegardés.
        """
        try:
            models_dir = "src/models/saved"

            # Chercher le meilleur modèle sauvegardé
            model_files = [
                f
                for f in os.listdir(models_dir)
                if f.startswith(f"{self.producer_type}_") and f.endswith("_model.pkl")
            ]

            if not model_files:
                raise FileNotFoundError(
                    f"Aucun modèle trouvé pour {self.producer_type}"
                )

            # Prendre le premier modèle trouvé (normalement il n'y en a qu'un de sauvegardé)
            model_path = os.path.join(models_dir, model_files[0])
            self.model = joblib.load(model_path)
            self.logger.info(f"Modèle chargé: {model_files[0]}")

            # Charge le scaler si existant
            scaler_path = os.path.join(models_dir, f"{self.producer_type}_scaler.pkl")
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
                self.logger.info(f"Scaler chargé pour {self.producer_type}")

        except Exception as e:
            self.logger.error(
                f"Erreur de chargement du modèle {self.producer_type}: {e}"
            )
            raise

    def predict(self, features: dict) -> float:
        """
        Prédit la production à partir des features.
        """
        try:
            # Conversion en DataFrame
            feature_df = pd.DataFrame([features])

            self.logger.info(f"Features reçues: {features}")
            self.logger.info(f"Colonnes du DataFrame: {feature_df.columns.tolist()}")

            # Application du scaler si disponible
            if self.scaler:
                feature_df = self.scaler.transform(feature_df)

            # Prédiction
            prediction = self.model.predict(feature_df)[0]

            # Assurer une prédiction positive
            prediction = max(0, prediction)

            self.logger.info(f"Prédiction réussie: {prediction:.2f} kWh")
            return prediction

        except Exception as e:
            self.logger.error(f"Erreur lors de la prédiction: {e}")
            raise
