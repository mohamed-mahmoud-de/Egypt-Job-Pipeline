# Egypt Jobs Pipeline

> A data pipeline that scrapes Egyptian tech job listings from [Wuzzuf.net](https://wuzzuf.net), stores them in Postgres, and sends real-time alerts when new jobs appear. Built as a portfolio project to learn data engineering fundamentals.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![Postgres](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-2.10-017CEE?logo=apacheairflow&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)
![Status](https://img.shields.io/badge/Status-V3%20Complete-green)

---

## Overview

This pipeline automates the collection of tech job listings in Egypt from Wuzzuf. It has evolved through three versions:

- **V1** scraped jobs on demand and loaded them into Postgres.
- **V2** added Airflow orchestration, running every 2 hours with retries, Discord alerts, backfill, and a Streamlit dashboard.
- **V3** added a real-time alert layer — a polling loop that checks Wuzzuf every 3 minutes, deduplicates with Redis, filters by keywords, and sends Discord notifications within minutes of a new listing appearing.

## Architecture

### V2 — Batch Pipeline (Airflow)

```
┌─────────────┐    ┌───────────────────────────────────────────────┐
│  Airflow     │    │                  DAG (every 2h)               │
│  Scheduler   │───>│  Extract ──> Transform ──> Load ──> Notify   │
└─────────────┘    └──────┬────────────────────────┬────────┬──────┘
                          │                        │        │
                     Wuzzuf.net               PostgreSQL   Discord
                    (all pages)              (permanent)  (success/fail)
```

### V3 — Real-Time Alerts (Polling Loop)

```
                    ┌──────────────────────────────────┐
                    │         poller.py (while True)    │
                    │         runs every 3 minutes      │
                    └───────────────┬──────────────────┘
                                    │
                              scraper.py
                                    │
                               Wuzzuf.net
                              (page 1 only)
                                    │
                              ┌─────▼──────┐
                              │  For each   │
                              │  job found  │
                              └─────┬──────┘
                                    │
                         ┌──────────▼──────────┐
                         │  redis_client.py     │
                         │  is_seen(job_id)?    │
                         │  (Redis Set lookup)  │
                         └──────┬───────┬──────┘
                                │       │
                            Yes │       │ No
                           Skip │       ▼
                                │  filter.py
                                │  matches keywords?
                                │       │
                                │   Yes │ No
                                │    │  │ mark_seen + skip
                                │    ▼  │
                                │  notifier.py
                                │  send Discord alert
                                │    │
                                │    ▼
                                │  mark_seen(job_id)
                                │
                         ┌──────▼──────────────┐
                         │  On crash:           │
                         │  send_error_alert()  │
                         │  wait 3 min, retry   │
                         └─────────────────────┘
```

### How V2 and V3 Work Together

V2 is the **bulk historical pipeline** — scrapes all pages every 2 hours, stores everything in Postgres, powers the dashboard.

V3 is the **real-time alert layer** — watches page 1 every 3 minutes, notifies you about new jobs fast. V3 only scrapes page 1 by design — new listings always appear on page 1 first, so scraping deeper pages every 3 minutes would add load without catching jobs any faster. V2 handles the full historical scrape. Both run simultaneously.

## Features

### V1/V2 — Batch Pipeline
- Paginated scraping (handles all pages dynamically, not just the first one)
- Defensive parsing — won't crash on missing fields
- Deduplicates on job URL
- Postgres runs in Docker — no local install needed
- Credentials stored in `.env`, never committed
- Automated scheduling via Apache Airflow (every 2 hours)
- Retry logic with exponential backoff (3 retries)
- Discord webhook alerts on task failure and success
- Backfill support for re-running past date intervals
- Streamlit dashboard for browsing and filtering jobs

### V3 — Real-Time Alerts
- Polls Wuzzuf every 3 minutes for new listings
- Redis Set deduplication — fast in-memory lookup to skip already-seen jobs
- Configurable keyword filters (wanted/unwanted) via `config.json`
- Discord embed notifications for every new matching job
- Crash-proof polling loop — survives scraper, Redis, and network failures
- Discord error alerts when the poller itself breaks
- Redis persistence via Docker volume — seen jobs survive container restarts

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
| Orchestration | Apache Airflow 2.10 |
| Dashboard | Streamlit |
| Cache | Redis 7 |
| Alerting | Discord Webhooks |

## Project Structure

    egypt-jobs-pipeline/
    ├── dags/
    │   ├── egypt_job_dag.py   # Main ETL DAG
    │   └── hello_dag.py       # Test DAG
    ├── src/
    │   ├── extract/           # Scraper (Wuzzuf)
    │   ├── transform/         # Cleaning logic
    │   ├── load/              # Postgres loader
    │   └── utils/             # Discord alerts
    ├── v3/
    │   ├── poller.py          # Main polling loop (entry point)
    │   ├── scraper.py         # Wuzzuf scraper for V3
    │   ├── redis_client.py    # Redis Set deduplication
    │   ├── filter.py          # Keyword matching filter
    │   ├── notifier.py        # Discord job + error alerts
    │   └── config.json        # Wanted/unwanted keywords
    ├── docs/                  # Architecture diagram
    ├── sql/                   # Table schemas
    ├── tests/                 # Tests
    ├── dashboard.py           # Streamlit job browser
    ├── docker-compose.yml
    ├── requirements.txt
    └── main.py                # V1 entry point

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
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your-webhook-url
```

### 3. Start services

```bash
docker-compose up -d
```

This starts Postgres (port `5433`), Redis (port `6379`), and the Airflow stack (webserver, scheduler, metadata DB).

### 4. Create the schema

```bash
type sql\create_tables.sql | docker exec -i egyptjobpipeline-postgres-1 psql -U pipeline_user -d egypt_jobs -p 5432
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

### 7. Run with Airflow

```bash
docker-compose up -d
```

Access the Airflow UI at `http://localhost:8080` (admin/admin). Enable the `egypt_job_dag` to start scheduled runs.

### 8. Launch the dashboard

```bash
streamlit run dashboard.py
```

Open `http://localhost:8501` to browse scraped jobs.

### 9. Run V3 real-time alerts

```bash
cd v3
python poller.py
```

The poller checks Wuzzuf every 3 minutes and sends Discord notifications for new jobs matching your filters. Edit `v3/config.json` to change wanted/unwanted keywords.

## Sample Output

After running, you can query the database directly:

```sql
SELECT company, COUNT(*) AS openings
FROM jobs
GROUP BY company
ORDER BY openings DESC
LIMIT 5;
```
## Dashboard

![Dashboard Overview](docs/dashboard.png)

![Jobs by Company](docs/dashboard_chart.png)

![Jobs Table](docs/dashboard_table.png)

## Roadmap

- **V1** — Naive Python script, single source, runs on demand *(complete)*
- **V2** — Airflow DAG with scheduling, retries, exponential backoff, Discord alerting, backfill, and Streamlit dashboard *(complete)*
- **V3 (current)** — Real-time alert system with Redis deduplication, crash-proof polling loop, keyword filters, and Discord notifications for new job listings *(complete)*

## Author

**Mohamed Mahmoud** — Data Engineering student & DEPI intern  
Building projects to learn data engineering hands-on.