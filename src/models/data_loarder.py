import pandas as pd
from supabase import create_client
from src.config.settings import settings


class SupabaseDataLoader:
    def __init__(self):
        self.supabase = create_client(settings.supabase_url, settings.supabase_key)

    def load_training_data(self, producer_type: str) -> pd.DataFrame:
        """
        Charge et joint les données pour l'entrainement.
        """
        # Jointure météo solaire + production solaire
        if producer_type == "solar":
            weather_data = (
                self.supabase.table("clean_solar_history").select("*").execute()
            )
            production_data = (
                self.supabase.table("clean_prod_solaire").select("*").execute()
            )

        # Jointure météo éolienne + production éolienne
        elif producer_type == "wind":
            weather_data = (
                self.supabase.table("clean_wind_history").select("*").execute()
            )
            production_data = (
                self.supabase.table("clean_prod_eolienne").select("*").execute()
            )

        # Jointure données Hub'Eau + production hydro
        elif producer_type == "hydro":
            weather_data = self.supabase.table("clean_hubeau").select("*").execute()
            production_data = (
                self.supabase.table("clean_prod_hydro").select("*").execute()
            )

        else:
            raise ValueError(f"Type de producteur inconnu: {producer_type}.")

        # Conversion en DataFrame et jointure sur date
        df_weather = pd.DataFrame(weather_data.data)
        df_production = pd.DataFrame(production_data.data)

        # Standardisation des colonnes date
        df_weather["date"] = pd.to_datetime(df_weather["date"])
        df_production["date"] = pd.to_datetime(df_production["date"])

        merged_df = pd.merge(df_weather, df_production, on="date", how="inner")

        return merged_df
