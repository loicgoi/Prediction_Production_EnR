import pandas as pd
import requests


def get_solar_forecast(
    latitude: float, longitude: float, start_date: str, end_date: str
) -> pd.DataFrame:
    """
    Prévisions solaires journalières (jusqu'à 16 jours) via Open-Meteo API.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
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
        "forecast_days": 16,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return pd.DataFrame(response.json()["daily"])


def get_solar_history(
    latitude: float, longitude: float, start_date: str, end_date: str
) -> pd.DataFrame:
    """
    Données historiques solaires journalières via Open-Meteo archive API.
    """
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
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
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return pd.DataFrame(response.json()["daily"])
