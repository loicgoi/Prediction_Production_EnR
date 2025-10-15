import pytest
import pandas as pd
from datetime import date
from unittest.mock import Mock, patch
from src.producers.wind_producer import WindProducer


def test_wind_producer_initialization():
    """Test l'initialisation du producteur éolien."""
    producer = WindProducer(
        "Éolienne", "Montpellier", 100.0, "data/raw/prod_eolienne.csv"
    )

    assert producer.name == "Éolienne"
    assert producer.location == "Montpellier"
    assert producer.nominal_power == 100.0
    assert producer.data_file == "data/raw/prod_eolienne.csv"


@patch("pandas.read_csv")
@patch("src.producers.wind_producer.DataCleaner")
def test_wind_producer_load_data_success(mock_cleaner, mock_read_csv):
    """Test le chargement réussi des données éoliennes."""
    # Mock de read_csv
    mock_read_csv.return_value = pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "prod_eolienne": [80.5, 75.2, 85.1],
        }
    )

    # Mock du cleaner
    mock_cleaner.clean_production_data.return_value = pd.DataFrame(
        {
            "date": [date(2024, 1, 1), date(2024, 1, 2), date(2024, 1, 3)],
            "production_kwh": [80.5, 75.2, 85.1],
        }
    )

    producer = WindProducer("Test", "Montpellier", 100.0, "test.csv")
    df = producer.load_production_data(date(2024, 1, 1), date(2024, 1, 2))

    assert not df.empty
    assert len(df) == 2  # Doit être filtré par dates
    assert "production_kwh" in df.columns
    mock_read_csv.assert_called_once_with("test.csv")
    mock_cleaner.clean_production_data.assert_called_once()


@patch("pandas.read_csv")
def test_wind_producer_load_data_file_not_found(mock_read_csv):
    """Test le chargement avec fichier non trouvé."""
    mock_read_csv.side_effect = FileNotFoundError("Fichier non trouvé")

    producer = WindProducer("Test", "Montpellier", 100.0, "test.csv")
    df = producer.load_production_data(date(2024, 1, 1), date(2024, 1, 2))

    assert df.empty
    mock_read_csv.assert_called_once_with("test.csv")


@patch("pandas.read_csv")
@patch("src.producers.wind_producer.DataCleaner")
def test_wind_producer_load_data_empty_file(mock_cleaner, mock_read_csv):
    """Test le chargement avec fichier vide."""
    mock_read_csv.return_value = pd.DataFrame()
    mock_cleaner.clean_production_data.return_value = pd.DataFrame()

    producer = WindProducer("Test", "Montpellier", 100.0, "test.csv")
    df = producer.load_production_data(date(2024, 1, 1), date(2024, 1, 2))

    assert df.empty
    mock_read_csv.assert_called_once_with("test.csv")


def test_wind_producer_calculate_statistics():
    """Test le calcul des statistiques éoliennes."""
    producer = WindProducer("Test", "Montpellier", 100.0, "test.csv")

    with patch.object(producer, "load_production_data") as mock_load:
        mock_load.return_value = pd.DataFrame(
            {
                "date": [date(2024, 1, 1), date(2024, 1, 2)],
                "production_kwh": [80.5, 75.2],
            }
        )

        stats = producer.calculate_statistics(date(2024, 1, 1), date(2024, 1, 2))

        assert "total_production" in stats
        assert "average_daily_production" in stats
        assert "max_daily_production" in stats
        assert "min_daily_production" in stats
        assert "capacity_factor" in stats
        assert stats["total_production"] == 155.7
        assert stats["average_daily_production"] == 77.85
        assert stats["max_daily_production"] == 80.5
        assert stats["min_daily_production"] == 75.2
        assert 0 <= stats["capacity_factor"] <= 1


def test_wind_producer_calculate_statistics_empty_data():
    """Test les statistiques avec données vides."""
    producer = WindProducer("Test", "Montpellier", 100.0, "test.csv")

    with patch.object(producer, "load_production_data") as mock_load:
        mock_load.return_value = pd.DataFrame()

        stats = producer.calculate_statistics(date(2024, 1, 1), date(2024, 1, 2))

        assert stats["total_production"] == 0
        assert stats["average_daily_production"] == 0
        assert stats["max_daily_production"] == 0
        assert stats["min_daily_production"] == 0
        assert stats["capacity_factor"] == 0.0


def test_wind_producer_capacity_factor():
    """Test le calcul du facteur de capacité."""
    producer = WindProducer("Test", "Montpellier", 100.0, "test.csv")

    with patch.object(producer, "load_production_data") as mock_load:
        # Production sur 2 jours : 155.7 kWh
        # Production max possible : 100 kW * 24h * 2 jours = 4800 kWh
        # Facteur de capacité : 155.7 / 4800 ≈ 0.0324
        mock_load.return_value = pd.DataFrame(
            {
                "date": [date(2024, 1, 1), date(2024, 1, 2)],
                "production_kwh": [80.5, 75.2],
            }
        )

        capacity_factor = producer.get_production_capacity_factor(
            date(2024, 1, 1), date(2024, 1, 2)
        )

        assert isinstance(capacity_factor, float)
        assert 0 <= capacity_factor <= 1
        assert abs(capacity_factor - 0.0324) < 0.001


def test_wind_producer_capacity_factor_empty_data():
    """Test le facteur de capacité avec données vides."""
    producer = WindProducer("Test", "Montpellier", 100.0, "test.csv")

    with patch.object(producer, "load_production_data") as mock_load:
        mock_load.return_value = pd.DataFrame()

        capacity_factor = producer.get_production_capacity_factor(
            date(2024, 1, 1), date(2024, 1, 2)
        )

        assert capacity_factor == 0.0
