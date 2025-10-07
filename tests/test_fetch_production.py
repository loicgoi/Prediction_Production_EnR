import pytest
import pandas as pd
<<<<<<< HEAD
from unittest.mock import patch, Mock
from data_ingestion.fetchers.fetch_production import fetch_production_data


def test_fetch_production_data_invalid_type():
    """Test avec un type de producteur invalide."""
    with pytest.raises(ValueError):
        fetch_production_data("invalid_type")


@patch("data_ingestion.fetchers.fetch_production.SolarProducer")
def test_fetch_production_data_solar(mock_solar_producer):
    """Test la récupération des données de production solaire."""
    mock_instance = Mock()
    mock_instance.load_production_data.return_value = pd.DataFrame(
        {"date": ["2024-01-01", "2024-01-02"], "production_kwh": [150.5, 160.2]}
    )
    mock_solar_producer.return_value = mock_instance

    df = fetch_production_data("solar")

    assert isinstance(df, pd.DataFrame)
    mock_solar_producer.assert_called_once()


@patch("data_ingestion.fetchers.fetch_production.WindProducer")
def test_fetch_production_data_wind(mock_wind_producer):
    """Test la récupération des données de production éolienne."""
    mock_instance = Mock()
    mock_instance.load_production_data.return_value = pd.DataFrame(
        {"date": ["2024-01-01", "2024-01-02"], "production_kwh": [80.3, 75.6]}
    )
    mock_wind_producer.return_value = mock_instance

    df = fetch_production_data("wind")

    assert isinstance(df, pd.DataFrame)
    mock_wind_producer.assert_called_once()


@patch("data_ingestion.fetchers.fetch_production.HydroProducer")
def test_fetch_production_data_hydro(mock_hydro_producer):
    """Test la récupération des données de production hydraulique."""
    mock_instance = Mock()
    mock_instance.load_production_data.return_value = pd.DataFrame(
        {"date": ["2024-01-01", "2024-01-02"], "production_kwh": [200.1, 195.8]}
    )
    mock_hydro_producer.return_value = mock_instance

    df = fetch_production_data("hydro")

    assert isinstance(df, pd.DataFrame)
    mock_hydro_producer.assert_called_once()
=======
from unittest.mock import patch, MagicMock
from datetime import date


class TestFetchProduction:
    """Tests pour fetch_production_data"""

    @patch("data_ingestion.fetch_production.SolarProducer")
    def test_fetch_solar_production(self, mock_solar_producer, mock_production_data):
        from data_ingestion.fetch_production import fetch_production_data

        # Mock SolarProducer
        mock_instance = MagicMock()
        mock_instance.load_production_data.return_value = mock_production_data
        mock_solar_producer.return_value = mock_instance

        result = fetch_production_data("solar")

        assert not result.empty
        mock_solar_producer.assert_called_once()

    @patch("data_ingestion.fetch_production.WindProducer")
    def test_fetch_wind_production(self, mock_wind_producer, mock_production_data):
        from data_ingestion.fetch_production import fetch_production_data

        # Mock WindProducer
        mock_instance = MagicMock()
        mock_instance.load_production_data.return_value = mock_production_data
        mock_wind_producer.return_value = mock_instance

        result = fetch_production_data("wind")

        assert not result.empty
        mock_wind_producer.assert_called_once()

    @patch("data_ingestion.fetch_production.HydroProducer")
    def test_fetch_hydro_production(self, mock_hydro_producer, mock_production_data):
        from data_ingestion.fetch_production import fetch_production_data

        # Mock HydroProducer
        mock_instance = MagicMock()
        mock_instance.load_production_data.return_value = mock_production_data
        mock_hydro_producer.return_value = mock_instance

        result = fetch_production_data("hydro")

        assert not result.empty
        mock_hydro_producer.assert_called_once()

    def test_fetch_production_invalid_type(self):
        from data_ingestion.fetch_production import fetch_production_data

        with pytest.raises(ValueError):
            fetch_production_data("invalid_type")

    @patch("data_ingestion.fetch_production.SolarProducer")
    def test_fetch_production_with_dates(
        self, mock_solar_producer, mock_production_data
    ):
        from data_ingestion.fetch_production import fetch_production_data

        # Mock SolarProducer
        mock_instance = MagicMock()
        mock_instance.load_production_data.return_value = mock_production_data
        mock_solar_producer.return_value = mock_instance

        start_date = date(2024, 1, 1)
        end_date = date(2024, 1, 5)

        result = fetch_production_data("solar", start_date, end_date)

        assert not result.empty
        # Vérifier que les dates sont passées au producer
        mock_instance.load_production_data.assert_called_once()

    @patch("data_ingestion.fetch_production.SolarProducer")
    def test_fetch_production_empty_result(self, mock_solar_producer):
        from data_ingestion.fetch_production import fetch_production_data

        # Mock empty result
        mock_instance = MagicMock()
        mock_instance.load_production_data.return_value = pd.DataFrame()
        mock_solar_producer.return_value = mock_instance

        result = fetch_production_data("solar")

        assert result.empty
>>>>>>> 3c7ab3c (réalisation des tests + correction erreurs d'import)
