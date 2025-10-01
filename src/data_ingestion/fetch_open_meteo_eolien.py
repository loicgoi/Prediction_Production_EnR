import requests
import pandas as pd


# construction du data_eolien previsionnelle
# Le paramétre de la requete data prévisionnelle
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 43.6109,
	"longitude": 3.8763,
	"daily": [
        "wind_speed_10m_max", 
        "wind_gusts_10m_max", 
        "wind_direction_10m_dominant",  
        "wind_gusts_10m_mean", 
        "temperature_2m_mean", 
        "surface_pressure_mean", 
        "cloud_cover_mean"],
	"timezone": "Europe/Paris",
	"forecast_days": 16,
}

# Récuperation des données
response = requests.get(url,params)
data = response.json()

# Transaformation du json en dataframe
df_previ_eolien = pd.DataFrame(data["daily"])
print (df_previ_eolien.head())

# Chargement du Dataframe en csv 
df_previ_eolien.to_csv("data/raw/eolien_previ.csv")
print(f'Fichier CSV :  eolien_previ.csv')



# Construction du data_eolien Historique
# Le paramétresde la requte historique
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
	"latitude": 43.6109,
	"longitude": 3.8763,
	"start_date": "2024-01-01",
	"end_date": "2025-09-30",
	"daily": [
        "wind_speed_10m_max", 
        "wind_gusts_10m_max", 
        "wind_direction_10m_dominant",
        "wind_gusts_10m_mean", 
        "temperature_2m_mean", 
        "cloud_cover_mean", 
        "surface_pressure_mean"],
    "timezone": "Europe/Paris",
}

# Récuperation des données
response = requests.get(url,params)
data = response.json()

# Transaformation du json en dataframe
df_histo_eolien = pd.DataFrame(data["daily"])
print (df_histo_eolien.head())

# Chargement du Dataframe en csv 
df_histo_eolien.to_csv("data/raw/eolien_histo.csv")
print(f'Fichier CSV : eolien_histo.csv')