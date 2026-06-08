import sqlite3
import pandas as pd
import sys

DB_PATH = "data/database.db"

def query_trade_metrics(ticker=None):
    conn = sqlite3.connect(DB_PATH)
    if ticker:
        query = """
            SELECT 
                asset_ticker,
                COUNT(*) as total_trades,
                ROUND(AVG(slippage_points), 4) as avg_slippage,
                ROUND(AVG(execution_latency_ms), 2) as avg_latency_ms,
                SUM(is_latency_anomaly) as total_latency_anomalies
            FROM fact_executed_trades
            WHERE asset_ticker = :ticker
            GROUP BY asset_ticker;
        """
        df = pd.read_sql_query(query, conn, params={"ticker": ticker})
    else:
        query = """
            SELECT 
                asset_ticker,
                COUNT(*) as total_trades,
                ROUND(AVG(slippage_points), 4) as avg_slippage,
                ROUND(AVG(execution_latency_ms), 2) as avg_latency_ms
            FROM fact_executed_trades
            GROUP BY asset_ticker;
        """
        df = pd.read_sql_query(query, conn)
    conn.close()
    
    if df.empty:
        print(f"No execution logs found for asset target parameter: {ticker}")
    else:
        print("\n=== Automated Self-Service Execution Audit Update ===")
        print(df.to_string(index=False))
        print("=====================================================\n")

if __name__ == "__main__":
    target_ticker = sys.argv[1].upper() if len(sys.argv) > 1 else None
    query_trade_metrics(target_ticker)
