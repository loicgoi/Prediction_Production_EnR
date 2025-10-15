from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
from src.prediction.model_predictor import ModelPredictor

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API de Prévision de Production d'Energie Renouvelable",
    description="API pour prédire la production solaire, éolienne et hydraulique",
    version="1.0.0",
)


# modèles Pydantic pour les features d'entrée
class SolarFeatures(BaseModel):
    temperature_2m_mean: float
    shortwave_radiation_sum_kwh_m2: float
    sunshine_duration: float
    cloud_cover_mean: float
    relative_humidity_2m_mean: float


class WindFeatures(BaseModel):
    wind_speed_10m_max: float
    wind_gusts_10m_max: float
    wind_direction_10m_dominant: float
    temperature_2m_mean: float


class HydroFeatures(BaseModel):
    debit_l_s: float


class PredictionResponse(BaseModel):
    producer_type: str
    prediction_kwh: float
    status: str


@app.get("/")
async def root():
    return {
        "message": "API de prévision de production d'énergie renouvelable",
        "endpoints": {
            "solar": "/predict/solar",
            "wind": "/predict/wind",
            "hydro": "/predict/hydro",
            "status": "/status",
        },
    }


@app.get("/status")
async def status_check():
    """Endpoint sur l'état de l'API"""
    return {"status": "Ok", "message": "API opérationnelle"}


@app.post("/predict/solar", response_model=PredictionResponse)
async def predict_solar(features: SolarFeatures):
    """Prédit la production solaire de la journée en kWh"""
    try:
        logger.info(f"Prédiction solaire avec features: {features.dict()}")

        predictor = ModelPredictor("solar")
        prediction = predictor.predict(features.dict())

        return PredictionResponse(
            producer_type="solar", prediction_kwh=round(prediction, 2), status="success"
        )

    except Exception as e:
        logger.error(f"Erreur prédiction solaire: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction: {str(e)}")


@app.post("/predict/wind", response_model=PredictionResponse)
async def predict_wind(features: WindFeatures):
    """Prédit la production éolienne de la journée en kWh"""
    try:
        logger.info(f"Prédiction éolienne avec features: {features.dict()}")

        predictor = ModelPredictor("wind")
        prediction = predictor.predict(features.dict())

        return PredictionResponse(
            producer_type="wind", prediction_kwh=round(prediction, 2), status="success"
        )

    except Exception as e:
        logger.error(f"Erreur prédiction éolienne: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction: {str(e)}")


@app.post("/predict/hydro", response_model=PredictionResponse)
async def predict_hydro(features: HydroFeatures):
    """Prédit la production hydraulique de la journée en kWh"""
    try:
        logger.info(f"Prédiction hydraulique avec features: {features.dict()}")

        predictor = ModelPredictor("hydro")
        prediction = predictor.predict(features.dict())

        return PredictionResponse(
            producer_type="hydro", prediction_kwh=round(prediction, 2), status="success"
        )

    except Exception as e:
        logger.error(f"Erreur prédiction hydraulique: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction: {str(e)}")


@app.get("/models/status")
async def models_status():
    """Retourne l'état des modèles chargés"""
    try:
        status = {}
        for producer_type in ["solar", "wind", "hydro"]:
            try:
                predictor = ModelPredictor(producer_type)
                status[producer_type] = {
                    "loaded": True,
                    "model_type": type(predictor.model).__name__,
                    "has_scaler": predictor.scaler is not None,
                }
            except Exception as e:
                status[producer_type] = {"loaded": False, "error": str(e)}

        return {"models_status": status}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur vérification modèles: {str(e)}"
        )
