from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from src.prediction.model_predictor import ModelPredictor
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# -------------------------------
# Schéma Pydantic pour la requête
# -------------------------------
class SolarForecastFeatures(BaseModel):
    date: str
    temperature_2m_mean: float
    shortwave_radiation_sum_kwh_m2: float
    sunshine_duration: float
    cloud_cover_mean: float
    relative_humidity_2m_mean: float

class SolarPredictionRequest(BaseModel):
    features: List[SolarForecastFeatures]

# -------------------------------
# Endpoint de prédiction solaire
# -------------------------------
@router.post("/predict/solar")
def predict_solar(request: SolarPredictionRequest):
    try:
        features_list = [f.dict() for f in request.features]
        logger.info(f"Prédiction solaire pour {len(features_list)} entrées")

        predictor = ModelPredictor(model_name="solar_model.pkl")  # ton modèle
        predictions = predictor.predict(features_list)  # prédiction batch

        # Retourner la date + prédiction
        results = [
            {"date": f["date"], "predicted_solar_power": pred}
            for f, pred in zip(features_list, predictions)
        ]

        return {"predictions": results}

    except Exception as e:
        logger.error(f"Erreur prédiction solaire: {e}")
        raise HTTPException(status_code=500, detail=str(e))
