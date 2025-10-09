# train_ridge.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import RidgeCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

# --- 1️ Charger les données ---
def load_data(filepath):
    """
    Charge le fichier CSV et retourne un DataFrame.
    """
    df = pd.read_csv(filepath, parse_dates=['date'])
    return df

# --- 2️ Feature engineering ---
def feature_engineering(df):
    """
    Création de features temporelles et dérivées pour la production solaire.
    """
    df = df.copy()
    df['dayofyear'] = df['date'].dt.dayofyear
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['sin_dayofyear'] = np.sin(2 * np.pi * df['dayofyear'] / 365)
    df['cos_dayofyear'] = np.cos(2 * np.pi * df['dayofyear'] / 365)

    if 'temperature_2m_max' in df.columns and 'temperature_2m_min' in df.columns:
        df['temp_mean'] = (df['temperature_2m_max'] + df['temperature_2m_min']) / 2
        df['temp_range'] = df['temperature_2m_max'] - df['temperature_2m_min']

    radiation_cols = ['shortwave_radiation_kwh_m2', 'shortwave_radiation_sum_kwh_m2', 'shortwave_radiation_sum']
    radiation_col = next((c for c in radiation_cols if c in df.columns), None)
    if radiation_col:
        df['prod_per_radiation'] = df['production_kwh'] / (df[radiation_col] + 1e-6)
        if 'sunshine_duration_h' in df.columns:
            df['radiation_per_hour'] = df[radiation_col] / (df['sunshine_duration_h'] + 1e-6)

    df = df.fillna(method='ffill').fillna(method='bfill')
    return df

# --- 3️ Préparer X et y ---
def prepare_xy(df):
    features = [
        'shortwave_radiation_sum_kwh_m2','sunshine_duration_h','temperature_2m_max','temperature_2m_min',
        'cloud_cover_mean','precipitation_sum','relative_humidity_2m_mean','month','day',
        'sin_dayofyear','cos_dayofyear','temp_mean','temp_range','radiation_per_hour'
    ]
    X = df[[c for c in features if c in df.columns]]
    y = df['production_kwh']
    return X, y

# --- 4️ Split train/test et standardisation ---
def split_and_scale(X, y, test_size=0.2, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, shuffle=False
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler

# --- 5️ Entraîner RidgeCV ---
def train_ridge(X_train, y_train, alphas=[0.01, 0.1, 1.0, 10.0, 100.0]):
    ridge_cv = RidgeCV(alphas=alphas, store_cv_values=False)
    ridge_cv.fit(X_train, y_train)
    return ridge_cv

# --- 6️ Évaluer le modèle ---
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"RMSE : {rmse:.4f} | MAE : {mae:.4f} | R2 : {r2:.4f}")
    return y_pred

# --- 7️ Sauvegarde modèle et scaler ---
def save_model(model, scaler, model_path="models/ridge_cv_solar.pkl", scaler_path="models/scaler_ridge_solar.pkl"):
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    print("Modèle et scaler sauvegardés !")

# --- 8️ Script principal ---
if __name__ == "__main__":
    df = load_data("data/clean/historique_solaire_clean.csv")
    df_features = feature_engineering(df)
    X, y = prepare_xy(df_features)
    X_train_scaled, X_test_scaled, y_train, y_test, scaler = split_and_scale(X, y)
    ridge_cv = train_ridge(X_train_scaled, y_train)
    print("Meilleur alpha trouvé :", ridge_cv.alpha_)
    y_pred = evaluate_model(ridge_cv, X_test_scaled, y_test)
    save_model(ridge_cv, scaler)
