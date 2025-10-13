import joblib
import pandas as pd
import numpy as np
import os


class ModelPredictor:
    def __init__(self, producer_type: str):
        self.producer_type = producer_type
        self.model = None
        self.scaler = None
        self._load_model()

    def _load_model(self):
        """
        Charge le modèle et le scaler sauvegardés.
        """

        try:
            # Charge le meilleur modèle (selon les résultats)
            model_path = f"models/saved/{self.producer_type}_xgboost_model.pkl"
            self.model = joblib.load(model_path)

            # Charge le scaler si existant
            scaler_path = f"models/saved/{self.producer_type}_scaler.pkl"
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)

        except Exception as e:
            raise ValueError(
                f"Erreur de chargement du modèle {self.producer_type}: {e}."
            )

    def predict(self, features: dict) -> float:
        """
        Prédit la production à partir des features.
        """
        # Conversion en DataFrame
        feature_df = pd.DataFrame([features])

        # Application du scaler
        if self.scaler:
            feature_df = self.scaler.transform(feature_df)

        # Prédiction
        prediction = self.model.predict(feature_df)[0]

        return max(0, prediction)
