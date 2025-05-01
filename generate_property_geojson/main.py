import dotenv
dotenv.load_dotenv()
import json
from google.cloud import bigquery, storage
import functions_framework

@functions_framework.http
def generate_clean_properties_geojson(request):
    # Initialize clients inside handler to avoid startup delays
    bigquery_client = bigquery.Client()
    storage_client = storage.Client()

    print('Starting BigQuery query...')
    sql = """
        SELECT
            property_id,
            value_2021,
            value_2022,
            value_2023,
            value_2024,
            value_2025,
            value_2026,
            change_2025_2026_absolute,
            change_2025_2026_change_relative,
            change_2024_2025_absolute,
            change_2024_2025_change_relative,
            change_2023_2024_absolute,
            change_2023_2024_change_relative,
            change_2022_2023_absolute,
            change_2022_2023_change_relative,
            change_2021_2022_absolute,
            change_2021_2022_change_relative,
            location,
            ST_AsGeoJSON(parcel_geog) AS geometry
        FROM derived.assessments_with_parcels
        WHERE parcel_geog IS NOT NULL
    """

    query_job = bigquery_client.query(sql)
    rows = list(query_job.result())
    print(f'Retrieved {len(rows)} geospatial records')

    # Build GeoJSON feature collection
    features = []
    for row in rows:
        try:
            features.append({
                'type': 'Feature',
                'properties': {k: v for k, v in row.items() if k != 'geometry'},
                'geometry': json.loads(row['geometry'])
            })
        except json.JSONDecodeError:
            print(f"Skipping invalid geometry for property {row['property_id']}")
            continue

    feature_collection = {
        'type': 'FeatureCollection',
        'features': features
    }

    # Upload to GCS
    print('Initiating GCS upload...')
    bucket = storage_client.bucket('musa5090s25-team2-temp_data')
    blob = bucket.blob('property-tile-info.geojson')
    blob.upload_from_string(json.dumps(feature_collection))
    
    print('Operation completed successfully')
    return 'GeoJSON data processed and uploaded to GCS', 200
