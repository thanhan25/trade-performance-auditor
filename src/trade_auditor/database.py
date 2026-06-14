import logging
import sqlite3
from contextlib import contextmanager
from typing import Generator

from trade_auditor.config import settings
from trade_auditor.exceptions import DataWarehouseIngestionError

logger = logging.getLogger("trade_auditor.database")


class DatabaseManager:
    """Provides secure database session boundaries with auto-rollback hooks."""

    def __init__(self, db_path: str):
        self.db_path = db_path

    @contextmanager
    def execution_session(self) -> Generator[sqlite3.Connection, None, None]:
        """Context manager providing an active SQLite transactional connection."""
        settings.validate_environment()
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("PRAGMA foreign_keys = ON;")
            yield conn
            conn.commit()
        except sqlite3.Error as sql_err:
            if conn:
                conn.rollback()
            raise DataWarehouseIngestionError(
                f"Database tracking operation failed: {sql_err}"
            )
        finally:
            if conn:
                conn.close()


db_manager = DatabaseManager(db_path=str(settings.DB_PATH))
