from scraper import extract
from redis_client import is_seen, mark_seen
import time
from notifier import send_new_job_alert
from filter import job_passes_filter

def poll_once():
    jobs = extract()
    for job in jobs:
        if is_seen(job["job_id"]) == True:
            continue
        else:
            mark_seen(job["job_id"])
            if not job_passes_filter(job):
                print(f'SKIPPED : {job["title"]}')
                continue
            print(f'NEW : {job["title"]}')
            send_new_job_alert(job)
    
        

while True:
    poll_once()
    print("Waiting 3 minutes...")
    time.sleep(180)