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

    def _get_expected_features(self) -> list:
        """Retourne les features attendues selon le type de producteur"""
        feature_mapping = {
            "solar": [
                "temperature_2m_mean",
                "shortwave_radiation_sum_kwh_m2",
                "sunshine_duration",
                "cloud_cover_mean",
                "relative_humidity_2m_mean",
            ],
            "wind": [
                "wind_speed_10m_max",
                "wind_gusts_10m_max",
                "wind_direction_10m_dominant",
                "temperature_2m_mean",
            ],
            "hydro": ["debit_l_s"],
        }
        return feature_mapping.get(self.producer_type, [])

    def _validate_features(self, features: dict) -> bool:
        """Valide que toutes les features requises sont présentes"""
        expected_features = self._get_expected_features()
        missing_features = [f for f in expected_features if f not in features]

        if missing_features:
            self.logger.error(f"Features manquantes: {missing_features}")
            self.logger.error(f"Features reçues: {list(features.keys())}")
            self.logger.error(f"Features attendues: {expected_features}")
            return False

        # Validation des types et valeurs
        for feature, value in feature.items():
            if feature in expected_features:
                try:
                    # Conversion en float
                    float_value = float(value)
                    # Validation des valeurs négatives pour certaines features
                    if (
                        feature
                        in [
                            "shortwave_radiation_sum_kwh_m2",
                            "sunshine_duration",
                            "debit_l_s",
                        ]
                        and float_value < 0
                    ):
                        self.logger.warning(
                            f"Valeur négative pour {feature}: {float_value}"
                        )
                except (ValueError, TypeError):
                    self.logger.error(f"Valeur invalide pour {feature}: {value}")
                    return False
        return True

    def _prepare_features_dataframe(self, features: dict) -> pd.DataFrame:
        """
        Prépare le DataFrame avec les features dans le bon ordre
        """
        expected_features = self._get_expected_features()

        # S'assurer que toutes les features sont présentes et dans le bon ordre
        prepared_features = {}
        for feature in expected_features:
            if feature in features:
                prepared_features[feature] = [float(features[feature])]
            else:
                # Si une feature manque (normalement déjà validé), utiliser 0
                self.logger.warning(f"Feature {feature} manquante, utilisation de 0")
                prepared_features[feature] = [0.0]

        return pd.DataFrame(prepared_features)

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

    def get_model_info(self) -> dict:
        """
        Retourne des informations sur le modèle chargé
        """
        if not self.model:
            return {"loaded": False}

        return {
            "loaded": True,
            "producer_type": self.producer_type,
            "model_type": type(self.model).__name__,
            "expected_features": self._get_expected_features(),
            "has_scaler": self.scaler is not None,
        }
