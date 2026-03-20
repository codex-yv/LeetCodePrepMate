import json
import os
import sys
from tkinter import messagebox

# Resolve base dir: next to the .exe when frozen, project root when running normally
if getattr(sys, 'frozen', False):
    # Running inside a PyInstaller bundle — use the directory containing the exe
    _project_root = os.path.dirname(sys.executable)
else:
    # Running as a plain script — go two levels up from utils/
    _project_root = os.path.join(os.path.dirname(__file__), '..')

json_file_path = os.path.join(_project_root, 'config', 'dashboard.json')

# Default structure if the file doesn't exist
default_data = {
    "Total Link Copied": 0,
    "Total Questions Searched": 0,
    "Total Companies Searched": 0
}

def load_json(file_path):
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
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

