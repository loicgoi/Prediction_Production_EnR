import pytest
import pandas as pd
from unittest.mock import patch, Mock
<<<<<<< HEAD
<<<<<<< HEAD
from src.data_ingestion.fetchers.fetch_all import fetch_all


@patch("src.data_ingestion.fetchers.fetch_all.SupabaseHandler")
@patch("src.data_ingestion.fetchers.fetch_all.WeatherDataHandler")
@patch("src.data_ingestion.fetchers.fetch_all.HubeauDataHandler")
@patch("src.data_ingestion.fetchers.fetch_all.DataUploader")
@patch("pandas.read_csv")
@patch("os.path.exists")
def test_fetch_all_success(
    mock_exists,
    mock_read_csv,
    mock_data_uploader,
    mock_hubeau_handler,
    mock_weather_handler,
    mock_supabase_handler,
):
    """Test la récupération de toutes les données."""
    # Mock des chemins existants
    mock_exists.return_value = True

    # Mock SupabaseHandler et DataUploader
    mock_supabase_instance = Mock()
    mock_supabase_handler.return_value = mock_supabase_instance

    mock_uploader_instance = Mock()
    mock_data_uploader.return_value = mock_uploader_instance

    # Mock WeatherDataHandler pour solaire et éolien
    mock_solar_instance = Mock()
    mock_wind_instance = Mock()

    # Configurer les retours pour load()
    mock_solar_instance.load.side_effect = [
        pd.DataFrame({"date": ["2024-01-01"], "solar_forecast": [1]}),
        pd.DataFrame({"date": ["2024-01-01"], "solar_history": [3]}),
    ]
    mock_wind_instance.load.side_effect = [
        pd.DataFrame({"date": ["2024-01-01"], "wind_forecast": [5]}),
        pd.DataFrame({"date": ["2024-01-01"], "wind_history": [7]}),
    ]

    mock_weather_handler.side_effect = [mock_solar_instance, mock_wind_instance]

    # Mock HubeauDataHandler
    mock_hubeau_instance = Mock()
    mock_hubeau_instance.load.return_value = pd.DataFrame(
        {"date": ["2024-01-01"], "hubeau_data": [9]}
    )
    mock_hubeau_instance.clean.return_value = None
    mock_hubeau_handler.return_value = mock_hubeau_instance

    # Mock pandas.read_csv
    mock_read_csv.return_value = pd.DataFrame(
        {"date": ["2024-01-01", "2024-01-02"], "production": [11, 12]}
    )

    # Appel de la fonction
    result = fetch_all()

    # VÉRIFICATIONS CORRIGÉES
    assert isinstance(result, dict)
    assert "hubeau" in result
    assert "solar_forecast" in result
    assert "solar_history" in result
    assert "wind_forecast" in result
    assert "wind_history" in result
    assert "prod_solaire" in result
    assert "prod_eolienne" in result
    assert "prod_hydro" in result

    # Vérifier que les méthodes d'upload ont été appelées
    assert mock_uploader_instance.upload_raw_dataset.call_count >= 1
    assert mock_uploader_instance.upload_clean_dataset.call_count >= 1


@patch("src.data_ingestion.fetchers.fetch_all.SupabaseHandler")
@patch("src.data_ingestion.fetchers.fetch_all.WeatherDataHandler")
@patch("src.data_ingestion.fetchers.fetch_all.HubeauDataHandler")
@patch("src.data_ingestion.fetchers.fetch_all.DataUploader")
@patch("os.path.exists")
def test_fetch_all_with_empty_data(
    mock_exists,
    mock_data_uploader,
    mock_hubeau_handler,
    mock_weather_handler,
    mock_supabase_handler,
):
    """Test fetch_all avec des données vides."""
    # Mock des chemins non existants
    mock_exists.return_value = False

    # Mock instances
    mock_supabase_instance = Mock()
    mock_supabase_handler.return_value = mock_supabase_instance

    mock_uploader_instance = Mock()
    mock_data_uploader.return_value = mock_uploader_instance

    # Mock handlers avec données vides
    mock_solar_instance = Mock()
    mock_wind_instance = Mock()
    mock_solar_instance.load.return_value = pd.DataFrame()
    mock_wind_instance.load.return_value = pd.DataFrame()
    mock_weather_handler.side_effect = [mock_solar_instance, mock_wind_instance]

    mock_hubeau_instance = Mock()
    mock_hubeau_instance.load.return_value = pd.DataFrame()
    mock_hubeau_handler.return_value = mock_hubeau_instance

    # Appel de la fonction
    result = fetch_all()

    # Vérifications avec DataFrames vides
    assert isinstance(result, dict)
    assert result["hubeau"].empty
    assert result["solar_forecast"].empty
    assert result["solar_history"].empty
