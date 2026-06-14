import sys

import pandas as pd

from trade_auditor.database import db_manager
from trade_auditor.exceptions import QueryExecutionError


def query_trade_metrics(ticker: str = None) -> None:
    """Parameterized reporting utility serving split-second transaction audits to operators."""
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
        params = {"ticker": ticker}
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
        params = {}

    try:
        with db_manager.execution_session() as conn:
            df = pd.read_sql_query(query, conn, params=params)

        if df.empty:
            print(f"No execution logs found for asset target parameter: {ticker}")
        else:
            print("\n=== Automated Self-Service Execution Audit Update ===")
            print(df.to_string(index=False))
            print("=====================================================\n")
    except Exception as err:
        raise QueryExecutionError(f"Self-service reporting query failed: {err}")


if __name__ == "__main__":
    target_ticker = sys.argv[1].upper() if len(sys.argv) > 1 else None
    query_trade_metrics(target_ticker)
