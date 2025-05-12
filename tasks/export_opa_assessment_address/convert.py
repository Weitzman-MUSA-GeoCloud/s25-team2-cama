from google.cloud import bigquery
client = bigquery.Client()
bucket_name = 'musa5090s25-team2-public'

destination_uri = "gs://{}/{}".format(bucket_name, "phl_opa_assessment_address.json")
dataset_ref = bigquery.DatasetReference('musa5090s25-team2', 'core')
table_ref = dataset_ref.table("phl_opa_assessment_address")
job_config = bigquery.job.ExtractJobConfig()
job_config.destination_format = bigquery.DestinationFormat.NEWLINE_DELIMITED_JSON

extract_job = client.extract_table(
    table_ref,
    destination_uri,
    job_config=job_config,
    # Location must match that of the source table.
    location="us-east4",
)  # API request
extract_job.result()  # Waits for job to complete.