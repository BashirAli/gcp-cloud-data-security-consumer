from google.cloud import bigquery
from google.cloud.bigquery import Table
from google.cloud.exceptions import NotFound
import json
import logging
import os
from src.model.logging import logger
from src.utils.helper import read_json_file

CURRENT_PATH = os.path.dirname(__file__)

class BigQuery:
    def __init__(self, gcp_project_id: str):
        self.project_id = gcp_project_id
        self.client = bigquery.Client(project=self.project_id)

    @staticmethod
    def load_bigquery_schema_from_json(schema_file: str) -> list:
        schema_json = read_json_file(CURRENT_PATH + schema_file)

        schema = []
        for field in schema_json:
            schema.append(bigquery.SchemaField(
                name=field['name'],
                field_type=field['type'],
                mode=field.get('mode', 'NULLABLE')
            ))

        return schema

    def get_or_create_bigquery_table(self, dataset_id:str, table_id:str, schema:list) -> Table:
        full_table_id = f"{self.project_id}.{dataset_id}.{table_id}"
        try:
            table = self.client.get_table(full_table_id)
            print(f"Table {table_id} already exists.")
        except NotFound:
            print(f"Table {table_id} not found. Creating new table...")
            table = bigquery.Table(full_table_id, schema=schema)
            table = self.client.create_table(table)
            print(f"Table {table_id} created successfully.")

        return table

    def load_json_rows_to_table(self, bq_table: Table, data: list):

        error_responses = self.client.insert_rows_json(
            json_rows=data,
            table=f"{bq_table.dataset_id}.{bq_table.table_id}"
        )

        if len(error_responses) > 0:
            logger.error(f"Error during BigQuery write: {error_responses}")


    def update_bigquery_table_with_policy_tags(self, table: bigquery.Table, updated_schema_file_path:str, policy_tag_map:dict):
        schema_with_policy_tags = read_json_file(CURRENT_PATH + updated_schema_file_path)

        updated_schema = []
        for field in schema_with_policy_tags:
            policy_tag = policy_tag_map.get(field.get("policy_tag"))
            bq_field = bigquery.SchemaField(
                name=field["name"],
                field_type=field["type"],
                mode=field["mode"],
                policy_tags=bigquery.PolicyTagList(names=[policy_tag]) if policy_tag else None
            )
            updated_schema.append(bq_field)

        table.schema = updated_schema
        self.client.update_table(table, ["schema"])
        logging.info(f"Updated {table.full_table_id} schema with policy tags")
