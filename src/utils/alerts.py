import requests
import os
from dotenv import load_dotenv

load_dotenv("/opt/airflow/.env")

def send_discord_alert(context):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("Discord webhook URL not set in environment variables.")
        return
    
    task_id = context["task_instance"].task_id
    dag_name = context["task_instance"].dag_id
    execution_date = context["execution_date"]
    error_message = context["exception"]
    
    
    payload = {
        "embeds": [{
            "title": "Airflow Task Failure Alert",
            "description": "Failure details for Airflow task",
            "fields": [
                {"name": "Task ID", "value": task_id, "inline": True},
                {"name": "DAG Name", "value": dag_name, "inline": True},
                {"name": "Execution Time", "value": str(execution_date), "inline": False},
                {"name": "Error", "value": str(error_message), "inline": False}
            ],
            "color": 16711680
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
        
        
def send_success_alert(context):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("Discord webhook URL not set in environment variables.")
        return
    
    task_id = context["task_instance"].task_id
    dag_name = context["task_instance"].dag_id
    execution_date = context["execution_date"]
    
    payload = {
        "embeds": [{
            "title": "Airflow Task Success Alert",
            "description": "Success details for Airflow task",
            "fields": [
                {"name": "Task ID", "value": task_id, "inline": True},
                {"name": "DAG Name", "value": dag_name, "inline": True},
                {"name": "Execution Time", "value": str(execution_date), "inline": False}
            ],
            "color": 65280
        }]
    }
    
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print("Discord success alert sent successfully.")
        else:
            print(f"Failed to send Discord success alert. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending Discord success alert: {e}")