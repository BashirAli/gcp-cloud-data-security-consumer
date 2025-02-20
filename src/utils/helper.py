from src.gcp.secret_manager import SecretManager
import json

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