import logging
import os
import sqlite3

import pandas as pd

# Configure enterprise-grade multi-handler logging infrastructure
log_format = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        logging.FileHandler("data/pipeline.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("trade_pipeline")

DB_PATH = "data/database.db"
RAW_DATA_PATH = "data/raw_execution_logs.csv"


def run_etl_pipeline():
    logger.info("Starting automated ETL pipeline execution wrapper...")

    if not os.path.exists(RAW_DATA_PATH):
        logger.error(
            f"Critical execution failure: Missing raw data asset at {RAW_DATA_PATH}"
        )
        raise FileNotFoundError(f"Missing raw data asset at {RAW_DATA_PATH}")

    df = pd.read_csv(RAW_DATA_PATH)
    initial_rows = len(df)

    # Execute structural sanitization rules
    df = df.dropna(subset=["filled_price", "requested_price"])
    df = df[df["execution_qty"] > 0]

    # Feature engineering processing steps
    df["slippage_points"] = df["filled_price"] - df["requested_price"]
    df.loc[df["order_side"] == "SELL", "slippage_points"] = (
        df["requested_price"] - df["filled_price"]
    )
    df["is_latency_anomaly"] = df["execution_latency_ms"] > 150.0

    cleaned_rows = len(df)
    logger.info(
        f"Data transformations complete. Filtered out {initial_rows - cleaned_rows} anomalous records."
    )

    # Database transaction layer execution
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("fact_executed_trades", conn, if_exists="replace", index=False)

    cursor = conn.cursor()
    cursor.execute("CREATE INDEX idx_ticker ON fact_executed_trades (asset_ticker);")
    conn.commit()
    conn.close()

    logger.info(
        f"Loaded records cleanly into indexed warehouse storage layer: {DB_PATH}"
    )


if __name__ == "__main__":
    run_etl_pipeline()
