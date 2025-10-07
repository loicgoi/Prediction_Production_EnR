import sys
from pathlib import Path

# Détermination automatique du chemin absolu vers src/
ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

print(f"Ajout du dossier src : {SRC_DIR}")
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

print(f"sys.path actuel : {sys.path[:3]}")  # vérification rapide

import pytest
import pandas as pd
from datetime import date


# === FIXTURES ===
@pytest.fixture
def mock_solar_data():
    """Données solaires mockées"""
    dates = pd.date_range(start="2024-01-01", end="2024-01-05", freq="D")
    return pd.DataFrame(
        {
            "time": dates,
            "shortwave_radiation_sum": [10.5, 12.3, 8.7, 15.2, 9.8],
            "sunshine_duration": [36000, 38000, 32000, 40000, 34000],
            "temperature_2m_max": [15.2, 16.8, 14.1, 18.3, 15.7],
        }
    )


@pytest.fixture
def mock_wind_data():
    """Données éoliennes mockées"""
    dates = pd.date_range(start="2024-01-01", end="2024-01-05", freq="D")
    return pd.DataFrame(
        {
            "time": dates,
            "wind_speed_10m_max": [12.5, 15.3, 10.7, 18.2, 11.8],
            "wind_direction_10m_dominant": [180, 190, 170, 200, 175],
        }
    )


@pytest.fixture
def mock_production_data():
    """Données de production mockées"""
    dates = pd.date_range(start="2024-01-01", end="2024-01-05", freq="D")
    return pd.DataFrame(
        {"date": dates, "production_kwh": [120.5, 135.2, 98.7, 156.3, 112.8]}
    )


@pytest.fixture
def mock_hydro_data():
    """Données hydrauliques mockées"""
    dates = pd.date_range(start="2024-01-01", end="2024-01-05", freq="D")
    return pd.DataFrame(
        {"date_obs_elab": dates, "result_obs_elab": [45.5, 52.3, 38.7, 65.2, 42.8]}
    )


@pytest.fixture
def test_dates():
    """Dates de test"""
    return {"start_date": date(2024, 1, 1), "end_date": date(2024, 1, 5)}
