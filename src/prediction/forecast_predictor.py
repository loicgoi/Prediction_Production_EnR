import logging
from typing import List, Dict, Any
from datetime import datetime
from .model_predictor import ModelPredictor
from .forecast_service import ForecastService


class ForecastPredictor:
    def __init__(self):
        self.forecast_service = ForecastService()
        self.logger = logging.getLogger(__name__)

    def predict_solar_forecast(self) -> List[Dict[str, Any]]:
        """
        Prédit la production solaire pour tous les jours de prévision
        Returns:
            Liste de prédictions avec date, prediction_kwh et features
        """
        try:
            self.logger.info("Début des prédictions solaires...")

            # Récupérer les prévisions météo
            forecasts = self.forecast_service.get_solar_forecast()

            if not forecasts:
                self.logger.warning("Aucune prévision solaire disponible")
                return []

            # Initialiser le prédicteur
            predictor = ModelPredictor("solar")
            model_info = predictor.get_model_info()

            if not model_info["loaded"]:
                self.logger.error("Modèle solaire non chargé")
                return []

            self.logger.info(f"Modèle solaire chargé: {model_info['model_type']}")

            # Générer les prédictions pour chaque jour
            predictions = []
            successful_predictions = 0

            for forecast in forecasts:
                try:
                    # Extraire les features (sans la date)
                    features = {k: v for k, v in forecast.items() if k != "date"}

                    # Faire la prédiction
                    prediction_kwh = predictor.predict(features)

                    # Créer l'objet de résultat
                    result = {
                        "date": forecast["date"],
                        "prediction_kwh": round(prediction_kwh, 2),
                        "producer_type": "solar",
                        "features": features,
                        "model_type": model_info["model_type"],
                        "timestamp": datetime.now().isoformat(),
                    }

                    predictions.append(result)
                    successful_predictions += 1

                    self.logger.debug(
                        f"Prédiction solaire {forecast['date']}: {prediction_kwh:.2f} kWh"
                    )

                except Exception as e:
                    self.logger.error(
                        f"Erreur prédiction solaire pour {forecast.get('date', 'date inconnue')}: {e}"
                    )
                    continue

            self.logger.info(
                f"Prédictions solaires terminées: {successful_predictions}/{len(forecasts)} réussies"
            )
            return predictions

        except Exception as e:
            self.logger.error(f"Erreur générale prédictions solaires: {e}")
            return []

    def predict_wind_forecast(self) -> List[Dict[str, Any]]:
        """
        Prédit la production éolienne pour tous les jours de prévision
        Returns:
            Liste de prédictions avec date, prediction_kwh et features
        """
        try:
            self.logger.info("Début des prédictions éoliennes...")

            # Récupérer les prévisions météo
            forecasts = self.forecast_service.get_wind_forecast()

            if not forecasts:
                self.logger.warning("Aucune prévision éolienne disponible")
                return []

            # Initialiser le prédicteur
            predictor = ModelPredictor("wind")
            model_info = predictor.get_model_info()

            if not model_info["loaded"]:
                self.logger.error("Modèle éolien non chargé")
                return []

            self.logger.info(f"Modèle éolien chargé: {model_info['model_type']}")

            # Générer les prédictions pour chaque jour
            predictions = []
            successful_predictions = 0

            for forecast in forecasts:
                try:
                    # Extraire les features (sans la date)
                    features = {k: v for k, v in forecast.items() if k != "date"}

                    # Faire la prédiction
                    prediction_kwh = predictor.predict(features)

                    # Créer l'objet de résultat
                    result = {
                        "date": forecast["date"],
                        "prediction_kwh": round(prediction_kwh, 2),
                        "producer_type": "wind",
                        "features": features,
                        "model_type": model_info["model_type"],
                        "timestamp": datetime.now().isoformat(),
                    }

                    predictions.append(result)
                    successful_predictions += 1

                    self.logger.debug(
                        f"Prédiction éolienne {forecast['date']}: {prediction_kwh:.2f} kWh"
                    )

                except Exception as e:
                    self.logger.error(
                        f"Erreur prédiction éolienne pour {forecast.get('date', 'date inconnue')}: {e}"
                    )
                    continue

            self.logger.info(
                f"Prédictions éoliennes terminées: {successful_predictions}/{len(forecasts)} réussies"
            )
            return predictions

        except Exception as e:
            self.logger.error(f"Erreur générale prédictions éoliennes: {e}")
            return []

    def predict_hydro_forecast(self) -> List[Dict[str, Any]]:
        """
        Prédit la production hydraulique pour les données disponibles
        Returns:
            Liste de prédictions avec date, prediction_kwh et features
        """
        try:
            self.logger.info("Début des prédictions hydrauliques...")

            # Récupérer les données hydrauliques
            forecasts = self.forecast_service.get_hydro_forecast()

            if not forecasts:
                self.logger.warning("Aucune donnée hydraulique disponible")
                return []

            # Initialiser le prédicteur
            predictor = ModelPredictor("hydro")
            model_info = predictor.get_model_info()

            if not model_info["loaded"]:
                self.logger.error("Modèle hydraulique non chargé")
                return []

            self.logger.info(f"Modèle hydraulique chargé: {model_info['model_type']}")

            # Générer les prédictions
            predictions = []
            successful_predictions = 0

            for forecast in forecasts:
                try:
                    # Extraire les features (sans la date)
                    features = {k: v for k, v in forecast.items() if k != "date"}

                    # Faire la prédiction
                    prediction_kwh = predictor.predict(features)

                    # Créer l'objet de résultat
                    result = {
                        "date": forecast["date"],
                        "prediction_kwh": round(prediction_kwh, 2),
                        "producer_type": "hydro",
                        "features": features,
                        "model_type": model_info["model_type"],
                        "timestamp": datetime.now().isoformat(),
                    }

                    predictions.append(result)
                    successful_predictions += 1

                    self.logger.debug(
                        f"Prédiction hydraulique {forecast['date']}: {prediction_kwh:.2f} kWh"
                    )

                except Exception as e:
                    self.logger.error(
                        f"Erreur prédiction hydraulique pour {forecast.get('date', 'date inconnue')}: {e}"
                    )
                    continue

            self.logger.info(
                f"Prédictions hydrauliques terminées: {successful_predictions}/{len(forecasts)} réussies"
            )
            return predictions

        except Exception as e:
            self.logger.error(f"Erreur générale prédictions hydrauliques: {e}")
            return []

    def predict_all_forecasts(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Génère les prédictions pour tous les types de producteurs
        Returns:
            Dictionnaire avec les prédictions pour chaque type
        """
        try:
            self.logger.info("Début des prédictions pour tous les producteurs...")

            # Lancer les prédictions en séquentiel (pour éviter les conflits de ressources)
            solar_predictions = self.predict_solar_forecast()
            wind_predictions = self.predict_wind_forecast()
            hydro_predictions = self.predict_hydro_forecast()

            result = {
                "solar": solar_predictions,
                "wind": wind_predictions,
                "hydro": hydro_predictions,
                "summary": {
                    "solar_days": len(solar_predictions),
                    "wind_days": len(wind_predictions),
                    "hydro_days": len(hydro_predictions),
                    "total_predictions": len(solar_predictions)
                    + len(wind_predictions)
                    + len(hydro_predictions),
                    "timestamp": datetime.now().isoformat(),
                },
            }

            self.logger.info(
                f"Prédictions terminées - "
                f"Solaire: {len(solar_predictions)} jours, "
                f"Éolien: {len(wind_predictions)} jours, "
                f"Hydraulique: {len(hydro_predictions)} jours"
            )

            return result

        except Exception as e:
            self.logger.error(f"Erreur générale prédictions tous producteurs: {e}")
            return {
                "solar": [],
                "wind": [],
                "hydro": [],
                "summary": {
                    "solar_days": 0,
                    "wind_days": 0,
                    "hydro_days": 0,
                    "total_predictions": 0,
                    "timestamp": datetime.now().isoformat(),
                    "error": str(e),
                },
            }

    def get_prediction_stats(self) -> Dict[str, Any]:
        """
        Retourne des statistiques sur les prédictions disponibles
        """
        try:
            # Récupérer les prévisions sans faire de prédictions
            forecasts = self.forecast_service.get_all_forecasts()

            # Vérifier la disponibilité des modèles - CORRECTION ICI
            models_status = {}
            for producer_type in ["solar", "wind", "hydro"]:
                try:
                    predictor = ModelPredictor(producer_type)
                    # Vérifier activement que le modèle est chargé
                    if predictor.model is not None:
                        models_status[producer_type] = {
                            "loaded": True,
                            "model_type": type(predictor.model).__name__,
                            "has_scaler": predictor.scaler is not None,
                        }
                    else:
                        models_status[producer_type] = {
                            "loaded": False,
                            "error": "Modèle non initialisé",
                        }
                except Exception as e:
                    models_status[producer_type] = {"loaded": False, "error": str(e)}

            stats = {
                "forecast_availability": {
                    "solar": len(forecasts["solar"]),
                    "wind": len(forecasts["wind"]),
                    "hydro": len(forecasts["hydro"]),
                },
                "models_status": models_status,
                "ready_for_prediction": all(
                    models_status[prod]["loaded"] and len(forecasts[prod]) > 0
                    for prod in ["solar", "wind", "hydro"]
                ),
                "timestamp": datetime.now().isoformat(),
            }

            return stats

        except Exception as e:
            self.logger.error(f"Erreur calcul statistiques prédictions: {e}")
            return {
                "forecast_availability": {"solar": 0, "wind": 0, "hydro": 0},
                "models_status": {},
                "ready_for_prediction": False,
                "error": str(e),
            }
