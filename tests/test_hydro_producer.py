import pytest
import pandas as pd
from datetime import date
from unittest.mock import Mock, patch
<<<<<<< HEAD
<<<<<<< HEAD
from src.producers.hydro_producer import HydroProducer
=======
from producers.hydro_producer import HydroProducer
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
=======
from src.producers.hydro_producer import HydroProducer
>>>>>>> 5594093 (màj des test + commentires code + README.md)


def test_hydro_producer_initialization():
    """Test l'initialisation du producteur hydraulique."""
    with patch("src.producers.hydro_producer.SupabaseHandler") as mock_handler:
        mock_instance = Mock()
        mock_handler.return_value = mock_instance

        producer = HydroProducer(
            "Centrale hydro", "Montpellier", 200.0, "data/raw/prod_hydro.csv"
        )

        assert producer.name == "Centrale hydro"
        assert producer.location == "Montpellier"
        assert producer.nominal_power == 200.0
        assert producer.data_file == "data/raw/prod_hydro.csv"


<<<<<<< HEAD
<<<<<<< HEAD
@patch("pandas.read_csv")
@patch("src.producers.hydro_producer.DataCleaner")
def test_hydro_producer_load_data_success(mock_cleaner, mock_read_csv):
    """Test le chargement réussi des données hydrauliques."""
    # Mock de read_csv
    mock_read_csv.return_value = pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "prod_hydro": [180.5, 195.2, 170.8],
        }
    )

    # Mock du cleaner
    mock_cleaner.clean_production_data.return_value = pd.DataFrame(
        {
            "date": [date(2024, 1, 1), date(2024, 1, 2), date(2024, 1, 3)],
            "production_kwh": [180.5, 195.2, 170.8],
        }
=======
@patch("producers.hydro_producer.CSVDataHandler")
@patch("producers.hydro_producer.DataCleaner")
=======
@patch("src.producers.hydro_producer.SupabaseHandler")
@patch("src.producers.hydro_producer.DataCleaner")
>>>>>>> 5594093 (màj des test + commentires code + README.md)
def test_hydro_producer_load_data(mock_cleaner, mock_handler):
    """Test le chargement des données hydrauliques."""
    mock_instance = Mock()
    mock_instance.load.return_value = pd.DataFrame(
        {"date": ["2024-01-01", "2024-01-02"], "prod_hydro": [180.5, 195.2]}
    )
    mock_handler.return_value = mock_instance

    mock_cleaner.clean_production_data.return_value = pd.DataFrame(
        {"date": ["2024-01-01", "2024-01-02"], "production_kwh": [180.5, 195.2]}
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
    )

    producer = HydroProducer("Test", "Montpellier", 200.0, "test.csv")
    df = producer.load_production_data(date(2024, 1, 1), date(2024, 1, 2))

    assert not df.empty
<<<<<<< HEAD
    assert len(df) == 2  # Doit être filtré par dates
    assert "production_kwh" in df.columns
    mock_read_csv.assert_called_once_with("test.csv")
    mock_cleaner.clean_production_data.assert_called_once()


@patch("pandas.read_csv")
@patch("src.producers.hydro_producer.DataCleaner")
def test_hydro_producer_load_data_with_date_obs_elab(mock_cleaner, mock_read_csv):
    """Test le chargement avec colonne date_obs_elab."""
    # Mock de read_csv avec date_obs_elab (cas spécial hydro)
    mock_read_csv.return_value = pd.DataFrame(
        {
            "date_obs_elab": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "prod_hydro": [180.5, 195.2, 170.8],
        }
    )

    # Mock du cleaner qui convertit date_obs_elab en date
    mock_cleaner.clean_production_data.return_value = pd.DataFrame(
        {
            "date": [date(2024, 1, 1), date(2024, 1, 2), date(2024, 1, 3)],
            "production_kwh": [180.5, 195.2, 170.8],
        }
    )

    producer = HydroProducer("Test", "Montpellier", 200.0, "test.csv")
    df = producer.load_production_data(date(2024, 1, 1), date(2024, 1, 2))

    assert not df.empty
    mock_read_csv.assert_called_once_with("test.csv")
    mock_cleaner.clean_production_data.assert_called_once()


@patch("pandas.read_csv")
def test_hydro_producer_load_data_file_not_found(mock_read_csv):
    """Test le chargement avec fichier non trouvé."""
    mock_read_csv.side_effect = FileNotFoundError("Fichier non trouvé")

    producer = HydroProducer("Test", "Montpellier", 200.0, "test.csv")
    df = producer.load_production_data(date(2024, 1, 1), date(2024, 1, 2))

    assert df.empty
    mock_read_csv.assert_called_once_with("test.csv")


@patch("pandas.read_csv")
@patch("src.producers.hydro_producer.DataCleaner")
def test_hydro_producer_load_data_empty_file(mock_cleaner, mock_read_csv):
    """Test le chargement avec fichier vide."""
    mock_read_csv.return_value = pd.DataFrame()
    mock_cleaner.clean_production_data.return_value = pd.DataFrame()

    producer = HydroProducer("Test", "Montpellier", 200.0, "test.csv")
    df = producer.load_production_data(date(2024, 1, 1), date(2024, 1, 2))

    assert df.empty
    mock_read_csv.assert_called_once_with("test.csv")


=======
    mock_cleaner.clean_production_data.assert_called_once()


>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
def test_hydro_producer_calculate_statistics():
    """Test le calcul des statistiques hydrauliques."""
    with patch("src.producers.hydro_producer.SupabaseHandler") as mock_handler:
        mock_instance = Mock()
        mock_handler.return_value = mock_instance

        producer = HydroProducer("Test", "Montpellier", 200.0, "test.csv")

        with patch.object(producer, "load_production_data") as mock_load:
            mock_load.return_value = pd.DataFrame(
                {
                    "date": [date(2024, 1, 1), date(2024, 1, 2)],
                    "production_kwh": [180.5, 195.2],
                }
            )

<<<<<<< HEAD
        assert "total_production" in stats
        assert "average_daily_production" in stats
<<<<<<< HEAD
        assert "max_daily_production" in stats
        assert "min_daily_production" in stats
        assert "capacity_factor" in stats
        assert stats["total_production"] == 375.7
        assert stats["average_daily_production"] == 187.85
        assert stats["max_daily_production"] == 195.2
        assert stats["min_daily_production"] == 180.5
        assert 0 <= stats["capacity_factor"] <= 1


def test_hydro_producer_calculate_statistics_empty_data():
    """Test les statistiques avec données vides."""
    producer = HydroProducer("Test", "Montpellier", 200.0, "test.csv")

    with patch.object(producer, "load_production_data") as mock_load:
        mock_load.return_value = pd.DataFrame()

        stats = producer.calculate_statistics(date(2024, 1, 1), date(2024, 1, 2))

        assert stats["total_production"] == 0
        assert stats["average_daily_production"] == 0
        assert stats["max_daily_production"] == 0
        assert stats["min_daily_production"] == 0
        assert stats["capacity_factor"] == 0.0


def test_hydro_producer_capacity_factor():
    """Test le calcul du facteur de capacité."""
    producer = HydroProducer("Test", "Montpellier", 200.0, "test.csv")

    with patch.object(producer, "load_production_data") as mock_load:
        # Production sur 2 jours : 375.7 kWh
        # Production max possible : 200 kW * 24h * 2 jours = 9600 kWh
        # Facteur de capacité : 375.7 / 9600 ≈ 0.0391
        mock_load.return_value = pd.DataFrame(
            {
                "date": [date(2024, 1, 1), date(2024, 1, 2)],
                "production_kwh": [180.5, 195.2],
            }
        )

        capacity_factor = producer.get_production_capacity_factor(
            date(2024, 1, 1), date(2024, 1, 2)
        )

        assert isinstance(capacity_factor, float)
        assert 0 <= capacity_factor <= 1
        assert abs(capacity_factor - 0.0391) < 0.001


def test_hydro_producer_capacity_factor_empty_data():
    """Test le facteur de capacité avec données vides."""
    producer = HydroProducer("Test", "Montpellier", 200.0, "test.csv")

    with patch.object(producer, "load_production_data") as mock_load:
        mock_load.return_value = pd.DataFrame()

        capacity_factor = producer.get_production_capacity_factor(
            date(2024, 1, 1), date(2024, 1, 2)
        )

        assert capacity_factor == 0.0


def test_hydro_producer_logger():
    """Test que le logger est correctement initialisé."""
    producer = HydroProducer("Test", "Montpellier", 200.0, "test.csv")
    assert producer.logger is not None
    assert producer.logger.name == "HydroProducer"
=======
        assert stats["total_production"] == 375.7
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
=======
            stats = producer.calculate_statistics(date(2024, 1, 1), date(2024, 1, 2))

            assert "total_production" in stats
            assert "average_daily_production" in stats
            assert stats["total_production"] == 375.7
>>>>>>> 5594093 (màj des test + commentires code + README.md)
