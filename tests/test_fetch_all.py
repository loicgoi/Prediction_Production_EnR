import pytest
import pandas as pd
from unittest.mock import patch, Mock
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
