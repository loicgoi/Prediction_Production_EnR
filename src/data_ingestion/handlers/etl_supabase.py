import logging
import pandas as pd
from supabase import create_client, Client
from src.config.settings import settings

# CONFIGURATION SUPABASE
SUPABASE_URL = settings.supabase_url
SUPABASE_KEY = settings.supabase_key


class SupabaseHandler:
    """Gestionnaire principal de connexion à Supabase via REST API."""

    def __init__(self):
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("SUPABASE_URL et SUPABASE_KEY doivent être fournis")

        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logging.info("Connexion Supabase initialisée avec succès.")

    def upsert_dataframe(self, df: pd.DataFrame, table_name: str):
        """Insère ou met à jour les données dans une table Supabase."""
        if df.empty:
            logging.warning(f"Le DataFrame pour {table_name} est vide, rien à insérer.")
            return

        try:
            # DEBUG: Afficher les colonnes envoyées
            logging.info(f"Colonnes envoyées à {table_name}: {list(df.columns)}")

            # Conversion des dates pour éviter les erreurs JSON
            df = df.copy()
            for col in df.columns:
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    df[col] = df[col].dt.strftime("%Y-%m-%d %H:%M:%S")
                elif (
                    col in ["date", "time", "date_obs_elab", "date_prod"]
                    and df[col].dtype == "object"
                ):
                    try:
                        df[col] = pd.to_datetime(df[col]).dt.strftime("%Y-%m-%d")
                    except:
                        pass

            data = df.to_dict(orient="records")

            # Utilisation de upsert directement
            result = self.supabase.table(table_name).upsert(data).execute()
            logging.info(f"{len(df)} lignes upsertées dans {table_name}.")

        except Exception as e:
            logging.error(f"Erreur lors de l'insertion dans {table_name} : {e}")


class DataUploader:
    """Classe dédiée uniquement à l'upload des données vers Supabase."""

    def __init__(self, supabase_handler: SupabaseHandler):
        self.supabase_handler = supabase_handler

    def upload_raw_dataset(self, df: pd.DataFrame, dataset_name: str):
        """
        Upload UNIQUEMENT les données brutes vers les tables raw_*
        """
        if df.empty:
            logging.warning(f"Dataset {dataset_name} vide, rien à uploader.")
            return

        try:
            raw_table = f"raw_{dataset_name}"
            self.supabase_handler.upsert_dataframe(df, raw_table)
            logging.info(f"Données brutes uploadées: {raw_table}")

        except Exception as e:
            logging.error(
                f"Erreur lors de l'upload des données brutes {dataset_name}: {e}"
            )

    def upload_clean_dataset(self, df: pd.DataFrame, dataset_name: str):
        """
        Upload UNIQUEMENT les données nettoyées vers les tables clean_*
        """
        if df.empty:
            logging.warning(f"Dataset {dataset_name} vide, rien à uploader.")
            return

        try:
            clean_table = f"clean_{dataset_name}"
            self.supabase_handler.upsert_dataframe(df, clean_table)
            logging.info(f"Données nettoyées uploadées: {clean_table}")

        except Exception as e:
            logging.error(
                f"Erreur lors de l'upload des données nettoyées {dataset_name}: {e}"
            )