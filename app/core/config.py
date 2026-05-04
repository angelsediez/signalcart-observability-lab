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
        self.simulation_latency_seconds = self._as_float(
            os.getenv("SIMULATION_LATENCY_SECONDS", "1.25")
        )
        self.simulation_error_status_code = self._as_int(
            os.getenv("SIMULATION_ERROR_STATUS_CODE", "500")
        )

    @staticmethod
    def _as_bool(value: str) -> bool:
        return value.strip().lower() in {"1", "true", "yes", "on"}

    @staticmethod
    def _as_float(value: str) -> float:
        try:
            return float(value)
        except ValueError:
            return 1.25

    @staticmethod
    def _as_int(value: str) -> int:
        try:
            return int(value)
        except ValueError:
            return 500


@lru_cache
def get_settings() -> Settings:
    return Settings()
