# src/data_ingestion/etl_supabase.py

from abc import ABC, abstractmethod
import pandas as pd
from supabase import create_client
from ..config.settings import settings
import logging
import os

# Configuration logging (infos + claires lors de l'exécution)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DataHandler(ABC):
    """
    Classe abstraite pour gérer le chargement, le nettoyage et la sauvegarde des données
    avec création automatique du schéma de la table dans Supabase.
    """

    def __init__(self):
        self.client = create_client(settings.supabase_url, settings.supabase_key)
        self.df = pd.DataFrame()

    @abstractmethod
    def load(self) -> pd.DataFrame:
        """
        Charge les données et retourne un Dataframe.
        """
        pass

    def clean(self):
        """
        Nettoyage optionnel des données. A redéfinir dans la sous-classe au besoin.
        """
        pass

    def _infer_sql_type(self, pd_type):
        """
        Infère le type SQL correspondant à un type de données pandas.
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

    def save_to_db(self, table_name: str, if_exists="append"):
        """
        Sauvegarde le DataFrame dans Supabase avec création automatique de table/colonne.
        """
        if self.df.empty:
            logging.warning(
                f"Le Dataframe est vide. Aucune données à insérer dans '{table_name}'."
            )
            return

        df_to_insert = self.df.copy()

        # Gérer les colonnes de date pour éviter les erreurs SQL.
        for col in df_to_insert.columns:
            if pd.api.types.is_datetime64_any_dtype(df_to_insert[col]):
                df_to_insert[col] = df_to_insert[col].dt.strftime("%Y-%m-%d")

        # Vérifier si la table existe.
        try:
            self.client.table(table_name).select("*").limit(1).execute()
            table_exists = True
        except Exception:
            table_exists = False

        # Si la table existe, ajoute les nouvelles colonnes si nécessaire.
        if table_exists and if_exists == "append":
            logging.info(
                f"La table '{table_name}' existe. Vérification des nouvelles colonnes."
            )
            existing_cols_response = (
                self.client.table("information_schema.columns")
                .select("column_name")
                .eq("table_name", table_name)
                .execute()
            )
            existing_cols = {col["column_name"] for col in existing_cols_response.data}

            new_cols = set(df_to_insert.columns) - existing_cols
            if new_cols:
                for col in new_cols:
                    sql_type = self._infer_sql_type(self.df[col].dtype)
                    try:
                        self.client.rpc(
                            "sql",
                            {
                                "query": f"ALTER TABLE {table_name} ADD COLUMN {col} {sql_type};"
                            },
                        ).execute()
                        logging.info(
                            f"Nouvelle colonne '{col}' ({sql_type}) ajoutée à la table '{table_name}'."
                        )
                    except Exception as e:
                        logging.error(
                            f"Impossible d'ajouter la colonne '{col}' à '{table_name}': {e}"
                        )
        # Si la table n'existe pas ou qu'on doit la remplacer.
        elif not table_exists or if_exists == "replace":
            if table_exists and if_exists == "replace":
                self.client.rpc(
                    "sql", {"query": f"DROP TABLE IF EXISTS {table_name};"}
                ).execute()

            cols_def = [
                f"{col} {self._infer_sql_type(self.df[col].dtype)}"
                for col in df_to_insert.columns
            ]
            create_table_query = f"CREATE TABLE {table_name} ({', '.join(cols_def)});"
            self.client.rpc("sql", {"query": create_table_query}).execute()
            logging.info(f"Table '{table_name}' créée.")

        # Insertion les données
        records = df_to_insert.to_dict(orient="records")
        self.client.table(table_name).insert(records).execute()
        logging.info(f"{len(records)} enregistrements insérés dans '{table_name}'.")


class CSVDataHandler(DataHandler):
    """
    Gestionnaire pour charger des CSV locaux.
    """

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path

    def load(self) -> pd.DataFrame:
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Le fichier {self.file_path} n'existe pas.")
        self.df = pd.read_csv(self.file_path)
        return self.df


class APIDataHandler(DataHandler):
    """
    Gestionnaire pour charger des données via API.
    """

    def __init__(self, loader_function, **kwargs):
        super().__init__()
        self.loader_function = loader_function
        self.loader_kwargs = kwargs

    def load(self) -> pd.DataFrame:
        self.df = self.loader_function(**self.loader_kwargs)
        return self.df
