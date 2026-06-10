from dotenv import load_dotenv
import os
import requests

load_dotenv()



def send_new_job_alert(job):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("Discord webhook URL not set in environment variables.")
        return
    
    title = job["title"]
    company = job["company"]
    job_type = job["job_type"]
    location = job["location"]
    link = job["link"]
    
    payload = {
        "embeds": [{
            "title": title,
            "url": link,
            "fields": [
                {"name": "Company", "value": company, "inline": True},
                {"name": "Job Type", "value": job_type, "inline": True},
                {"name": "Location", "value": location, "inline": True},
            ],
            "color": 65280
        }]
    }
    
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print("Discord alert sent successfully.")
        else:
            print(f"Failed to send Discord alert. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending Discord alert: {e}")