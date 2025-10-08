import pytest
import pandas as pd
from unittest.mock import patch, Mock
from data_ingestion.handlers.handler_meteo import WeatherDataHandler


def test_weather_handler_initialization():
    """Test l'initialisation du handler météo."""
    handler = WeatherDataHandler(43.6109, 3.8763, "solar")

    assert handler.latitude == 43.6109
    assert handler.longitude == 3.8763
    assert handler.data_type == "solar"
    assert handler.table_name == "meteo_solaire"


def test_weather_handler_initialization_invalid_type():
    """Test l'initialisation avec type invalide."""
    with pytest.raises(ValueError):
        WeatherDataHandler(43.6109, 3.8763, "invalid_type")


@patch("data_ingestion.handlers.handler_meteo.get_solar_forecast")
def test_weather_handler_load_solar_forecast(mock_forecast):
    """Test le chargement des prévisions solaires."""
    mock_forecast.return_value = pd.DataFrame(
        {"time": ["2024-01-01", "2024-01-02"], "shortwave_radiation_sum": [15.5, 16.2]}
    )

    handler = WeatherDataHandler(43.6109, 3.8763, "solar")
    df = handler.load(forecast=True)

    assert not df.empty
    mock_forecast.assert_called_once()


@patch("data_ingestion.handlers.handler_meteo.get_wind_history")
def test_weather_handler_load_wind_history(mock_history):
    """Test le chargement de l'historique éolien."""
    mock_history.return_value = pd.DataFrame(
        {"time": ["2024-01-01", "2024-01-02"], "wind_speed_10m_max": [8.5, 9.2]}
    )

    handler = WeatherDataHandler(43.6109, 3.8763, "wind")
    df = handler.load(forecast=False)

    assert not df.empty
    mock_history.assert_called_once()


@patch("data_ingestion.handlers.handler_meteo.DataCleaner")
def test_weather_handler_clean_solar(mock_cleaner):
    """Test le nettoyage des données solaires."""
    mock_cleaner.clean_solar_data.return_value = pd.DataFrame(
        {"date": ["2024-01-01", "2024-01-02"], "shortwave_radiation_sum": [15.5, 16.2]}
    )

    handler = WeatherDataHandler(43.6109, 3.8763, "solar")
    handler.df = pd.DataFrame({"test": [1, 2]})
    handler.clean()

    mock_cleaner.clean_solar_data.assert_called_once()


@patch("data_ingestion.handlers.handler_meteo.DataCleaner")
def test_weather_handler_clean_wind(mock_cleaner):
    """Test le nettoyage des données éoliennes."""
    mock_cleaner.clean_wind_data.return_value = pd.DataFrame(
        {"date": ["2024-01-01", "2024-01-02"], "wind_speed_10m_max": [8.5, 9.2]}
    )

    handler = WeatherDataHandler(43.6109, 3.8763, "wind")
    handler.df = pd.DataFrame({"test": [1, 2]})
    handler.clean()

    mock_cleaner.clean_wind_data.assert_called_once()
