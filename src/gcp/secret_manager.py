from src.model.logging import logger

from google.api_core.exceptions import GoogleAPICallError, RetryError
from google.cloud import secretmanager

class SecretManager:
    def __init__(self, gcp_project_id: str) -> None:
        self.gcp_project_id = gcp_project_id
        self._client = secretmanager.SecretManagerServiceClient()

    def get_secret(self, secret_id, version="latest") -> None | bytes:
        logger.info(f"Retrieving secret {secret_id}")
        name = self._client.secret_version_path(
            self.gcp_project_id, secret_id, version
        )

        try:
            response = self._client.access_secret_version(request={"name": name})
            payload = response.payload.data.decode("UTF-8")

        except (GoogleAPICallError, RetryError, ValueError, UnicodeDecodeError) as err:
            error_str = f"Error Fetching or Decoding Secret: {str(err)}"
            logger.error(error_str)
            return None

        return payload
