from datetime import datetime, timedelta

def parse_date_posted(text):
    if text == "N/A" or not text:
        return None
    
    parts = text.split()
    number = int(parts[0])
    unit = parts[1].lower()
    
    if unit in ("day", "days"):
        delta = timedelta(days=number)
    elif unit in ("month", "months"):
        delta = timedelta(days=number * 30)
    else: 
        return None
    
    return (datetime.now() - delta).date()   
        
        
def clean_jobs(jobs):
    for job in jobs:
        job["date_posted"] = parse_date_posted(job["date_posted"])
    return jobs        
