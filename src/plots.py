import logging
import os
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Bind to the central repository logging stream array
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("data/pipeline.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("trade_plots")

DB_PATH = "data/database.db"
OUTPUT_IMAGE_PATH = "assets/latency_slippage_audit.png"  # Updated to drop into assets directory directly


def generate_performance_charts():
    logger.info(
        "Extracting warehouse execution metrics for analytical visualization..."
    )

    if not os.path.exists(DB_PATH):
        logger.error(
            f"Visualization aborted: Database target missing at reference path {DB_PATH}"
        )
        raise FileNotFoundError(f"Database missing at {DB_PATH}. Run pipeline first.")

    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT 
            asset_ticker,
            AVG(slippage_points) as avg_slippage,
            AVG(execution_latency_ms) as avg_latency
        FROM fact_executed_trades
        GROUP BY asset_ticker;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(
        "Quantitative Trade Execution Performance Audit", fontsize=16, fontweight="bold"
    )

    sns.barplot(
        x="asset_ticker",
        y="avg_latency",
        data=df,
        ax=axes[0],
        palette="coolwarm",
        hue="asset_ticker",
        legend=False,
    )
    axes[0].set_title("Average Execution Latency (Lower is Better)")
    axes[0].set_ylabel("Latency (Milliseconds)")
    axes[0].set_xlabel("Asset Ticker")

    sns.barplot(
        x="asset_ticker",
        y="avg_slippage",
        data=df,
        ax=axes[1],
        palette="viridis",
        hue="asset_ticker",
        legend=False,
    )
    axes[1].set_title("Average Execution Slippage Over Requested Target")
    axes[1].set_ylabel("Slippage Points")
    axes[1].set_xlabel("Asset Ticker")

    plt.tight_layout()
    os.makedirs(os.path.dirname(OUTPUT_IMAGE_PATH), exist_ok=True)
    plt.savefig(OUTPUT_IMAGE_PATH, dpi=300)
    logger.info(
        f"Success! High-resolution analytics charts exported to active portfolio layer: {OUTPUT_IMAGE_PATH}"
    )


if __name__ == "__main__":
    generate_performance_charts()
