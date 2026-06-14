import logging
import os

import pandas as pd

from trade_auditor.config import settings
from trade_auditor.database import db_manager
from trade_auditor.exceptions import DataWarehouseIngestionError

logger = logging.getLogger("trade_auditor.pipeline")


def run_etl_pipeline() -> None:
    """Executes the high-frequency log cleaning and aggregation cycle."""
    logger.info("Initializing trade audit ETL tracking execution track.")

    if not settings.RAW_LOGS_PATH.exists():
        raise FileNotFoundError(
            f"Missing raw execution log asset at: '{settings.RAW_LOGS_PATH}'"
        )

    df = pd.read_csv(settings.RAW_LOGS_PATH)
    initial_count = len(df)

    # Structural clean-up operations
    df = df.dropna(subset=["filled_price", "requested_price"])
    df = df[df["execution_qty"] > 0].copy()

    # Calculate quantitative slippage and performance indicators
    df["slippage_points"] = df["filled_price"] - df["requested_price"]
    df.loc[df["order_side"] == "SELL", "slippage_points"] = (
        df["requested_price"] - df["filled_price"]
    )
    df["is_latency_anomaly"] = (
        df["execution_latency_ms"] > settings.LATENCY_THRESHOLD_MS
    ).astype(int)

    logger.info(
        f"Transformations finished. Purged {initial_count - len(df)} volatile record entries."
    )

    try:
        with db_manager.execution_session() as conn:
            df.to_sql("fact_executed_trades", conn, if_exists="replace", index=False)
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_ticker ON fact_executed_trades (asset_ticker);"
            )
        logger.info(f"Loaded records cleanly into automated data warehouse layer.")
    except Exception as err:
        raise DataWarehouseIngestionError(
            f"Data warehouse tracking ingestion failed: {err}"
        )


if __name__ == "__main__":
    run_etl_pipeline()
