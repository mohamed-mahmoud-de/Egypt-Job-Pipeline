# Egypt Jobs Pipeline

> A data pipeline that scrapes Egyptian tech job listings from [Wuzzuf.net](https://wuzzuf.net), stores them in Postgres, and prepares them for analysis. Built as a portfolio project to learn data engineering fundamentals.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![Postgres](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Status](https://img.shields.io/badge/Status-V1%20MVP-green)

---

## Overview

This pipeline automates the collection of Python job listings in Egypt and the MENA region. It pulls structured job data straight from Wuzzuf's search results, cleans it, and loads it into a local Postgres database — ready for analysis or downstream tools.

## Features

- Paginated scraping (handles all pages dynamically, not just the first one)
- Defensive parsing — won't crash on missing fields
- Deduplicates on job URL
- Postgres runs in Docker — no local install needed
- Credentials stored in `.env`, never committed

## Tech Stack

| Layer | Tool |
|-------|------|
| Language | Python 3.13 |
| HTTP | requests |
| Parsing | BeautifulSoup4 |
| Database | PostgreSQL 16 |
| DB Driver | psycopg2 |
| Infra | Docker Compose |
| Config | python-dotenv |

## Project Structure

    egypt-jobs-pipeline/
    ├── src/
    │   ├── extract/      # Scraper (Wuzzuf)
    │   ├── transform/    # Cleaning logic (coming in V1.5)
    │   └── load/         # Postgres loader
    ├── sql/              # Table schemas
    ├── tests/            # Tests (TODO)
    ├── config/           # Settings
    ├── data/             # Raw dumps for debugging
    ├── logs/             # Pipeline run logs
    ├── docker-compose.yml
    ├── requirements.txt
    └── main.py           # Pipeline entry point

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/mohamed-mahmoud-de/Egypt-Job-Pipeline.git
cd Egypt-Job-Pipeline
```

### 2. Create a `.env` file in the project root

```
POSTGRES_USER=pipeline_user
POSTGRES_PASSWORD=pipeline_pass123
POSTGRES_DB=egypt_jobs
```

### 3. Start Postgres

```bash
docker-compose up -d
```
### 4. Create the schema

```bash
type sql\create_tables.sql | docker exec -i egyptjobpipeline-postgres-1 psql -U pipeline_user -d egypt_jobs
```

### 5. Set up Python

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 6. Run the pipeline

```bash
python main.py
```

You should see `Inserted N jobs.` and the data will be available in your Postgres `jobs` table.

## Sample Output

After running, you can query the database directly:

```sql
SELECT company, COUNT(*) AS openings
FROM jobs
GROUP BY company
ORDER BY openings DESC
LIMIT 5;
```
## Roadmap

- **V1 (current)** — Naive Python script, single source, runs on demand
- **V2** — Airflow DAG with scheduled runs, retries, alerting, and a Metabase dashboard
- **V3** — Streaming pipeline with Kafka + Spark for real-time job ingestion

## Author

**Mohamed Mahmoud** — Data Engineering student & DEPI intern  
Building projects to learn data engineering hands-on.