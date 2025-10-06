from abc import ABC, abstractmethod
import pandas as pd
from supabase import create_client
import os


class DataHandler(ABC):
    """
    Classe abstraite pour gérer le chargement, le nettoyage et la sauvegarde des données.
    """

    def __init__(self, supabase_url: str, supabase_key: str):
        self.client = create_client(supabase_url, supabase_key)
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

    def save_to_db(self, table_name: str):
        """
        Sauvegarde le DataFrame dans Supabase avec création automatique de table/colonne.
        """
        if self.df.empty:
            self.df = self.load()
            self.clean()

        df_to_insert = self.df.copy()
        df_to_insert = df_to_insert.astype(str)
        columns = df_to_insert.columns.tolist()

        tables = (
            self.client.table("information_schema.table")
            .select("table_name")
            .execute()
            .data
        )
        table_names = [table["table_name"] for table in tables]

        if table_name not in table_names:
            cols_def = ", ".join([f"{col} TEXT" for col in columns])
            self.client.rpc(
                "sql", {"query": f"CREATE TABLE {table_name} ({cols_def});"}
            ).execute()
        else:
            existing_cols_info = (
                self.client.table("information_schema.columns")
                .select("column_name")
                .eq("table_name", table_name)
                .execute()
                .data
            )
            existing_cols = [column["column_name"] for column in existing_cols_info]

            for col in columns:
                if col not in existing_cols:
                    self.client.rpc(
                        "sql",
                        {"query": f"ALTER TABLE {table_name} ADD COLUMN {col} TEXT;"},
                    ).execute()

        records = df_to_insert.to_dict(orient="records")
        self.client.table(table_name).insert(records).execute()
        print(f"Données insérées dans la table '{table_name}'")


class CSVDataHandler(DataHandler):
    """
    Gestionnaire pour charger des CSV locaux.
    """

    def __init__(self, file_path: str, supabase_url: str, supabase_key: str):
        super().__init__(supabase_url, supabase_key)
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

    def __init__(self, loader_function, supabase_url: str, supabase_key: str, **kwargs):
        super().__init__(supabase_url, supabase_key)
        self.loader_function = loader_function
        self.loader_kwargs = kwargs

    def load(self) -> pd.DataFrame:
        self.df = self.loader_function(**self.loader_kwargs)
        return self.df
