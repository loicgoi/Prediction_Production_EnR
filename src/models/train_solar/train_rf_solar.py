# train_rf.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

def load_data(path_csv):
    df = pd.read_csv(path_csv, parse_dates=['date'], index_col='date')
    X = df.drop(columns=['production'])
    y = df['production']
    return X, y

def preprocess_data(X, y, test_size=0.2):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, shuffle=False)
    return X_train, X_test, y_train, y_test

def train_rf(X_train, y_train, n_estimators=200, max_depth=20, random_state=42):
    model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=random_state)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print("RandomForest - Évaluation")
    print("RMSE :", rmse)
    print("MAE  :", mae)
    print("R2   :", r2)
    return y_pred

if __name__ == "__main__":
    X, y = load_data("data/clean/historique_solaire_clean.csv")
    X_train, X_test, y_train, y_test = preprocess_data(X, y)
    model = train_rf(X_train, y_train)
    y_pred = evaluate_model(model, X_test, y_test)
    
    # Sauvegarde
    joblib.dump(model, "models/rf_solar.pkl")
    print("Modèle sauvegardé !")
