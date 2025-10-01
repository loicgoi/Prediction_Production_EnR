# soleil ######
import requests
import pandas as pd

# URL MP Open-Meteo
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 43.6119,
    "longitude": 3.8777,
    "daily": "temperature_2m_max,temperature_2m_min,windspeed_10m_max,shortwave_radiation_sum,precipitation_sum",
    "timezone": "Europe/Paris"
}

# Récupération des données
response = requests.get(url, params=params)
data = response.json()

# Transformation en DataFrame
df = pd.DataFrame(data["daily"])
print(df.head())