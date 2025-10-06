import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# load_dotenv()

# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    supabase_url: str
    supabase_key: str

    montpellier_latitude: float = 43.6109
    montpellier_longitude: float = 3.8763
    hubeau_station: str = "Y321002101"


settings = Settings()
