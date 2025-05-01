import json
import pandas as pd
from google.cloud import storage

def process_geojson(request):
    # Configuration
    bucket_name = 'musa5090s25-team2-temp_data'
    input_blob_name = 'property-tile-info.geojson'
    output_bucket_name = 'musa5090s25-team2-public'
    output_blob_name = 'metadata/style_metadata.json'

    # Download GeoJSON from GCS
    storage_client = storage.Client()
    input_bucket = storage_client.bucket(bucket_name)
    input_blob = input_bucket.blob(input_blob_name)
    geojson_data = json.loads(input_blob.download_as_bytes().decode("utf-8"))

    # Flatten features
    df = pd.json_normalize(geojson_data["features"])

    # Select fields of interest
    fields = [
        'properties.value_2021',
        'properties.value_2022',
        'properties.value_2023',
        'properties.value_2024',
        'properties.value_2025',
        'properties.value_2026',
        'properties.change_2025_2026_absolute',
        'properties.change_2025_2026_change_relative',
        'properties.change_2024_2025_absolute',
        'properties.change_2024_2025_change_relative',
        'properties.change_2023_2024_absolute',
        'properties.change_2023_2024_change_relative',
        'properties.change_2022_2023_absolute',
        'properties.change_2022_2023_change_relative',
        'properties.change_2021_2022_absolute',
        'properties.change_2021_2022_change_relative'
    ]

    # Initialize metadata output
    metadata = {}

    for field in fields:
        if field in df.columns:
            series = pd.to_numeric(df[field], errors='coerce').dropna()
            if not series.empty:
                metadata[field.replace('properties.', '')] = {
                    "min": float(series.min()),
                    "max": float(series.max()),
                    "breakpoints": series.quantile([0.0, 0.25, 0.5, 0.75, 1.0]).tolist()
                }

    # Upload output JSON to GCS
    output_bucket = storage_client.bucket(output_bucket_name)
    output_blob = output_bucket.blob(output_blob_name)
    output_blob.upload_from_string(
        data=json.dumps(metadata, indent=2),
        content_type='application/json'
    )

    return "Style metadata successfully generated and uploaded.", 200
