# soleil ######
import requests

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 43.6119,
    "longitude": 3.8777,
    "daily": "temperature_2m_max,temperature_2m_min,windspeed_10m_max,shortwave_radiation_sum,precipitation_sum",
    "timezone": "Europe/Paris"
}

response = requests.get(url, params=params)
print(response.json())