=======
from data_ingestion.fetchers.fetch_all import fetch_all, fetch_weather_data
=======
from src.data_ingestion.fetchers.fetch_all import fetch_all
>>>>>>> 5594093 (màj des test + commentires code + README.md)


@patch("src.data_ingestion.fetchers.fetch_all.SupabaseHandler")
@patch("src.data_ingestion.fetchers.fetch_all.WeatherDataHandler")
@patch("src.data_ingestion.fetchers.fetch_all.HubeauDataHandler")
@patch("src.data_ingestion.fetchers.fetch_all.CSVDataHandler")
@patch("pandas.read_csv")
@patch("os.path.exists")
def test_fetch_all_success(
    mock_exists,
    mock_read_csv,
    mock_csv_handler,
    mock_hubeau_handler,
    mock_weather_handler,
    mock_supabase_handler,
):
    """Test la récupération de toutes les données."""
    # Mock des chemins existants
    mock_exists.return_value = True

    # Mock SupabaseHandler
    mock_supabase_instance = Mock()
    mock_supabase_handler.return_value = mock_supabase_instance

    # Mock CSVDataHandler
    mock_csv_instance = Mock()
    mock_csv_handler.return_value = mock_csv_instance

    # Mock WeatherDataHandler pour solaire et éolien
    mock_solar_instance = Mock()
    mock_wind_instance = Mock()

    # Configurer les retours pour load()
    mock_solar_instance.load.side_effect = [
        pd.DataFrame({"solar_forecast": [1, 2]}),  # Premier appel: forecast=True
        pd.DataFrame({"solar_history": [3, 4]}),  # Deuxième appel: forecast=False
    ]
    mock_wind_instance.load.side_effect = [
        pd.DataFrame({"wind_forecast": [5, 6]}),  # Premier appel: forecast=True
        pd.DataFrame({"wind_history": [7, 8]}),  # Deuxième appel: forecast=False
    ]

    # Alterner entre les instances
    mock_weather_handler.side_effect = [mock_solar_instance, mock_wind_instance]

    # Mock HubeauDataHandler
    mock_hubeau_instance = Mock()
    mock_hubeau_instance.load.return_value = pd.DataFrame({"hubeau_data": [9, 10]})
    mock_hubeau_instance.clean.return_value = None
    mock_hubeau_handler.return_value = mock_hubeau_instance

    # Mock pandas.read_csv
    mock_read_csv.return_value = pd.DataFrame({"production": [11, 12]})

    # Appel de la fonction
    result = fetch_all()

    # Vérifications
<<<<<<< HEAD
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert "wind_speed" in result.columns
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
=======
    assert isinstance(result, dict)
    assert "hubeau" in result
    assert "solar_forecast" in result
    assert "solar_history" in result
    assert "wind_forecast" in result
    assert "wind_history" in result
    assert "solar_production" in result
    assert "wind_production" in result
    assert "hydro_production" in result

    # Vérifier que upload_to_supabase a été appelé
    assert mock_csv_instance.upload_to_supabase.call_count >= 1


@patch("src.data_ingestion.fetchers.fetch_all.SupabaseHandler")
@patch("src.data_ingestion.fetchers.fetch_all.WeatherDataHandler")
@patch("src.data_ingestion.fetchers.fetch_all.HubeauDataHandler")
@patch("src.data_ingestion.fetchers.fetch_all.CSVDataHandler")
@patch("os.path.exists")
def test_fetch_all_with_empty_data(
    mock_exists,
    mock_csv_handler,
    mock_hubeau_handler,
    mock_weather_handler,
    mock_supabase_handler,
):
    """Test fetch_all avec des données vides."""
    # Mock des chemins non existants
    mock_exists.return_value = False

    # Mock instances
    mock_supabase_instance = Mock()
    mock_supabase_handler.return_value = mock_supabase_instance

    mock_csv_instance = Mock()
    mock_csv_handler.return_value = mock_csv_instance

    # Mock handlers avec données vides
    mock_solar_instance = Mock()
    mock_wind_instance = Mock()
    mock_solar_instance.load.return_value = pd.DataFrame()
    mock_wind_instance.load.return_value = pd.DataFrame()
    mock_weather_handler.side_effect = [mock_solar_instance, mock_wind_instance]

    mock_hubeau_instance = Mock()
    mock_hubeau_instance.load.return_value = pd.DataFrame()
    mock_hubeau_handler.return_value = mock_hubeau_instance

    # Appel de la fonction
    result = fetch_all()

    # Vérifications avec DataFrames vides
    assert isinstance(result, dict)
    assert result["hubeau"].empty
    assert result["solar_forecast"].empty
    assert result["solar_history"].empty
>>>>>>> 5594093 (màj des test + commentires code + README.md)
