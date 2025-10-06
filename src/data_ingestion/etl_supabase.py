from abc import ABC, abstractmethod
import pandas as pd
from supabase import create_client
from ..config.settings import settings
import logging
import os

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

    def save_to_db(self, table_name: str, if_exists="append"):
        """
        Sauvegarde le DataFrame dans Supabase avec création automatique de table/colonne.
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
