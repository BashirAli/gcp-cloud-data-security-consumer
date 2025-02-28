import time

from src.model.logging import logger
from src.utils.helper import fetch_secrets, load_json_or_jsonlines
from src.gcp.bigquery import BigQuery
from src.gcp.gcs import GoogleCloudStorage
from src.gcp.datacatalog import DataCatalogManager
from src.service.gpg import GPGManager
import os

class DataConsumer:
    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.gpg_manager = GPGManager()
        self.bq_client = BigQuery(gcp_project_id=self.project_id)
        self.gcs_client = GoogleCloudStorage(gcp_project_id=self.project_id)
        self.datacatalog_client = DataCatalogManager(gcp_project_id=self.project_id, location=os.getenv("GCP_PROJECT_LOCATION"))

    def _fetch_decryption_secrets(self) -> tuple:
        secret_keys = fetch_secrets(secret_id=os.getenv("DECRYPTION_KEY_SECRET_ID"), gcp_project_id=self.project_id)
        secret_passphrase = fetch_secrets(secret_id=os.getenv("DECRYPTION_PASS_SECRET_ID"),
                                          gcp_project_id=self.project_id)

        logger.info(msg="Encryption key and passphrase fetched successfully from secret manager")
        return secret_keys, secret_passphrase


    def setup_table_infra(self):
        taxonomy_id, policy_tag_map = self.datacatalog_client.create_taxonomy_and_policy_tags("Bigquery PII Taxonomy", "/schema/taxonomy_policy_tags.json")

        table = self.bq_client.get_or_create_bigquery_table(os.getenv("DATASET_ID"),
                                                    os.getenv("TABLE_ID"),
                                                    self.bq_client.load_bigquery_schema_from_json("/schema/bigquery_schema.json"))

        time.sleep(5)  # Ensure taxonomy and tags are available before applying to BQ
        self.bq_client.update_bigquery_table_with_policy_tags(table, "/schema/bigquery_schema.json", policy_tag_map)

        return table

    def decrypt_and_ingest_data(self):
        # fetch decryption secrets
        private_key, password = self._fetch_decryption_secrets()
        self.gpg_manager.set_decrypt_passphrase(passphrase=password)

        # create table and tag
        bq_table = self.setup_table_infra()

        # read file from gcs
        gcs_data = self.gcs_client.read_gcs_file_to_bytes(gcs_bucket_name=os.getenv("GCS_BUCKET"), gcs_source_blob=os.getenv("GCS_FILE_NAME"))
        if gcs_data:
            # decrypt data
            decrypted_data = self.gpg_manager.decrypt_data(data=gcs_data)

            # write to bigquery
            self.bq_client.load_json_rows_to_table(bq_table, load_json_or_jsonlines(str(decrypted_data)))
