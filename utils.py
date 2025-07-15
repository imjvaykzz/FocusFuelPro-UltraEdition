
import json
import os
from datetime import datetime

FIREBASE_CONFIG_PATH = "firebase_config.json"
TODO_FILE = "data/todo_data.json"
SESSION_FILE = "data/study_sessions.json"
QUOTE_FILE = "data.json"
MUSIC_FILE = "data.json"

def load_firebase_config():
    if os.path.exists(FIREBASE_CONFIG_PATH):
        with open(FIREBASE_CONFIG_PATH, 'r') as f:
            return json.load(f)
    else:
        raise FileNotFoundError("Firebase config not found.")

def save_data(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def load_data(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}

def add_todo_item(task, due=None):
    todos = load_data(TODO_FILE)
    task_id = str(len(todos) + 1)
    todos[task_id] = {
        "task": task,
        "completed": False,
        "due": due
    }
    save_data(TODO_FILE, todos)

def complete_todo(task_id):
    todos = load_data(TODO_FILE)
    if task_id in todos:
        todos[task_id]["completed"] = True
        save_data(TODO_FILE, todos)

def delete_todo(task_id):
    todos = load_data(TODO_FILE)
    if task_id in todos:
        del todos[task_id]
        save_data(TODO_FILE, todos)

def log_study_session(subject, duration, music, timestamp=None):
    sessions = load_data(SESSION_FILE)
    session_id = str(len(sessions) + 1)
    if not timestamp:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sessions[session_id] = {
        "subject": subject,
        "duration": duration,
        "music": music,
        "timestamp": timestamp
    }
    save_data(SESSION_FILE, sessions)

def load_quotes():
    return load_data(QUOTE_FILE).get("quotes", [])

def load_music_library():
    return load_data(MUSIC_FILE).get("tracks", [])

def get_today_focus_data():
    sessions = load_data(SESSION_FILE)
    today = datetime.now().strftime("%Y-%m-%d")
    total_minutes = 0
    for session in sessions.values():
        if session["timestamp"].startswith(today):
            total_minutes += session["duration"]
    return total_minutes
