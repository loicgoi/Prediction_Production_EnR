import pandas as pd
from .etl_supabase import APIDataHandler
import logging
from fetch_hubeau import get_hubeau_data


class HubeauDataHandler(APIDataHandler):
    """Gestionnaire pour charger, nettoyer et sauvegarder les données hydrométriques provenant de l'API Hub'Eau."""

    def __init__(self, code_station: str, start_date: str, end_date: str):
        super().__init__(
            loader_function=get_hubeau_data,
            code_station=code_station,
            start_date=start_date,
            end_date=end_date,
        )
        self.code_station = code_station
        self.table_name = "hydro_data"

    def clean(self):
        """Nettoie et prépare le DataFrame pour l'insertion en BDD."""
        if self.df.empty():
            logging.warning("Le DataFrame est vide, aucun nettoyage à faire.")
            return

        # Renommage des colonnes pour plus de clarté.
        column_mapping = {
            "date_obs_elab": "date",
            "result_obs_elab": "debit_l_s",
        }

        # Application des nouveaux noms de colonnes uniquement si existantes.
        for old_name, new_name in column_mapping.items():
            if old_name in self.df.columns:
                self.df = self.df.rename(columns={old_name: new_name})
                logging.info(f"Colonne '{old_name}' renommée en '{new_name}'.")

        # Conversion des types de données.
        if "date" in self.df.columns:
            self.df["date"] = pd.to_datetime(self.df["date"]).dt.date
            logging.info("Conversion de la 'date' en type date.")

        if "debit_l_s" in self.df.columns:
            self.df["debit_l_s"] = pd.to_numeric(self.df["debit_l_s"], errors="coerce")
            logging.info("Conversion de la colonne 'debit_l_s' en type numérique.")

        # Vérification et suppression des doublons.
        if "date" in self.df.columns:
            duplicate_count = self.df.duplicated(subset=["date"]).sum()
            if duplicate_count > 0:
                logging.info(
                    f"{duplicate_count} doublons trouvés basé sur la colonne 'date'."
                )
                self.df = self.df.drop_duplicates(subset=["date"], keep="first")
                logging.info(f"Suppresion des {duplicate_count} doublons.")

        # Gestion des valeurs manquantes.
        if "debit_l_s" in self.df.columns:
            missing_values = self.df["debit_l_s"].isna().sum()
            if missing_values > 0:
                logging.warning(
                    f"{missing_values} valeurs manquantes trouvées dans la colonne 'debit_l_s'."
                )
                if missing_values <= 100:
                    self.df = self.df.dropna(subset=["debit_l_s"])
                    logging.info(
                        f"Suppression des {missing_values} lignes avec des valeurs manquantes."
                    )
                else:
                    median_value = self.df["debit_l_s"].median()
                    self.df["debit_l_s"] = self.df["debit_l_s"].fillna(median_value)
                    logging.info(
                        f"Remplacement des {missing_values} valeurs manquantes par la mediane."
                    )

        # Gestion des valeurs aberrantes.
        if "debit_l_s" in self.df.columns:
            negative_count = (self.df["debit_l_s"] < 0).sum()
            if negative_count > 0:
                logging.warning(
                    f"{negative_count} valeurs négatives trouvées dans la colonne 'debit_m3_s'"
                )
                self.df = self.df[self.df["debit_m3_s"] >= 0]
                logging.info(f"Suppression des {negative_count} valeurs négatives")

        # Tri par date
        if "date" in self.df.columns:
            self.df = self.df.sort_values("date")
            logging.info("Tri du DataFrame par date")

        logging.info(f"Nettoyage terminé. {len(self.df)} enregistrements conservés.")
