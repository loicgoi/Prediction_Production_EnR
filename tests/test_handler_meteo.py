import pytest
import pandas as pd
from unittest.mock import patch, Mock
from src.data_ingestion.handlers.handler_meteo import WeatherDataHandler


def test_weather_handler_initialization():
    """Test l'initialisation du handler météo."""
    handler = WeatherDataHandler(latitude=43.6109, longitude=3.8763, data_type="solar")

    assert handler.latitude == 43.6109
    assert handler.longitude == 3.8763
    assert handler.data_type == "solar"


def test_weather_handler_initialization_invalid_type():
    """Test l'initialisation avec type invalide."""
    with pytest.raises(ValueError):
        WeatherDataHandler(43.6109, 3.8763, "invalid_type")


@patch("src.data_ingestion.handlers.handler_meteo.get_solar_forecast")
@patch("src.data_ingestion.handlers.handler_meteo.DataCleaner.clean_solar_data")
def test_weather_handler_load_solar_forecast(mock_clean, mock_forecast):
    """Test le chargement des prévisions solaires."""
    # Configurer les mocks pour retourner de vrais DataFrames
    raw_data = pd.DataFrame(
        {"time": ["2024-01-01", "2024-01-02"], "shortwave_radiation_sum": [15.5, 16.2]}
    )
    cleaned_data = pd.DataFrame(
        {"date": ["2024-01-01", "2024-01-02"], "shortwave_radiation_sum": [15.5, 16.2]}
    )

    mock_forecast.return_value = raw_data
    mock_clean.return_value = cleaned_data

    # Créer le handler et appeler load
    handler = WeatherDataHandler(43.6109, 3.8763, "solar")
    df = handler.load(forecast=True)

    # Vérifications
    assert not df.empty
    assert isinstance(df, pd.DataFrame)
    mock_forecast.assert_called_once()
    mock_clean.assert_called_once_with(raw_data)


@patch("src.data_ingestion.handlers.handler_meteo.get_wind_history")
@patch("src.data_ingestion.handlers.handler_meteo.DataCleaner.clean_wind_data")
def test_weather_handler_load_wind_history(mock_clean, mock_history):
    """Test le chargement de l'historique éolien."""
    # Configurer les mocks pour retourner de vrais DataFrames
    raw_data = pd.DataFrame(
        {"time": ["2024-01-01", "2024-01-02"], "wind_speed_10m_max": [8.5, 9.2]}
    )
    cleaned_data = pd.DataFrame(
        {"date": ["2024-01-01", "2024-01-02"], "wind_speed_10m_max": [8.5, 9.2]}
    )

    mock_history.return_value = raw_data
    mock_clean.return_value = cleaned_data

    # Créer le handler et appeler load
    handler = WeatherDataHandler(43.6109, 3.8763, "wind")
    df = handler.load(start_date="2024-01-01", end_date="2024-01-02", forecast=False)

    # Vérifications
    assert not df.empty
    assert isinstance(df, pd.DataFrame)
    mock_history.assert_called_once_with(43.6109, 3.8763, "2024-01-01", "2024-01-02")
    mock_clean.assert_called_once_with(raw_data)


@patch("src.data_ingestion.handlers.handler_meteo.get_solar_history")
@patch("src.data_ingestion.handlers.handler_meteo.DataCleaner.clean_solar_data")
def test_weather_handler_load_solar_history(mock_clean, mock_history):
    """Test le chargement de l'historique solaire."""
    # Configurer les mocks pour retourner de vrais DataFrames
    raw_data = pd.DataFrame(
        {"time": ["2024-01-01", "2024-01-02"], "shortwave_radiation_sum": [14.5, 15.2]}
    )
    cleaned_data = pd.DataFrame(
        {"date": ["2024-01-01", "2024-01-02"], "shortwave_radiation_sum": [14.5, 15.2]}
    )

    mock_history.return_value = raw_data
    mock_clean.return_value = cleaned_data

    # Créer le handler et appeler load
    handler = WeatherDataHandler(43.6109, 3.8763, "solar")
    df = handler.load(start_date="2024-01-01", end_date="2024-01-02", forecast=False)

    # Vérifications
    assert not df.empty
    assert isinstance(df, pd.DataFrame)
    mock_history.assert_called_once_with(43.6109, 3.8763, "2024-01-01", "2024-01-02")
    mock_clean.assert_called_once_with(raw_data)


@patch("src.data_ingestion.handlers.handler_meteo.get_wind_forecast")
@patch("src.data_ingestion.handlers.handler_meteo.DataCleaner.clean_wind_data")
def test_weather_handler_load_wind_forecast(mock_clean, mock_forecast):
    """Test le chargement des prévisions éoliennes."""
    # Configurer les mocks pour retourner de vrais DataFrames
    raw_data = pd.DataFrame(
        {"time": ["2024-01-01", "2024-01-02"], "wind_speed_10m_max": [7.5, 8.2]}
    )
    cleaned_data = pd.DataFrame(
        {"date": ["2024-01-01", "2024-01-02"], "wind_speed_10m_max": [7.5, 8.2]}
    )

    mock_forecast.return_value = raw_data
    mock_clean.return_value = cleaned_data

    # Créer le handler et appeler load
    handler = WeatherDataHandler(43.6109, 3.8763, "wind")
    df = handler.load(forecast=True)

    # Vérifications
    assert not df.empty
    assert isinstance(df, pd.DataFrame)
    mock_forecast.assert_called_once()
    mock_clean.assert_called_once_with(raw_data)


def test_weather_handler_load_with_exception():
    """Test le comportement en cas d'exception."""
    with patch(
        "src.data_ingestion.handlers.handler_meteo.get_solar_forecast"
    ) as mock_forecast:
        mock_forecast.side_effect = Exception("API Error")

        handler = WeatherDataHandler(43.6109, 3.8763, "solar")
        df = handler.load(forecast=True)

        # Doit retourner un DataFrame vide en cas d'erreur
        assert df.empty
