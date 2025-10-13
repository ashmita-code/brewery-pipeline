# 🍺 Brewery Data Pipeline — End-to-End Modern ETL with DuckDB

> A complete data engineering project built from scratch — from API ingestion to warehouse modeling, data quality audits, and lineage visualization.

---

## 🚀 Overview

This project ingests brewery data from the [Open Brewery DB API](https://www.openbrewerydb.org/), processes it through an ETL pipeline, and models it inside **DuckDB** using the **Medallion Architecture (Bronze → Silver → Gold)**.  
It concludes with **Data Quality (DQ) audits**, **factless modeling**, and **ETL lineage charts** — all automated inside Colab.

> ⚙️ The notebook runs on a **sample subset (~51 rows)** for speed and reproducibility in Colab,  
> but the pipeline design, transformations, and DQ logic are **fully scalable to 9K+ brewery records**.

---

## 🧱 Architecture

Raw API Ingestion (Bronze)  
↓  
Python Cleaning & Transformation (Silver)  
↓  
DuckDB Warehouse Modeling (Gold)  
↓  
Star / Snowflake / Factless Schemas  
↓  
Data Quality Audits & Lineage Visualization  

---

## 🧩 Warehouse Modeling

### Schemas

| Layer | Schema Name | Description |
|--------|--------------|--------------|
| 🥉 **Bronze** | `stg_brewery` | Raw brewery data directly from the API |
| 🥈 **Silver** | `star.stg_brewery` | Cleaned and standardized brewery records |
| 🥇 **Gold** | `star`, `geo_snowflake`, `tags`, `factless`, `mart` | Analytical warehouse schemas (ready for BI) |

---

### Key Tables

| Table | Type | Purpose |
|--------|------|----------|
| `dim_country` | Dimension | Country lookup |
| `dim_brewery_type` | Dimension | Brewery type classification |
| `dim_brewery` | Dimension | Brewery master entity |
| `fact_brewery_counts` | Fact | Brewery counts by date/type/country |
| `fact_brewery_open` | Factless | Tracks when breweries are “open” by date |
| `brewery_detail` | Detail | Latest brewery state for analytical join enrichment |

---

## 🧮 Data Quality (DQ) Audits

Automated in Python + DuckDB:

- Row count reconciliation (staging → fact/dim)
- Null / empty value validation
- Orphan key detection across relationships
- DQ summary exports (`.csv`, `.xlsx`)
- Visual DQ bar charts and lineage tracking

<img width="559" height="317" alt="dq" src="https://github.com/user-attachments/assets/716ede96-15dc-4d22-8584-6ae1075864e1" />

---

## 📊 Sample Visualization

ETL Lineage Sankey and Row Counts Summary  

<img width="1453" height="539" alt="viz" src="https://github.com/user-attachments/assets/9ffaac03-e34c-441f-ac0e-e32a479155c8" />

---

## ⚙️ Pipeline Scalability

This project runs on a **sample subset (51 rows)** for reproducibility,  
but the architecture, joins, and lineage design are **production-ready** and scale to the full **8.9K+ record Open Brewery dataset**.  

Every schema (Bronze → Silver → Gold) maintains referential integrity and DQ audits at scale.

---

## 🧠 Tech Stack

| Layer | Tools |
|--------|--------|
| **Data Ingestion** | Python, Requests, Pandas |
| **Processing & Modeling** | DuckDB, SQL (CTAS, Hash Joins, Window Functions) |
| **Data Architecture** | Medallion (Bronze → Silver → Gold), Star, Snowflake, Factless |
| **Visualization** | Matplotlib, Plotly |
| **Audit & DQ** | DuckDB + Python (Pandas, Excel Export, DQ Tests) |

---

## ▶️ Run Locally or in Colab

```bash
# 1️⃣ Clone the repo
git clone https://github.com/ashmita-code/brewery-pipeline.git
cd brewery-pipeline

# 2️⃣ Install dependencies
pip install -r duckdb-etl/requirements.txt

# 3️⃣ Run the notebook or scripts
# (see duckdb-etl/Brewery_Insight.ipynb)
