import pathlib
import functions_framework
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

print("Cloud Function is starting up...")


@functions_framework.http
def run_sql_derived_current_assessment_bins(request):
    # Path to the SQL file
    sql_file_path = 'derived_current_assessment_bins.sql'

    # Load the SQL query from the file
    with open(sql_file_path, 'r') as sql_file:
        sql_query = sql_file.read()

    # Initialize BigQuery client
    bigquery_client = bigquery.Client()

    # Run the query to create or replace the table
    query_job = bigquery_client.query(sql_query)
    query_job.result()  # Wait for the query to finish

    # Return a success message
    return "Table created or replaced successfully.", 200
