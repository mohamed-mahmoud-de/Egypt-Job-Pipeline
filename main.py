from src.extract.scraper import scrape_jobs
from src.load.db import insert_jobs
from src.transform.cleaner import clean_jobs

jobs = scrape_jobs()
jobs = clean_jobs(jobs)
insert_jobs(jobs)