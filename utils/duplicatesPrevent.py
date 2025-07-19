import json
import os

# Path to the history file
base_dir = os.path.dirname(__file__)

history_file_path = os.path.join(base_dir, '..', 'config','history.json')


# Default structure if the file doesn't exist
default_history = {
    "Companies": [],
    "Questions": [],
    "Links": []
}

def load_history(file_path):
    if not os.path.exists(file_path):
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

