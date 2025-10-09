import pytest
import pandas as pd
from unittest.mock import patch, Mock


@patch("src.data_ingestion.fetchers.fetch_production.SolarProducer")
def test_fetch_production_data_solar(mock_solar_producer):
    """Test la récupération des données de production solaire."""
    mock_instance = Mock()
    mock_instance.load_production_data.return_value = pd.DataFrame(
        {"date": ["2024-01-01", "2024-01-02"], "production_kwh": [150.5, 160.2]}
    )
    mock_solar_producer.return_value = mock_instance

    from src.data_ingestion.fetchers.fetch_production import fetch_production_data

    df = fetch_production_data("solar")

    assert isinstance(df, pd.DataFrame)
    mock_solar_producer.assert_called_once()


@patch("src.data_ingestion.fetchers.fetch_production.WindProducer")
def test_fetch_production_data_wind(mock_wind_producer):
    """Test la récupération des données de production éolienne."""
    mock_instance = Mock()
    mock_instance.load_production_data.return_value = pd.DataFrame(
        {"date": ["2024-01-01", "2024-01-02"], "production_kwh": [80.3, 75.6]}
    )
    mock_wind_producer.return_value = mock_instance

    from src.data_ingestion.fetchers.fetch_production import fetch_production_data

    df = fetch_production_data("wind")

    assert isinstance(df, pd.DataFrame)
    mock_wind_producer.assert_called_once()


@patch("src.data_ingestion.fetchers.fetch_production.HydroProducer")
def test_fetch_production_data_hydro(mock_hydro_producer):
    """Test la récupération des données de production hydraulique."""
    mock_instance = Mock()
    mock_instance.load_production_data.return_value = pd.DataFrame(
        {"date": ["2024-01-01", "2024-01-02"], "production_kwh": [200.1, 195.8]}
    )
    mock_hydro_producer.return_value = mock_instance

    from src.data_ingestion.fetchers.fetch_production import fetch_production_data

    df = fetch_production_data("hydro")

    assert isinstance(df, pd.DataFrame)
    mock_hydro_producer.assert_called_once()


def test_fetch_production_data_invalid_type():
    """Test avec un type de producteur invalide."""
    from src.data_ingestion.fetchers.fetch_production import fetch_production_data

    with pytest.raises(ValueError):
        fetch_production_data("invalid_type")
