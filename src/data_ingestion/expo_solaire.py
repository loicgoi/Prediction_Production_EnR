from logging import info
import os
import pandas as pd


#########_________Chargement des données__________#######
def load_and_clean_solar_data(filepath: str) -> pd.DataFrame:
    """
    Charge et prépare les données solaires historiques.
    
    Étapes :
    1. Lecture du fichier CSV.
    2. Renommage de la colonne 'time' en 'date'.
    3. Conversion en datetime des colonnes date, sunrise et sunset.
    
    Args:
        filepath (str): chemin du fichier CSV contenant les données brutes.
    
    Returns:
        pd.DataFrame: DataFrame nettoyé et prêt à l'analyse.
    """
    # Charger les données
    df = pd.read_csv(filepath)

    # Renommer 'time' to  'date' et convertir en datetime
    df = df.rename(columns={'time': 'date'})
    df['date'] = pd.to_datetime(df['date'])

    # Convertir sunrise et sunset en datetime
    df['sunrise'] = pd.to_datetime(df['sunrise'])
    df['sunset'] = pd.to_datetime(df['sunset'])
    
    return df

if __name__ == "__main__":
    # Détection automatique du chemin racine du projet
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    filepath = os.path.join(BASE_DIR, "data", "raw", "historique_solaire.csv")

    print(f"Chargement du fichier : {filepath}")

    # Chargement des données
    df_historical_solaire = load_and_clean_solar_data(filepath)
    print("\nAperçu des 5 premières lignes :")
    
print(df_historical_solaire.head())
### verification des types de données ###
print("\nInfos du DataFrame :")
print(df_historical_solaire.info())

#######__________________Vérification doublons + drop_____________________###########

def check_and_remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Vérifie s'il y a des doublons dans le DataFrame.
    Si des doublons existent, ils sont supprimés.
    Sinon, le DataFrame est retourné tel quel.
    """
    nb_doublons = df.duplicated().sum()
    if nb_doublons > 0:
        print(f"{nb_doublons} doublons trouvés. Suppression en cours...")
        df = df.drop_duplicates()
        print("Doublons supprimés.")
    else:
        print("Aucun doublon trouvé. Rien à faire.")
    return df

# Exemple d'utilisation
df_historical_solaire = check_and_remove_duplicates(df_historical_solaire)

##########___________________verification valeurs manquantes___________________________#########
def check_missing_values(df):
    """
    Vérifie les valeurs manquantes dans le DataFrame.
    Affiche le nombre de valeurs nulles par colonne.
    """
    missing = df.isnull().sum()
    total_missing = missing.sum()
    
    if total_missing == 0:
        print("Aucune valeur manquante dans le DataFrame.")
    else:
        print(f"{total_missing} valeurs manquantes trouvées :")
        print(missing[missing > 0])
    return df
# Exemple d'utilisation
df_historical_solaire = check_missing_values(df_historical_solaire)

#########______________traitement des valeurs manquantes avec interpolation_______________#########
def fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remplace les valeurs manquantes par interpolation temporelle ('time')
    uniquement sur les colonnes numériques.
    Définit la colonne 'date' comme index pour garantir la continuité temporelle.
    """
    df = df.copy()

    # Vérifier la colonne 'date'
    if 'date' not in df.columns:
        raise ValueError("La colonne 'date' est requise pour l'interpolation temporelle.")
    
    # Définir 'date' comme index temporel
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    # Sélectionner uniquement les colonnes numériques
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

    # Interpolation temporelle sur les colonnes numériques
    df[numeric_cols] = df[numeric_cols].interpolate(method='time')

    # Vérification des valeurs manquantes
    remaining_missing = df[numeric_cols].isnull().sum().sum()
    if remaining_missing == 0:
        print("Toutes les valeurs manquantes ont été interpolées avec succès.")
    else:
        print(f"Il reste {remaining_missing} valeurs manquantes après interpolation.")
    
    # Réinitialiser l'index
    df.reset_index(inplace=True)
    
    return df
#exemple d'utilisation : 
df_historical_solaire = fill_missing_values(df_historical_solaire)

##########________________________verification valeurs aberrantes ________________________________#########

