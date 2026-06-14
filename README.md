
# Quantitative Trade Performance Auditor & Analytics Pipeline 📊

[![Continuous Integration Quality Gate](https://github.com/thanhan25/trade-performance-auditor/actions/workflows/ci.yml/badge.svg)](https://github.com/thanhan25/trade-performance-auditor/actions)
![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)
![Test Coverage](https://img.shields.io/badge/coverage-90.91%25-green.svg)

An automated, enterprise-grade data processing framework engineered to ingest, clean, and audit high-frequency multi-source algorithmic order execution files. This architecture isolates transactional execution anomalies (slippage matrices and latency deviations), handles variable missing metadata constraints, structures optimized database tables, and provides analytical reporting distributions.

## 🏗️ Architecture Design & Quality Standards

- **PEP 517 Package Structures:** Built using modular package distribution architectures (`pyproject.toml` utilizing `setuptools` find filters) to decouple development dependency modules completely from operational runtime contexts.
- **Context-Managed Database Sessions:** Implements zero-dangling connection context layers featuring automatic transaction rollbacks to protect relational schemas under unexpected data warehouse disruptions.
- **Decoupled Error Topologies:** Uses isolated custom exception hierarchies (`DataWarehouseIngestionError`, `QueryExecutionError`) to enforce strict internal boundaries instead of loose native string evaluations.
- **Robust Continuous Integration (CI):** Backed by active GitHub Actions orchestrations executing formatting validation routines (`black`, `isort`) and regression testing loops across parallel Python environments automatically on every push.

## 📦 Core Package Map

```text
trade-performance-auditor/
│
├── .github/workflows/
│   └── ci.yml               # Multi-version continuous integration workflow runner
│
├── sql/
│   └── schema.sql           # Defensive data warehouse schema layout initializations
│
├── src/trade_auditor/
│   ├── __init__.py          # Package identification namespace hook
│   ├── app.py               # Parameterized user reporting CLI module
│   ├── config.py            # Central environment hydration and validation vault
│   ├── database.py          # Relational storage context-session orchestrator
│   ├── exceptions.py        # Project specific standalone domain error types
│   ├── generate_data.py     # Sandbox mock dataset parsing pipeline
│   ├── pipeline.py          # High-frequency processing ETL module
│   └── plots.py             # Visual distribution charting utility
│
├── tests/
│   └── test_pipeline.py     # Sandbox path tracking logic verification tests
│
└── pyproject.toml           # Unified metadata manifest and tool configuration matrix
```

## 🚀 Installation & Environment Setup

Isolate your system environment variables and install the distribution package in editable development mode:

```bash
# Clone the open-source tracking repository assets
git clone [https://github.com/thanhan25/trade-performance-auditor.git](https://github.com/thanhan25/trade-performance-auditor.git)
cd trade-performance-auditor

# Sync package metadata structures along with quality tracking tools
python -m pip install -e .[dev]
```

## 🏃‍♂️ Running the Testing Framework Locally

Evaluate your local code layout modifications against our strict automated coverage targets:

```bash
python -m pytest
```

## 📊 Operating the Analytical Command Interface

Ingest fresh raw transaction metrics, compile analytical reports, and query specific instruments securely through runtime parameter inputs:

```bash
# 1. Trigger the transaction extraction and database cleaning loop
python src/trade_auditor/pipeline.py

# 2. Extract calculations and save high-resolution analytics charts
python src/trade_auditor/plots.py

# 3. Query all operational data lines across all tickers
python src/trade_auditor/app.py

# 4. Filter and query metrics targeted directly to Nasdaq Futures profiles
python src/trade_auditor/app.py NQ=F
```
