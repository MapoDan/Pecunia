from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://pecunia:change-me@localhost:5432/pecunia"
    app_origin: str = "http://localhost:5173"
    session_secret: str = "change-me"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
