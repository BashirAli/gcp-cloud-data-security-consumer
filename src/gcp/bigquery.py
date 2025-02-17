from google.cloud import bigquery
from google.cloud.bigquery import Table
from google.cloud.exceptions import NotFound
import json
import os

CURRENT_PATH = os.path.dirname(__file__)

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

def get_or_create_bigquery_table(project_id:str, dataset_id:str, table_id:str, schema:list) -> Table:
    client = bigquery.Client(project=project_id)

    table_ref = client.dataset(dataset_id).table(table_id)

    try:
        table = client.get_table(table_ref)
        print(f"Table {table_id} already exists.")
    except NotFound:
        print(f"Table {table_id} not found. Creating new table...")
        table = bigquery.Table(table_ref, schema=schema)
        table = client.create_table(table)
        print(f"Table {table_id} created successfully.")

    return table
