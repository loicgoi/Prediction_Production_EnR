from data_ingestion.api.api_config import HUBEAU_CONFIG, OPEN_METEO_CONFIG, DATA_FILES


def test_hubeau_config():
    """Test la configuration Hub'Eau."""
    assert (
        HUBEAU_CONFIG["url"]
        == "https://hubeau.eaufrance.fr/api/v2/hydrometrie/obs_elab"
    )
    assert HUBEAU_CONFIG["params"]["grandeur_hydro_elab"] == "QmnJ"
    assert HUBEAU_CONFIG["params"]["size"] == 20000


def test_open_meteo_config():
    """Test la configuration Open-Meteo."""
    assert OPEN_METEO_CONFIG["forecast_url"] == "https://api.open-meteo.com/v1/forecast"
    assert (
        OPEN_METEO_CONFIG["archive_url"]
        == "https://archive-api.open-meteo.com/v1/archive"
    )
    assert OPEN_METEO_CONFIG["timezone"] == "Europe/Paris"
    assert OPEN_METEO_CONFIG["forecast_days"] == 16


def test_data_files_config():
    """Test la configuration des fichiers de données."""
    assert DATA_FILES["solar"] == "data/raw/prod_solaire.csv"
    assert DATA_FILES["wind"] == "data/raw/prod_eolienne.csv"
    assert DATA_FILES["hydro"] == "data/raw/prod_hydro.csv"
