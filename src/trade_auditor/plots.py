import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from trade_auditor.config import settings
from trade_auditor.database import db_manager
from trade_auditor.exceptions import QueryExecutionError


def generate_performance_charts() -> None:
    """Extracts analytical warehouse aggregations and compiles quality assurance distribution plots."""
    query = """
        SELECT 
            asset_ticker,
            AVG(slippage_points) as avg_slippage,
            AVG(execution_latency_ms) as avg_latency
        FROM fact_executed_trades
        GROUP BY asset_ticker;
    """
    try:
        with db_manager.execution_session() as conn:
            df = pd.read_sql_query(query, conn)

        if df.empty:
            raise QueryExecutionError(
                "Visualizer engine stalled: Data warehouse table targets are empty."
            )

        sns.set_theme(style="whitegrid")
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle(
            "Quantitative Trade Execution Performance Audit",
            fontsize=16,
            fontweight="bold",
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
        plt.savefig(settings.OUTPUT_CHART_PATH, dpi=300)
        print(
            f"Success! High-resolution analytics chart saved cleanly at: {settings.OUTPUT_CHART_PATH}"
        )
    except Exception as err:
        raise QueryExecutionError(f"Visualization plot compiling failed: {err}")


if __name__ == "__main__":
    generate_performance_charts()
