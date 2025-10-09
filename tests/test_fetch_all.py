import pytest
import pandas as pd
from unittest.mock import patch, Mock
from src.data_ingestion.fetchers.fetch_all import fetch_all


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
