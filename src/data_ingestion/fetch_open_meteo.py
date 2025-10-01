# soleil ######
import requests
import pandas as pd

# Setup Open-Meteo client avec cache et retry

cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Paramètres pour le solaire
url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
params = {
    "latitude": 43.6109,
    "longitude": 3.8763,
    "start_date": "2025-09-14",
    "end_date": "2025-09-28",
    "hourly": "shortwave_radiation,direct_radiation,diffuse_radiation,direct_normal_irradiance,global_tilted_irradiance"
}

# Requête Open-Meteo
responses = openmeteo.weather_api(url, params=params)


# Traitement des données pour la première localisation
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone offset: {response.UtcOffsetSeconds()}s")

# Données horaires
hourly = response.Hourly()
hourly_shortwave = hourly.Variables(0).ValuesAsNumpy()
hourly_direct = hourly.Variables(1).ValuesAsNumpy()
hourly_diffuse = hourly.Variables(2).ValuesAsNumpy()
hourly_dni = hourly.Variables(3).ValuesAsNumpy()
hourly_gti = hourly.Variables(4).ValuesAsNumpy()

# Création du DataFrame
hourly_data = {
    "date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ),
    "shortwave_radiation": hourly_shortwave,
    "direct_radiation": hourly_direct,
    "diffuse_radiation": hourly_diffuse,
    "direct_normal_irradiance": hourly_dni,
    "global_tilted_irradiance": hourly_gti
}

hourly_dataframe = pd.DataFrame(data=hourly_data)
print("\nHourly solar data\n", hourly_dataframe)
