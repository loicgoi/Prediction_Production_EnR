import pytest
import pandas as pd
from datetime import date
from unittest.mock import Mock, patch
from producers.hydro_producer import HydroProducer


def test_hydro_producer_initialization():
    """Test l'initialisation du producteur hydraulique."""
    producer = HydroProducer(
        "Centrale hydro", "Montpellier", 200.0, "data/raw/prod_hydro.csv"
    )

    assert producer.name == "Centrale hydro"
    assert producer.location == "Montpellier"
    assert producer.nominal_power == 200.0
    assert producer.data_file == "data/raw/prod_hydro.csv"


@patch("producers.hydro_producer.CSVDataHandler")
@patch("producers.hydro_producer.DataCleaner")
def test_hydro_producer_load_data(mock_cleaner, mock_handler):
    """Test le chargement des données hydrauliques."""
    mock_instance = Mock()
    mock_instance.load.return_value = pd.DataFrame(
        {"date": ["2024-01-01", "2024-01-02"], "prod_hydro": [180.5, 195.2]}
    )
    mock_handler.return_value = mock_instance

    mock_cleaner.clean_production_data.return_value = pd.DataFrame(
        {"date": ["2024-01-01", "2024-01-02"], "production_kwh": [180.5, 195.2]}
    )

    producer = HydroProducer("Test", "Montpellier", 200.0, "test.csv")
    df = producer.load_production_data(date(2024, 1, 1), date(2024, 1, 2))

    assert not df.empty
    mock_cleaner.clean_production_data.assert_called_once()


def test_hydro_producer_calculate_statistics():
    """Test le calcul des statistiques hydrauliques."""
    producer = HydroProducer("Test", "Montpellier", 200.0, "test.csv")

    with patch.object(producer, "load_production_data") as mock_load:
        mock_load.return_value = pd.DataFrame(
            {
                "date": [date(2024, 1, 1), date(2024, 1, 2)],
                "production_kwh": [180.5, 195.2],
            }
        )

        stats = producer.calculate_statistics(date(2024, 1, 1), date(2024, 1, 2))

        assert "total_production" in stats
        assert "average_daily_production" in stats
        assert stats["total_production"] == 375.7
