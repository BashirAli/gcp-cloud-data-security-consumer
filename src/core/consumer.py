from src.model.logging import logger
from src.utils.helper import fetch_secrets
from src.gcp.bigquery import get_or_create_bigquery_table

class DataConsumer:
    def __init__(self):
        pass

    def _fetch_decryption_secrets(self) -> tuple:
        secret_keys = fetch_secrets(secret_id=settings.decryption_key_secret_id, gcp_project_id=gcp_project_id)
        secret_passphrase = fetch_secrets(secret_id=settings.decryption_passphrase_secret_id,
                                          gcp_project_id=gcp_project_id)

        logger.info(msg="Encryption key and passphrase fetched successfully from secret manager")
        return secret_keys, secret_passphrase
    def _get_or_create_bigquery_table(self):
        pass
    def _assign_policy_tags_to_bigquery_table(self):
        pass

    def setup_infra(self):
        self._get_or_create_bigquery_table()
        self._assign_policy_tags_to_bigquery_table()

    def decrypt_and_ingest_data(self):
        private_key, password = self._fetch_decryption_secrets()

