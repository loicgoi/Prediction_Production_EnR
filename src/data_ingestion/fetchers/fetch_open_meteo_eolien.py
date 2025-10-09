import pandas as pd
import requests


def get_wind_forecast(
<<<<<<< HEAD
<<<<<<< HEAD
    latitude: float, longitude: float, start_date: str = None, end_date: str = None
=======
    latitude: float, longitude: float, start_date: str, end_date: str
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
=======
    latitude: float, longitude: float, start_date: str = None, end_date: str = None
>>>>>>> 65ccff1 (refacto code + ajout du main.py fonctionnel)
) -> pd.DataFrame:
    """
    Prévisions éoliennes journalières via Open-Meteo API.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
<<<<<<< HEAD
<<<<<<< HEAD
        "daily": "wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant,wind_gusts_10m_mean,temperature_2m_mean,surface_pressure_mean,cloud_cover_mean",
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
            "wind_speed_10m_max",
            "wind_gusts_10m_max",
            "wind_direction_10m_dominant",
            "wind_gusts_10m_mean",
            "temperature_2m_mean",
            "surface_pressure_mean",
            "cloud_cover_mean",
        ],
=======
        "daily": "wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant",
>>>>>>> 65ccff1 (refacto code + ajout du main.py fonctionnel)
        "timezone": "Europe/Paris",
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


def get_wind_history(
    latitude: float, longitude: float, start_date: str, end_date: str
) -> pd.DataFrame:
    """
    Données historiques éoliennes journalières via Open-Meteo archive API.
    """
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
<<<<<<< HEAD
<<<<<<< HEAD
        "daily": "wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant,wind_gusts_10m_mean,temperature_2m_mean,surface_pressure_mean,cloud_cover_mean",
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
            "wind_speed_10m_max",
            "wind_gusts_10m_max",
            "wind_direction_10m_dominant",
            "cloud_cover_mean",
            "surface_pressure_mean",
            "temperature_2m_mean",
        ],
=======
        "daily": "wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant",
>>>>>>> 65ccff1 (refacto code + ajout du main.py fonctionnel)
        "timezone": "Europe/Paris",
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
