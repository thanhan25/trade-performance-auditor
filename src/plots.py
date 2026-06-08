import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

DB_PATH = "data/database.db"
OUTPUT_IMAGE_PATH = "data/latency_slippage_audit.png"

def generate_performance_charts():
    print("Extracting relational database metrics for visualization...")
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database missing at {DB_PATH}. Run pipeline first.")
        
    # Connect and extract metrics via SQL aggregation
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

    # Set up clean professional charting aesthetics
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Quantitative Trade Execution Performance Audit", fontsize=16, fontweight="bold")

    # Chart 1: Latency Distribution across Futures lines
    sns.barplot(x="asset_ticker", y="avg_latency", data=df, ax=axes[0], palette="coolwarm", hue="asset_ticker", legend=False)
    axes[0].set_title("Average Execution Latency (Lower is Better)")
    axes[0].set_ylabel("Latency (Milliseconds)")
    axes[0].set_xlabel("Asset Ticker")

    # Chart 2: Slippage Spreads across Futures lines
    sns.barplot(x="asset_ticker", y="avg_slippage", data=df, ax=axes[1], palette="viridis", hue="asset_ticker", legend=False)
    axes[1].set_title("Average Execution Slippage Over Requested Target")
    axes[1].set_ylabel("Slippage Points")
    axes[1].set_xlabel("Asset Ticker")

    plt.tight_layout()
    plt.savefig(OUTPUT_IMAGE_PATH, dpi=300)
    print(f"Success! High-resolution analytics chart saved cleanly at: {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    generate_performance_charts()