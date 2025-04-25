import os
import pathlib
import functions_framework
from google.cloud import bigquery

# Print startup message
print("Cloud Function is starting up...")

# Set paths to SQL files
DIR_NAME = pathlib.Path(__file__).parent
DERIVED_SQL_PATH = DIR_NAME / 'sql' / 'derived.current_assessment_bins.sql'


def ensure_datasets(client):
    """Create both derived datasets if they don't exist"""
    project = client.project
    derived_dataset = f"{project}.{os.getenv('DERIVED_DATASET', 'derived')}"

    for dataset_id in [derived_dataset]:
        try:
            client.get_dataset(dataset_id)
            print(f"Dataset {dataset_id} exists")
        except Exception:
            print(f"Creating dataset {dataset_id}")
            dataset = bigquery.Dataset(dataset_id)
            dataset.location = "US"
            client.create_dataset(dataset, timeout=30)

@functions_framework.http
def run_sql_derived_current_assessments(request):
    client = bigquery.Client()


    # Ensure datasets exist
    ensure_datasets(client)

    # Run derived SQL (transformed table)
    result_source = run_sql(client, DERIVED_SQL_PATH)


def run_sql(client, sql_path):
    if not sql_path.exists():
        return f'SQL file {sql_path} not found', 404

    try:
        with open(sql_path, 'r', encoding='utf-8') as f:
            sql_template = f.read()

        rendered_sql = sql_template.format(
            derived_dataset=os.getenv('DERIVED_DATASET', 'derived'),
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
    app = create_app(target=run_sql_derived_current_assessments)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)