import os
import pathlib
import functions_framework
from google.cloud import bigquery

# Print startup message
print("Cloud Function is starting up...")

# Set paths to SQL files
DIR_NAME = pathlib.Path(__file__).parent
SOURCE_SQL_PATH = DIR_NAME / 'sql' / 'source_phl_parks.sql'
CORE_SQL_PATH = DIR_NAME / 'sql' / 'core_phl_parks.sql'

# Validate critical environment variables
assert os.getenv('DATA_LAKE_BUCKET'), "Missing DATA_LAKE_BUCKET environment variable"
assert os.getenv('DATA_LAKE_DATASET'), "Missing DATA_LAKE_DATASET environment variable"
assert os.getenv('CORE_DATASET', 'core'), "Missing CORE_DATASET environment variable"

def ensure_dataset_exists(client, dataset_id):
    """Create dataset if it doesn't exist"""
    try:
        client.get_dataset(dataset_id)
        print(f"Dataset {dataset_id} already exists.")
    except Exception as e:
        print(f"Creating dataset {dataset_id}: {str(e)}")
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"
        client.create_dataset(dataset, timeout=30)
        print(f"Successfully created dataset {dataset_id}")

@functions_framework.http
def run_sql_parks(request):
    client = bigquery.Client()

    # Resolve dataset names
    project = client.project
    source_dataset = os.getenv('DATA_LAKE_DATASET')
    core_dataset = os.getenv('CORE_DATASET', 'core')

    # Ensure both datasets exist
    ensure_dataset_exists(client, f"{project}.{source_dataset}")
    ensure_dataset_exists(client, f"{project}.{core_dataset}")

    # Run source SQL
    result_source = run_sql(client, SOURCE_SQL_PATH)
    if result_source[1] != 200:
        return result_source

    # Run core SQL
    return run_sql(client, CORE_SQL_PATH)

def run_sql(client, sql_path):
    """Execute SQL from file with environment variables"""
    if not sql_path.exists():
        error_msg = f'SQL file {sql_path} not found'
        print(error_msg)
        return error_msg, 404

    try:
        with open(sql_path, 'r', encoding='utf-8') as sql_file:
            sql_template = sql_file.read()

        sql_query = render_template(
            sql_template,
            {
                'bucket_name': os.getenv('DATA_LAKE_BUCKET'),
                'source_dataset': os.getenv('DATA_LAKE_DATASET'),
                'core_dataset': os.getenv('CORE_DATASET', 'core'),
            }
        )

        print(f"\nExecuting SQL from {sql_path.name}:\n{sql_query[:500]}...\n")

        query_job = client.query(sql_query)
        query_job.result(timeout=300)
        print(f"Successfully executed {sql_path.name}")
        return f"Executed {sql_path.name}", 200

    except Exception as e:
        error_msg = f"Error executing {sql_path.name}: {str(e)}"
        print(error_msg)
        return error_msg, 500

def render_template(template, context):
    try:
        return template.replace('${', '{').format(**context)
    except KeyError as e:
        raise ValueError(f"Missing template variable: {str(e)}")
