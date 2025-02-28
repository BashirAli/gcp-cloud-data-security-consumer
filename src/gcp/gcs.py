import logging.config

from google.api_core.exceptions import GoogleAPIError
from google.cloud import storage
from google.cloud.exceptions import NotFound

class GoogleCloudStorage:
    def __init__(self, gcp_project_id):
        self._client = storage.Client(gcp_project_id)

    def read_gcs_file_to_bytes(self, gcs_bucket_name, gcs_source_blob) -> bytes:
        try:
            logging.info(msg=f"Reading file from: {gcs_bucket_name} bucket")
            bucket = self._client.bucket(gcs_bucket_name)
            blob = bucket.blob(gcs_source_blob)
            file_as_bytes = blob.download_as_bytes()
            logging.info(msg=f"Read file {gcs_source_blob} from {gcs_bucket_name} bucket")

        except (GoogleAPIError, NotFound,  Exception) as e:
            logging.error(msg=f"Failed to read file from google cloud storage: {e}")
            file_as_bytes = None

        return file_as_bytes
