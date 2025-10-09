import pytest
import pandas as pd
from unittest.mock import patch, Mock
<<<<<<< HEAD
<<<<<<< HEAD
from src.data_ingestion.fetchers.fetch_open_meteo_solaire import (
=======
from data_ingestion.fetchers.fetch_open_meteo_solaire import (
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
=======
from src.data_ingestion.fetchers.fetch_open_meteo_solaire import (
>>>>>>> 5594093 (màj des test + commentires code + README.md)
    get_solar_forecast,
    get_solar_history,
)


<<<<<<< HEAD
@patch("src.data_ingestion.fetchers.fetch_open_meteo_solaire.requests.get")
=======
@patch("data_ingestion.fetchers.fetch_open_meteo_solaire.requests.get")
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
def test_get_solar_forecast_success(mock_get):
    """Test la récupération des prévisions solaires."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "daily": {
            "time": ["2024-01-01", "2024-01-02"],
<<<<<<< HEAD
            "temperature_2m_max": [15, 16],
=======
            "cloud_cover_max": [50, 60],
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
            "shortwave_radiation_sum": [15.5, 16.2],
        }
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

<<<<<<< HEAD
    df = get_solar_forecast(43.6109, 3.8763)
=======
    df = get_solar_forecast(43.6109, 3.8763, "2024-01-01", "2024-01-02")
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "time" in df.columns


<<<<<<< HEAD
@patch("src.data_ingestion.fetchers.fetch_open_meteo_solaire.requests.get")
=======
@patch("data_ingestion.fetchers.fetch_open_meteo_solaire.requests.get")
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
def test_get_solar_history_success(mock_get):
    """Test la récupération de l'historique solaire."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "daily": {
            "time": ["2024-01-01", "2024-01-02"],
            "sunshine_duration": [36000, 35000],
            "shortwave_radiation_sum": [14.8, 15.1],
        }
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    df = get_solar_history(43.6109, 3.8763, "2024-01-01", "2024-01-02")

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
