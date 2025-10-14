# Prediction Production Énergies Renouvelables  
### Système de prédiction de production d'énergie solaire, éolienne et hydraulique

![python](https://img.shields.io/badge/python-3.13-blue)
![architecture](https://img.shields.io/badge/architecture-modulaire-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-0.119-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.50-red)
![ML](https://img.shields.io/badge/ML-MachineLearning-yellow)

---

## Table des matières
- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [API](#api)
- [Interface Web](#interface-web)
- [Tests](#tests)
- [Développement](#développement)
- [Licence](#licence)

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
- Tables séparées pour données brutes (raw_*) et nettoyées (clean_*) 
- Historique complet des données  

### Machine Learning
- 3 algorithmes : Ridge, Random Forest, XGBoost
- Modèles par type : Solaire, Éolien, Hydraulique
- Entraînement automatique avec sélection du meilleur modèle
- Métriques : MAE, R², RMSE
- Sauvegarde automatique des modèles et scalers 

### API
- FastAPI avec documentation interactive
- Endpoints de prédiction : /predict/solar, /predict/wind, /predict/hydro
- Validation avec Pydantic
- Statut des modèles en temps réel

### Interface Web
- Streamlit pour la visualisation
- Formulaires interactifs avec sliders
- Graphiques avec Plotly
- Prédictions en temps réel

### Automatisation
- Script principal avec arguments
- Lancement sélectif des composants
- Pipeline complet données → entraînement → API → Interface

---

## Architecture
```
Prediction_Production_EnR
├──archives
├──docs
├──logs
├──scripts
│   ├──__init__.py
│   ├──daily_fetch.py
│   └──train_models.py
├──src
│   ├──api
│   │   ├──__init__.py
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
│   │   │   ├──etl_supabase.py
│   │   │   ├──handler_hubeau.py
│   │   │   └──handler_meteo.py
│   │   ├──utils
│   │   │   ├──__init__.py
│   │   │   └──data_cleaner.py
│   │   └──__init__.py
│   ├──frontend
│   │   ├──__init__.py
│   │   └──app.py
│   ├──models
│   │   ├──saved
│   │   │   ├──hydro_random_forest_model.pkl
│   │   │   ├──hydro_scaler.pkl
│   │   │   ├──hydro_xgboost_model.pkl
│   │   │   ├──solar_ridge_model.pkl
│   │   │   ├──solar_scaler.pkl
│   │   │   ├──wind_random_forest_model.pkl
│   │   │   └──wind_scaler.pkl
│   │   ├──__init__.py
│   │   ├──data_loarder.py
│   │   ├──model_config.py
│   │   └──model_trainer.py
│   ├──prediction
│   │   └──model_predictor.py
│   ├──producers
│   │   ├──__init__.py
│   │   ├──base_producer.py
│   │   ├──hydro_producer.py
│   │   ├──solar_producer.py
│   │   └──wind_producer.py
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
├──run_api.py
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
- Accès aux API **Open-Meteo** et **Hub'Eau**

### Installation pas à pas

#### 1. Cloner le repository
```bash
git clone https://github.com/loicgoi/Prediction_Production_EnR.git
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
MODELS_PATH=models/saved
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

### 1. Lancement complet
```python
# Lance tous les composants : données → entraînement → API → Streamlit
python main.py all
```

### 2. Commandes modulaires  
```python 
# Pipeline de données seulement
python main.py data

# Entraînement des modèles seulement
python main.py train

# API FastAPI seulement
python main.py api

# Interface Streamlit seulement  
python main.py streamlit

# Vérification du statut
python main.py status

# Combinaisons
python main.py data train      # Données + entraînement
python main.py api streamlit   # API + interface
```

### 3. Utilisations des producteurs
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

### 4. Récupération données météo
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

---

## API

### Démarrage de l'API

```bash
python main.py api
# ou directement
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Endpoints disponibles


|        Endpoint	    |     Méthode     |       Description       |
| :-------------------- |:---------------:| -----------------------:|
| GET /	                |      GET	      | Page d'accueil          |
| GET /health	        |      GET        | Statut de l'API         |
| GET /models/status	|      GET        | Statut des modèles      |
| POST /predict/solar   |	   POST       | Prédiction solaire      |
| POST /predict/win     |      POST	      | Prédiction éolienne     |
| POST /predict/hydro   |	   POST	      | Prédiction hydraulique  |

### Exemple de prédiction

```bash
# Prédiction solaire
curl -X POST "http://localhost:8000/predict/solar" \
     -H "Content-Type: application/json" \
     -d '{
       "temperature_2m_mean": 18.5,
       "shortwave_radiation_sum_kwh_m2": 4.8,
       "sunshine_duration": 45000,
       "cloud_cover_mean": 25.0,
       "relative_humidity_2m_mean": 65.0
     }'
```

### Documentation interactive
- Swagger UI : http://localhost:8000/docs
- Redoc : http://localhost:8000/redoc

---

## Interface Web

### Démarrage de Streamlit

```bash
python main.py streamlit
# ou directement
streamlit run src/frontend/app.py
```

### Accès

- Interface principale : http://localhost:8500

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
 
- Tests des producteurs : solaire, éolien, hydraulique  
- Tests des handlers : données météo et Hub'Eau  
- Tests des cleaners : nettoyage des données  
- Tests des APIs : configuration et endpoints  
- Tests des modèles : entraînement et prédictions  

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

- Créer un fetcher dans **_src/data_ingestion/fetchers/_**  
- Créer un handler dans **_src/data_ingestion/handlers/_**  
- Ajouter les méthodes de nettoyage dans **_DataCleaner_**  


### Worflow de développement

```bash
# 1. Récupérer les données
python main.py data

# 2. Entraîner les modèles  
python main.py train

# 3. Tester l'API
python main.py api

# 4. Tester l'interface
python main.py streamlit

# 5. Vérifier le statut
python main.py status
```

---

## Licence
Ce projet n'est pas sous licence open-source.  
Il a été développé dans le cadre d’un projet scolaire et est destiné à un usage éducatif uniquement.  
Toute réutilisation ou diffusion du code nécessite l’accord préalable de l’auteur.

## Auteurs
**Équipe de développement**
- Loïc - Chaïma - Fadilatou : Développement principal

**Supervision**
- Nadège