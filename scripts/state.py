import os
import json

from scripts.config import load_config


def get_state_path(filename):
    config = load_config()
    base = os.path.join(os.path.dirname(__file__), "..", config["state_dir"])
    return os.path.join(base, filename)


def load_progress():
    path = get_state_path("progress.json")
    with open(path, "r") as f:
        return json.load(f)


def save_progress(data):
    path = get_state_path("progress.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_current():
    path = get_state_path("current.json")
    with open(path, "r") as f:
        return json.load(f)
    

def save_current(data):
    path = get_state_path("current.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def clear_current():
    save_current({})