def check_solar_data(df):
    """
    Vérifie la qualité des données pour un parc solaire.

    Contrôles réalisés :
    1️ Limites physiques : température, irradiation solaire, éventuellement production solaire.
    2️ Cohérence : sunshine_duration ≤ daylight_duration.
    3️ Pourcentages : cloud_cover_mean et relative_humidity_2m_mean entre 0 et 100.
    4️ Météo : précipitations et vent non négatifs.

    Args:
        df (pd.DataFrame): DataFrame contenant les données solaires.

    Affiche les anomalies détectées pour chaque contrôle.
    """
    # 1️ Min/max physiques
    physical_limits = {
        'temperature_2m_max': (-20, 50),
        'temperature_2m_min': (-30, 40),
        'shortwave_radiation_sum': (0, 35),  # extremes possibles a regler
        # 'production_solaire' si on a  une colonne réelle : (0, 150)
    }

    for col, (min_val, max_val) in physical_limits.items():
        if col in df.columns:
            outliers = df[(df[col] < min_val) | (df[col] > max_val)]
            if not outliers.empty:
                print(f"Valeurs aberrantes détectées dans {col} :")
                print(outliers[[col]])
            else:
                print(f"{col} OK.")

    # 2️ Cohérence entre colonnes
    if 'sunshine_duration' in df.columns and 'daylight_duration' in df.columns:
        invalid_sunshine = df[df['sunshine_duration'] > df['daylight_duration']]
        if not invalid_sunshine.empty:
            print("Durée d'ensoleillement > durée du jour détectée :")
            print(invalid_sunshine[['sunshine_duration', 'daylight_duration']])
        else:
            print("Durée d'ensoleillement OK.")

    # 3️ Pourcentages
    for col in ['cloud_cover_mean', 'relative_humidity_2m_mean']:
        if col in df.columns:
            invalid = df[(df[col] < 0) | (df[col] > 100)]
            if not invalid.empty:
                print(f"Valeurs aberrantes détectées dans {col} :")
                print(invalid[[col]])
            else:
                print(f"{col} OK.")

    # 4️ Précipitations et vent
    for col in ['precipitation_sum', 'wind_speed_10m_max']:
        if col in df.columns:
            invalid = df[df[col] < 0]
            if not invalid.empty:
                print(f"Valeurs négatives détectées dans {col} :")
                print(invalid[[col]])
            else:
                print(f"{col} OK.")
check_solar_data(df_historical_solaire)
##########_________Nettoyage / transformation des données________########
def convert_units(df):
    """
    Convertit certaines unités du dataset solaire pour faciliter l'interprétation :
    - Durées (sunshine_duration, daylight_duration) : secondes → heures pour etre plus lisibles.
    - Irradiation (shortwave_radiation_sum) : MJ/m² → kWh/m² utile pour calculer la production solaire

    Args:
        df (pd.DataFrame): DataFrame contenant les données solaires

    Returns:
        pd.DataFrame: DataFrame enrichi avec les colonnes converties
    """
    df = df.copy()

    # Conversion des durées en heures
    df["sunshine_duration_h"] = df["sunshine_duration"] / 3600
    df["daylight_duration_h"] = df["daylight_duration"] / 3600

    # Conversion de l'irradiation solaire de MJ/m² en kWh/m²
# 1 MJ = 1 000 000 J
# 1 kWh = 3 600 000 J
# Donc 1 MJ = 1 / 3.6 kWh ≈ 0.27778 kWh
    df["shortwave_radiation_sum_kWhm2"] = (
        df["shortwave_radiation_sum"] * 0.27778
    )

    return df
df_historical_solaire = convert_units(df_historical_solaire)
# Après nettoyage
df_historical_solaire = convert_units(df_historical_solaire)

