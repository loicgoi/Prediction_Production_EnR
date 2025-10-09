import pandas as pd
import requests


def get_solar_forecast(
<<<<<<< HEAD
<<<<<<< HEAD
    latitude: float, longitude: float, start_date: str = None, end_date: str = None
) -> pd.DataFrame:
    """
    Prévisions solaires journalières optimisées pour la prédiction de production.
=======
    latitude: float, longitude: float, start_date: str, end_date: str
) -> pd.DataFrame:
    """
    Prévisions solaires journalières (jusqu'à 16 jours) via Open-Meteo API.
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
=======
    latitude: float, longitude: float, start_date: str = None, end_date: str = None
) -> pd.DataFrame:
    """
    Prévisions solaires journalières optimisées pour la prédiction de production.
>>>>>>> 65ccff1 (refacto code + ajout du main.py fonctionnel)
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
<<<<<<< HEAD
<<<<<<< HEAD
        "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,shortwave_radiation_sum,sunshine_duration,daylight_duration,cloud_cover_mean,relative_humidity_2m_mean,precipitation_sum,wind_speed_10m_mean",
        "timezone": "Europe/Paris",
        "forecast_days": 16,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame(data["daily"])
    if "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"])

    return df
=======
        "start_date": start_date,
        "end_date": end_date,
        "daily": [
            "cloud_cover_max",
            "cloud_cover_min",
            "temperature_2m_mean",
            "apparent_temperature_mean",
            "shortwave_radiation_sum",
            "sunshine_duration",
            "cloud_cover_mean",
            "uv_index_max",
            "uv_index_clear_sky_max",
            "precipitation_sum",
            "precipitation_hours",
            "relative_humidity_2m_mean",
            "wind_speed_10m_mean",
            "wind_gusts_10m_mean",
            "sunrise",
            "sunset",
            "daylight_duration",
            "temperature_2m_max",
            "temperature_2m_min",
        ],
        "current": "cloud_cover",
=======
        "daily": "shortwave_radiation_sum,cloud_cover_mean,precipitation_sum,temperature_2m_max,temperature_2m_min,relative_humidity_2m_mean,wind_speed_10m_mean",
        "timezone": "Europe/Paris",
>>>>>>> 65ccff1 (refacto code + ajout du main.py fonctionnel)
        "forecast_days": 16,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
<<<<<<< HEAD
    return pd.DataFrame(response.json()["daily"])
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
=======
    data = response.json()

    df = pd.DataFrame(data["daily"])
    if "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"])

    return df
>>>>>>> 65ccff1 (refacto code + ajout du main.py fonctionnel)


def get_solar_history(
    latitude: float, longitude: float, start_date: str, end_date: str
) -> pd.DataFrame:
    """
<<<<<<< HEAD
<<<<<<< HEAD
    Données historiques solaires optimisées pour l'entraînement des modèles.
=======
    Données historiques solaires journalières via Open-Meteo archive API.
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
=======
    Données historiques solaires optimisées pour l'entraînement des modèles.
>>>>>>> 65ccff1 (refacto code + ajout du main.py fonctionnel)
    """
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
<<<<<<< HEAD
<<<<<<< HEAD
        "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,shortwave_radiation_sum,sunshine_duration,daylight_duration,cloud_cover_mean,relative_humidity_2m_mean,precipitation_sum,wind_speed_10m_mean",
        "timezone": "Europe/Paris",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame(data["daily"])
    if "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"])

    return df
=======
        "daily": [
            "sunrise",
            "sunset",
            "daylight_duration",
            "sunshine_duration",
            "precipitation_sum",
            "temperature_2m_max",
            "temperature_2m_min",
            "shortwave_radiation_sum",
            "cloud_cover_mean",
            "precipitation_hours",
            "relative_humidity_2m_mean",
            "wind_gusts_10m_mean",
            "wind_speed_10m_mean",
        ],
=======
        "daily": "shortwave_radiation_sum,cloud_cover_mean,precipitation_sum,temperature_2m_max,temperature_2m_min,relative_humidity_2m_mean,wind_speed_10m_mean",
        "timezone": "Europe/Paris",
>>>>>>> 65ccff1 (refacto code + ajout du main.py fonctionnel)
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
<<<<<<< HEAD
    return pd.DataFrame(response.json()["daily"])
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
=======
    data = response.json()

    df = pd.DataFrame(data["daily"])
    if "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"])

    return df
>>>>>>> 65ccff1 (refacto code + ajout du main.py fonctionnel)
