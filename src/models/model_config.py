MODEL_CONFIG = {
    "solar": {
        "features": [
            "temperature_2m_mean",
            "shortwave_radiation_sum_kwh_m2",
            "sunshine_duration",
            "cloud_cover_mean",
            "relative_humidity_2m_mean",
        ],
        "target": "production_kwh",
        "models": {
            "ridge": {"alpha": 0.01},
            "xgboost": {"n_estimators": 100, "max_depth": 6, "learning_rate": 0.1},
            "random_forest": {
                "n_estimators": 100,
                "max_depth": None,
                "random_state": 42,
            },
        },
    },
    "wind": {
        "features": [
            "wind_speed_10m_max",
            "wind_gusts_10m_max",
            "wind_direction_10m_dominant",
            "temperature_2m_mean",
        ],
        "target": "production_kwh",
        "models": {
            "ridge": {"alpha": 0.01},
            "xgboost": {"n_estimators": 100, "max_depth": 6, "learning_rate": 0.1},
            "random_forest": {"n_estimators": 100, "max_depth": 10},
        },
    },
    "hydro": {
        "features": ["debit_l_s"],
        "target": "production_kwh",
        "models": {
            "ridge": {"alpha": 0.01},
            "xgboost": {"n_estimators": 100, "max_depth": 6, "learning_rate": 0.1},
            "random_forest": {"n_estimators": 100, "max_depth": 10},
        },
    },
}
