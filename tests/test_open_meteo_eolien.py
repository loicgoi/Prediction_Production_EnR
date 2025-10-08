import pytest
import pandas as pd
from unittest.mock import patch, Mock
from data_ingestion.fetchers.fetch_open_meteo_eolien import (
    get_wind_forecast,
    get_wind_history,
)


@patch("data_ingestion.fetchers.fetch_open_meteo_eolien.requests.get")
def test_get_wind_forecast_success(mock_get):
    """Test la récupération des prévisions éoliennes."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "daily": {
            "time": ["2024-01-01", "2024-01-02"],
            "wind_speed_10m_max": [8.5, 9.2],
            "wind_gusts_10m_max": [12.1, 13.5],
        }
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    df = get_wind_forecast(43.6109, 3.8763, "2024-01-01", "2024-01-02")

    assert isinstance(df, pd.DataFrame)
    assert not df.empty


@patch("data_ingestion.fetchers.fetch_open_meteo_eolien.requests.get")
def test_get_wind_history_success(mock_get):
    """Test la récupération de l'historique éolien."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "daily": {
            "time": ["2024-01-01", "2024-01-02"],
            "wind_speed_10m_max": [7.8, 8.4],
            "wind_direction_10m_dominant": [180, 190],
        }
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    df = get_wind_history(43.6109, 3.8763, "2024-01-01", "2024-01-02")

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
