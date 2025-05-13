import os
import pathlib
from dotenv import load_dotenv
import functions_framework
from google.cloud import bigquery

# Load environment variables
load_dotenv()
print("Cloud Function is starting up...")

DIR_NAME = pathlib.Path(__file__).parent
SOURCE_SQL_PATH = DIR_NAME / 'sql' / 'source_phl_septa.sql'
CORE_SQL_PATH = DIR_NAME / 'sql' / 'core_phl_septa.sql'

def ensure_datasets(client):
    """Create both datasets if they don't exist"""
    project = client.project
    source_dataset = f"{project}.{os.getenv('DATA_LAKE_DATASET')}"
    core_dataset = f"{project}.{os.getenv('CORE_DATASET', 'core')}"
    
    for dataset_id in [source_dataset, core_dataset]:
        try:
            client.get_dataset(dataset_id)
            print(f"Dataset {dataset_id} exists")
        except Exception:
            print(f"Creating dataset {dataset_id}")
            dataset = bigquery.Dataset(dataset_id)
            dataset.location = "US"
            client.create_dataset(dataset, timeout=30)

@functions_framework.http
def run_sql_septa(request):
    client = bigquery.Client()
    
    # Validate environment variables
    assert os.getenv('DATA_LAKE_BUCKET'), "Missing DATA_LAKE_BUCKET"
    assert os.getenv('DATA_LAKE_DATASET'), "Missing DATA_LAKE_DATASET"
    
    # Ensure datasets exist
    ensure_datasets(client)
    
    # Run source SQL
    result_source = run_sql(client, SOURCE_SQL_PATH)
    if result_source[1] != 200:
        return result_source

    # Run core SQL
    return run_sql(client, CORE_SQL_PATH)

def run_sql(client, sql_path):
    if not sql_path.exists():
        return f'SQL file {sql_path} not found', 404

    try:
        with open(sql_path, 'r', encoding='utf-8') as f:
            sql_template = f.read()
            
        rendered_sql = sql_template.format(
            bucket_name=os.getenv('DATA_LAKE_BUCKET'),
            source_dataset=os.getenv('DATA_LAKE_DATASET'),
            core_dataset=os.getenv('CORE_DATASET', 'core'),
            project_id=client.project
        )
        
        print(f"Executing {sql_path.name}:\n{rendered_sql[:500]}...")
        
        job = client.query(rendered_sql)
        job.result(timeout=300)
        return f"Success: {sql_path.name}", 200
    
    except Exception as e:
        error = f"Error in {sql_path.name}: {str(e)}"
        print(error)
        return error, 500

if __name__ == '__main__':
    from functions_framework import create_app
    app = create_app(target=run_sql_septa)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
