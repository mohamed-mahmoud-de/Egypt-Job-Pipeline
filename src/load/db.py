import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5433,
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    
    
def insert_jobs(jobs):
    conn = get_connection()
    cur = conn.cursor()
    
    for job in jobs:
        cur.execute("""
            INSERT INTO jobs (title, company, location, date_posted, job_type, link)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (link) DO NOTHING
        """, (
            job["title"],
            job["company"],
            job["location"],
            job["date_posted"],
            job["job_type"],
            job["link"]
        ))
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"Inserted {len(jobs)} jobs.")