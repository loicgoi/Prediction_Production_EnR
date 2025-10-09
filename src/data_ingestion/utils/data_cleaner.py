import pandas as pd
import logging


class DataCleaner:
    """Classe pour centraliser toutes les opérations de nettoyage des données."""

    @staticmethod
    def clean_solar_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Nettoie les données solaires avec toutes les vérifications de expo_solaire.py
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

        # Conversion sunrise/sunset
        for col in ["sunrise", "sunset"]:
            if col in df_clean.columns:
                df_clean[col] = pd.to_datetime(df_clean[col])

        # Suppression des doublons
        df_clean = DataCleaner._remove_duplicates(df_clean, "date")

        # Vérification valeurs manquantes
        df_clean = DataCleaner._handle_missing_values(df_clean)

        # Vérification valeurs aberrantes
        df_clean = DataCleaner._check_solar_outliers(df_clean)

        # Conversion des unités
        df_clean = DataCleaner._convert_solar_units(df_clean)

        return df_clean

    @staticmethod
    def clean_wind_data(df: pd.DataFrame) -> pd.DataFrame:
        """Nettoie les données éoliennes."""
        if df.empty:
            return df

        df_clean = df.copy()

        # Renommage
        if "time" in df_clean.columns:
            df_clean = df_clean.rename(columns={"time": "date"})

        # Conversion datetime
        if "date" in df_clean.columns:
            df_clean["date"] = pd.to_datetime(df_clean["date"]).dt.date

        # Suppression des doublons
        df_clean = DataCleaner._remove_duplicates(df_clean, "date")

        # Gestion valeurs manquantes
        df_clean = DataCleaner._handle_missing_values(df_clean)

        return df_clean

    @staticmethod
    def clean_hydro_data(df: pd.DataFrame) -> pd.DataFrame:
        """Nettoie les données hydrauliques."""
        if df.empty:
            return df

        df_clean = df.copy()

        # Renommage des colonnes
        column_mapping = {
            "date_obs_elab": "date",
            "result_obs_elab": "debit_l_s",
        }

        for old_name, new_name in column_mapping.items():
            if old_name in df_clean.columns:
                df_clean = df_clean.rename(columns={old_name: new_name})

        # Conversion des types
        if "date" in df_clean.columns:
            df_clean["date"] = pd.to_datetime(df_clean["date"]).dt.date

        if "debit_l_s" in df_clean.columns:
            df_clean["debit_l_s"] = pd.to_numeric(
                df_clean["debit_l_s"], errors="coerce"
            )

        # Suppression des doublons
        df_clean = DataCleaner._remove_duplicates(df_clean, "date")

        # Gestion valeurs manquantes et négatives
        if "debit_l_s" in df_clean.columns:
            df_clean = df_clean[df_clean["debit_l_s"] >= 0]
            df_clean = DataCleaner._handle_missing_values(df_clean, ["debit_l_s"])

        return df_clean

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
        # Limites physiques
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

        # Cohérence entre durée d'ensoleillement et durée du jour
        if all(col in df.columns for col in ["sunshine_duration", "daylight_duration"]):
            invalid = df["sunshine_duration"] > df["daylight_duration"]
            if invalid.any():
                logging.warning("Durée d'ensoleillement > durée du jour détectée")

        return df

    @staticmethod
    def _convert_solar_units(df: pd.DataFrame) -> pd.DataFrame:
        """Convertit les unités des données solaires."""
        # Conversion secondes -> heures
        if "sunshine_duration" in df.columns:
            df["sunshine_duration_h"] = df["sunshine_duration"] / 3600
        if "daylight_duration" in df.columns:
            df["daylight_duration_h"] = df["daylight_duration"] / 3600

        # Conversion MJ/m² -> kWh/m²
        if "shortwave_radiation_sum" in df.columns:
            df["shortwave_radiation_sum_kwh_m2"] = (
                df["shortwave_radiation_sum"] * 0.27778
            )

        return df
