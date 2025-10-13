import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import joblib
import logging
import os
from .data_loarder import SupabaseDataLoader
from .model_config import MODEL_CONFIG


class RenewableModelTrainer:
    def __init__(self, producer_type: str):
        self.producer_type = producer_type
        self.data_loader = SupabaseDataLoader()
        self.config = MODEL_CONFIG[producer_type]
        self.models = {}
        self.scalers = {}
        self.logger = logging.getLogger(__name__)

    def prepare_features(self, df: pd.DataFrame) -> tuple:
        """
        Prépare les features et la target.
        """

        features = self.config["features"]
        target = self.config["target"]

        # Vérifie que les colonnes existent
        missing_features = [f for f in features if f not in df.columns]
        if missing_features:
            self.logger.warning(f"Features manquantes: {missing_features}.")
            features = [f for f in features if f in df.columns]

        if target not in df.columns:
            raise ValueError(f"Target {target} non trouvées dans les données.")

        X = df[features].copy()
        y = df[target].copy()

        # Gestion des valeurs manquantes
        X = X.fillna(X.mean())
        y = y.fillna(0)

        return X, y

    def train_models(self, test_size: float = 0.2) -> dict:
        """
        Entraine les modèles.
        """

        # Chargement des données
        df = self.data_loader.load_training_data(self.producer_type)
        if df.empty:
            raise ValueError(f"Aucune donnée trouvée pour {self.producer_type}.")

        X, y = self.prepare_features(df)

        # Split Train/Test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )

        # Standardisation des données
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        self.scalers["standard"] = scaler

        results = {}

        # Entrainement Ridge
        self.logger.info("Entrainement Ridge...")
        ridge_model = Ridge(**self.config["models"]["ridge"])
        ridge_model.fit(X_train_scaled, y_train)
        self.models["ridge"] = ridge_model

        # Evaluation Ridge
        y_pred_ridge = ridge_model.predict(X_test_scaled)
        results["ridge"] = self._evaluate_model(y_test, y_pred_ridge)

        # Entraînement XGBoost
        self.logger.info("Entraînement XGBoost...")
        xgb_model = xgb.XGBRegressor(**self.config["models"]["xgboost"])
        xgb_model.fit(X_train_scaled, y_train)
        self.models["xgboost"] = xgb_model

        # Évaluation XGBoost
        y_pred_xgb = xgb_model.predict(X_test_scaled)
        results["xgboost"] = self._evaluate_model(y_test, y_pred_xgb)

        # Entraînement Random Forest
        self.logger.info("Entraînement Random Forest...")
        rf_model = RandomForestRegressor(**self.config["models"]["random_forest"])
        rf_model.fit(X_train, y_train)  # RF moins sensible à la normalisation
        self.models["random_forest"] = rf_model

        # Évaluation Random Forest
        y_pred_rf = rf_model.predict(X_test)
        results["random_forest"] = self._evaluate_model(y_test, y_pred_rf)

        # Sauvegarde du meilleur modèle
        best_model_name = min(results, key=lambda x: results[x]["mae"])
        self._save_best_model(best_model_name)

        return results

    def _evaluate_model(self, y_true: pd.Series, y_pred: np.ndarray) -> dict:
        """
        Evalue les performances du modèle.
        """
        return {
            "mae": mean_absolute_error(y_true, y_pred),
            "mse": mean_squared_error(y_true, y_pred),
            "rmse": np.sqrt(mean_squared_error(y_true, y_pred)),
            "r2": r2_score(y_true, y_pred),
        }

    def _save_best_model(self, model_name: str):
        """
        Sauvegarde le meilleur modèle et son scaler.
        """
        model = self.models[model_name]
        scaler = self.scalers.get("standard")

        # Sauvegarde modèle
        model_path = f"src/models/saved/{self.producer_type}_{model_name}_model.pkl"
        joblib.dump(model, model_path)
        logging.info(f"Modèle '{model}' sauvegardé !")

        # Sauvegarde scaler
        if scaler:
            scaler_path = f"src/models/saved/{self.producer_type}_scaler.pkl"
            joblib.dump(scaler, scaler_path)

        self.logger.info(f"Meilleur modèle sauvegardé: {model_path}.")
