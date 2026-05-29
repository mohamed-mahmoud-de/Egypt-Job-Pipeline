from src.extract.scraper import scrape_jobs
from src.load.db import insert_jobs

jobs = scrape_jobs()
insert_jobs(jobs)