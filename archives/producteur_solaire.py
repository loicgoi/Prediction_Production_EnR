import pandas as pd
from abc import ABC, abstractmethod


# Classe abstraite
class Producteur(ABC):
    def __init__(self, nom: str, lieu: str, puissance_nominale: float):
        self.nom = nom
        self.lieu = lieu
        self.puissance_nominale = puissance_nominale
        self.df = None  
        
    @abstractmethod
    def load_data(self, filepath: str):
        """Charge les données du producteur"""
        pass

    @abstractmethod
    def clean_data(self):
        """Nettoie et prépare les données"""
        pass
    
    def calcul_stats(self):
        """Calcule des stats de base sur la production/variables météo"""
        if self.df is not None:
            return self.df.describe()
        else:
            return "Pas de données chargées."
    
#########_________________ProducteurSolaire____________###########

    # Sous-classe ProducteurSolaire  
class ProducteurSolaire(Producteur):
    def __init__(self, nom: str, lieu: str, puissance_nominale: float = 150.0):
        super().__init__(nom, lieu, puissance_nominale)
    
    def load_data(self, filepath: str):
        """Charge les données solaires depuis un CSV"""
        df = pd.read_csv(filepath)
        df = df.rename(columns={'time': 'date'})
        df['date'] = pd.to_datetime(df['date'])
        self.df = df
        print(f"{len(df)} lignes chargées pour {self.nom}")
        return self.df

    def clean_data(self):
        """Nettoyage basique : doublons, valeurs manquantes, conversions unités"""
        if self.df is None:
            raise ValueError("Les données doivent être chargées avant nettoyage.")
        
        # Suppression doublons
        self.df.drop_duplicates(inplace=True)

        # Valeurs manquantes + interpolation
        self.df.set_index("date", inplace=True)
        self.df = self.df.interpolate(method="linear")

        # Conversion des unités
        if "sunshine_duration" in self.df.columns:
            self.df["sunshine_duration_h"] = self.df["sunshine_duration"] / 3600
        if "daylight_duration" in self.df.columns:
            self.df["daylight_duration_h"] = self.df["daylight_duration"] / 3600
        if "shortwave_radiation_sum" in self.df.columns:
            self.df["shortwave_radiation_sum_kWhm2"] = self.df["shortwave_radiation_sum"] * 0.27778
# Conversion de l'irradiation solaire de MJ/m² en kWh/m²: 
# 1 MJ = 1 000 000 J   # 1 kWh = 3 600 000 J  # Donc 1 MJ = 1 / 3.6 kWh ≈ 0.27778 kWh
        print("Nettoyage terminé pour les données solaires.")
        return self.df