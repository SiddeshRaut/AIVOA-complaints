from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Groq / LLM
    groq_api_key: str = ""
    groq_extraction_model: str = "llama-3.1-8b-instant"
    groq_chat_model: str = "llama-3.3-70b-versatile"

    # MySQL
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "aivoa_app"
    mysql_password: str = "devapp123"
    mysql_database: str = "aivoa_complaints"

    # Backend
    backend_cors_origins: str = "http://localhost:5173"
    max_upload_size_mb: int = 10
    upload_dir: str = "uploaded_docs"

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
        )

    @property
    def groq_configured(self) -> bool:
        return bool(self.groq_api_key.strip())

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.backend_cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
