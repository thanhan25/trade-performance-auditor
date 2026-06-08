import pandas as pd
import sqlite3
import os

DB_PATH = "data/database.db"
RAW_DATA_PATH = "data/raw_execution_logs.csv"

def run_etl_pipeline():
    print("Starting ETL pipeline execution...")
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"Missing raw data asset at {RAW_DATA_PATH}")
    df = pd.read_csv(RAW_DATA_PATH)
    
    initial_rows = len(df)
    df = df.dropna(subset=["filled_price", "requested_price"])
    df = df[df["execution_qty"] > 0]
    
    df["slippage_points"] = df["filled_price"] - df["requested_price"]
    df.loc[df["order_side"] == "SELL", "slippage_points"] = df["requested_price"] - df["filled_price"]
    df["is_latency_anomaly"] = df["execution_latency_ms"] > 150.0
    
    cleaned_rows = len(df)
    print(f"Data transformations complete. Filtered out {initial_rows - cleaned_rows} anomalous records.")
    
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("fact_executed_trades", conn, if_exists="replace", index=False)
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX idx_ticker ON fact_executed_trades (asset_ticker);")
    conn.commit()
    conn.close()
    print(f"Loaded records cleanly into automated data warehouse storage layer: {DB_PATH}")

if __name__ == "__main__":
    run_etl_pipeline()
