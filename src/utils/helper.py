import json
import logging

from src.gcp.secret_manager import SecretManager


def fetch_secrets(secret_id: str, gcp_project_id: str) -> str:
    secret_manager = SecretManager(gcp_project_id)
    secret_value = secret_manager.get_secret(
        secret_id=secret_id, version="latest"
    )

    return secret_value

def read_json_file(file_path: str):
    with open(file_path, 'r') as f:
        data = json.load(f)

    return data

def load_json_or_jsonlines(data: str) -> list:
    try:
        # Attempt to parse as JSON
        json_obj = json.loads(data)
        if isinstance(json_obj, dict):
            return [json_obj]

        return json_obj
    except json.JSONDecodeError:
        # If parsing fails, it is most likely a JSON Lines file, so parse each line separately
        jsonl = []
        for line in data.strip().splitlines():
            try:
                jsonl.append(json.loads(line))
            except json.JSONDecodeError:
                logging.error("Data is not in a valid JSON/JSON Lines format.")
        return jsonl