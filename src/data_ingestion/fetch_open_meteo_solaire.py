import requests
import pandas as pd

# URL MP Open-Meteo
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 43.6109,
	"longitude": 3.8763,
	"daily": ["cloud_cover_max", "cloud_cover_min", "temperature_2m_mean", "apparent_temperature_mean", "shortwave_radiation_sum", "sunshine_duration", "cloud_cover_mean", "uv_index_max", "uv_index_clear_sky_max", "precipitation_sum", "precipitation_hours", "relative_humidity_2m_mean", "wind_speed_10m_mean", "wind_gusts_10m_mean", "sunrise", "sunset", "daylight_duration", "temperature_2m_max", "temperature_2m_min"],
	"current": "cloud_cover",
	"forecast_days": 16,
}

# Récupération des données
response = requests.get(url, params=params)
data = response.json()

# Transformation en DataFrame
df_previsions_solaire = pd.DataFrame(data["daily"])
print(df_previsions_solaire.head())
#############------#############

######### solaire_historique #########
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
	"latitude": 43.6109,
	"longitude": 3.8763,
	"start_date": "2016-09-01",
	"end_date": "2025-09-30",
	"daily": ["sunrise", "sunset", "daylight_duration", "sunshine_duration", "precipitation_sum", "temperature_2m_max", "temperature_2m_min", "shortwave_radiation_sum", "cloud_cover_mean", "precipitation_hours", "relative_humidity_2m_mean", "wind_gusts_10m_mean", "wind_speed_10m_mean", "temperature_2m_mean", "cloud_cover_max", "cloud_cover_min", "apparent_temperature_mean", "apparent_temperature_max", "apparent_temperature_min", "relative_humidity_2m_max", "relative_humidity_2m_min", "rain_sum", "snowfall_sum", "wind_speed_10m_max"],
}
response = requests.get(url, params=params)
data = response.json()
df_historical_solaire = pd.DataFrame(data["daily"])
print(df_historical_solaire.head())
##########------#############
# Enregistrer les prévisions solaires
df_previsions_solaire.to_csv("data/raw/previsions_solaire.csv", index=False)
print("Prévisions solaires sauvegardées en CSV.")

# Enregistrer l'historique solaire
df_historical_solaire.to_csv("data/raw/historique_solaire.csv", index=False)
print("Historique solaire sauvegardé en CSV.")




# def fetch_solar_forecast(latitude: float, longitude: float, forecast_days: int = 16) -> pd.DataFrame:
#     """
#     Récupère les prévisions solaires quotidiennes depuis l'API Open-Meteo.

#     Paramètres
#     ----------
#     latitude : float
#         Latitude du lieu d'intérêt.
#     longitude : float
#         Longitude du lieu d'intérêt.
#     forecast_days : int, optionnel
#         Nombre de jours de prévision à récupérer (par défaut : 16).

#     Retour
#     ------
#     pd.DataFrame
#         DataFrame contenant les données météorologiques quotidiennes de prévision.
#     """
#     url = "https://api.open-meteo.com/v1/forecast"
#     params = {
#         "latitude": latitude,
#         "longitude": longitude,
#         "daily": [
#             "cloud_cover_max", "cloud_cover_min", "temperature_2m_mean",
#             "apparent_temperature_mean", "shortwave_radiation_sum",
#             "sunshine_duration", "cloud_cover_mean", "uv_index_max",
#             "uv_index_clear_sky_max", "precipitation_sum", "precipitation_hours",
#             "relative_humidity_2m_mean", "wind_speed_10m_mean",
#             "wind_gusts_10m_mean", "sunrise", "sunset", "daylight_duration",
#             "temperature_2m_max", "temperature_2m_min"
#         ],
#         "current": "cloud_cover",
#         "forecast_days": forecast_days,
#     }

#     response = requests.get(url, params=params)
#     response.raise_for_status()
#     data = response.json()
#     df_forecast = pd.DataFrame(data["daily"])
#     return df_forecast


# def fetch_solar_history(latitude: float, longitude: float,
#                         start_date: str, end_date: str) -> pd.DataFrame:
#     """
#     Récupère les données solaires historiques depuis l'API Open-Meteo Archive.

#     Paramètres
#     ----------
#     latitude : float
#         Latitude du lieu d'intérêt.
#     longitude : float
#         Longitude du lieu d'intérêt.
#     start_date : str
#         Date de début au format 'YYYY-MM-DD'.
#     end_date : str
#         Date de fin au format 'YYYY-MM-DD'.

#     Retour
#     ------
#     pd.DataFrame
#         DataFrame contenant les données météorologiques historiques.
#     """
#     url = "https://archive-api.open-meteo.com/v1/archive"
#     params = {
#         "latitude": latitude,
#         "longitude": longitude,
#         "start_date": start_date,
#         "end_date": end_date,
#         "daily": [
#             "sunrise", "sunset", "daylight_duration", "sunshine_duration",
#             "precipitation_sum", "temperature_2m_max", "temperature_2m_min",
#             "shortwave_radiation_sum", "cloud_cover_mean", "precipitation_hours",
#             "relative_humidity_2m_mean", "wind_gusts_10m_mean",
#             "wind_speed_10m_mean", "temperature_2m_mean", "cloud_cover_max",
#             "cloud_cover_min", "apparent_temperature_mean",
#             "apparent_temperature_max", "apparent_temperature_min",
#             "relative_humidity_2m_max", "relative_humidity_2m_min",
#             "rain_sum", "snowfall_sum", "wind_speed_10m_max"
#         ],
#     }

#     response = requests.get(url, params=params)
#     response.raise_for_status()
#     data = response.json()
#     df_history = pd.DataFrame(data["daily"])
#     return df_history


# def save_dataframe(df: pd.DataFrame, filepath: str) -> None:
#     """
#     Sauvegarde un DataFrame au format CSV.

#     Paramètres
#     ----------
#     df : pd.DataFrame
#         Le DataFrame à sauvegarder.
#     filepath : str
#         Chemin complet du fichier CSV de sortie.

#     Retour
#     ------
#     None
#     """
#     df.to_csv(filepath, index=False)
#     print(f"Données sauvegardées : {filepath}")


# if __name__ == "__main__":
#     # Coordonnées de Montpellier
#     LAT, LON = 43.6109, 3.8763

#     # Récupération des données
#     df_forecast = fetch_solar_forecast(LAT, LON)
#     df_history = fetch_solar_history(LAT, LON, "2016-09-01", "2025-09-30")

#     # # Sauvegarde locale
#     # save_dataframe(df_forecast, "data/raw/previsions_solaire.csv")
#     # save_dataframe(df_history, "data/raw/historique_solaire.csv")
    
#     # --- Vérification des DataFrames ---
#     print("\nAperçu des prévisions solaires :") 
#     print(df_forecast.head()) 
#     print("\nAperçu de l'historique solaire :") 
#     print(df_history.head())