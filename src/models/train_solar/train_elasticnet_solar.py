# train_elasticnet.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ElasticNetCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

def load_data(path_csv):
    df = pd.read_csv(path_csv, parse_dates=['date'], index_col='date')
    X = df.drop(columns=['production'])
    y = df['production']
    return X, y

def preprocess_data(X, y, test_size=0.2):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, shuffle=False)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler

def train_elasticnet(X_train, y_train, l1_ratio=[0.1,0.5,0.7,0.9,1.0], alphas=None):
    model = ElasticNetCV(l1_ratio=l1_ratio, alphas=alphas, cv=5)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print("ElasticNet - Évaluation")
    print("RMSE :", rmse)
    print("MAE  :", mae)
    print("R2   :", r2)
    return y_pred

if __name__ == "__main__":
    X, y = load_data("data/clean/historique_solaire_clean.csv")
    X_train, X_test, y_train, y_test, scaler = preprocess_data(X, y)
    model = train_elasticnet(X_train, y_train)
    y_pred = evaluate_model(model, X_test, y_test)
    
    # Sauvegarde
    joblib.dump(model, "models/elasticnet_solar.pkl")
    joblib.dump(scaler, "models/scaler_elasticnet_solar.pkl")
    print("Modèle et scaler sauvegardés !")
