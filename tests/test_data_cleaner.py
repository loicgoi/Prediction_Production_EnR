import pytest
import pandas as pd
import numpy as np
from src.data_ingestion.utils.data_cleaner import DataCleaner


def test_clean_solar_data():
    """Test le nettoyage des données solaires."""
    df_input = pd.DataFrame(
        {
            "time": ["2024-01-01", "2024-01-02"],
            "temperature_2m_max": [15, 16],
            "shortwave_radiation_sum": [15.5, 16.2],
        }
    )

    df_clean = DataCleaner.clean_solar_data(df_input)

    assert not df_clean.empty
    assert "date" in df_clean.columns
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
