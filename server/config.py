from pydantic_settings import BaseSettings, SettingsConfigDict

THESS_LAT = 40.6401
THESS_LON = 22.9444


class Settings(BaseSettings):
    openaq_api_key: str
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
