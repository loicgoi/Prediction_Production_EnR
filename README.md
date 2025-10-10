# Prediction Production Énergies Renouvelables  
### Système de prédiction de production d'énergie solaire, éolienne et hydraulique

![python](https://img.shields.io/badge/python-3.13-blue)
![architecture](https://img.shields.io/badge/architecture-modulaire-orange)

---

## Table des matières
- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#️-architecture)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Utilisation](#-utilisation)
- [Tests](#-tests)
- [Développement](#-développement)
- [Licence](#-licence)

---

## Fonctionnalités

### Récupération de données
- **Données solaires** : Prévisions et historiques via **Open-Meteo API**  
- **Données éoliennes** : Vitesse du vent, rafales et direction  
- **Données hydrauliques** : Débits des rivières via **Hub'Eau**  
- **Données de production** : Historique de production énergétique  

### Nettoyage et traitement
- Nettoyage automatique des données  
- Gestion des valeurs manquantes et aberrantes  
- Conversion d’unités et standardisation  
- Suppression des doublons  

### Stockage
- Base de données **Supabase** pour le stockage  
- Tables séparées pour données brutes et nettoyées  
- Historique complet des données  

### Prédictions
- Modèles de **machine learning** pour la prédiction  
- Facteurs de capacité de production  
- Statistiques de performance  

---

## Architecture
```
Prediction_Production_EnR
├──archives
│   ├──expo_solaire.py
│   ├──producteur_solaire.py
│   └──producteur.py
├──notebooks
├──scripts
│   ├──__init__.py
│   └──daily_fetch.py
├──src
│   ├──api
│   │   ├──main.py
│   │   └──utils.py
│   ├──config
│   │   └──settings.py
│   ├──data_ingestion
│   │   ├──api
│   │   │   ├──__init__.py
│   │   │   └──api_config.py
│   │   ├──fetchers
│   │   │   ├──__init__.py
│   │   │   ├──fetch_all.py
│   │   │   ├──fetch_hubeau.py
│   │   │   ├──fetch_open_meteo_eolien.py
│   │   │   ├──fetch_open_meteo_solaire.py
│   │   │   └──fetch_production.py
│   │   ├──handlers
│   │   │   ├──__init__.py
│   │   │   ├──db_models.py
│   │   │   ├──etl_supabase.py
│   │   │   ├──handler_hubeau.py
│   │   │   └──handler_meteo.py
│   │   ├──utils
│   │   │   ├──__init__.py
│   │   │   └──data_cleaner.py
│   │   └──__init__.py
│   ├──frontend
│   │   └──app.py
│   ├──models
│   │   ├──__init__.py
│   │   ├──feature_engineering.py
│   │   ├──predict.py
│   │   └──train_model.py
│   ├──producers
│   │   ├──__init__.py
│   │   ├──base_producer.py
│   │   ├──hydro_producer.py
│   │   ├──solar_producer.py
│   │   └──wind_producer.py
│   ├──utils
│   │   ├──helpers.py
│   │   └──visualization.py
│   └──__init__.py
├──tests
│   ├──test_api_config.py
│   ├──test_base_producer.py
│   ├──test_data_cleaner.py
│   ├──test_etl_supabase.py
│   ├──test_fetch_all.py
│   ├──test_fetch_hubeau.py
│   ├──test_fetch_open_meteo_solaire.py
│   ├──test_fetch_production.py
│   ├──test_handler_hubeau.py
│   ├──test_handler_meteo.py
│   ├──test_hydro_producer.py
│   ├──test_open_meteo_eolien.py
│   ├──test_settings.py
│   ├──test_solar_producer.py
│   └──test_wind_producer.py
├──main.py
├──pyproject.toml
├──pytest.ini
├──README.md
├──setup.py
├──uv.lock
├──.gitignore
└──.python-version
```

---

## Installation

### Prérequis
- Python **3.13+**
- Compte **Supabase**
- Clés API pour **Open-Meteo** et **Hub'Eau**

### Installation pas à pas

#### 1. Cloner le repository
```bash
git clone https://github.com/your-username/Prediction_Production_EnR.git
cd Prediction_Production_EnR
```

#### 2. Créer l'environnement virtuel
```bash
# Créer un environnement isolé avec uv
uv venv

# Activer l’environnement
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

#### 3. Installer les dépendances
```bash
uv sync
```

#### 4. Configurer les variables d'environnement
```bash
cp .env.example .env
# Éditer .env avec vos configurations
```

---

## Configuration

### Variables d'environnement (.env)
```bash
# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Localisation par défaut (Montpellier)
MONTPELLIER_LATITUDE=43.6109
MONTPELLIER_LONGITUDE=3.8763

# Station Hub'Eau
HUBEAU_STATION=Y321002101

# Puissances nominales (kW)
SOLAR_NOMINAL_POWER=150.0
WIND_NOMINAL_POWER=100.0
HYDRO_NOMINAL_POWER=200.0

# Chemins des données
DATA_RAW_PATH=data/raw
```

### Configuration des APIs  

Fichier : src/data_ingestion/api/api_config.py  
```python
# Configuration Open-Meteo
OPEN_METEO_CONFIG = {
    "forecast_url": "https://api.open-meteo.com/v1/forecast",
    "archive_url": "https://archive-api.open-meteo.com/v1/archive",
    "timezone": "Europe/Paris",
    "forecast_days": 16,
}

# Configuration Hub'Eau
HUBEAU_CONFIG = {
    "url": "https://hubeau.eaufrance.fr/api/v2/hydrometrie/obs_elab",
    "params": {
        "grandeur_hydro_elab": "QmnJ",  # Débit moyen journalier
        "size": 20000,
    },
}
```

---

## Utilisation

### 1. Récupération de toutes les données
```python
from src.data_ingestion.fetchers.fetch_all import fetch_all

# Récupère toutes les données et les envoie dans Supabase
results = fetch_all()
print(f"Données solaires: {len(results['solar_history'])} enregistrements")
print(f"Données éoliennes: {len(results['wind_history'])} enregistrements")
print(f"Données hydrauliques: {len(results['hubeau'])} enregistrements")
```

### 2. Utilisation des producteurs   
```python 
from src.producers.solar_producer import SolarProducer
from datetime import date

# Créer un producteur solaire
solar_producer = SolarProducer(
    name="Parc solaire Montpellier",
    location="Montpellier", 
    nominal_power=150.0,
    data_file="data/raw/prod_solaire.csv"
)

# Charger les données de production
start_date = date(2024, 1, 1)
end_date = date(2024, 1, 31)
production_data = solar_producer.load_production_data(start_date, end_date)

# Calculer les statistiques
stats = solar_producer.calculate_statistics(start_date, end_date)
print(f"Production totale: {stats['total_production']} kWh")
print(f"Facteur de capacité: {stats['capacity_factor']:.2%}")
```

### 3. Récupération données météo
```python
from src.data_ingestion.handlers.handler_meteo import WeatherDataHandler

# Données solaires
solar_handler = WeatherDataHandler(43.6109, 3.8763, "solar")
solar_forecast = solar_handler.load(forecast=True)
solar_history = solar_handler.load(
    start_date="2024-01-01", 
    end_date="2024-01-31", 
    forecast=False
)

# Données éoliennes  
wind_handler = WeatherDataHandler(43.6109, 3.8763, "wind")
wind_forecast = wind_handler.load(forecast=True)
```

### 4. Lancement de l'API
-- à venir --

---

## Tests

### Exécution des tests
```bash
# Tous les tests
pytest tests/ -v

# Tests avec couverture
pytest --cov=src tests/

# Tests spécifiques
pytest tests/test_producers.py -v
pytest tests/test_handlers.py -v
```

### Structure des tests

- 57 tests unitaires couvrant toutes les fonctionnalités  
- Tests des producteurs : solaire, éolien, hydraulique  
- Tests des handlers : données météo et Hub'Eau  
- Tests des cleaners : nettoyage des données  
- Tests des APIs : configuration et endpoints  

---

## Développement

### Ajouter un nouveau producteur

Créer la classe dans src/producers/ :

```python
from .base_producer import BaseProducer

class NewProducer(BaseProducer):
    def load_production_data(self, start_date, end_date):
        # Implémentation spécifique
        pass
        
    def calculate_statistics(self, start_date, end_date):
        # Calcul des statistiques
        pass
```

- Ajouter la configuration dans src/data_ingestion/api/api_config.py  
- Créer les tests dans tests/test_new_producer.py  

### Ajouter une nouvelle source de données

- Créer un fetcher dans src/data_ingestion/fetchers/  
- Créer un handler dans src/data_ingestion/handlers/  
- Ajouter les méthodes de nettoyage dans DataCleaner  

---

## Licence
Ce projet n'est pas sous licence open-source.  
Il a été développé dans le cadre d’un projet scolaire et est destiné à un usage éducatif uniquement.  
Toute réutilisation ou diffusion du code nécessite l’accord préalable de l’auteur.