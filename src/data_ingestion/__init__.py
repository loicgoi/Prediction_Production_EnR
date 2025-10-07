<<<<<<< HEAD

=======
"""
Package pour l'ingestion de données météorologiques et de production d'énergie.
"""

from .etl_supabase import DataHandler, CSVDataHandler, APIDataHandler
from .fetch_all import fetch_all, fetch_weather_data, fetch_production_data
from .fetch_hubeau import get_hubeau_data
from .fetch_production import fetch_production_data
from .fetch_open_meteo_eolien import get_wind_forecast, get_wind_history
from .fetch_open_meteo_solaire import get_solar_forecast, get_solar_history
from .handler_hubeau import HubeauDataHandler
from .handler_meteo import WeatherDataHandler
from .data_cleaner import DataCleaner

__all__ = [
    "DataHandler",
    "CSVDataHandler",
    "APIDataHandler",
    "fetch_all",
    "fetch_weather_data",
    "fetch_production_data",
    "get_hubeau_data",
    "get_wind_forecast",
    "get_wind_history",
    "get_solar_forecast",
    "get_solar_history",
    "HubeauDataHandler",
    "WeatherDataHandler",
    "DataCleaner",
]
>>>>>>> cbfd918 (Refacto de tout le code existant pour harmonisation et que tout soit fonctionnel)
