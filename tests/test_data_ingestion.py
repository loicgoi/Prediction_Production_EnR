import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import date, timedelta

# Import des modules à tester
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_ingestion.fetch_hubeau import get_hubeau_data
from src.data_ingestion.fetch_open_meteo_eolien import (
    get_wind_forecast,
    get_wind_history,
)
from src.data_ingestion.fetch_open_meteo_solaire import (
    get_solar_forecast,
    get_solar_history,
)
from src.data_ingestion.handler_hubeau import HubeauDataHandler
from src.data_ingestion.handler_meteo import WeatherDataHandler


class TestHubeauData(unittest.TestCase):
    """Tests pour les fonctions de récupération de données Hub'Eau."""

    @patch("src.data_ingestion.fetch_hubeau.requests.get")
    def test_get_hubeau_data_success(self, mock_get):
        """Test de récupération réussie des données Hub'Eau."""
        # Configuration du mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [
                {
                    "code_station": "Y321002101",
                    "date_obs_elab": "2023-01-01",
                    "result_obs_elab": 100.5,
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Appel de la fonction
        result = get_hubeau_data("Y321002101", "2023-01-01", "2023-01-31")

        # Vérifications
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["code_station"], "Y321002101")
        mock_get.assert_called_once()

    @patch("src.data_ingestion.fetch_hubeau.requests.get")
    def test_get_hubeau_data_error(self, mock_get):
        """Test de gestion d'erreur lors de la récupération des données Hub'Eau."""
        # Configuration du mock pour lever une exception
        mock_get.side_effect = Exception("Erreur de connexion")

        # Appel de la fonction et vérification de l'exception
        with self.assertRaises(Exception):
            get_hubeau_data("Y321002101", "2023-01-01", "2023-01-31")


class TestOpenMeteoData(unittest.TestCase):
    """Tests pour les fonctions de récupération de données Open-Meteo."""

    @patch("src.data_ingestion.fetch_open_meteo_solaire.requests.get")
    def test_get_solar_forecast_success(self, mock_get):
        """Test de récupération réussie des données de prévision solaire."""
        # Configuration du mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "daily": {
                "time": ["2023-01-01"],
                "shortwave_radiation_sum": [10.5],
                "sunshine_duration": [36000],
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Appel de la fonction
        result = get_solar_forecast(43.6109, 3.8763, "2023-01-01", "2023-01-01")

        # Vérifications
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 1)
        mock_get.assert_called_once()

    @patch("src.data_ingestion.fetch_open_meteo_eolien.requests.get")
    def test_get_wind_history_success(self, mock_get):
        """Test de récupération réussie des données historiques éoliennes."""
        # Configuration du mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "daily": {
                "time": ["2023-01-01"],
                "wind_speed_10m_max": [15.5],
                "wind_direction_10m_dominant": [180],
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Appel de la fonction
        result = get_wind_history(43.6109, 3.8763, "2023-01-01", "2023-01-31")

        # Vérifications
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 1)
        mock_get.assert_called_once()


class TestHandlers(unittest.TestCase):
    """Tests pour les gestionnaires de données."""

    @patch("src.data_ingestion.handler_hubeau.get_hubeau_data")
    def test_hubeau_data_handler_load(self, mock_get_data):
        """Test du chargement des données avec HubeauDataHandler."""
        # Configuration du mock
        mock_df = pd.DataFrame(
            {
                "code_station": ["Y321002101"],
                "date_obs_elab": ["2023-01-01"],
                "result_obs_elab": [100.5],
            }
        )
        mock_get_data.return_value = mock_df

        # Création du gestionnaire et appel de la méthode load
        handler = HubeauDataHandler("Y321002101", "2023-01-01", "2023-01-31")
        result = handler.load()

        # Vérifications
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 1)
        mock_get_data.assert_called_once_with(
            code_station="Y321002101", start_date="2023-01-01", end_date="2023-01-31"
        )

    @patch("src.data_ingestion.handler_meteo.get_solar_history")
    def test_weather_data_handler_load(self, mock_get_data):
        """Test du chargement des données météorologiques avec WeatherDataHandler."""
        # Configuration du mock
        mock_df = pd.DataFrame(
            {
                "time": ["2023-01-01"],
                "shortwave_radiation_sum": [10.5],
                "sunshine_duration": [36000],
            }
        )
        mock_get_data.return_value = mock_df

        # Création du gestionnaire et appel de la méthode load
        handler = WeatherDataHandler(43.6109, 3.8763, "solar")
        result = handler.load(start_date="2023-01-01", end_date="2023-01-31")

        # Vérifications
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 1)
        mock_get_data.assert_called_once_with(
            latitude=43.6109,
            longitude=3.8763,
            start_date="2023-01-01",
            end_date="2023-01-31",
        )


if __name__ == "__main__":
    unittest.main()
