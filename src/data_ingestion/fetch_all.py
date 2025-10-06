from fetch_hubeau import get_hubeau_data
from fetch_open_meteo_eolien import get_wind_forecast, get_wind_history
from fetch_open_meteo_solaire import get_solar_forecast, get_solar_history
import os
import pandas as pd

RAW_DATA_PATH = "data/raw"


def fetch_all():
    os.makedirs(RAW_DATA_PATH, exist_ok=True)

    # Hydro
    try:
        df_hydro = get_hubeau_data(
            code_station="Y321002101",
            start_date="2022-07-01",
            end_date="2025-09-30",
        )
        df_hydro.to_csv(os.path.join(RAW_DATA_PATH, "data_hubeau.csv"), index=False)
        print("Hydro : données sauvegardées")
    except Exception as e:
        print(f"Erreur Hubeau : {e}")
        df_hydro = pd.DataFrame()

    # Solaire
    try:
        df_solar_forecast = get_solar_forecast(latitude=43.6109, longitude=3.8763)
        df_solar_forecast.to_csv(
            os.path.join(RAW_DATA_PATH, "data_solar_forecast.csv"), index=False
        )
        df_solar_history = get_solar_history(
            latitude=43.6109,
            longitude=3.8763,
            start_date="2016-09-01",
            end_date="2025-09-30",
        )
        df_solar_history.to_csv(
            os.path.join(RAW_DATA_PATH, "data_solar_history.csv"), index=False
        )
        print("Solaire : données sauvegardées")
    except Exception as e:
        print(f"Erreur solaire : {e}")
        df_solar_forecast, df_solar_history = pd.DataFrame(), pd.DataFrame()

    # Vent
    try:
        df_wind_forecast = get_wind_forecast(latitude=43.6109, longitude=3.8763)
        df_wind_forecast.to_csv(
            os.path.join(RAW_DATA_PATH, "data_wind_forecast.csv"), index=False
        )
        df_wind_history = get_wind_history(
            latitude=43.6109,
            longitude=3.8763,
            start_date="2016-09-01",
            end_date="2025-09-30",
        )
        df_wind_history.to_csv(
            os.path.join(RAW_DATA_PATH, "data_wind_history.csv"), index=False
        )
        print("Vent : données sauvegardées")
    except Exception as e:
        print(f"Erreur vent : {e}")
        df_wind_forecast, df_wind_history = pd.DataFrame(), pd.DataFrame()

    return (
        df_hydro,
        df_solar_forecast,
        df_solar_history,
        df_wind_forecast,
        df_wind_history,
    )
