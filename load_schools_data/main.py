import os
import pathlib
from dotenv import load_dotenv
import functions_framework
from google.cloud import bigquery

# Load environment variables
load_dotenv()
print("Cloud Function is starting up...")

DIR_NAME = pathlib.Path(__file__).parent
SOURCE_SQL_PATH = DIR_NAME / 'sql' / 'source_phl_schools.sql'
CORE_SQL_PATH = DIR_NAME / 'sql' / 'core_phl_schools.sql'

def ensure_dataset_exists(client, dataset_id):
    """Create dataset if it doesn't exist"""
    try:
        client.get_dataset(dataset_id)
        print(f"Dataset {dataset_id} exists")
    except Exception:
        print(f"Creating dataset {dataset_id}")
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"
        client.create_dataset(dataset, timeout=30)

@functions_framework.http
def run_sql_schools(request):
    client = bigquery.Client()

    # Resolve dataset names from environment
    project = client.project
    source_dataset = f"{project}.{os.getenv('DATA_LAKE_DATASET')}"
    core_dataset = f"{project}.{os.getenv('CORE_DATASET', 'core')}"

    # Ensure both datasets exist
    ensure_dataset_exists(client, source_dataset)
    ensure_dataset_exists(client, core_dataset)

    # Run source SQL (external table)
    result_source = run_sql(client, SOURCE_SQL_PATH)
    if result_source[1] != 200:
        return result_source

    # Run core SQL (transformed table)
    return run_sql(client, CORE_SQL_PATH)

def run_sql(client, sql_path):
    if not sql_path.exists():
        return f'SQL file {sql_path} not found', 404

    try:
        with open(sql_path, 'r', encoding='utf-8') as f:
            sql_template = f.read()

        # Inject both source and core dataset references
        sql_query = render_template(
            sql_template,
            {
                'bucket_name': os.getenv('DATA_LAKE_BUCKET'),
                'source_dataset': os.getenv('DATA_LAKE_DATASET'),
                'core_dataset': os.getenv('CORE_DATASET', 'core'),
                'project_id': client.project
            }
        )

        print(f"Executing {sql_path.name}:\n{sql_query[:500]}...")

        query_job = client.query(sql_query)
        query_job.result(timeout=300)
        return f"Success: {sql_path.name}", 200

    except Exception as e:
        error = f"Error in {sql_path.name}: {str(e)}"
        print(error)
        return error, 500

def render_template(template, context):
    """Handle both ${VAR} and {VAR} template formats"""
    template = template.replace('${', '{')
    return template.format(**context)

if __name__ == '__main__':
    from functions_framework import create_app
    app = create_app(target=run_sql_schools)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
