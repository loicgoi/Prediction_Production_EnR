import pandas as pd
import logging


class DataCleaner:
    """Classe pour centraliser toutes les opérations de nettoyage des données."""

    @staticmethod
    def clean_solar_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Nettoie les données solaires - POUR TABLES CLEAN AVEC CONVERSIONS
        """
        if df.empty:
            return df

        df_clean = df.copy()

        # Renommage
        if "time" in df_clean.columns:
            df_clean = df_clean.rename(columns={"time": "date"})

        # Conversion datetime
        if "date" in df_clean.columns:
            df_clean["date"] = pd.to_datetime(df_clean["date"])

        # CORRECTION : Appliquer les conversions UNIQUEMENT pour les données clean
        df_clean = DataCleaner._convert_solar_units_for_clean_tables(df_clean)

        # Sélection des colonnes POUR TABLES CLEAN (avec noms convertis)
        relevant_cols = [
            "date",
            "temperature_2m_max",
            "temperature_2m_min",
            "temperature_2m_mean",
            "shortwave_radiation_sum_kwh_m2",  # Nom converti pour tables clean
            "sunshine_duration",
            "daylight_duration",
            "cloud_cover_mean",
            "relative_humidity_2m_mean",
            "precipitation_sum",
            "wind_speed_10m_mean",
        ]

        # Garder uniquement les colonnes disponibles
        available_cols = [col for col in relevant_cols if col in df_clean.columns]
        df_clean = df_clean[available_cols]

        # Suppression des doublons
        df_clean = DataCleaner._remove_duplicates(df_clean, "date")

        # Vérification valeurs manquantes
        df_clean = DataCleaner._handle_missing_values(df_clean)

        # Vérification valeurs aberrantes
        df_clean = DataCleaner._check_solar_outliers(df_clean)

        return df_clean

    @staticmethod
    def prepare_solar_data_raw(df: pd.DataFrame) -> pd.DataFrame:
        """
        Prépare les données solaires brutes - SANS AUCUNE CONVERSION
        Pour les tables raw_*
        """
        if df.empty:
            return df

        df_raw = df.copy()

        # Renommage basique
        if "time" in df_raw.columns:
            df_raw = df_raw.rename(columns={"time": "date"})

        # Conversion datetime uniquement
        if "date" in df_raw.columns:
            df_raw["date"] = pd.to_datetime(df_raw["date"])

        # CORRECTION CRITIQUE : NE PAS APPLIQUER LES CONVERSIONS DU TOUT
        # Garder TOUTES les colonnes originales sans modifications
        # Les tables raw attendent shortwave_radiation_sum (pas kwh_m2)

        # Sélection des colonnes POUR TABLES RAW (noms originaux)
        relevant_cols_raw = [
            "date",
            "temperature_2m_max",
            "temperature_2m_min",
            "temperature_2m_mean",
            "shortwave_radiation_sum",  # Nom ORIGINAL pour tables raw
            "sunshine_duration",
            "daylight_duration",
            "cloud_cover_mean",
            "relative_humidity_2m_mean",
            "precipitation_sum",
            "wind_speed_10m_mean",
        ]

        # Garder uniquement les colonnes disponibles
        available_cols = [col for col in relevant_cols_raw if col in df_raw.columns]
        df_raw = df_raw[available_cols]

        return df_raw

    @staticmethod
    def clean_hydro_data(df: pd.DataFrame) -> pd.DataFrame:
        """Nettoie les données hydrauliques - POUR TABLES CLEAN."""
        if df.empty:
            return df

        df_clean = df.copy()

        # CORRECTION : Pour clean_hubeau, utiliser 'date' et 'debit_l_s'
        if "date_obs_elab" in df_clean.columns:
            df_clean = df_clean.rename(columns={"date_obs_elab": "date"})

        # CORRECTION : Utiliser 'debit_l_s' pour clean_hubeau (nom de la table)
        if "result_obs_elab" in df_clean.columns:
            df_clean = df_clean.rename(columns={"result_obs_elab": "debit_l_s"})
        # CORRECTION : Gérer aussi le nom 'resultat_obs_elab' venant de l'API
        elif "resultat_obs_elab" in df_clean.columns:
            df_clean = df_clean.rename(columns={"resultat_obs_elab": "debit_l_s"})

        # Conversion des types
        if "date" in df_clean.columns:
            df_clean["date"] = pd.to_datetime(df_clean["date"])

        if "debit_l_s" in df_clean.columns:
            df_clean["debit_l_s"] = pd.to_numeric(
                df_clean["debit_l_s"], errors="coerce"
            )

        # Suppression des colonnes inutiles
        columns_to_drop = [
            "code_site",
            "code_station",
            "date_prod",
            "code_statut",
            "libelle_statut",
            "code_methode",
            "libelle_methode",
            "code_qualification",
            "libelle_qualification",
            "longitude",
            "latitude",
            "grandeur_hydro_elab",
        ]

        existing_columns_to_drop = [
            col for col in columns_to_drop if col in df_clean.columns
        ]
        if existing_columns_to_drop:
            df_clean = df_clean.drop(columns=existing_columns_to_drop)

        # Suppression des doublons
        df_clean = DataCleaner._remove_duplicates(df_clean, "date")

        # Gestion valeurs manquantes et négatives
        if "debit_l_s" in df_clean.columns:
            df_clean = df_clean[df_clean["debit_l_s"] >= 0]
            df_clean = DataCleaner._handle_missing_values(df_clean, ["debit_l_s"])

        return df_clean

    @staticmethod
    def prepare_hydro_data_raw(df: pd.DataFrame) -> pd.DataFrame:
        """
        Prépare les données hydrauliques brutes - SANS NETTOYAGE
        Pour les tables raw_*
        """
        if df.empty:
            return df

        df_raw = df.copy()

        # Conversion datetime uniquement - garder les noms originaux pour raw_hubeau
        if "date_obs_elab" in df_raw.columns:
            df_raw["date_obs_elab"] = pd.to_datetime(df_raw["date_obs_elab"])

        return df_raw

    @staticmethod
    def clean_wind_data(df: pd.DataFrame) -> pd.DataFrame:
        """Nettoie les données éoliennes."""
        if df.empty:
            return df

        df_clean = df.copy()

        # Renommage et conversion de la date
        if "time" in df_clean.columns:
            df_clean = df_clean.rename(columns={"time": "date"})
        if "date" in df_clean.columns:
            df_clean["date"] = pd.to_datetime(df_clean["date"], errors="coerce")
            df_clean = df_clean.dropna(subset=["date"]).reset_index(drop=True)

        relevant_cols = [
            "date",
            "wind_speed_10m_max",
            "wind_gusts_10m_max",
            "wind_direction_10m_dominant",
            "wind_gusts_10m_mean",
            "temperature_2m_mean",
            "surface_pressure_mean",
            "cloud_cover_mean",
        ]

        # Garder uniquement les colonnes disponibles dans df
        df_clean = df_clean[[col for col in relevant_cols if col in df_clean.columns]]

        # Suppression des doublons
        df_clean = DataCleaner._remove_duplicates(df_clean, "date")

        # Vérification valeurs manquantes
        df_clean = DataCleaner._handle_missing_values(df_clean)

        # Valeurs aberrantes
        if "wind_speed_10m_max" in df_clean.columns:
            df_clean = DataCleaner._remove_outliers(
                df_clean, "wind_speed_10m_max", 0, 150
            )

        if "wind_direction_10m_dominant" in df_clean.columns:
            df_clean = DataCleaner._remove_outliers(
                df_clean, "wind_direction_10m_dominant", 0, 360
            )

        if "surface_pressure_mean" in df_clean.columns:
            df_clean = DataCleaner._remove_outliers(
                df_clean, "surface_pressure_mean", 950, 1050
            )

        return df_clean

    @staticmethod
    def prepare_wind_data_raw(df: pd.DataFrame) -> pd.DataFrame:
        """
        Prépare les données éoliennes brutes - SANS NETTOYAGE
        Pour les tables raw_*
        """
        if df.empty:
            return df

        df_raw = df.copy()

        # Renommage basique
        if "time" in df_raw.columns:
            df_raw = df_raw.rename(columns={"time": "date"})

        # Conversion datetime uniquement
        if "date" in df_raw.columns:
            df_raw["date"] = pd.to_datetime(df_raw["date"], errors="coerce")

        return df_raw

    @staticmethod
    def clean_production_data(df: pd.DataFrame, producer_type: str) -> pd.DataFrame:
        """Nettoie les données de production."""
        if df.empty:
            return df

        df_clean = df.copy()

        # Standardisation des noms de colonnes
        production_columns = {
            "solar": {"prod_solaire": "production_kwh"},
            "wind": {"prod_eolienne": "production_kwh"},
            "hydro": {"prod_hydro": "production_kwh", "date_obs_elab": "date"},
        }

        if producer_type in production_columns:
            for old_name, new_name in production_columns[producer_type].items():
                if old_name in df_clean.columns:
                    df_clean = df_clean.rename(columns={old_name: new_name})

        # Conversion des types
        if "date" in df_clean.columns:
            df_clean["date"] = pd.to_datetime(df_clean["date"])

        if "production_kwh" in df_clean.columns:
            df_clean["production_kwh"] = pd.to_numeric(
                df_clean["production_kwh"], errors="coerce"
            )

        # Suppression des valeurs négatives et manquantes
        if "production_kwh" in df_clean.columns:
            df_clean = df_clean[df_clean["production_kwh"] >= 0]
            df_clean = df_clean.dropna(subset=["date", "production_kwh"])

        # Suppression des doublons
        df_clean = DataCleaner._remove_duplicates(df_clean, "date")

        # Tri par date
        if "date" in df_clean.columns:
            df_clean = df_clean.sort_values("date")

        return df_clean

    @staticmethod
    def prepare_production_data_raw(
        df: pd.DataFrame, producer_type: str
    ) -> pd.DataFrame:
        """
        Prépare les données de production brutes - SANS NETTOYAGE
        Pour les tables raw_*
        """
        if df.empty:
            return df

        df_raw = df.copy()

        # Conversion datetime uniquement - GARDER LES NOMS ORIGINAUX
        if "date" in df_raw.columns:
            df_raw["date"] = pd.to_datetime(df_raw["date"])

        # CORRECTION SPÉCIALE pour raw_prod_hydro : utiliser date_obs_elab si nécessaire
        if producer_type == "hydro" and "date" in df_raw.columns:
            # Pour raw_prod_hydro qui attend date_obs_elab
            df_raw = df_raw.rename(columns={"date": "date_obs_elab"})

        # Garder prod_solaire, prod_eolienne, prod_hydro pour les tables raw
        # Sélectionner uniquement les colonnes existantes
        available_cols = []

        if producer_type == "solar":
            if "date" in df_raw.columns:
                available_cols.append("date")
            if "prod_solaire" in df_raw.columns:
                available_cols.append("prod_solaire")

        elif producer_type == "wind":
            if "date" in df_raw.columns:
                available_cols.append("date")
            if "prod_eolienne" in df_raw.columns:
                available_cols.append("prod_eolienne")

        elif producer_type == "hydro":
            # CORRECTION : Pour hydro, utiliser date_obs_elab et prod_hydro
            if "date_obs_elab" in df_raw.columns:
                available_cols.append("date_obs_elab")
            elif "date" in df_raw.columns:
                available_cols.append("date")
            if "prod_hydro" in df_raw.columns:
                available_cols.append("prod_hydro")

        return df_raw[available_cols] if available_cols else df_raw

    @staticmethod
    def _convert_solar_units_for_clean_tables(df: pd.DataFrame) -> pd.DataFrame:
        """Convertit les unités SPÉCIALEMENT pour les tables clean."""
        # Conversion MJ/m² -> kWh/m² UNIQUEMENT
        if "shortwave_radiation_sum" in df.columns:
            df["shortwave_radiation_sum_kwh_m2"] = (
                df["shortwave_radiation_sum"] * 0.27778
            )
            # Supprimer la colonne originale pour ne garder que la convertie
            df = df.drop(columns=["shortwave_radiation_sum"])

        return df

    @staticmethod
    def _remove_duplicates(df: pd.DataFrame, subset: str) -> pd.DataFrame:
        """Supprime les doublons basés sur une colonne."""
        if subset in df.columns:
            duplicate_count = df.duplicated(subset=[subset]).sum()
            if duplicate_count > 0:
                logging.info(
                    f"Suppression de {duplicate_count} doublons basés sur '{subset}'"
                )
                df = df.drop_duplicates(subset=[subset], keep="first")
        return df

    @staticmethod
    def _handle_missing_values(df: pd.DataFrame, numeric_columns=None) -> pd.DataFrame:
        """Gère les valeurs manquantes par interpolation."""
        if numeric_columns is None:
            numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()

        missing_count = df[numeric_columns].isnull().sum().sum()
        if missing_count > 0:
            logging.info(f"Interpolation de {missing_count} valeurs manquantes")
            df[numeric_columns] = df[numeric_columns].interpolate(method="linear")

        return df

    @staticmethod
    def _check_solar_outliers(df: pd.DataFrame) -> pd.DataFrame:
        """Vérifie les valeurs aberrantes pour les données solaires."""
        limits = {
            "temperature_2m_max": (-20, 50),
            "temperature_2m_min": (-30, 40),
            "shortwave_radiation_sum": (0, 35),
        }

        for col, (min_val, max_val) in limits.items():
            if col in df.columns:
                outliers = (df[col] < min_val) | (df[col] > max_val)
                if outliers.any():
                    logging.warning(f"Valeurs aberrantes détectées dans {col}")

        if all(col in df.columns for col in ["sunshine_duration", "daylight_duration"]):
            invalid = df["sunshine_duration"] > df["daylight_duration"]
            if invalid.any():
                logging.warning("Durée d'ensoleillement > durée du jour détectée")

        return df

    @staticmethod
    def _remove_outliers(
        df: pd.DataFrame, col: str, min_val: float, max_val: float
    ) -> pd.DataFrame:
        """Supprime les valeurs aberrantes pour une colonne numérique."""
        before = len(df)
        df_clean = df[(df[col] >= min_val) & (df[col] <= max_val)].copy()
        removed = before - len(df_clean)
        if removed > 0:
            logging.warning(f"{removed} valeurs aberrantes supprimées dans {col}")
        return df_clean