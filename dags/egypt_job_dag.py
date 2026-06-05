from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.extract.scraper import scrape_jobs
from src.transform.cleaner import clean_jobs
from src.load.db import insert_jobs
from src.utils.alerts import send_discord_alert, send_success_alert

def extract(**kwargs):
    jobs = scrape_jobs()
    db = pd.DataFrame(jobs)
    file_path = f"/opt/airflow/raw_data_{kwargs['logical_date'].strftime('%Y-%m-%d')}.csv"
    db.to_csv(file_path, index=False)
    return file_path

def transform(**kwargs):
    ti = kwargs["ti"]
    raw_csv_path  = ti.xcom_pull(task_ids="extract")
    raw_csv_df = pd.read_csv(raw_csv_path)
    raw_jobs = raw_csv_df.to_dict(orient="records")
    cleaned = clean_jobs(raw_jobs)
    cleaned_path = f"/opt/airflow/cleaned_data_{kwargs['logical_date'].strftime('%Y-%m-%d')}.csv"
    pd.DataFrame(cleaned).to_csv(cleaned_path, index=False)
    return cleaned_path

def load(**kwargs):
    ti = kwargs["ti"]
    load_jobs_csv = ti.xcom_pull(task_ids="transform")
    df = pd.read_csv(load_jobs_csv)
    df = df.where(df.notna(), None)
    cleaned_jobs = df.to_dict(orient="records")
    insert_jobs(cleaned_jobs)
    
default_args = { 
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "exponential_backoff": True,
    "on_failure_callback": send_discord_alert,
    "on_success_callback": send_success_alert
}

with DAG(
    dag_id = "egypt_job_dag",
    start_date = datetime(2026, 6, 1),
    schedule = timedelta(hours= 2),
    catchup = False,
    default_args= default_args
) as dag:
    extract_task = PythonOperator(
        task_id = "extract",
        python_callable = extract,
    )
    
    transform_task = PythonOperator(
        task_id = "transform",
        python_callable = transform,
    )
    
    load_task = PythonOperator(
        task_id = "load",
        python_callable = load,
    )
    
    extract_task >> transform_task >> load_task
    

