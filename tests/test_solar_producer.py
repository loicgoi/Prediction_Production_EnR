import pytest
import pandas as pd
from datetime import date
from unittest.mock import Mock, patch
from producers.solar_producer import SolarProducer


def test_solar_producer_initialization():
    """Test l'initialisation du producteur solaire."""
    producer = SolarProducer(
        "Parc solaire", "Montpellier", 150.0, "data/raw/prod_solaire.csv"
    )

    assert producer.name == "Parc solaire"
    assert producer.location == "Montpellier"
    assert producer.nominal_power == 150.0
    assert producer.data_file == "data/raw/prod_solaire.csv"


@patch("producers.solar_producer.CSVDataHandler")
@patch("producers.solar_producer.DataCleaner")
def test_solar_producer_load_data(mock_cleaner, mock_handler):
    """Test le chargement des données solaires."""
    # Mock du handler
    mock_instance = Mock()
    mock_instance.load.return_value = pd.DataFrame(
        {"date": ["2024-01-01", "2024-01-02"], "prod_solaire": [150.5, 160.2]}
    )
    mock_handler.return_value = mock_instance

    # Mock du cleaner
    mock_cleaner.clean_production_data.return_value = pd.DataFrame(
        {"date": ["2024-01-01", "2024-01-02"], "production_kwh": [150.5, 160.2]}
    )

    producer = SolarProducer("Test", "Montpellier", 150.0, "test.csv")
    df = producer.load_production_data(date(2024, 1, 1), date(2024, 1, 2))

    assert not df.empty
    mock_instance.load.assert_called_once()
    mock_cleaner.clean_production_data.assert_called_once()


def test_solar_producer_calculate_statistics():
    """Test le calcul des statistiques solaires."""
    producer = SolarProducer("Test", "Montpellier", 150.0, "test.csv")

    # Mock de load_production_data
    with patch.object(producer, "load_production_data") as mock_load:
        mock_load.return_value = pd.DataFrame(
            {
                "date": [date(2024, 1, 1), date(2024, 1, 2)],
                "production_kwh": [150.5, 160.2],
            }
        )

        stats = producer.calculate_statistics(date(2024, 1, 1), date(2024, 1, 2))

        assert "total_production" in stats
        assert "average_daily_production" in stats
        assert "capacity_factor" in stats
        assert stats["total_production"] == 310.7


def test_solar_producer_statistics_empty_data():
    """Test les statistiques avec données vides."""
    producer = SolarProducer("Test", "Montpellier", 150.0, "test.csv")

    with patch.object(producer, "load_production_data") as mock_load:
        mock_load.return_value = pd.DataFrame()

        stats = producer.calculate_statistics(date(2024, 1, 1), date(2024, 1, 2))

        assert stats["total_production"] == 0
        assert stats["capacity_factor"] == 0.0
