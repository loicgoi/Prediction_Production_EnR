import pandas as pd
import requests


def get_wind_forecast(
    latitude: float, longitude: float, start_date: str, end_date: str
) -> pd.DataFrame:
    """
    Prévisions éoliennes journalières via Open-Meteo API.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
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
        "timezone": "Europe/Paris",
        "forecast_days": 16,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return pd.DataFrame(response.json()["daily"])


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
        "daily": [
            "wind_speed_10m_max",
            "wind_gusts_10m_max",
            "wind_direction_10m_dominant",
            "cloud_cover_mean",
            "surface_pressure_mean",
            "temperature_2m_mean",
        ],
        "timezone": "Europe/Paris",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return pd.DataFrame(response.json()["daily"])
