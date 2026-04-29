from functools import lru_cache
import os


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self) -> None:
        self.app_name = os.getenv("APP_NAME", "SignalCart API")
        self.app_version = os.getenv("APP_VERSION", "0.1.0")
        self.app_env = os.getenv("APP_ENV", "local")
        self.database_url = os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://signalcart:signalcart-local-password@127.0.0.1:5432/signalcart",
        )
        self.simulation_mode = self._as_bool(os.getenv("SIMULATION_MODE", "false"))
        self.simulation_token = os.getenv("SIMULATION_TOKEN", "change-me-for-local-lab-only")

    @staticmethod
    def _as_bool(value: str) -> bool:
        return value.strip().lower() in {"1", "true", "yes", "on"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
