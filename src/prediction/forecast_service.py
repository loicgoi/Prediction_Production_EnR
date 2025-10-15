import pandas as pd
from supabase import create_client
from typing import List, Dict, Any
import logging
from src.config.settings import settings


class ForecastService:
    def __init__(self):
        self.supabase = create_client(settings.supabase_url, settings.supabase_key)
        self.logger = logging.getLogger(__name__)

    def get_solar_forecast(self) -> List[Dict[str, Any]]:
        """
        Récupère les prévisions solaires depuis la table clean_solar_forecast
        Returns:
            Liste de dictionnaires avec les features pour la prédiction solaire
        """
        try:
            self.logger.info("Récupération des prévisions solaires...")

            response = (
                self.supabase.table("clean_solar_forecast")
                .select(
                    "date, temperature_2m_mean, shortwave_radiation_sum_kwh_m2, sunshine_duration, cloud_cover_mean, relative_humidity_2m_mean"
                )
                .order("date")
                .execute()
            )

            forecasts = response.data
            self.logger.info(f"Récupéré {len(forecasts)} prévisions solaires")

            # Validation et nettoyage des données
            valid_forecasts = []
            for forecast in forecasts:
                cleaned_forecast = self._clean_solar_forecast(forecast)
                if cleaned_forecast:
                    valid_forecasts.append(cleaned_forecast)

            self.logger.info(
                f"{len(valid_forecasts)} prévisions solaires valides après nettoyage"
            )
            return valid_forecasts

        except Exception as e:
            self.logger.error(f"Erreur récupération prévisions solaires: {e}")
            return []

    def _clean_solar_forecast(self, forecast: Dict[str, Any]) -> Dict[str, Any]:
        """
        Nettoie et valide une prévision solaire
        """
        try:
            # Vérifier que toutes les features requises sont présentes
            required_features = [
                "temperature_2m_mean",
                "shortwave_radiation_sum_kwh_m2",
                "sunshine_duration",
                "cloud_cover_mean",
                "relative_humidity_2m_mean",
            ]

            # Vérifier la présence des features
            for feature in required_features:
                if feature not in forecast or forecast[feature] is None:
                    self.logger.warning(
                        f"Feature {feature} manquante dans la prévision solaire du {forecast.get('date', 'date inconnue')}"
                    )
                    return None

            # Convertir les types et valider les valeurs
            cleaned = {
                "date": forecast["date"],
                "temperature_2m_mean": float(forecast["temperature_2m_mean"]),
                "shortwave_radiation_sum_kwh_m2": max(
                    0, float(forecast["shortwave_radiation_sum_kwh_m2"])
                ),
                "sunshine_duration": max(0, float(forecast["sunshine_duration"])),
                "cloud_cover_mean": max(
                    0, min(100, float(forecast["cloud_cover_mean"]))
                ),  # 0-100%
                "relative_humidity_2m_mean": max(
                    0, min(100, float(forecast["relative_humidity_2m_mean"]))
                ),  # 0-100%
            }

            return cleaned

        except (ValueError, TypeError) as e:
            self.logger.error(
                f"Erreur nettoyage prévision solaire {forecast.get('date', 'date inconnue')}: {e}"
            )
            return None

    def get_wind_forecast(self) -> List[Dict[str, Any]]:
        """
        Récupère les prévisions éoliennes depuis la table clean_wind_forecast
        Returns:
            Liste de dictionnaires avec les features pour la prédiction éolienne
        """
        try:
            self.logger.info("Récupération des prévisions éoliennes...")

            response = (
                self.supabase.table("clean_wind_forecast")
                .select(
                    "date, wind_speed_10m_max, wind_gusts_10m_max, wind_direction_10m_dominant, temperature_2m_mean"
                )
                .order("date")
                .execute()
            )

            forecasts = response.data
            self.logger.info(f"Récupéré {len(forecasts)} prévisions éoliennes")

            # Validation et nettoyage des données
            valid_forecasts = []
            for forecast in forecasts:
                cleaned_forecast = self._clean_wind_forecast(forecast)
                if cleaned_forecast:
                    valid_forecasts.append(cleaned_forecast)

            self.logger.info(
                f"{len(valid_forecasts)} prévisions éoliennes valides après nettoyage"
            )
            return valid_forecasts

        except Exception as e:
            self.logger.error(f"Erreur récupération prévisions éoliennes: {e}")
            return []

    def _clean_wind_forecast(self, forecast: Dict[str, Any]) -> Dict[str, Any]:
        """
        Nettoie et valide une prévision éolienne
        """
        try:
            # Vérifier que toutes les features requises sont présentes
            required_features = [
                "wind_speed_10m_max",
                "wind_gusts_10m_max",
                "wind_direction_10m_dominant",
                "temperature_2m_mean",
            ]

            # Vérifier la présence des features
            for feature in required_features:
                if feature not in forecast or forecast[feature] is None:
                    self.logger.warning(
                        f"Feature {feature} manquante dans la prévision éolienne du {forecast.get('date', 'date inconnue')}"
                    )
                    return None

            # Convertir les types et valider les valeurs
            cleaned = {
                "date": forecast["date"],
                "wind_speed_10m_max": max(0, float(forecast["wind_speed_10m_max"])),
                "wind_gusts_10m_max": max(0, float(forecast["wind_gusts_10m_max"])),
                "wind_direction_10m_dominant": float(
                    forecast["wind_direction_10m_dominant"]
                )
                % 360,  # Normaliser 0-360°
                "temperature_2m_mean": float(forecast["temperature_2m_mean"]),
            }

            return cleaned

        except (ValueError, TypeError) as e:
            self.logger.error(
                f"Erreur nettoyage prévision éolienne {forecast.get('date', 'date inconnue')}: {e}"
            )
            return None

    def get_hydro_forecast(self) -> List[Dict[str, Any]]:
        """
        Récupère les dernières données hydrauliques pour prévision
        Pour l'hydro, on utilise les données les plus récentes de clean_hubeau
        Returns:
            Liste de dictionnaires avec les features pour la prédiction hydraulique
        """
        try:
            self.logger.info("Récupération des données hydrauliques...")

            # Récupérer les 7 derniers jours pour avoir un historique récent
            response = (
                self.supabase.table("clean_hubeau")
                .select("date, debit_l_s")
                .order("date", desc=True)
                .limit(7)
                .execute()
            )

            forecasts = response.data
            self.logger.info(f"Récupéré {len(forecasts)} données hydrauliques récentes")

            # Utiliser la moyenne des 7 derniers jours pour la prévision
            if forecasts:
                # Calculer la moyenne des débits
                debits = [
                    max(0, float(f["debit_l_s"]))
                    for f in forecasts
                    if f.get("debit_l_s") is not None
                ]
                if debits:
                    avg_debit = sum(debits) / len(debits)

                    # Créer une prévision pour aujourd'hui
                    latest_date = forecasts[0]["date"]
                    forecast_data = {"date": latest_date, "debit_l_s": avg_debit}

                    self.logger.info(
                        f"Prévision hydro: débit moyen {avg_debit:.2f} L/s sur {len(debits)} jours"
                    )
                    return [forecast_data]

            self.logger.warning("Aucune donnée hydraulique valide trouvée")
            return []

        except Exception as e:
            self.logger.error(f"Erreur récupération données hydrauliques: {e}")
            return []

    def get_all_forecasts(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Récupère toutes les prévisions en une seule requête
        Returns:
            Dictionnaire avec les prévisions pour chaque type de producteur
        """
        try:
            self.logger.info("Récupération de toutes les prévisions...")

            solar_forecasts = self.get_solar_forecast()
            wind_forecasts = self.get_wind_forecast()
            hydro_forecasts = self.get_hydro_forecast()

            result = {
                "solar": solar_forecasts,
                "wind": wind_forecasts,
                "hydro": hydro_forecasts,
            }

            self.logger.info(
                f"Prévisions récupérées - Solaire: {len(solar_forecasts)}, Éolien: {len(wind_forecasts)}, Hydro: {len(hydro_forecasts)}"
            )
            return result

        except Exception as e:
            self.logger.error(f"Erreur récupération toutes les prévisions: {e}")
            return {"solar": [], "wind": [], "hydro": []}

    def check_forecast_availability(self) -> Dict[str, bool]:
        """
        Vérifie la disponibilité des données prévisionnelles
        Returns:
            Dictionnaire indiquant si chaque type de prévision est disponible
        """
        try:
            # Vérifier les tables existent et ont des données
            availability = {}

            # Vérifier solaire
            solar_response = (
                self.supabase.table("clean_solar_forecast")
                .select("date", count="exact")
                .limit(1)
                .execute()
            )
            availability["solar"] = solar_response.count > 0

            # Vérifier éolien
            wind_response = (
                self.supabase.table("clean_wind_forecast")
                .select("date", count="exact")
                .limit(1)
                .execute()
            )
            availability["wind"] = wind_response.count > 0

            # Vérifier hydro
            hydro_response = (
                self.supabase.table("clean_hubeau")
                .select("date", count="exact")
                .limit(1)
                .execute()
            )
            availability["hydro"] = hydro_response.count > 0

            self.logger.info(f"Disponibilité prévisions: {availability}")
            return availability

        except Exception as e:
            self.logger.error(f"Erreur vérification disponibilité prévisions: {e}")
            return {"solar": False, "wind": False, "hydro": False}
