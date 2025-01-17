from src.model import logger
from src.utils.helper import fetch_secrets

class DataConsumer:
    def __init__(self):
        pass

    def _fetch_decryption_secrets(self) -> tuple:
        secret_keys = fetch_secrets(secret_id=settings.decryption_key_secret_id, gcp_project_id=gcp_project_id)
        secret_passphrase = fetch_secrets(secret_id=settings.decryption_passphrase_secret_id,
                                          gcp_project_id=gcp_project_id)

        logger.info(msg="Encryption key and passphrase fetched successfully from secret manager")
        return secret_keys, secret_passphrase


    def consume(self):
        pass

