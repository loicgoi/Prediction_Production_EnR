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
df = pd.DataFrame(data["daily"])
print(df.head())
#############------#############