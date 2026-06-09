import redis

r = redis.Redis(host="localhost", port=6379, db=0)

SEEN_JOBS_KEY = "v3:seen_jobs"

def is_seen(job_id):
    return r.sismember(SEEN_JOBS_KEY, job_id)

def mark_seen(job_id):
    r.sadd(SEEN_JOBS_KEY, job_id)