import logging

from google.cloud import datacatalog_v1, bigquery
import os
from src.utils.helper import read_json_file

CURRENT_PATH = os.path.dirname(__file__)


class DataCatalogManager:
    def __init__(self, gcp_project_id, location):
        self.gcp_project_id = gcp_project_id
        self.location = location
        self.datacatalog_client = datacatalog_v1.PolicyTagManagerClient()

    def create_taxonomy_and_policy_tags(self, taxonomy_name:str, policy_tags_json_path: str):
        parent = f"projects/{self.gcp_project_id}/locations/{self.location}"

        taxonomy = datacatalog_v1.Taxonomy(
            display_name=taxonomy_name,
            description="Taxonomy for BigQuery table policy tags",
            activated_policy_types=[datacatalog_v1.Taxonomy.PolicyType.POLICY_TYPE_UNSPECIFIED]
        )

        created_taxonomy = self.datacatalog_client.create_taxonomy(parent=parent, taxonomy=taxonomy)
        taxonomy_id = created_taxonomy.name
        logging.info(f"Created taxonomy: {taxonomy_id}")

        # Create policy tags
        policy_tags_json = read_json_file(CURRENT_PATH + policy_tags_json_path)

        policy_tag_map = {}
        for tag in policy_tags_json:
            policy_tag = datacatalog_v1.PolicyTag(
                display_name=tag["name"],
                description=tag.get("description", "")
            )
            created_policy_tag = self.datacatalog_client.create_policy_tag(
                parent=taxonomy_id, policy_tag=policy_tag
            )
            policy_tag_map[tag["name"]] = created_policy_tag.name
            logging.info(f"Created policy tag: {tag['name']} -> {created_policy_tag.name}")

        return taxonomy_id, policy_tag_map
