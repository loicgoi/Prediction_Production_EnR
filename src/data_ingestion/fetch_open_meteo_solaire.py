#######-solaire######
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
	"start_date": "2024-01-01",
	"end_date": "2025-09-30",
	"daily": ["sunrise", "sunset", "daylight_duration", "sunshine_duration", "precipitation_sum", "temperature_2m_max", "temperature_2m_min", "shortwave_radiation_sum", "cloud_cover_mean", "precipitation_hours", "relative_humidity_2m_mean", "wind_gusts_10m_mean", "wind_speed_10m_mean"],
}
response = requests.get(url, params=params)
data = response.json()
df_historical_solaire = pd.DataFrame(data["daily"])
print(df_historical_solaire.head())
##########------#############
