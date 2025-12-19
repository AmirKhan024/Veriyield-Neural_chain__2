import json
import os
from datetime import datetime

DB_FILE = "veriyield_db.json"

def load_history():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_transaction(tx_type, details):
    history = load_history()
    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": tx_type, # "Insurance Claim", "Carbon Mint", "Crop Sale"
        "details": details
    }
    history.append(record)
    with open(DB_FILE, "w") as f:
        json.dump(history, f, indent=4)