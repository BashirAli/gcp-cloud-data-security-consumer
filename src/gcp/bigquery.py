from google.cloud import bigquery
from google.cloud.bigquery import Table
from google.cloud.exceptions import NotFound
import json
import os
from src.model.logging import logger


CURRENT_PATH = os.path.dirname(__file__)

class BigQuery:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.client = bigquery.Client(project=self.project_id)

    @staticmethod
    def load_bigquery_schema_from_json(schema_file: str) -> list:
        with open(CURRENT_PATH + schema_file, 'r') as f:
            schema_json = json.load(f)

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
