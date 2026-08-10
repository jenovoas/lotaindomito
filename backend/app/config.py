"""Configuración de la aplicación — variables de entorno.

Uso:
    Pydantic Settings lee DATABASE_URL, CORS_ORIGINS, LOTASERVER_URL del entorno
    o del archivo .env en la raíz del backend.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings de la aplicación — validados en startup."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Base de datos
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/lotaindomito"
    )

    # CORS — orígenes permitidos separados por coma
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # Motor Rust (lota-server)
    LOTASERVER_URL: str = "http://localhost:8001"

    @property
    def cors_list(self) -> list[str]:
        """Convierte CORS_ORIGINS (comma-separated) a lista."""
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


# Instancia global — importada por db.py, main.py, routers
settings = Settings()
