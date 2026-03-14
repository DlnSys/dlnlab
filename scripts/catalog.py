import os
import yaml

from scripts.config import load_config


def load_catalog():
    config = load_config()
    catalog_dir = os.path.join(os.path.dirname(__file__), "..", config["catalog_dir"])
    challenges = []

    for root, dirs, files in os.walk(catalog_dir):
        for file in files:
            if file.endswith(".yml"):
                path = os.path.join(root, file)
                with open(path, "r") as f:
                    data = yaml.safe_load(f)
                    if data and data.get("enabled", True):
                        challenges.append(data)

    return challenges