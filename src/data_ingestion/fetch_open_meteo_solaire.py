import requests
import pandas as pd


def get_solar_forecast(latitude: float, longitude: float) -> pd.DataFrame:
    """
    Récupère les prévisions solaires journalières à partir de l'API Open-Meteo.

    Cette fonction interroge l'API Open-Meteo (endpoint `forecast`) pour obtenir
    jusqu'à 16 jours de prévisions incluant des variables telles que
    la couverture nuageuse, la température, la durée d'ensoleillement,
    le rayonnement solaire, l'humidité, la vitesse du vent, etc.

    Args:
        latitude (float): Latitude de la zone géographique d'intérêt.
        longitude (float): Longitude de la zone géographique d'intérêt.

    Returns:
        pd.DataFrame: Un DataFrame Pandas contenant les prévisions solaires
        journalières. Les colonnes incluent :
            - `time` : date de la prévision
            - variables météorologiques quotidiennes (ex. `sunshine_duration`,
              `shortwave_radiation_sum`, `temperature_2m_mean`, etc.)
    """

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
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

    # Récupération des données
    response = requests.get(url, params=params)
    response.raise_for_status()
    return pd.DataFrame(response.json()["daily"])


def get_solar_history(
    latitude: float, longitude: float, start_date: str, end_date: str
) -> pd.DataFrame:
    """
    Récupère les données historiques d'ensoleillement et de conditions météorologiques
    à partir de l'API Open-Meteo (archive).

    Args:
            latitude (float): Latitude de la localisation.
            longitude (float): Longitude de la localisation.
            start_date (str): Date de début de la période (format "YYYY-MM-DD").
            end_date (str): Date de fin de la période (format "YYYY-MM-DD").

    Returns:
            pd.DataFrame: Tableau contenant les données journalières historiques, incluant :
                    - sunrise : heure de lever du soleil
                    - sunset : heure de coucher du soleil
                    - daylight_duration : durée du jour (secondes)
                    - sunshine_duration : durée d’ensoleillement (secondes)
                    - precipitation_sum : précipitations journalières totales (mm)
                    - temperature_2m_max : température maximale quotidienne (°C)
                    - temperature_2m_min : température minimale quotidienne (°C)
                    - shortwave_radiation_sum : rayonnement solaire global (MJ/m²)
                    - cloud_cover_mean : couverture nuageuse moyenne (%)
                    - precipitation_hours : nombre d’heures de précipitation
                    - relative_humidity_2m_mean : humidité relative moyenne (%)
                    - wind_gusts_10m_mean : rafales de vent moyennes à 10 m (km/h)
                    - wind_speed_10m_mean : vitesse moyenne du vent à 10 m (km/h)

    Raises:
            requests.HTTPError: Si la requête à l'API échoue.

    Exemple:
            >>> df = get_solar_history(43.61, 3.87, "2024-01-01", "2024-12-31")
            >>> df.head()
    """

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": 43.6109,
        "longitude": 3.8763,
        "start_date": "2024-01-01",
        "end_date": "2025-09-30",
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
