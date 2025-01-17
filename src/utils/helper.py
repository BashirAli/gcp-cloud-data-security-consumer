from src.gcp.secret_manager import SecretManager

def fetch_secrets(secret_id: str, gcp_project_id: str) -> str:
    secret_manager = SecretManager(gcp_project_id)
    secret_value = secret_manager.get_secret(
        secret_id=secret_id, version="latest"
    )

    return secret_value