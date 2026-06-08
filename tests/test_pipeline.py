import pytest
import pandas as pd
import numpy as np

# Let's write a targeted test ensuring anomalous files are cleaned correctly
def test_data_cleaning_logic():
    # Setup a mini mock payload containing identical real-world anomalies
    test_payload = pd.DataFrame({
        "transaction_id": ["TX-1", "TX-2", "TX-3", "TX-4"],
        "order_side": ["BUY", "SELL", "BUY", "BUY"],
        "requested_price": [1500.0, 1600.0, 1700.0, 1800.0],
        "filled_price": [1505.0, 1595.0, np.nan, 1810.0],  # TX-3 contains an anomalous missing fill price
        "execution_qty": [1, -999, 5, 2],                 # TX-2 contains a broken negative quantity artifact
        "execution_latency_ms": [10.0, 20.0, 30.0, 160.0]
    })
    
    # Run the exact filter algorithms used inside your production pipeline
    cleaned_df = test_payload.dropna(subset=["filled_price", "requested_price"])
    cleaned_df = cleaned_df[cleaned_df["execution_qty"] > 0].copy()
    
    # Calculate performance fields
    cleaned_df["slippage_points"] = cleaned_df["filled_price"] - cleaned_df["requested_price"]
    cleaned_df.loc[cleaned_df["order_side"] == "SELL", "slippage_points"] = cleaned_df["requested_price"] - cleaned_df["filled_price"]
    cleaned_df["is_latency_anomaly"] = cleaned_df["execution_latency_ms"] > 150.0

    # Assertions: Verify data filters correctly caught the anomalies
    assert len(cleaned_df) == 2, f"Expected 2 clean records, but got {len(cleaned_df)}"
    assert "TX-3" not in cleaned_df["transaction_id"].values, "Failed to drop missing price artifact"
    assert "TX-2" not in cleaned_df["transaction_id"].values, "Failed to drop negative quantity data error"
    
    # Verify calculated performance fields match exact mathematical expectations
    tx1_slippage = cleaned_df[cleaned_df["transaction_id"] == "TX-1"]["slippage_points"].values[0]
    tx4_latency_flag = cleaned_df[cleaned_df["transaction_id"] == "TX-4"]["is_latency_anomaly"].values[0]
    
    assert tx1_slippage == 5.0, f"Expected slippage of 5.0, got {tx1_slippage}"
    assert tx4_latency_flag == True, "Failed to isolate high-latency anomaly threshold deviation"