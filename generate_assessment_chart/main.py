import json
from google.cloud import bigquery
from google.cloud import storage

def generate_assessment_chart_configs(request):
    bq_client = bigquery.Client()
    storage_client = storage.Client()

    query = """
        SELECT lower_bound, upper_bound, property_count
        FROM derived.current_assessment_bin
    """
    query_job = bq_client.query(query)
    rows = list(query_job.result())

    results = [
        {
            "lower_bound": row.lower_bound,
            "upper_bound": row.upper_bound,
            "property_count": row.property_count
        }
        for row in rows
    ]

    bucket = storage_client.bucket("musa5090s25-team2-public")
    blob = bucket.blob("configs/current_tax_year_assessment_bins.json")
    blob.upload_from_string(json.dumps(results, indent=2), content_type='application/json')

    return ("Assessment chart config generated successfully.", 200)
