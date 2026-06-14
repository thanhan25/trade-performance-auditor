-- Defensive relational schema initializing your analytics ledger data warehouse
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS fact_executed_trades (
    transaction_id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    asset_ticker TEXT NOT NULL,
    order_side TEXT NOT NULL,
    execution_qty INTEGER NOT NULL CHECK(execution_qty > 0),
    requested_price REAL NOT NULL,
    filled_price REAL NOT NULL,
    execution_latency_ms REAL NOT NULL,
    slippage_points REAL NOT NULL,
    is_latency_anomaly INTEGER NOT NULL CHECK(is_latency_anomaly IN (0, 1))
);

-- Optimize high-frequency reporting search performance arrays
CREATE INDEX IF NOT EXISTS idx_ticker ON fact_executed_trades (asset_ticker);