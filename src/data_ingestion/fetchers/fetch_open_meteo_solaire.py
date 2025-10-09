import pandas as pd
import requests


def get_solar_forecast(
    latitude: float, longitude: float, start_date: str = None, end_date: str = None
) -> pd.DataFrame:
    """
    Prévisions solaires journalières optimisées pour la prédiction de production.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "shortwave_radiation_sum,cloud_cover_mean,precipitation_sum,temperature_2m_max,temperature_2m_min,relative_humidity_2m_mean,wind_speed_10m_mean",
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


def get_solar_history(
    latitude: float, longitude: float, start_date: str, end_date: str
) -> pd.DataFrame:
    """
    Données historiques solaires optimisées pour l'entraînement des modèles.
    """
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "shortwave_radiation_sum,cloud_cover_mean,precipitation_sum,temperature_2m_max,temperature_2m_min,relative_humidity_2m_mean,wind_speed_10m_mean",
        "timezone": "Europe/Paris",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame(data["daily"])
    if "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"])

    return df
