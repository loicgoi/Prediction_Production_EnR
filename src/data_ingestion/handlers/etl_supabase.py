<<<<<<< HEAD
<<<<<<< HEAD
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
=======
<<<<<<<< HEAD:src/data_ingestion/etl_supabase.py
<<<<<<< HEAD
=======
# src/data_ingestion/etl_supabase.py (modifié)

>>>>>>> cbfd918 (Refacto de tout le code existant pour harmonisation et que tout soit fonctionnel)
from abc import ABC, abstractmethod
import pandas as pd
from supabase import create_client
from ..config.settings import settings
========
from abc import ABC, abstractmethod
import pandas as pd
from supabase import create_client
from src.config.settings import settings
>>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels):src/data_ingestion/handlers/etl_supabase.py
=======
# src/data_ingestion/handlers/etl_supabase.py
>>>>>>> 65ccff1 (refacto code + ajout du main.py fonctionnel)
import logging
import pandas as pd
from supabase import create_client, Client
from src.config.settings import settings
from pathlib import Path

<<<<<<< HEAD
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DataHandler(ABC):
    """
    Classe abstraite pour gérer le chargement, le nettoyage et la sauvegarde des données.
    """

    def __init__(self):
        self.client = create_client(settings.supabase_url, settings.supabase_key)
        self.pd = pd.DataFrame()
=======
# --- CONFIGURATION SUPABASE ---
SUPABASE_URL = settings.supabase_url
SUPABASE_KEY = settings.supabase_key


class SupabaseHandler:
    """Gestionnaire principal de connexion à Supabase via REST API."""

    def __init__(self):
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("SUPABASE_URL et SUPABASE_KEY doivent être fournis")
>>>>>>> 65ccff1 (refacto code + ajout du main.py fonctionnel)

        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logging.info("Connexion Supabase initialisée avec succès.")

        # Créer les tables via l'API REST (approche simplifiée)
        self.create_tables_simple()

<<<<<<< HEAD
    def _infert_sql_type(self, pd_type):
        """
        Infère le type SQL correspondant à un type de données pandas.

        Cette méthode prend un type pandas (`pd_type`) et renvoie
        le type SQL le plus approprié pour ce type.

        Types pandas gérés :
            - Integer   -> "INTEGER"
            - Float     -> "FLOAT"
            - Boolean   -> "BOOLEAN"
            - Datetime  -> "TIMESTAMP"
            - Autres    -> "TEXT"

        Paramètres
        ----------
        pd_type : pandas.api.types.CategoricalDtype, numpy.dtype ou similaire
            Le type de la colonne pandas à convertir en type SQL.

        Retour
        ------
        str
            Le type SQL correspondant sous forme de chaîne de caractères.
        """
        if pd.api.types.is_integer_dtype(pd_type):
            return "INTEGER"
        elif pd.api.types.is_float_dtype(pd_type):
            return "FLOAT"
        elif pd.api.types.is_bool_dtype(pd_type):
            return "BOOLEAN"
        elif pd.api.types.is_datetime64_any_dtype(pd_type):
            return "TIMESTAMP"
        else:
            return "TEXT"

    def save_to_db(
        self,
        table_name: str,
        if_exists="append",
        conflict_columns: Optional[List[str]] = None,
    ):
        """
        Sauvegarde le DataFrame dans Supabase avec création automatique de table/colonne.

        Args:
            table_name (str): Nom de la table dans Supabase.
            if_exists (str): Comportement si la table existe ('append' ou 'replace').
            conflict_columns (List[str], optional): Colonnes à utiliser pour détecter les conflits lors de l'insertion.
        """
        if self.df.empty:
            logging.warning(f"Dataframe vide pour la table '{table_name}'.")
            return

        df_to_insert = self.df.copy()
        for col in df_to_insert.columns:
            if pd.api.types.is_datetime64_any_dtype(df_to_insert[col]):
                df_to_insert[col] = df_to_insert[col].dt.strftime("%Y-%m-%d")

        try:
            self.client.table(table_name).select("*").limit(1).execute()
            table_exists = True
        except Exception:
            table_exists = False

        if table_exists and if_exists == "append":
            pass
        elif not table_exists or if_exists == "replace":
            if table_exists and if_exists == "replace":
                self.client.rpc(
                    "sql", {"query": f"DROP TABLE IF EXISTS {table_name};"}
                ).execute()

            cols_def = [
                f"{col} {self._infert_sql_type(self.df[col].dtype)}"
                for col in df_to_insert.columns
            ]
            create_table_query = f"CREATE TABLE {table_name} ({', '.join(cols_def)});"
            self.client.rpc("sql", {"query": create_table_query}).execute()
            logging.info(f"Table '{table_name}' créée.")

<<<<<<< HEAD
=======
        # Gestion des conflits si des colonnes de conflit sont spécifiées
        if conflict_columns and table_exists and if_exists == "append":
            # Récupération des enregistrements existants pour éviter les doublons
            existing_records = self.client.table(table_name).select("*").execute()
            existing_df = pd.DataFrame(existing_records.data)

            if not existing_df.empty:
                # Conversion des colonnes de conflit en types comparables
                for col in conflict_columns:
                    if col in existing_df.columns and col in df_to_insert.columns:
                        existing_df[col] = existing_df[col].astype(str)
                        df_to_insert[col] = df_to_insert[col].astype(str)

                # Fusion pour identifier les nouveaux enregistrements
                merged_df = df_to_insert.merge(
                    existing_df[conflict_columns],
                    on=conflict_columns,
                    how="left",
                    indicator=True,
                )

                # Ne conserver que les nouveaux enregistrements
                new_records = merged_df[merged_df["_merge"] == "left_only"].drop(
                    columns=["_merge"]
                )
                df_to_insert = new_records

                if not df_to_insert.empty:
                    logging.info(
                        f"{len(df_to_insert)} nouveaux enregistrements à insérer."
                    )
                else:
                    logging.info(
                        "Aucun nouvel enregistrement à insérer (tous existent déjà)."
                    )
                    return

        # Insertion des données
>>>>>>> cbfd918 (Refacto de tout le code existant pour harmonisation et que tout soit fonctionnel)
        records = df_to_insert.to_dict(orient="records")

        # Insertion par lots pour éviter les problèmes avec de grands volumes de données
        batch_size = 1000
        for i in range(0, len(records), batch_size):
            batch = records[i : i + batch_size]
=======
    def create_tables_simple(self):
        """Crée les tables via des insertions initiales."""
        # Cette approche laisse Supabase créer les tables automatiquement
        # au premier insert. C'est plus simple et évite les problèmes de connexion.
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

            # Utiliser insert au lieu de upsert pour la première création
>>>>>>> 65ccff1 (refacto code + ajout du main.py fonctionnel)
            try:
                result = self.supabase.table(table_name).insert(data).execute()
                logging.info(
                    f"{len(df)} lignes insérées dans {table_name} (première création)."
                )
            except Exception as e:
                # Si l'insert échoue, essayer upsert
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


# --- HANDLER POUR LES CSV LOCAUX ---
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

<<<<<<< HEAD
    def load(self) -> pd.DataFrame:
        self.df = self.loader_function(**self.loader_kwargs)
        return self.df
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
=======
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
>>>>>>> 65ccff1 (refacto code + ajout du main.py fonctionnel)
