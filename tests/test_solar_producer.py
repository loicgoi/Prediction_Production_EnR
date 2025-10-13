import pytest
import pandas as pd
from datetime import date
from unittest.mock import Mock, patch
from src.producers.solar_producer import SolarProducer


def test_solar_producer_initialization():
    """Test l'initialisation du producteur solaire."""
    producer = SolarProducer(
        "Parc solaire", "Montpellier", 150.0, "data/raw/prod_solaire.csv"
    )

    assert producer.name == "Parc solaire"
    assert producer.location == "Montpellier"
    assert producer.nominal_power == 150.0
    assert producer.data_file == "data/raw/prod_solaire.csv"


@patch("pandas.read_csv")
@patch("src.producers.solar_producer.DataCleaner")
def test_solar_producer_load_data_success(mock_cleaner, mock_read_csv):
    """Test le chargement réussi des données solaires."""
    # Mock de read_csv
    mock_read_csv.return_value = pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "prod_solaire": [150.5, 160.2, 140.8],
        }
    )

    # Mock du cleaner
    mock_cleaner.clean_production_data.return_value = pd.DataFrame(
        {
            "date": [date(2024, 1, 1), date(2024, 1, 2), date(2024, 1, 3)],
            "production_kwh": [150.5, 160.2, 140.8],
        }
    )

    producer = SolarProducer("Test", "Montpellier", 150.0, "test.csv")
    df = producer.load_production_data(date(2024, 1, 1), date(2024, 1, 2))

    assert not df.empty
    assert len(df) == 2  # Doit être filtré par dates
    assert "production_kwh" in df.columns
    mock_read_csv.assert_called_once_with("test.csv")
    mock_cleaner.clean_production_data.assert_called_once()


@patch("pandas.read_csv")
def test_solar_producer_load_data_file_not_found(mock_read_csv):
    """Test le chargement avec fichier non trouvé."""
    mock_read_csv.side_effect = FileNotFoundError("Fichier non trouvé")

    producer = SolarProducer("Test", "Montpellier", 150.0, "test.csv")
    df = producer.load_production_data(date(2024, 1, 1), date(2024, 1, 2))

    assert df.empty
    mock_read_csv.assert_called_once_with("test.csv")


@patch("pandas.read_csv")
@patch("src.producers.solar_producer.DataCleaner")
def test_solar_producer_load_data_empty_file(mock_cleaner, mock_read_csv):
    """Test le chargement avec fichier vide."""
    mock_read_csv.return_value = pd.DataFrame()
    mock_cleaner.clean_production_data.return_value = pd.DataFrame()

    producer = SolarProducer("Test", "Montpellier", 150.0, "test.csv")
    df = producer.load_production_data(date(2024, 1, 1), date(2024, 1, 2))

    assert df.empty
    mock_read_csv.assert_called_once_with("test.csv")


def test_solar_producer_calculate_statistics():
    """Test le calcul des statistiques solaires."""
    producer = SolarProducer("Test", "Montpellier", 150.0, "test.csv")

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
        assert "max_daily_production" in stats
        assert "min_daily_production" in stats
        assert "capacity_factor" in stats
        assert stats["total_production"] == 310.7
        assert stats["average_daily_production"] == 155.35
        assert stats["max_daily_production"] == 160.2
        assert stats["min_daily_production"] == 150.5
        assert 0 <= stats["capacity_factor"] <= 1


def test_solar_producer_calculate_statistics_empty_data():
    """Test les statistiques avec données vides."""
    producer = SolarProducer("Test", "Montpellier", 150.0, "test.csv")

    with patch.object(producer, "load_production_data") as mock_load:
        mock_load.return_value = pd.DataFrame()

        stats = producer.calculate_statistics(date(2024, 1, 1), date(2024, 1, 2))

        assert stats["total_production"] == 0
        assert stats["average_daily_production"] == 0
        assert stats["max_daily_production"] == 0
        assert stats["min_daily_production"] == 0
        assert stats["capacity_factor"] == 0.0


def test_solar_producer_capacity_factor():
    """Test le calcul du facteur de capacité."""
    producer = SolarProducer("Test", "Montpellier", 150.0, "test.csv")

    with patch.object(producer, "load_production_data") as mock_load:
        # Production sur 2 jours : 310.7 kWh
        # Production max possible : 150 kW * 24h * 2 jours = 7200 kWh
        # Facteur de capacité : 310.7 / 7200 ≈ 0.043
        mock_load.return_value = pd.DataFrame(
            {
                "date": [date(2024, 1, 1), date(2024, 1, 2)],
                "production_kwh": [150.5, 160.2],
            }
        )

        capacity_factor = producer.get_production_capacity_factor(
            date(2024, 1, 1), date(2024, 1, 2)
        )

        assert isinstance(capacity_factor, float)
        assert 0 <= capacity_factor <= 1
        assert abs(capacity_factor - 0.043) < 0.001


def test_solar_producer_capacity_factor_empty_data():
    """Test le facteur de capacité avec données vides."""
    producer = SolarProducer("Test", "Montpellier", 150.0, "test.csv")

    with patch.object(producer, "load_production_data") as mock_load:
        mock_load.return_value = pd.DataFrame()

        capacity_factor = producer.get_production_capacity_factor(
            date(2024, 1, 1), date(2024, 1, 2)
        )

        assert capacity_factor == 0.0
