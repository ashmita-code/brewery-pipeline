# 🍺 Brewery Data Pipeline — End-to-End Modern ETL with DuckDB

> A complete data engineering project built from scratch — from API ingestion to warehouse modeling and data quality audits.

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

<img width="559" height="317" alt="image" src="https://github.com/user-attachments/assets/716ede96-15dc-4d22-8584-6ae1075864e1" />

---

## 📊 Sample Visualization

<img width="1453" height="539" alt="image" src="https://github.com/user-attachments/assets/9ffaac03-e34c-441f-ac0e-e32a479155c8" />


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
---

## ⚙️ Pipeline Scalability

This project runs on a **sample (51 rows)** for clarity and speed in Colab,  
but the ETL logic, schema design, and DQ framework are **fully scalable**. 
All joins, referential integrity, and lineage graphs are built to handle production-size data.

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

---




