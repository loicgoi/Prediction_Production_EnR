import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from datetime import date


class TestDataCleaner:
    """Tests pour DataCleaner"""

    def test_clean_solar_data(self, mock_solar_data):
        from data_ingestion.data_cleaner import DataCleaner

        result = DataCleaner.clean_solar_data(mock_solar_data)

        assert not result.empty
        assert "date" in result.columns
        assert "sunshine_duration_h" in result.columns
        assert result["date"].dtype == "datetime64[ns]"

    def test_clean_wind_data(self, mock_wind_data):
        from data_ingestion.data_cleaner import DataCleaner

        result = DataCleaner.clean_wind_data(mock_wind_data)

        assert not result.empty
        assert "date" in result.columns

    def test_clean_production_data_solar(self, mock_production_data):
        from data_ingestion.data_cleaner import DataCleaner

        result = DataCleaner.clean_production_data(mock_production_data, "solar")

        assert not result.empty
        assert "production_kwh" in result.columns
        assert "date" in result.columns
        assert all(result["production_kwh"] >= 0)

    def test_clean_hydro_data(self, mock_hydro_data):
        from data_ingestion.data_cleaner import DataCleaner

        result = DataCleaner.clean_hydro_data(mock_hydro_data)

        assert not result.empty
        assert "date" in result.columns
        assert "debit_l_s" in result.columns


class TestWeatherDataHandler:
    """Tests pour WeatherDataHandler"""

    @patch("data_ingestion.fetch_open_meteo_solaire.requests.get")
    def test_solar_handler_load(self, mock_get, mock_solar_data):
        from data_ingestion.handler_meteo import WeatherDataHandler

        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"daily": mock_solar_data.to_dict("list")}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        handler = WeatherDataHandler(43.61, 3.88, "solar")
        result = handler.load(start_date="2024-01-01", end_date="2024-01-05")

        assert not result.empty
        mock_get.assert_called_once()

    @patch("data_ingestion.fetch_open_meteo_eolien.requests.get")
    def test_wind_handler_load(self, mock_get, mock_wind_data):
        from data_ingestion.handler_meteo import WeatherDataHandler

        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"daily": mock_wind_data.to_dict("list")}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        handler = WeatherDataHandler(43.61, 3.88, "wind")
        result = handler.load(start_date="2024-01-01", end_date="2024-01-05")

        assert not result.empty
        mock_get.assert_called_once()


class TestHubeauDataHandler:
    """Tests pour HubeauDataHandler"""

    @patch("data_ingestion.fetch_hubeau.requests.get")
    def test_hubeau_handler_load(self, mock_get, mock_hydro_data):
        from data_ingestion.handler_hubeau import HubeauDataHandler

        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": mock_hydro_data.to_dict("records")}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        handler = HubeauDataHandler("Y321002101", "2024-01-01", "2024-01-05")
        result = handler.load()

        assert not result.empty
        mock_get.assert_called_once()


class TestFetchFunctions:
    """Tests pour les fonctions fetch"""

    @patch("data_ingestion.fetch_open_meteo_solaire.requests.get")
    def test_get_solar_forecast(self, mock_get, mock_solar_data):
        from data_ingestion.fetch_open_meteo_solaire import get_solar_forecast

        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"daily": mock_solar_data.to_dict("list")}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_solar_forecast(43.61, 3.88, "2024-01-01", "2024-01-05")

        assert not result.empty
        assert "time" in result.columns

    @patch("data_ingestion.fetch_hubeau.requests.get")
    def test_get_hubeau_data(self, mock_get, mock_hydro_data):
        from data_ingestion.fetch_hubeau import get_hubeau_data

        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": mock_hydro_data.to_dict("records")}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_hubeau_data("Y321002101", "2024-01-01", "2024-01-05")

        assert not result.empty
        assert "date_obs_elab" in result.columns
