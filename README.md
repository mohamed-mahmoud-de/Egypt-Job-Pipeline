# Egypt Jobs Pipeline

A data pipeline that scrapes Egyptian tech job listings from Wuzzuf.net, stores them in Postgres, and prepares them for analysis. Built as a portfolio project to learn data engineering fundamentals.

## What It Does

- Scrapes all Python job listings from Wuzzuf.net (with pagination)
- Extracts: title, company, location, job type, date posted, and link
- Loads cleaned data into a Postgres database
- Deduplicates by job URL to prevent re-inserts

## Tech Stack

- **Python 3.13** — scraper and orchestration
- **BeautifulSoup4** — HTML parsing
- **Requests** — HTTP client
- **PostgreSQL 16** — data storage (running in Docker)
- **psycopg2** — Postgres driver
- **Docker Compose** — local database setup

## Project Structure
egypt-jobs-pipeline/
├── src/
│ ├── extract/ # Scraper logic
│ ├── transform/ # (Coming in next iteration)
│ └── load/ # Postgres loader
├── sql/ # Table schemas
├── tests/ # Tests (TODO)
├── config/ # Settings
├── data/ # Raw data dumps for debugging
├── logs/ # Pipeline run logs
├── docker-compose.yml
├── requirements.txt
└── main.py # Pipeline entry point

## How to Run
1. Clone the repo
2. Create a `.env` file in the root:
POSTGRES_USER=pipeline_user
POSTGRES_PASSWORD=pipeline_pass123
POSTGRES_DB=egypt_jobs

3. Start Postgres: `docker-compose up -d`
4. Create the schema: `type sql\create_tables.sql | docker exec -i egyptjobpipeline-postgres-1 psql -U pipeline_user -d egypt_jobs`
5. Set up Python: `python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt`
6. Run the pipeline: `python main.py`
## Roadmap
- **V1 (current)** — Naive Python script, single source, runs on demand
- **V2** — Airflow DAG with scheduled runs, retries, alerting, and a dashboard
- **V3** — Streaming pipeline with Kafka + Spark
## Author
Mohamed Mahmoud — Data Engineer student, DEPI intern