from src.model.logging import logger
from src.utils.helper import fetch_secrets
from src.gcp.bigquery import BigQuery
from src.service.gpg import GPGManager
import os

class DataConsumer:
    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.gpg_manager = GPGManager
        self.bq_client = BigQuery(project_id=self.project_id)

    def _fetch_decryption_secrets(self) -> tuple:
        secret_keys = fetch_secrets(secret_id=os.getenv("DECRYPTION_KEY_SECRET_ID"), gcp_project_id=self.project_id)
        secret_passphrase = fetch_secrets(secret_id=os.getenv("DECRYPTION_PASS_SECRET_ID"),
                                          gcp_project_id=self.project_id)

        logger.info(msg="Encryption key and passphrase fetched successfully from secret manager")
        return secret_keys, secret_passphrase

    def _assign_policy_tags_to_bigquery_table(self):
        pass

    def setup_infra(self):
        table = self.bq_client.get_or_create_bigquery_table(os.getenv("DATASET_ID"),
                                                    os.getenv("TABLE_ID"),
                                                    self.bq_client.load_bigquery_schema_from_json("/schema/bigquery_schema.json"))

        self._assign_policy_tags_to_bigquery_table()

    def decrypt_and_ingest_data(self):
        private_key, password = self._fetch_decryption_secrets()
        self.gpg_manager.set_decrypt_passphrase(passphrase=password)

        #read from gcs

        decrypted_data = self.gpg_manager.decrypt_data()

