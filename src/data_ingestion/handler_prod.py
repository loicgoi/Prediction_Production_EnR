import pandas as pd
from .etl_supabase import CSVDataHandler
import logging


class ProductionDataHandler(CSVDataHandler):
    def __init__(self, file_path: str, producer_type: str):
        super().__init__(file_path)
        self.producer_type = producer_type
        self.table_name = f"production_{producer_type}"

    def clean(self):
        """Nettoie et prépare le DataFrame pour l'insertion."""
        super().clean()

        if self.producer_type == "eolien":
            self.df = self.df.rename(columns={"prod_eolienne": "production_kwh"})
        elif self.producer_type == "hydraulique":
            self.df = self.df.rename(
                columns={"date_obs_elab": "date", "prod_hydro": "production_kwh"}
            )
        elif self.producer_type == "solaire":
            self.df = self.df.rename(columns={"prod_solaire": "production_kwh"})

        if "date" not in self.df.columns:
            logging.error(
                f"Colonne 'date' non trouvées dans le fichier {self.file_path}"
            )
            return

        self.df["date"] = pd.to_datetime(self.df["date"]).dt.date
        self.df["production_kwh"] = pd.to_numeric(
            self.df["production_kwh"], errors="coerce"
        )

        self.df.dropna(subset=["date", "production_kwh"], inplace=True)
        self.df = self.df[self.df["production_kwh"] >= 0]
        self.df.drop_duplicates(subset=["date"], keep="first", inplace=True)

        logging.info(
            f"Nettoyage des données de production '{self.producer_type}' terminé. {len(self.df)} lignes."
        )
