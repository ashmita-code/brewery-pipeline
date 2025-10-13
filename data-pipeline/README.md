# 🍺 Brewery Data Pipeline — End-to-End Modern ETL with DuckDB

> A complete data engineering project built from scratch — from API ingestion to warehouse modeling, data quality audits, and FAANG-style lineage visualization.

---

## 🚀 Overview

This project ingests brewery data from the [Open Brewery DB API](https://www.openbrewerydb.org/), processes it through an ETL pipeline, and models it inside **DuckDB** using **Medallion architecture** (Silver → Gold).  
It concludes with **Data Quality (DQ) audits**, **factless modeling**, and **ETL lineage charts** — all automated inside Colab.

---

## 🧱 Architecture

Open Brewery API
↓
Python ETL (data-pipeline/)
↓
Silver Layer (cleaned)
↓
Gold Layer (DuckDB)
↓
Star / Snowflake Schemas
↓
Data Quality & Visualization


---

## 🧩 Warehouse Modeling

### Schemas
| Layer | Schema Name | Description |
|--------|--------------|--------------|
| 🥈 **Silver** | `star.stg_brewery` | Cleaned brewery records |
| 🥇 **Gold** | `star`, `geo_snowflake`, `tags`, `factless`, `mart` | Analytical warehouse schemas |

### Key Tables
| Table | Type | Purpose |
|--------|------|----------|
| `dim_country` | Dimension | Country lookup |
| `dim_brewery_type` | Dimension | Brewery type classification |
| `dim_brewery` | Dimension | Brewery master entity |
| `fact_brewery_counts` | Fact | Brewery counts by date/type/country |
| `fact_brewery_open` | Factless | Track brewery “open” days |
| `brewery_detail` | Detail | Latest state per brewery |

---

## 🧮 Data Quality (DQ) Audits

Automated via Python + DuckDB:
- Row count reconciliation (staging → fact/dim)
- Null/empty value checks
- Orphan key validation across relationships
- Exported DQ summary (`.csv`, `.xlsx`)
- Visual DQ charts (bar plots)

<p align="center">
  <img src="duckdb-etl/images/table_counts_bar.png" width="500"><br>
  <em>Row-count reconciliation across staging and modeled layers</em>
</p>

---

## 📊 Sample Visualization

<p align="center">
  <img src="duckdb-etl/images/etl_sankey.png" width="700"><br>
  <em>ETL lineage showing data flow from Silver → Gold → Factless layers</em>
</p>

---

## 🧠 Tech Stack

| Layer | Tools |
|--------|--------|
| **Data Ingestion** | Python, Requests, Pandas |
| **Processing** | DuckDB, SQL (CTAS, Hash Joins, Window Functions) |
| **Modeling** | Star, Snowflake, Factless, Bridge Tables |
| **Visualization** | Matplotlib, Plotly |
| **Audit & DQ** | DuckDB + Python (pandas & Excel export) |

---

## ▶️ Run Locally (Colab or Desktop)

```bash
# 1️⃣ Clone the repo
git clone https://github.com/ashmita-code/brewery-pipeline.git
cd brewery-pipeline

# 2️⃣ Install dependencies
pip install -r duckdb-etl/requirements.txt

# 3️⃣ Run the Colab notebook or scripts
# (see duckdb-etl/brewery_pipeline.ipynb)
