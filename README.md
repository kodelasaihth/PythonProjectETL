# 📦 ETL Snowflake Project

## 🚀 Overview

This project implements a **modern data pipeline** using:

* **Snowpipe** for real-time ingestion
* **Prefect** for orchestration
* **dbt** for transformations
* **Snowflake** as the data warehouse

---

## 🏗️ Architecture

```
Raw Data (Parquet files)
        ↓
Snowpipe (auto ingestion)
        ↓
Snowflake RAW tables
        ↓
Prefect Flow (orchestration)
        ↓
dbt (staging → marts)
        ↓
Analytics-ready tables
```

---

## 📁 Project Structure

```
etl-snowflake-project/
│
├── flows/
│   └── main_flow.py
│
├── tasks/
│   ├── snowflake_tasks.py
│   ├── validation.py
│   └── alerts.py
│
├── dbt/
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   └── dbt_project.yml
│
├── sql/
│   ├── raw_tables.sql
│   ├── streams.sql
│   └── tasks.sql
│
├── config/
│   └── config.yaml
│
├── utils/
│   └── connection.py
│
├── prefect.yaml
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```
git clone <repo-url>
cd etl-snowflake-project
```

---

### 2. Create Virtual Environment

```
python -m venv .venv
.venv\Scripts\activate   # Windows
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

### 4. Setup Environment Variables

Create `.env` file:

```
# Prefect
PREFECT_API_URL=http://127.0.0.1:4200/api

# PostgreSQL (Prefect backend)
PREFECT_API_DATABASE_CONNECTION_URL=postgresql+asyncpg://user:password@localhost:5432/prefect

# Snowflake
SNOWFLAKE_ACCOUNT=xxx
SNOWFLAKE_USER=xxx
SNOWFLAKE_PASSWORD=xxx
SNOWFLAKE_WH=COMPUTE_WH
SNOWFLAKE_DB=ANALYTICS_DB
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_ROLE=SYSADMIN
```

---

### 5. Setup dbt

```
cd dbt
dbt deps
dbt debug
```

---

## ▶️ Running the Pipeline

### 🔹 Option 1: Simple (Development)

```
python flows/main_flow.py
```

---

### 🔹 Option 2: Prefect Orchestration (Production)

#### Start Prefect Server

```
prefect server start
```

---

#### Start Worker

```
prefect worker start --pool default
```

---

#### Deploy Flow

```
prefect deploy
```

---

#### Run Deployment

```
prefect deployment run "snowflake-etl-pipeline/etl-job"
```

---

## 🔄 Pipeline Flow

1. Snowpipe loads data into **RAW tables**
2. Prefect detects new data
3. dbt runs:

   * staging models (cleaning)
   * marts models (business logic)
4. Data becomes analytics-ready

---

## 🧪 dbt Layer

### Staging

* Clean raw data
* Cast data types
* Handle nulls

### Marts

* Aggregations
* KPIs
* Business-ready tables

---

## ⚠️ Common Issues

### SQLite Lock Error

* Happens in local Prefect setup
* Use PostgreSQL backend
* Avoid multiple workers

---

### Deployment Not Found

Use correct format:

```
prefect deployment run "<flow_name>/<deployment_name>"
```

---

### dbt Adapter Missing

```
pip install dbt-snowflake
```

---

## 🔐 Security Best Practices

* Do NOT commit `.env`
* Use environment variables
* Use Snowflake roles and least privilege

---

## 🚀 Future Improvements

* CI/CD integration
* Alerting (Slack / Email)
* Data quality checks
* Event-driven triggers

---

## 🧠 Interview Summary

Built an end-to-end ETL pipeline using Snowflake, Snowpipe, Prefect, and dbt. Implemented real-time ingestion, orchestrated transformations, and handled concurrency issues by migrating from SQLite to PostgreSQL.

---
