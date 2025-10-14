# solar_api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
from src.prediction.model_predictor import ModelPredictor

# ===============================
# CONFIGURATION DU LOGGER
# ===============================
logger = logging.getLogger(__name__)

# ===============================
# INITIALISATION DU ROUTER
# ===============================
router = APIRouter(
    prefix="/predict/solar",
    tags=["solar"],
    responses={404: {"description": "Not found"}},
)

# ===============================
# MODELE DE DONNÉES PREDICTION
# ===============================
class SolarFeatures(BaseModel):
    temperature_2m_mean: float
    shortwave_radiation_sum_kwh_m2: float
    sunshine_duration: float
    cloud_cover_mean: float
    relative_humidity_2m_mean: float


class PredictionResponse(BaseModel):
    producer_type: str
    prediction_kwh: float
    status: str


# ===============================
# ENDPOINT DE PREDICTION SOLAIRE
# ===============================
@router.post("/", response_model=PredictionResponse)
async def predict_solar(features: SolarFeatures):
    """Prédit la production solaire de la journée en kWh"""
    try:
<<<<<<< HEAD
        logger.info(f"Prédiction solaire avec features: {features.model_dump()}")

        predictor = ModelPredictor("solar")
        prediction = predictor.predict(features.model_dump())
        
=======
        logger.info(f"Prédiction solaire avec features: {features.dict()}")

        predictor = ModelPredictor("solar")
        prediction = predictor.predict(features.dict())

>>>>>>> 8d91632 (feat(api): ajout route /solar pour prédiction solaire)
        return PredictionResponse(
            producer_type="solar",
            prediction_kwh=round(prediction, 2),
            status="success"
        )

    except Exception as e:
        logger.error(f"Erreur prédiction solaire: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction: {str(e)}")
