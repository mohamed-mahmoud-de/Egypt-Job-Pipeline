from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.extract.scraper import scrape_jobs
from src.transform.cleaner import clean_jobs
from src.load.db import insert_jobs

def extract():
    jobs = scrape_jobs()
    db = pd.DataFrame(jobs)
    file_path = f"/opt/airflow/raw_data_{datetime.now().strftime('%Y-%m-%d')}.csv"
    db.to_csv(file_path, index=False)
    return file_path

def transform(**kwargs):
    ti = kwargs["ti"]
    raw_csv_path  = ti.xcom_pull(task_ids="extract")
    raw_csv_df = pd.read_csv(raw_csv_path)
    raw_jobs = raw_csv_df.to_dict(orient="records")
    cleaned = clean_jobs(raw_jobs)
    cleaned_path = f"/opt/airflow/cleaned_data_{datetime.now().strftime('%Y-%m-%d')}.csv"
    pd.DataFrame(cleaned).to_csv(cleaned_path, index=False)
    return cleaned_path

def load(**kwargs):
    ti = kwargs["ti"]
    load_jobs_csv = ti.xcom_pull(task_ids="transform")
    df = pd.read_csv(load_jobs_csv)
    df = df.where(df.notna(), None)
    cleaned_jobs = df.to_dict(orient="records")
    insert_jobs(cleaned_jobs)
    

with DAG(
    dag_id = "egypt_job_dag",
    start_date = datetime(2026, 6, 1),
    schedule = None,
    catchup = False,
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
    

