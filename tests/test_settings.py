import pytest
from src.config.settings import settings


def test_settings_loaded():
    """Test que les paramètres sont chargés correctement."""
    assert settings.supabase_url is not None
    assert settings.supabase_key is not None
    assert settings.montpellier_latitude == 43.6109
    assert settings.montpellier_longitude == 3.8763
    assert settings.api_host == "0.0.0.0"
    assert settings.api_port == 8000


def test_nominal_powers():
    """Test des puissances nominales des producteurs."""
    assert settings.solar_nominal_power == 150.0
    assert settings.wind_nominal_power == 100.0
    assert settings.hydro_nominal_power == 200.0
