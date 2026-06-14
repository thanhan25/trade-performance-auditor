from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from trade_auditor.config import settings


def generate_mock_logs(filename=None, rows=1000):
    """Generates synthetic, messy trade execution files for test pipelines."""
    np.random.seed(42)
    start_time = datetime(2026, 6, 1, 9, 30, 0)
    target_file = filename if filename else settings.RAW_LOGS_PATH

    data = {
        "transaction_id": [f"TX-{10000 + i}" for i in range(rows)],
        "timestamp": [
            (start_time + timedelta(seconds=int(np.random.randint(0, 86400)))).strftime(
                "%Y-%m-%d %H:%M:%S.%f"
            )
            for i in range(rows)
        ],
        "asset_ticker": np.random.choice(["NQ=F", "ES=F", "GC=F", "CL=F"], rows),
        "order_side": np.random.choice(["BUY", "SELL"], rows),
        "execution_qty": np.random.choice([1, 2, 5, 10], rows, p=[0.5, 0.3, 0.1, 0.1]),
        "requested_price": np.random.uniform(1500, 18000, rows).round(2),
        "filled_price": np.random.uniform(1500, 18000, rows).round(2),
        "execution_latency_ms": np.random.exponential(scale=50, size=rows).round(1),
    }
    df = pd.DataFrame(data)
    df.loc[df.sample(frac=0.05).index, "filled_price"] = np.nan
    df.loc[df.sample(frac=0.03).index, "execution_qty"] = -999

    settings.validate_environment()
    df.to_csv(target_file, index=False)
    print(f"Generated {rows} messy logs at {target_file}")


if __name__ == "__main__":
    generate_mock_logs()
