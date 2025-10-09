import logging
import pandas as pd
from supabase import create_client, Client
from src.config.settings import settings
from pathlib import Path

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

        # Créer les tables via l'API REST
        self.create_tables_simple()

    def create_tables_simple(self):
        """Crée les tables via des insertions initiales."""
        logging.info("Les tables seront créées automatiquement au premier insert")

    def upsert_dataframe(self, df: pd.DataFrame, table_name: str):
        """Insère ou met à jour les données dans une table Supabase."""
        if df.empty:
            logging.warning(f"Le DataFrame pour {table_name} est vide, rien à insérer.")
            return

        try:
            # Conversion des dates pour éviter les erreurs JSON
            df = df.copy()
            for col in df.columns:
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    df[col] = df[col].dt.strftime("%Y-%m-%d %H:%M:%S")
                elif (
                    col in ["date", "time", "date_obs_elab", "date_prod"]
                    and df[col].dtype == "object"
                ):
                    # Essayer de convertir les colonnes de date string
                    try:
                        df[col] = pd.to_datetime(df[col]).dt.strftime("%Y-%m-%d")
                    except:
                        pass

            data = df.to_dict(orient="records")

            # Utilisation de insert pour la première création
            try:
                result = self.supabase.table(table_name).insert(data).execute()
                logging.info(
                    f"{len(df)} lignes insérées dans {table_name} (première création)."
                )
            except Exception as e:
                # Si l'insert échoue, on essaye upsert
                try:
                    result = self.supabase.table(table_name).upsert(data).execute()
                    logging.info(f"{len(df)} lignes upsertées dans {table_name}.")
                except Exception as e2:
                    logging.error(
                        f"Erreur lors de l'insertion dans {table_name} : {e2}"
                    )

        except Exception as e:
            logging.error(
                f"Erreur lors du traitement des données pour {table_name} : {e}"
            )


# HANDLER POUR LES CSV LOCAUX
class CSVDataHandler:
    """Gère le chargement, le nettoyage et l'envoi vers Supabase des CSV."""

    def __init__(self, supabase_handler: SupabaseHandler):
        self.supabase_handler = supabase_handler
        self.raw_path = Path(settings.data_raw_path)
        self.raw_path.mkdir(parents=True, exist_ok=True)

    def load_csv(self, file_path: str) -> pd.DataFrame:
        """Charge un CSV et renvoie un DataFrame."""
        try:
            df = pd.read_csv(file_path)
            logging.info(f"{len(df)} enregistrements chargés depuis {file_path}")
            return df
        except Exception as e:
            logging.error(f"Erreur lors du chargement du CSV {file_path}: {e}")
            return pd.DataFrame()

    def save_csv(self, df: pd.DataFrame, file_name: str):
        """Sauvegarde un DataFrame dans le dossier local data/raw."""
        try:
            path = self.raw_path / file_name
            df.to_csv(path, index=False)
            logging.info(f"CSV sauvegardé : {path}")
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde du CSV {file_name}: {e}")

    def upload_to_supabase(self, df: pd.DataFrame, table_prefix: str):
        """Insère les données dans Supabase (raw + clean)."""
        try:
            from src.data_ingestion.utils.data_cleaner import DataCleaner

            # Upload des données brutes
            self.supabase_handler.upsert_dataframe(df, f"raw_{table_prefix}")

            # Nettoyage et upload des données nettoyées
            if "solar" in table_prefix:
                df_clean = DataCleaner.clean_solar_data(df)
            elif "wind" in table_prefix:
                df_clean = DataCleaner.clean_wind_data(df)
            elif "hydro" in table_prefix or "hubeau" in table_prefix:
                df_clean = DataCleaner.clean_hydro_data(df)
            else:
                df_clean = df.copy()

            self.supabase_handler.upsert_dataframe(df_clean, f"clean_{table_prefix}")

        except Exception as e:
            logging.error(f"Erreur lors de l'upload Supabase {table_prefix}: {e}")
