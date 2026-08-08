from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Pecunia"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: str = Field(default="postgresql+psycopg://pecunia:pecunia@postgres:5432/pecunia")
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])
    google_client_id: str = ""
    session_secret: str = "change-me-only-for-development"
    session_cookie_name: str = "pecunia_session"
    session_ttl_minutes: int = 60 * 24 * 14
    cookie_secure: bool = False
    cookie_samesite: str = "lax"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="PECUNIA_", extra="ignore")


settings = Settings()
