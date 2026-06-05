import streamlit as st 
import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()



def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5433,
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    
def fetch_jobs():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT title, company, location, date_posted, job_type, link FROM jobs ORDER BY date_posted DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

rows = fetch_jobs()
df = pd.DataFrame(rows, columns=["Title", "Company", "Location", "Date Posted", "Job Type", "Link"])

st.title("Egypt Job Dashboard")
company_filter = st.sidebar.selectbox("Company", options=["All"] + list(df["Company"].unique()))
if company_filter != "All":
    df = df[df["Company"] == company_filter]

location_filter = st.sidebar.selectbox("Location", options=["All"] + list(df["Location"].unique()))
if location_filter != "All":
    df = df[df["Location"] == location_filter]
    
job_type_filter = st.sidebar.selectbox("Job Type", options=["All"] + list(df["Job Type"].unique()))
if job_type_filter != "All":
    df = df[df["Job Type"] == job_type_filter]    

st.bar_chart(df["Company"].value_counts().head(10))
st.metric("Total Jobs", len(df))
st.dataframe(df)
