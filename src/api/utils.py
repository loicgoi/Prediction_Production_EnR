"""
Utilitaires pour l'API FastAPI
"""

import pandas as pd
from typing import Dict, Any


def validate_features(features: Dict[str, Any], expected_features: list) -> bool:
    """
    Valide que toutes les features attendues sont présentes
    """
    return all(feature in features for feature in expected_features)


def prepare_features_df(features: Dict[str, Any]) -> pd.DataFrame:
    """
    Prépare un DataFrame à partir des features
    """
<<<<<<< HEAD
    return pd.DataFrame([features])
=======
    return pd.DataFrame([features])
>>>>>>> 0ece31b (feat(api): ajout route /solar pour prédiction solaire)
