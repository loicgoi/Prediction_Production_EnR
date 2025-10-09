import pytest
import pandas as pd
import numpy as np
from src.data_ingestion.utils.data_cleaner import DataCleaner


def test_clean_solar_data():
    """Test le nettoyage des données solaires."""
    df_input = pd.DataFrame(
        {
            "time": ["2024-01-01", "2024-01-02"],
            "sunshine_duration": [36000, 35000],
            "shortwave_radiation_sum": [15.5, 16.2],
        }
    )

    df_clean = DataCleaner.clean_solar_data(df_input)

    assert not df_clean.empty
    assert "date" in df_clean.columns


def test_clean_wind_data():
    """Test le nettoyage des données éoliennes."""
    df_input = pd.DataFrame(
        {"time": ["2024-01-01", "2024-01-02"], "wind_speed_10m_max": [8.5, 9.2]}
    )

    df_clean = DataCleaner.clean_wind_data(df_input)

    assert not df_clean.empty
    assert "date" in df_clean.columns


def test_clean_hydro_data():
    """Test le nettoyage des données hydrauliques."""
    df_input = pd.DataFrame(
        {"date_obs_elab": ["2024-01-01", "2024-01-02"], "result_obs_elab": [10.5, 11.2]}
    )

    df_clean = DataCleaner.clean_hydro_data(df_input)

    assert not df_clean.empty
    assert "date" in df_clean.columns
    assert "debit_l_s" in df_clean.columns


def test_clean_production_data_solar():
    """Test le nettoyage des données de production solaire."""
    df_input = pd.DataFrame(
        {"date": ["2024-01-01", "2024-01-02"], "prod_solaire": [150.5, 160.2]}
    )

    df_clean = DataCleaner.clean_production_data(df_input, "solar")

    assert not df_clean.empty
    assert "production_kwh" in df_clean.columns


def test_clean_production_data_wind():
    """Test le nettoyage des données de production éolienne."""
    df_input = pd.DataFrame(
        {"date": ["2024-01-01", "2024-01-02"], "prod_eolienne": [80.5, 75.2]}
    )

    df_clean = DataCleaner.clean_production_data(df_input, "wind")

    assert not df_clean.empty
    assert "production_kwh" in df_clean.columns


def test_clean_production_data_hydro():
    """Test le nettoyage des données de production hydraulique."""
    df_input = pd.DataFrame(
        {"date_obs_elab": ["2024-01-01", "2024-01-02"], "prod_hydro": [180.5, 195.2]}
    )

    df_clean = DataCleaner.clean_production_data(df_input, "hydro")

    assert not df_clean.empty
    assert "production_kwh" in df_clean.columns


def test_remove_duplicates():
    """Test la suppression des doublons."""
    df_input = pd.DataFrame(
        {"date": ["2024-01-01", "2024-01-01", "2024-01-02"], "value": [1, 2, 3]}
    )

    df_clean = DataCleaner._remove_duplicates(df_input, "date")

    assert len(df_clean) == 2  # Un doublon supprimé


def test_handle_missing_values():
    """Test la gestion des valeurs manquantes."""
    df_input = pd.DataFrame({"value1": [1, np.nan, 3], "value2": [4, 5, np.nan]})

    df_clean = DataCleaner._handle_missing_values(df_input)

    assert not df_clean.isnull().any().any()


def test_convert_solar_units():
    """Test la conversion des unités solaires."""
    df_input = pd.DataFrame(
        {
            "sunshine_duration": [36000, 72000],
            "daylight_duration": [36000, 72000],
            "shortwave_radiation_sum": [1.0, 2.0],
        }
    )

    df_clean = DataCleaner._convert_solar_units(df_input)

    assert "sunshine_duration_h" in df_clean.columns
    assert "daylight_duration_h" in df_clean.columns
    assert "shortwave_radiation_sum_kwh_m2" in df_clean.columns
    assert df_clean["sunshine_duration_h"].iloc[0] == 10.0