# Vérification rapide
print(df_historical_solaire[[
    "sunshine_duration", "sunshine_duration_h",
    "daylight_duration", "daylight_duration_h",
    "shortwave_radiation_sum", "shortwave_radiation_sum_kWhm2"
]].head()) 
###########________ Selection des colonnes pertinentes________#########
def select_relevant_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sélectionne uniquement les colonnes utiles pour l'analyse et l'entraînement futur.
    
    Args:
        df (pd.DataFrame): DataFrame complet après nettoyage et conversion des unités
    
    Returns:
        pd.DataFrame: DataFrame réduit aux colonnes pertinentes
    """
    relevant_cols = [
        "date",
        "temperature_2m_max ",
        "temperature_2m_min ",
        "temperature_2m_mean",
        "shortwave_radiation_sum_kWhm2",
        "sunshine_duration_h",
        "daylight_duration_h",
        "cloud_cover_mean ",
        "relative_humidity_2m_mean",
        "precipitation_sum ",
        "wind_speed_10m_max"
    ]

    # Garder uniquement les colonnes disponibles dans df
    df_selected = df[[col for col in relevant_cols if col in df.columns]]
    
    print("\nColonnes retenues pour l'entraînement :")
    print(df_selected.columns.tolist())
    
    return df_selected

# Exemple d'utilisation
df_historical_solaire = select_relevant_columns(df_historical_solaire)
print(df_historical_solaire.head())
############_____________________________________###################
import os
import pandas as pd


#########_________Chargement des données__________#######
def load_and_clean_solar_data(filepath: str) -> pd.DataFrame:
    """
    Charge et prépare les données solaires historiques.
    
    Étapes :
    1. Lecture du fichier CSV.
    2. Renommage de la colonne 'time' en 'date'.
    3. Conversion en datetime des colonnes date, sunrise et sunset.
    
    Args:
        filepath (str): chemin du fichier CSV contenant les données brutes.
    
    Returns:
        pd.DataFrame: DataFrame nettoyé et prêt à l'analyse.
    """
    # Charger les données
    df = pd.read_csv(filepath)

    # Renommer 'time' -> 'date' et convertir en datetime
    df = df.rename(columns={'time': 'date'})
    df['date'] = pd.to_datetime(df['date'])

    # Convertir sunrise et sunset en datetime
    df['sunrise (iso8601)'] = pd.to_datetime(df['sunrise (iso8601)'])
    df['sunset (iso8601)'] = pd.to_datetime(df['sunset (iso8601)'])
    
    return df

if __name__ == "__main__":
    # Détection automatique du chemin racine du projet
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    filepath = os.path.join(BASE_DIR, "data", "raw", "open-meteo-solaire_hq.csv")

    print(f"Chargement du fichier : {filepath}")

    # Chargement des données
    df_historical_solaire = load_and_clean_solar_data(filepath)
    print("\nAperçu des 5 premières lignes :")
    
print(df_historical_solaire.head())
### verification des types de données ###
print("\nInfos du DataFrame :")
print(df_historical_solaire.info())

#######__________________Vérification doublons + drop_____________________###########

def check_and_remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Vérifie s'il y a des doublons dans le DataFrame.
    Si des doublons existent, ils sont supprimés.
    Sinon, le DataFrame est retourné tel quel.
    """
    nb_doublons = df.duplicated().sum()
    if nb_doublons > 0:
        print(f"{nb_doublons} doublons trouvés. Suppression en cours...")
        df = df.drop_duplicates()
        print("Doublons supprimés.")
    else:
        print("Aucun doublon trouvé. Rien à faire.")
    return df

# Exemple d'utilisation
df_historical_solaire = check_and_remove_duplicates(df_historical_solaire)

##########___________________verification valeurs manquantes___________________________#########
def check_missing_values(df):
    """
    Vérifie les valeurs manquantes dans le DataFrame.
    Affiche le nombre de valeurs nulles par colonne.
    """
    missing = df.isnull().sum()
    total_missing = missing.sum()
    
    if total_missing == 0:
        print("Aucune valeur manquante dans le DataFrame.")
    else:
        print(f"{total_missing} valeurs manquantes trouvées :")
        print(missing[missing > 0])
    return df
# Exemple d'utilisation
df_historical_solaire = check_missing_values(df_historical_solaire)

#########______________traitement des valeurs manquantes avec interpolation_______________#########

def fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remplace les valeurs manquantes par interpolation linéaire.
    Définit la colonne 'date' comme index pour garantir la continuité temporelle.
    
    Args:
        df (pd.DataFrame): DataFrame contenant des valeurs manquantes.
    
    Returns:
        pd.DataFrame: DataFrame avec les valeurs interpolées et index temporel.
    """
    df = df.copy()
    
    # S'assurer que la colonne 'date' existe
    if 'date' in df.columns:
        df.set_index('date', inplace=True)
    
    # Interpolation linéaire sur les colonnes numériques
    df = df.interpolate(method='linear')
    
    # Vérification finale
    remaining_missing = df.isnull().sum().sum()
    if remaining_missing == 0:
        print("Toutes les valeurs manquantes ont été interpolées.")
    else:
        print(f" Il reste {remaining_missing} valeurs manquantes après interpolation.")
    
    return df


# Exemple d'utilisation
df_historical_solaire = fill_missing_values(df_historical_solaire)

##########________________________verification valeurs aberrantes ________________________________#########

def check_solar_data(df):
    """
    Vérifie la qualité des données pour un parc solaire.

    Contrôles réalisés :
    1️ Limites physiques : température, irradiation solaire, éventuellement production solaire.
    2️ Cohérence : sunshine_duration ≤ daylight_duration.
    3️ Pourcentages : cloud_cover_mean et relative_humidity_2m_mean entre 0 et 100.
    4️ Météo : précipitations et vent non négatifs.

    Args:
        df (pd.DataFrame): DataFrame contenant les données solaires.

    Affiche les anomalies détectées pour chaque contrôle.
    """
    # 1️ Min/max physiques
    physical_limits = {
        'temperature_2m_max (°C)': (-20, 50),
        'temperature_2m_min (°C)': (-30, 40),
        'shortwave_radiation_sum (MJ/m²)': (0, 35),  # extremes possibles a regler 
        # 'production_solaire' si on a  une colonne réelle : (0, 150)
    }

    for col, (min_val, max_val) in physical_limits.items():
        if col in df.columns:
            outliers = df[(df[col] < min_val) | (df[col] > max_val)]
            if not outliers.empty:
                print(f"Valeurs aberrantes détectées dans {col} :")
                print(outliers[[col]])
            else:
                print(f"{col} OK.")

    # 2️ Cohérence entre colonnes
    if 'sunshine_duration (s)' in df.columns and 'daylight_duration (s)' in df.columns:
        invalid_sunshine = df[df['sunshine_duration (s)'] > df['daylight_duration (s)']]
        if not invalid_sunshine.empty:
            print("Durée d'ensoleillement > durée du jour détectée :")
            print(invalid_sunshine[['sunshine_duration (s)', 'daylight_duration (s)']])
        else:
            print("Durée d'ensoleillement OK.")

    # 3️ Pourcentages
    for col in ['cloud_cover_mean (%)', 'relative_humidity_2m_mean (%)']:
        if col in df.columns:
            invalid = df[(df[col] < 0) | (df[col] > 100)]
            if not invalid.empty:
                print(f"Valeurs aberrantes détectées dans {col} :")
                print(invalid[[col]])
            else:
                print(f"{col} OK.")

    # 4️ Précipitations et vent
    for col in ['precipitation_sum (mm)', 'wind_speed_10m_max (km/h)']:
        if col in df.columns:
            invalid = df[df[col] < 0]
            if not invalid.empty:
                print(f"Valeurs négatives détectées dans {col} :")
                print(invalid[[col]])
            else:
                print(f"{col} OK.")
check_solar_data(df_historical_solaire)
##########_________Nettoyage / transformation des données________########
def convert_units(df):
    """
    Convertit certaines unités du dataset solaire pour faciliter l'interprétation :
    - Durées (sunshine_duration, daylight_duration) : secondes → heures pour etre plus lisibles.
    - Irradiation (shortwave_radiation_sum) : MJ/m² → kWh/m² utile pour calculer la production solaire

    Args:
        df (pd.DataFrame): DataFrame contenant les données solaires

    Returns:
        pd.DataFrame: DataFrame enrichi avec les colonnes converties
    """
    df = df.copy()

    # Conversion des durées en heures
    df["sunshine_duration_h"] = df["sunshine_duration (s)"] / 3600
    df["daylight_duration_h"] = df["daylight_duration (s)"] / 3600

    # Conversion irradiation MJ/m² → kWh/m²
    df["shortwave_radiation_sum_kWhm2"] = (
        df["shortwave_radiation_sum (MJ/m²)"] * 0.27778
    )

    return df
df_historical_solaire = convert_units(df_historical_solaire)
# Après nettoyage
df_historical_solaire = convert_units(df_historical_solaire)

# Vérification rapide
print(df_historical_solaire[[
    "sunshine_duration (s)", "sunshine_duration_h",
    "daylight_duration (s)", "daylight_duration_h",
    "shortwave_radiation_sum (MJ/m²)", "shortwave_radiation_sum_kWhm2"
]].head()) 
###########________ Selection des colonnes pertinentes________#########
def select_relevant_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sélectionne uniquement les colonnes utiles pour l'analyse et l'entraînement futur.
    
    Args:
        df (pd.DataFrame): DataFrame complet après nettoyage et conversion des unités
    
    Returns:
        pd.DataFrame: DataFrame réduit aux colonnes pertinentes
    """
    relevant_cols = [
        "date",
        "temperature_2m_max (°C)",
        "temperature_2m_min (°C)",
        "temperature_2m_mean (°C)",
        "shortwave_radiation_sum_kWhm2",
        "sunshine_duration_h",
        "daylight_duration_h",
        "cloud_cover_mean (%)",
        "relative_humidity_2m_mean (%)",
        "precipitation_sum (mm)",
        "wind_speed_10m_max (km/h)"
    ]

    # Garder uniquement les colonnes disponibles dans df
    df_selected = df[[col for col in relevant_cols if col in df.columns]]
    
    print("\nColonnes retenues pour l'entraînement :")
    print(df_selected.columns.tolist())
    
    return df_selected

# Exemple d'utilisation
df_historical_solaire = select_relevant_columns(df_historical_solaire)
print(df_historical_solaire.head())
############_____________________________________###################