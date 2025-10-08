import pandas as pd

# Chargement de données 

def wind_loader(df_eolien_histo):

    """
    Chargement des données et affichage des 5 premiers lignes du DataFrame"""

    # Chargement des données csv 
    df_eolien_histo = pd.read_csv('/home/fadilatou/Prediction_Production_EnR/data/raw/eolien_histo.csv')

    # Affichage des 5 premiers lignes du df
    print (df_eolien_histo.head(5))


# Gestion des valeurs manquantes

def wind_isnull(df_eolien_histo):
    """
    Supprime les lignes contenant des valeurs manquantes (NaN)
    Retourne un DataFrame nettoyé.
    """
    df_clean = df_eolien_histo.copy()
    print("Valeurs manquantes avant nettoyage :")
    print(df_clean.isnull().sum())
    
    # Suppression des NaN
    df_clean = df_clean.dropna().reset_index(drop=True)
    print("\nValeurs manquantes après nettoyage :")
    print(df_clean.isnull().sum())
    
    return df_clean



#  Gestion des doublons

def wind_doublons(df_eolien_histo):
    """
    Supprime les doublons dans le DataFrame.
    Retourne un DataFrame nettoyé.
    """
    df_clean = df_eolien_histo.copy()
    print(f"Nombre de doublons avant nettoyage : {df_clean.duplicated().sum()}")
    
    # Suppression des doublons
    df_clean = df_clean.drop_duplicates().reset_index(drop=True)
    print(f"Nombre de doublons après nettoyage : {df_clean.duplicated().sum()}")
    
    return df_clean



#  Nettoyage et formatage des dates

def date_time(df_eolien_histo):
    """
    Renomme la colonne 'time' en 'date' si nécessaire
    et convertit la colonne 'date' au format datetime.
    """
    df_clean = df_eolien_histo.copy()

    # Renommer si la colonne 'time' existe
    if "time" in df_clean.columns:
        df_clean = df_clean.rename(columns={"time": "date"})
    
    # Conversion en datetime
    df_clean["date"] = pd.to_datetime(df_clean["date"], errors="coerce")

    # Supprimer les lignes avec dates invalides
    df_clean = df_clean.dropna(subset=["date"]).reset_index(drop=True)

    return df_clean



#  Valeurs aberrantes : vitesse du vent

def outliers_wind_speed(df, col="wind_speed_10m_max", min_val=0, max_val=150):
    """
    Supprime les valeurs aberrantes de la vitesse du vent (m/s).
    """
    df_clean = df[(df[col] >= min_val) & (df[col] <= max_val)].copy()
    return df_clean



#  Valeurs aberrantes : direction du vent

def outliers_wind_direction(df, col="wind_direction_10m_dominant", min_val=0, max_val=360):
    """
    Supprime les valeurs aberrantes de la direction du vent (°).
    """
    df_clean = df[(df[col] >= min_val) & (df[col] <= max_val)].copy()
    return df_clean



#  Valeurs aberrantes : pression de surface

def outliers_surface_pressure(df, col="surface_pressure_mean", min_val=950, max_val=1050):
    """
    Supprime les valeurs aberrantes de la pression de surface (hPa).
    """
    df_clean = df[(df[col] >= min_val) & (df[col] <= max_val)].copy()
    return df_clean




# # Vérification et teste des fonction prédéfini

# if __name__ == "__main__":

#     # Chargement des données csv 
#     df_eolien_histo = pd.read_csv('/home/fadilatou/Prediction_Production_EnR/data/raw/eolien_histo.csv')
#     df_clean = df_eolien_histo.copy()

# # Gestion des valeurs manquantes
#     df_clean = wind_isnull(df_clean)

# # Gestion des doublons 
#     df_clean = wind_doublons(df_clean)

# # Nettoyage et formatage de la colonne date
#     df_clean = date_time(df_clean)

# # Valeurs aberrantes vitesse du vent
#     df_clean = outliers_wind_speed(df_clean)

# # Valeurs aberrantes direction du vent
#     df_clean = outliers_wind_direction(df_clean)

# # Valeurs aberrantes pression de surface
#     df_clean = outliers_surface_pressure(df_clean)