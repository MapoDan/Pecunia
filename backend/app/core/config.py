from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Pecunia"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: str = Field(default="postgresql+psycopg://pecunia:pecunia@postgres:5432/pecunia")
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])

    model_config = SettingsConfigDict(env_file=".env", env_prefix="PECUNIA_", extra="ignore")


settings = Settings()
