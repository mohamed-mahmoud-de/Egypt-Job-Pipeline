from scraper import extract
from redis_client import is_seen, mark_seen
import time
from notifier import send_new_job_alert, send_error_alert
from filter import job_passes_filter

def poll_once():
    jobs = extract()
    for job in jobs:
        if is_seen(job["job_id"]):
            continue

        if not job_passes_filter(job):
            print(f'SKIPPED : {job["title"]}')
            mark_seen(job["job_id"])
            continue

        print(f'NEW : {job["title"]}')
        send_new_job_alert(job)
        mark_seen(job["job_id"])
    
        

while True:
    try:
        poll_once()
    except Exception as e:
        print(f"Poller crashed: {e}")
        try:
            send_error_alert(str(e))
        except Exception:
            print("Failed to send error alert to Discord too.")
    print("Waiting 3 minutes...")
    time.sleep(180)