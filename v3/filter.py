import json




with open("config.json", "r") as f:
    config = json.load(f)

wanted_keywords = config["wanted_keywords"]
not_wanted_keywords = config["not_wanted_keywords"]

def job_passes_filter(job):
    if any(keyword in job['title'].lower() for keyword in not_wanted_keywords):
        return False
    if any(keyword in job['title'].lower() for keyword in wanted_keywords):
        return True
    else:
        return False

    
