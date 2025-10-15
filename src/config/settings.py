from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Supabase
    supabase_url: str
    supabase_key: str

    # Localisation
    montpellier_latitude: float = 43.6109
    montpellier_longitude: float = 3.8763
    hubeau_station: str = "Y321002101"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Chemins
    models_path: str = "models/saved"
    data_raw_path: str = "data/raw"

    # Configuration des producteurs
    solar_nominal_power: float = 150.0  # kWc
    wind_nominal_power: float = 100.0  # kW
    hydro_nominal_power: float = 200.0  # kW


# Instanciation unique
settings = Settings()