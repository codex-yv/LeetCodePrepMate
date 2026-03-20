import json
import os
import sys

# Resolve base dir: next to the .exe when frozen, project root when running normally
if getattr(sys, 'frozen', False):
    _project_root = os.path.dirname(sys.executable)
else:
    _project_root = os.path.join(os.path.dirname(__file__), '..')

history_file_path = os.path.join(_project_root, 'config', 'history.json')


# Default structure if the file doesn't exist
default_history = {
    "Companies": [],
    "Questions": [],
    "Links": []
}

def load_history(file_path):
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(default_history, f, indent=4)
        return default_history
    with open(file_path, 'r') as f:
        return json.load(f)

def save_history(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def append_to_history(field, value):
    data = load_history(history_file_path)
    
    if field not in data or not isinstance(data[field], list):
        return 404

    if value in data[field]:
        return 404

    data[field].append(value)
    save_history(data, history_file_path)
    return 200

