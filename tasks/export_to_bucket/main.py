from google.cloud import bigquery
import functions_framework

client = bigquery.Client()


def export_to_bucket(bucket_name, project, dataset_id, table_id, output_name):

    destination_uri = "gs://{}/{}".format(bucket_name, output_name)
    dataset_ref = bigquery.DatasetReference(project, dataset_id)
    table_ref = dataset_ref.table(table_id)

    extract_job = client.extract_table(
        table_ref,
        destination_uri,
        # Location must match that of the source table.
        location="us-east4",
    )

    # API request
    extract_job.result()  # Waits for job to complete.

    print(
        "Exported {}:{}.{} to {}".format(project, dataset_id, table_id, destination_uri)
    )


@functions_framework.http
def export_assessments_changes(request):

    bucket_name = "musa5090s25-team2-public"
    project = "musa5090s25-team2"
    dataset_id = "derived"
    table_id = "assessments_changes"
    output_name = "assessments_changes.csv"

    print('Exporting table...')

    export_to_bucket(bucket_name, project, dataset_id, table_id, output_name)
    
    return f'✅ Export complete'
