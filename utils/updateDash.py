import json
import os
from tkinter import messagebox

# Path to your JSON file
base_dir = os.path.dirname(__file__)

json_file_path = os.path.join(base_dir, '..', 'config','dashboard.json')

# Default structure if the file doesn't exist
default_data = {
    "Total Link Copied": 0,
    "Total Questions Searched": 0,
    "Total Companies Searched": 0
}

def load_json(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump(default_data, f, indent=4)
        return default_data
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def update_stat(field, increment=1):
    data = load_json(json_file_path)
    if field in data:
        data[field] += increment
        save_json(data, json_file_path)

    else:
        print(f"Field '{field}' not found in JSON.")
        messagebox.showerror("Invalid Field", f"Field '{field}' not found in JSON.")
def get_stat(field):
    data = load_json(json_file_path)
    if field in data:
        return data[field]
    else:
        print(f"Field '{field}' not found in JSON.")
        return None


# value = get_stat("Total Questions Searched")

