import os, sys
import yaml
import json
from typing import List, Dict, Any
import datetime

def load_config():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml'))
    with open(path, 'r') as file:
        config = yaml.safe_load(file)
    
    return config


def load_kafka_config():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "config", 'kafka_config.yaml'))
    with open(path, 'r') as file:
        config = yaml.safe_load(file)
    
    return config


def save_to_json(data: List[Dict[str, Any]], filename: str):
    """
    Save data to a JSON file
    Args:
        data (List[Dict[str, Any]]): Data to be saved
        filename (str): File name (e.g., 'data.json')
    """
    try:
        # Convert datetime objects to strings
        for item in data:
            if "created_at" in item and isinstance(item["created_at"], datetime.datetime):
                item["created_at"] = item["created_at"].isoformat()

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print(f"\n[+] Data successfully saved to '{filename}'\n")

    except Exception as e:
        print(f"ERROR: Failed to save data to {filename}: {e}")

if __name__=='__main__':
    print(load_config())

    print(load_kafka_config())