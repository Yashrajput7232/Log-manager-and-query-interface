import requests
import json
import random
from datetime import datetime, timedelta

# Function to generate random log data
def generate_random_log():
    # levels = ["info", "warning", "error"]
    levels=["critical",'normal','attention-required']
    resources = ["server-1234", "server-5678", "server-9101"]
    
    log_data = {
        "level": random.choice(levels),
        "message": f"Operation {random.randint(1, 100)} failed",
        "resourceId": random.choice(resources),
        "timestamp": (datetime.utcnow() - timedelta(days=random.randint(1, 30))).isoformat() + "Z",
        "traceId": f"{random.choice(['abc', 'def', 'ghi'])}-{random.randint(100, 999)}-{random.randint(100, 999)}",
        "spanId": f"span-{random.randint(100, 999)}",
        "commit": f"{random.randint(100000, 999999)}",
        "metadata": {
            "parentResourceId": f"server-{random.randint(1000, 9999)}"
        }
    }
    return log_data

# URL of your log ingestor
ingestor_url = "http://localhost:3000/ingest"

# Number of logs to ingest
num_logs = 10

# Ingest logs
for _ in range(num_logs):
    log_entry = generate_random_log()
    response = requests.post(ingestor_url, json=log_entry)

    if response.status_code == 201:
        print("Log ingested successfully")
    else:
        print(f"Failed to ingest log. Status code: {response.status_code}, Response: {response.text}")
