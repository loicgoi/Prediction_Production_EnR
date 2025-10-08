import pytest
import pandas as pd
from unittest.mock import patch, Mock
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


@patch("data_ingestion.fetchers.fetch_all.HubeauDataHandler")
@patch("data_ingestion.fetchers.fetch_all.WeatherDataHandler")
@patch("data_ingestion.fetchers.fetch_all.SolarProducer")
@patch("data_ingestion.fetchers.fetch_all.WindProducer")
@patch("data_ingestion.fetchers.fetch_all.HydroProducer")
def test_fetch_all_success(
    mock_hydro_producer,
    mock_wind_producer,
    mock_solar_producer,
    mock_weather_handler,
    mock_hubeau_handler,
):
    """Test la récupération de toutes les données."""
    # Mock HubeauHandler
    mock_hubeau_instance = Mock()
    mock_hubeau_instance.load.return_value = pd.DataFrame({"hydro_data": [1, 2]})
    mock_hubeau_handler.return_value = mock_hubeau_instance

    # Mock WeatherHandler pour solaire
    mock_solar_weather_instance = Mock()
    mock_solar_weather_instance.load.side_effect = [
        pd.DataFrame({"solar_history": [1, 2]}),  # Premier appel: historique
        pd.DataFrame({"solar_forecast": [3, 4]}),  # Deuxième appel: prévision
    ]

    # Mock WeatherHandler pour éolien
    mock_wind_weather_instance = Mock()
    mock_wind_weather_instance.load.side_effect = [
        pd.DataFrame({"wind_history": [5, 6]}),  # Premier appel: historique
        pd.DataFrame({"wind_forecast": [7, 8]}),  # Deuxième appel: prévision
    ]

    # Alterner entre les instances pour solaire et éolien
    mock_weather_handler.side_effect = [
        mock_solar_weather_instance,
        mock_wind_weather_instance,
    ]

    # Mock Producers
    mock_solar_instance = Mock()
    mock_solar_instance.load_production_data.return_value = pd.DataFrame(
        {"solar_production": [9, 10]}
    )
    mock_solar_producer.return_value = mock_solar_instance

    mock_wind_instance = Mock()
    mock_wind_instance.load_production_data.return_value = pd.DataFrame(
        {"wind_production": [11, 12]}
    )
    mock_wind_producer.return_value = mock_wind_instance

    mock_hydro_instance = Mock()
    mock_hydro_instance.load_production_data.return_value = pd.DataFrame(
        {"hydro_production": [13, 14]}
    )
    mock_hydro_producer.return_value = mock_hydro_instance

    # Appel de la fonction - fetch_all n'accepte aucun paramètre
    result = fetch_all()

    # Vérifications - fetch_all retourne un tuple de 8 DataFrames
    assert len(result) == 8
    assert isinstance(result[0], pd.DataFrame)  # df_hydro
    assert isinstance(result[1], pd.DataFrame)  # df_solar_forecast
    assert isinstance(result[2], pd.DataFrame)  # df_solar_history
    assert isinstance(result[3], pd.DataFrame)  # df_wind_forecast
    assert isinstance(result[4], pd.DataFrame)  # df_wind_history
    assert isinstance(result[5], pd.DataFrame)  # production_data["solar"]
    assert isinstance(result[6], pd.DataFrame)  # production_data["wind"]
    assert isinstance(result[7], pd.DataFrame)  # production_data["hydro"]


@patch("data_ingestion.fetchers.fetch_all.WeatherDataHandler")
def test_fetch_weather_data_success(mock_handler):
    """Test la récupération des données météo."""
    mock_instance = Mock()
    # fetch_weather_data retourne un DataFrame, pas un dict
    mock_instance.load.return_value = pd.DataFrame(
        {"temperature": [20, 25], "humidity": [60, 70]}
    )
    mock_handler.return_value = mock_instance

    result = fetch_weather_data(
        latitude=43.6109,
        longitude=3.8763,
        start_date="2024-01-01",
        end_date="2024-01-31",
        data_type="solar",
    )

    # Vérifications - fetch_weather_data retourne un DataFrame
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    # Vérifier que c'est bien un DataFrame avec des colonnes
    assert len(result.columns) > 0


@patch("data_ingestion.fetchers.fetch_all.WeatherDataHandler")
def test_fetch_weather_data_wind(mock_handler):
    """Test la récupération des données météo éoliennes."""
    mock_instance = Mock()
    mock_instance.load.return_value = pd.DataFrame(
        {"wind_speed": [5.0, 7.5], "wind_direction": [180, 200]}
    )
    mock_handler.return_value = mock_instance

    result = fetch_weather_data(
        latitude=43.6109,
        longitude=3.8763,
        start_date="2024-01-01",
        end_date="2024-01-31",
        data_type="wind",
    )

    # Vérifications
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert "wind_speed" in result.columns
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
