# Quantitative Trade Performance Auditor & Analytics Pipeline

An automated, self-service end-to-end data processing framework engineered to ingest, clean, and analyze high-frequency multi-source algorithmic execution files. This system isolates transactional execution anomalies (slippage metrics and latency deviations) and translates them into an optimized database environment for cross-functional business stakeholders.

## Technical Architecture & Core Capabilities

* **Exploratory Data Analysis & Transformation:** Parses variable transaction streams, handles missing metadata constraints, flags mathematical data errors, and engineers customized performance fields (`slippage_points`).
* **SQL & Python Execution Pipeline:** Features an automated extraction layer loading unstructured logs directly into an indexed SQLite storage structure optimizing retrieval paths.
* **Self-Service Business Interface:** Implements an intuitive parameterized CLI query framework, shielding business operators from manual database querying while delivering split-second metric extraction.

---

## Project Structure

```text
trade-performance-auditor/
├── data/                       # Local file arrays and storage database engine
├── src/
│   ├── pipeline.py             # Python & SQL ETL execution pipeline module
│   └── app.py                  # Self-service parameter configuration interface
├── .gitignore                  # Tracking exclusion matrices
└── README.md                   # Operational portfolio documentation