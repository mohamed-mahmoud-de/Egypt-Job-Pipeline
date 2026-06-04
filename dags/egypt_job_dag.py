from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.extract.scraper import scrape_jobs
from src.transform.cleaner import clean_jobs
from src.load.db import insert_jobs

def extract():
    jobs = scrape_jobs()
    return jobs

def transform(**kwargs):
    ti = kwargs["ti"]
    jobs = ti.xcom_pull(task_ids="extract")
    cleaned = clean_jobs(jobs)
    return cleaned

def load(**kwargs):
    ti = kwargs["ti"]
    jobs = ti.xcom_pull(task_ids="transform")
    insert_jobs(jobs)
    

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
    

