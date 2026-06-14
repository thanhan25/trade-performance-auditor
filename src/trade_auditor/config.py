import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")


class AuditorSettings:
    """Central configuration manager validating environment variables."""

    def __init__(self):
        self.ENVIRONMENT: str = os.getenv("AUDITOR_ENV", "development").lower()
        self.DB_PATH: Path = BASE_DIR / os.getenv("DATABASE_PATH", "data/database.db")
        self.RAW_LOGS_PATH: Path = BASE_DIR / os.getenv(
            "RAW_LOGS_PATH", "data/raw_execution_logs.csv"
        )
        self.OUTPUT_CHART_PATH: Path = BASE_DIR / os.getenv(
            "OUTPUT_CHART_PATH", "data/latency_slippage_audit.png"
        )

        try:
            self.LATENCY_THRESHOLD_MS: float = float(
                os.getenv("LATENCY_THRESHOLD_MS", "150.0")
            )
        except ValueError as err:
            from trade_auditor.exceptions import DataWarehouseIngestionError

            raise DataWarehouseIngestionError(f"Configuration validation failed: {err}")

    def validate_environment(self) -> None:
        """Enforces that operational data storage folders exist."""
        self.DB_PATH.parent.mkdir(parents=True, exist_ok=True)


settings = AuditorSettings()
