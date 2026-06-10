from scraper import extract
from redis_client import is_seen, mark_seen
import time

def poll_once():
    jobs = extract()
    for job in jobs:
        if is_seen(job["job_id"]) == True:
            continue
        else:
            mark_seen(job["job_id"])
            print(f'NEW : {job["title"]}')
    
        

while True:
    poll_once()
    print("Waiting 3 minutes...")
    time.sleep(180)