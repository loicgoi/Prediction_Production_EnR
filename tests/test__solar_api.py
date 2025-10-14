import pytest
from fastapi.testclient import TestClient
from src.api.route_api_solar import router
from unittest.mock import patch

# Création d’un client de test à partir du router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)
client = TestClient(app)

# ===============================
# TEST 1 : Vérifie que la route fonctionne et renvoie un statut 200
# ===============================
@patch('src.api.route_api_solar.ModelPredictor.predict')  # On mocke le modèle pour éviter un vrai appel
def test_predict_solar_success(mock_model_predictor):
    # Simule un retour de prédiction du modèle
    mock_instance = mock_model_predictor.return_value
    mock_instance.predict.return_value = 123.45

    payload = {
        "temperature_2m_mean": 20.5,
        "shortwave_radiation_sum_kwh_m2": 5.8,
        "sunshine_duration": 3600.0,
        "cloud_cover_mean": 25.0,
        "relative_humidity_2m_mean": 45.0
    }

    response = client.post("/predict/solar/", json=payload)

    # Vérifie le statut HTTP
    assert response.status_code == 200

    # Vérifie la structure de la réponse
    data = response.json()
    assert data["producer_type"] == "solar"
    assert isinstance(data["prediction_kwh"], float)
    assert data["status"] == "success"


# ===============================
# TEST 2 : Vérifie la gestion des erreurs (ex: ModelPredictor lève une exception)
# ===============================
@patch("src.api.route_api_solar.ModelPredictor")
def test_predict_solar_failure(mock_model_predictor):
    mock_instance = mock_model_predictor.return_value
    mock_instance.predict.side_effect = Exception("Erreur interne")

    payload = {
        "temperature_2m_mean": 15.0,
        "shortwave_radiation_sum_kwh_m2": 3.5,
        "sunshine_duration": 1800.0,
        "cloud_cover_mean": 50.0,
        "relative_humidity_2m_mean": 60.0
    }

    response = client.post("/predict/solar/", json=payload)

    assert response.status_code == 500
    assert "Erreur de prédiction" in response.json()["detail"]
