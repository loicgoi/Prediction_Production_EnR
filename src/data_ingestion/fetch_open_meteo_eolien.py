import requests
import pandas as pd


def get_wind_forecast(latitude: float, longitude: float) -> pd.DataFrame:
    """
    Récupère les prévisions éoliennes et conditions météorologiques associées
    à partir de l'API Open-Meteo (prévisions).

    Args:
        latitude (float): Latitude de la localisation.
        longitude (float): Longitude de la localisation.

    Returns:
        pd.DataFrame: Tableau contenant les données journalières de prévision, incluant :
            - wind_speed_10m_max : vitesse maximale du vent à 10 m (km/h)
            - wind_gusts_10m_max : rafales maximales de vent à 10 m (km/h)
            - wind_direction_10m_dominant : direction dominante du vent (°)
            - wind_gusts_10m_mean : rafales moyennes de vent à 10 m (km/h)
            - temperature_2m_mean : température moyenne quotidienne (°C)
            - surface_pressure_mean : pression atmosphérique moyenne (hPa)
            - cloud_cover_mean : couverture nuageuse moyenne (%)

    Raises:
        requests.HTTPError: Si la requête à l'API échoue.

    Exemple:
        >>> df = get_wind_forecast(43.61, 3.87)
        >>> df.head()
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
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

    # Récuperation des données
    response = requests.get(url, params)
    response.raise_for_status()
    return pd.DataFrame(response.json()["daily"])


def get_wind_history(
    latitude: float, longitude: float, start_date: str, end_date: str
) -> pd.DataFrame:
    """
    Récupère l'historique des données éoliennes et conditions météorologiques associées
    à partir de l'API Open-Meteo (données archivées).

    Args:
        latitude (float): Latitude de la localisation.
        longitude (float): Longitude de la localisation.
        start_date (str): Date de début de la période au format 'YYYY-MM-DD'.
        end_date (str): Date de fin de la période au format 'YYYY-MM-DD'.

    Returns:
        pd.DataFrame: Tableau contenant les données journalières historiques, incluant :
            - wind_speed_10m_max : vitesse maximale du vent à 10 m (km/h)
            - wind_gusts_10m_max : rafales maximales de vent à 10 m (km/h)
            - wind_direction_10m_dominant : direction dominante du vent (°)
            - cloud_cover_mean : couverture nuageuse moyenne (%)
            - surface_pressure_mean : pression atmosphérique moyenne (hPa)
            - temperature_2m_mean : température moyenne quotidienne (°C)

    Raises:
        requests.HTTPError: Si la requête à l'API échoue.

    Exemple:
        >>> df = get_wind_history(43.61, 3.87, "2024-01-01", "2024-12-31")
        >>> df.head()
    """
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": 43.6109,
        "longitude": 3.8763,
        "start_date": "2016-09-01",
        "end_date": "2025-09-30",
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

    # Récuperation des données
    response = requests.get(url, params)
    response.raise_for_status()
    return pd.DataFrame(response.json()["daily"])
