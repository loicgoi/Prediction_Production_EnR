import pytest
import pandas as pd
import numpy as np
<<<<<<< HEAD
<<<<<<< HEAD
from src.data_ingestion.utils.data_cleaner import DataCleaner
=======
from data_ingestion.utils.data_cleaner import DataCleaner
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
=======
from src.data_ingestion.utils.data_cleaner import DataCleaner
>>>>>>> 5594093 (màj des test + commentires code + README.md)


def test_clean_solar_data():
    """Test le nettoyage des données solaires."""
    df_input = pd.DataFrame(
        {
            "time": ["2024-01-01", "2024-01-02"],
<<<<<<< HEAD
<<<<<<< HEAD
            "temperature_2m_max": [15, 16],
=======
            "sunshine_duration": [36000, 35000],
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
=======
            "temperature_2m_max": [15, 16],
>>>>>>> b6ddba9 (update tests)
            "shortwave_radiation_sum": [15.5, 16.2],
        }
    )

    df_clean = DataCleaner.clean_solar_data(df_input)

    assert not df_clean.empty
    assert "date" in df_clean.columns
<<<<<<< HEAD
<<<<<<< HEAD
    assert "shortwave_radiation_sum_kwh_m2" in df_clean.columns


def test_prepare_solar_data_raw():
    """Test la préparation des données solaires brutes."""
    df_input = pd.DataFrame(
        {
            "time": ["2024-01-01", "2024-01-02"],
            "shortwave_radiation_sum": [15.5, 16.2],
        }
    )

    df_raw = DataCleaner.prepare_solar_data_raw(df_input)

    assert not df_raw.empty
    assert "shortwave_radiation_sum" in df_raw.columns
=======
=======
    assert "shortwave_radiation_sum_kwh_m2" in df_clean.columns
>>>>>>> b6ddba9 (update tests)


def test_prepare_solar_data_raw():
    """Test la préparation des données solaires brutes."""
    df_input = pd.DataFrame(
        {
            "time": ["2024-01-01", "2024-01-02"],
            "shortwave_radiation_sum": [15.5, 16.2],
        }
    )

    df_raw = DataCleaner.prepare_solar_data_raw(df_input)

<<<<<<< HEAD
    assert "sunshine_duration_h" in df_clean.columns
    assert "daylight_duration_h" in df_clean.columns
    assert "shortwave_radiation_sum_kwh_m2" in df_clean.columns
    assert df_clean["sunshine_duration_h"].iloc[0] == 10.0
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
=======
    assert not df_raw.empty
    assert "shortwave_radiation_sum" in df_raw.columns
>>>>>>> b6ddba9 (update tests)
