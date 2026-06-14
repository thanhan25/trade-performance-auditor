import numpy as np
import pandas as pd
import pytest

from trade_auditor.config import AuditorSettings, settings
from trade_auditor.exceptions import DataWarehouseIngestionError
from trade_auditor.pipeline import run_etl_pipeline


def test_data_cleaning_logic(tmp_path, monkeypatch):
    """Verifies data ingestion filtering rules securely remove pipeline anomalies."""
    test_csv = tmp_path / "raw_logs_mock.csv"
    test_db = tmp_path / "test_warehouse.db"

    test_payload = pd.DataFrame(
        {
            "transaction_id": ["TX-1", "TX-2", "TX-3", "TX-4"],
            "timestamp": [
                "2026-06-01 09:30:01",
                "2026-06-01 09:30:02",
                "2026-06-01 09:30:03",
                "2026-06-01 09:30:04",
            ],
            "asset_ticker": ["NQ=F", "ES=F", "GC=F", "CL=F"],
            "order_side": ["BUY", "SELL", "BUY", "BUY"],
            "requested_price": [1500.0, 1600.0, 1700.0, 1800.0],
            "filled_price": [1505.0, 1595.0, np.nan, 1810.0],
            "execution_qty": [1, -999, 5, 2],
            "execution_latency_ms": [10.0, 20.0, 30.0, 160.0],
        }
    )
    test_payload.to_csv(test_csv, index=False)

    # Secure isolated configuration injections
    monkeypatch.setattr(settings, "RAW_LOGS_PATH", test_csv)
    monkeypatch.setattr(settings, "DB_PATH", test_db)
    monkeypatch.setattr("trade_auditor.database.db_manager.db_path", str(test_db))

    run_etl_pipeline()

    from trade_auditor.database import db_manager

    with db_manager.execution_session() as conn:
        cleaned_df = pd.read_sql_query("SELECT * FROM fact_executed_trades", conn)

    assert len(cleaned_df) == 2
    assert "TX-3" not in cleaned_df["transaction_id"].values
    assert "TX-2" not in cleaned_df["transaction_id"].values

    tx1_row = cleaned_df[cleaned_df["transaction_id"] == "TX-1"]
    assert tx1_row["slippage_points"].values[0] == 5.0
    assert tx1_row["is_latency_anomaly"].values[0] == 0


def test_configuration_validation_failure(monkeypatch):
    """Enforces error conditions if critical numerical parameters are unparsable."""
    monkeypatch.setenv("LATENCY_THRESHOLD_MS", "invalid_corrupted_string")
    with pytest.raises(DataWarehouseIngestionError):
        AuditorSettings()
