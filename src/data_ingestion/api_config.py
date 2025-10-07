# Configuration Hub'Eau
HUBEAU_CONFIG = {
    "url": "https://hubeau.eaufrance.fr/api/v2/hydrometrie/obs_elab",
    "params": {
        "grandeur_hydro_elab": "QmnJ",
        "size": 20000,
    },
}

# Configuration Open-Meteo
OPEN_METEO_CONFIG = {
    "forecast_url": "https://api.open-meteo.com/v1/forecast",
    "archive_url": "https://archive-api.open-meteo.com/v1/archive",
    "timezone": "Europe/Paris",
    "forecast_days": 16,
}

# Configuration des fichiers de données
DATA_FILES = {
    "solar": "data/raw/prod_solaire.csv",
    "wind": "data/raw/prod_eolienne.csv",
    "hydro": "data/raw/prod_hydro.csv",
}
